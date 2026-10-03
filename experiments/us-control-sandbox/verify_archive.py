"""Verify archived artifacts without rerunning historical or container code."""
import hashlib
import json
from pathlib import Path
from verify_run import verify

ROOT = Path(__file__).resolve().parent


def main():
    runs = ['runs/rehearsal-002', 'runs/recovery-001',
            'container-runs/isolated-001/result', 'container-runs/recovery-001/result']
    counts = {run: verify(ROOT/run) for run in runs}
    old = json.loads((ROOT/'runs/rehearsal-001/manifest.json').read_text())
    if hashlib.sha256((ROOT/'archive/rehearsal-v0/sandbox.py').read_bytes()).hexdigest() != old['source_sha256']:
        raise ValueError('Initial source snapshot differs from recorded hash')
    tests = ROOT/'container-runs/isolated-tests-002'
    expected = json.loads((tests/'source-manifest.json').read_text())
    actual = {str(p.relative_to(tests/'source')):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (tests/'source').rglob('*') if p.is_file()}
    if expected != actual:
        raise ValueError('Test source snapshot differs from recorded hashes')
    print(json.dumps({'artifact_counts': counts, 'initial_source_verified': True,
                      'expanded_test_sources_verified': len(expected)}, indent=2))


if __name__ == '__main__':
    main()
