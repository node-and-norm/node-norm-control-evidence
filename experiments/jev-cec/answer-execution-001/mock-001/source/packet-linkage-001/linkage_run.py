"""Bounded CEC Jev runner: mock by default, explicit live mode with preflight."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import json
import os
from pathlib import Path
import platform
import subprocess
import time
import urllib.error
import urllib.request

from linkage_inputs import encode, sha, check, BASE, FILES, schedule
from v2_execution import MODEL, unique, reject_constant, validate_response
from linkage_analysis import summarize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RATE = Decimal('0.000000042')
TOKEN_LIMIT = 64000
CAP = Decimal('1')
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class LiveTransport:
    def __init__(self, key):
        if not key.strip():
            raise ValueError('TYPESAFE_API_KEY is unavailable')
        self.key = key
        self.opener = urllib.request.build_opener(NoRedirect())

    def __call__(self, payload):
        request = urllib.request.Request(ENDPOINT, data=payload, method='POST',
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.key})
        try:
            with self.opener.open(request, timeout=30) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()


def mock_transport(payload):
    # Deliberately uniform plumbing output; never consults the reference key.
    request = json.loads(payload)
    return 200, encode({'model': MODEL, 'usage': {'input_tokens': 100, 'output_tokens': 30},
        'answers': {name: {'type': 'choice', 'choice': 'unknown', 'confidence': 0,
                          'probabilities': {label: 0.125 for label in question['criteria']}}
                    for name, question in request['questions'].items()}})


def usage_and_model(raw):
    try:
        doc = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
    except (ValueError, UnicodeDecodeError):
        return None, None
    if not isinstance(doc, dict):
        return None, None
    usage = doc.get('usage')
    if not isinstance(usage, dict) or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ('input_tokens','output_tokens')):
        return None, doc.get('model')
    return usage, doc.get('model')


def artifacts(output):
    return {str(p.relative_to(output)): sha(p.read_bytes()) for p in sorted(output.rglob('*'))
            if p.is_file() and p != output/'manifest.json'}


def verify(output):
    manifest = json.loads((output/'manifest.json').read_text())
    if any(p.is_symlink() for p in output.rglob('*')) or artifacts(output) != manifest['artifacts']:
        raise ValueError('Run artifact set or hashes differ')
    return manifest


def run(output, transport, mode, preflight=None):
    if mode not in ('mock', 'live'):
        raise ValueError('Unknown mode')
    if mode == 'live':
        if not isinstance(preflight, dict) or preflight != {
            'checked_date_utc': datetime.now(timezone.utc).date().isoformat(),
            'input_usd_per_million': '0.042', 'request_token_limit': 64000,
            'output_usd_per_million': '0', 'max_requests': 8, 'max_usd': '1'}:
            raise ValueError('Current pricing/limits preflight required')
    check()
    if mode == 'live' and subprocess.run(['git','status','--porcelain'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip():
        raise ValueError('Live execution requires a clean committed checkout')
    rows = schedule()
    output.mkdir(parents=True, exist_ok=False)
    (output/'schedule.json').write_bytes(encode(rows))
    (output/'requests').mkdir(); (output/'responses').mkdir()
    snapshots = output/'source'; snapshots.mkdir()
    for name in FILES:
        target=snapshots/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((BASE/name).read_bytes())
    (snapshots/'freeze.json').write_bytes((HERE/'freeze.json').read_bytes())
    revision = subprocess.run(['git','rev-parse','HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    records = [{'attempt_id': row['attempt_id'], 'status': 'not_attempted'} for row in rows]
    charge = Decimal('0'); unknown_usage = False; stop = None
    (output/'metadata.json').write_bytes(encode({'mode':mode, 'python':platform.python_version(),
        'code_revision':revision, 'working_tree_dirty':bool(subprocess.run(['git','status','--porcelain'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()), 'started_at':datetime.now(timezone.utc).isoformat(),
        'model_requested':MODEL, 'endpoint':ENDPOINT if mode=='live' else None, 'preflight':preflight}))
    def persist():
        (output/'attempts.json').write_bytes(encode(records))
    persist()
    try:
        for row, record in zip(rows, records):
            if charge + RATE * TOKEN_LIMIT > CAP:
                stop = 'budget_reservation'; break
            identity = row['attempt_id']; raw_request = encode(row['payload'])
            (output/'requests'/f'{identity}.json').write_bytes(raw_request)
            # An interrupted marker is persisted before dispatch. Never auto-resume.
            record.update(status='interrupted', started_at=datetime.now(timezone.utc).isoformat(),
                          request_sha256=sha(raw_request))
            persist(); started = time.monotonic()
            try:
                status, raw = transport(raw_request)
            except Exception as exc:
                record.update(status='transport_error', exception_type=type(exc).__name__,
                              seconds=time.monotonic()-started)
                unknown_usage=True; stop='transport_error'; persist(); break
            record.update(http_status=status, seconds=time.monotonic()-started)
            (output/'responses'/f'{identity}.bin').write_bytes(raw)
            record['response_sha256']=sha(raw)
            usage, resolved = usage_and_model(raw)
            record.update(usage=usage, model_resolved=resolved)
            if usage is None:
                unknown_usage=True
            else:
                charge += RATE * usage['input_tokens']
            if status != 200:
                record['status']='http_error'; stop='http_error'; persist(); break
            try:
                validate_response(raw)
            except (ValueError, UnicodeDecodeError) as exc:
                record.update(status='invalid', validation_error=str(exc))
            else:
                record['status']='valid'
            persist()
            if usage is None:
                stop='usage_unavailable'; break
            if resolved != MODEL:
                stop='model_mismatch'; break
            if usage['input_tokens'] + usage['output_tokens'] > TOKEN_LIMIT:
                stop='provider_token_limit_exceeded'; break
    except BaseException:
        unknown_usage=True; stop='interrupted'; raise
    finally:
        persist()
        # Load authored values only for arithmetic after dispatch has stopped.
        key=json.loads((snapshots/'packet-linkage-001/reference.json').read_text())
        analysis_records=[]
        for record in records:
            item=dict(record)
            if item['status']=='valid':
                item['response_raw']=(output/'responses'/f'{item["attempt_id"]}.bin').read_bytes()
            analysis_records.append(item)
        report=summarize(rows,analysis_records,key,mode)
        report.update(stop_reason=stop, known_usage_estimated_usd=str(charge), unknown_usage=unknown_usage,
                      live_requests_sent=report['attempted_requests'] if mode=='live' else 0)
        (output/'report.json').write_bytes(encode(report))
        (output/'manifest.json').write_bytes(encode({'mode':mode,'artifacts':artifacts(output)}))
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['mock','live'], default='mock')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--preflight', type=Path)
    args=parser.parse_args()
    preflight=json.loads(args.preflight.read_text()) if args.preflight else None
    transport=mock_transport if args.mode=='mock' else LiveTransport(os.environ.get('TYPESAFE_API_KEY',''))
    report=run(args.output,transport,args.mode,preflight)
    print(json.dumps({'mode':args.mode,'counts':report['request_counts'],'live_requests_sent':report['live_requests_sent']}))
