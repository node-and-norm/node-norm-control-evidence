"""Render a validated synthetic bundle as a review dossier or blind source packet.

Review views expose labels and must not be supplied for independent initial coding.
Packet views omit control enumeration, claims, ratings, and adjudication.
"""
import argparse
import html
import json
from pathlib import Path
from export import export
from validate import ROOT


def cell(value):
    """Keep record text inert inside GitHub Markdown tables and headings."""
    special = {'\\', '`', '*', '_', '[', ']', '|', '#', '~'}
    value = ''.join(f'&#{ord(char)};' if char in special else html.escape(char, quote=True) for char in str(value))
    return value.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>')


def table(headers, rows):
    out = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(':---' for _ in headers) + ' |']
    out += ['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows]
    return '\n'.join(out)


def render(data, view='review'):
    if view not in {'review', 'packet'}:
        raise ValueError('view must be review or packet')
    package = export(data)  # Includes structural validation and synthetic-only guard.
    dims = json.loads((ROOT / 'schemas/annotation.schema.json').read_text())['properties']['dimension']['enum']
    out = [f'# Synthetic {"review dossier" if view == "review" else "source packet"}',
           '> **Invented demonstration. No observed event, human judgment, or empirical finding.**']
    if view == 'review':
        out += ['> **Review view exposes proposed controls and labels. Do not use it for blind enumeration or independent initial coding.**']
    else:
        out += ['Control enumeration, source-claim objects, ratings, and adjudications are omitted from this view. This projection does not certify reviewer independence or remove clues present in source evidence.']
    out += ['## Event scope', table(['Event', 'Period', 'Scope note'],
            [(e['title'], e['occurred_at'], e['time_note']) for e in data['event']])]
    out += ['## Frozen packets', table(['Packet / event', 'Cutoff / version', 'Retrieval and omissions'],
            [(p['id']+' / '+p['event_id'],p['cutoff']+' / '+p['version'],p['retrieval_log']+' '+p['omissions']) for p in data['packet']])]
    # Display only evidence in packets, and only sources connected to that evidence.
    evidence_ids = {identity for p in data['packet'] for identity in p['evidence_ids']}
    evidence = [e for e in data['evidence_item'] if e['id'] in evidence_ids]
    source_ids = {e['source_id'] for e in evidence}
    while True:
        linked = {r['to_source_id'] for r in data['provenance_relation'] if r['from_source_id'] in source_ids}
        if linked <= source_ids: break
        source_ids |= linked
    sources = [s for s in data['source'] if view == 'review' or s['id'] in source_ids]
    out += ['## Located evidence', table(['Evidence / source', 'Location', 'Observation'],
            [(e['id']+' / '+e['source_id'],e['locator'],e['observation']) for e in evidence])]
    out += ['## Sources and dependence', 'Review views include all bundle source metadata; packet views include only sources connected to frozen evidence.', table(['Source', 'Role', 'Family'],
            [(s['id']+': '+s['title'],s['role'],s['family_id']) for s in sources])]
    relations=[r for r in data['provenance_relation'] if view == 'review' or r['from_source_id'] in source_ids]
    if relations:
        out += [table(['From', 'Relation', 'To', 'Basis'], [(r['from_source_id'],r['relation'],r['to_source_id'],r['basis']) for r in relations])]
    out += ['<details>\n<summary><strong>Source URLs and evidence-quality notes</strong></summary>\n',
            table(['Source / field', 'Recorded value'],[(s['id']+' / '+k,s[k]) for s in sources for k in ['url','source_date','retrieved_at','version','rights','rights_basis']]),
            table(['Evidence', 'Dimension', 'Recorded assessment'],[(e['id'],k,v) for e in evidence for k,v in dict(valid_from=e['valid_from'],time_note=e['time_note'],**e['quality']).items()]),'</details>']
    if view == 'review':
        out += ['## Proposed controls',table(['Control / event','Objective and opportunity','Functions / relevant period'],
                [(c['id']+' / '+c['event_id'],c['objective']+' '+c['opportunity'],', '.join(c['functions'])+' / '+str(c['relevant_from'])+' to '+str(c['relevant_to'])) for c in data['control']])]
        out += ['## Source claims',table(['Claim / source','Statement','Evidence IDs / status'],
                [(c['id']+' / '+c['asserted_by_source_id'],c['statement'],', '.join(c['evidence_ids'])+' / '+c['status']) for c in data['claim']])]
        out += ['## Initial judgments', 'Each value belongs to its stated packet. **Uncoded** means no annotation was supplied; it is a display label, never a missingness code.']
        for c in data['control']:
            for p in data['packet']:
                if p['event_id'] != c['event_id']: continue
                ratings=[a for a in data['annotation'] if a['control_id']==c['id'] and a['packet_id']==p['id']]
                rows=[]
                for dim in dims:
                    matches=[a for a in ratings if a['dimension']==dim]
                    if not matches: continue
                    for a in matches:
                        rows.append((dim,a['value'],a['id']))
                out += ['### '+cell(c['id'])+' · '+cell(p['id']),table(['Dimension','Value','Annotation'],rows)]
                if ratings:
                    out += ['<details>\n<summary><strong>Judgment provenance, evidence, and rationale</strong></summary>\n']
                    for a in ratings:
                        out += ['**'+cell(a['id'])+'**',table(['Field','Recorded value'],[(k,', '.join(a[k]) if isinstance(a[k],list) else a[k]) for k in ['coder_id','coder_kind','status','independent','eligibility_record','evidence_ids','rationale','codebook_version','coded_at']])]
                    out += ['</details>']
                uncoded=[d for d in dims if not any(a['dimension']==d for a in ratings)]
                if uncoded:
                    out += ['<details>\n<summary><strong>Uncoded dimensions ('+str(len(uncoded))+')</strong></summary>\n', ', '.join(cell(d) for d in uncoded)+'. No value is inferred for these dimensions.','</details>']
        out += ['## Separate adjudication', table(['Adjudication','Initial records','Value','Reason'],
                [(a['id'],', '.join(a['annotation_ids']),a['value'],a['reason']) for a in data['adjudication']]),
                'No human agreement or validity result can be calculated from these invented judgments.']
    # Packet view deliberately omits the full-bundle hash: it commits only to frozen source content.
    out += ['<details>\n<summary><strong>Integrity commitments</strong></summary>\n',
            table(['Packet', 'Content SHA-256'],[(p['id'],p['content_sha256']) for p in data['packet']]),
            'Packet hashes commit to supplied metadata, including the predefined control scope. They do not prove source-byte custody or reviewer non-exposure. Blind enumeration requires separately governed packet construction.']
    if view == 'review': out += ['Input SHA-256: `'+package['input_sha256']+'`']
    out += ['</details>', '**Development boundary:** this renderer accepts synthetic bundles only. Empirical display requires a reviewed projection, rights decisions, and research approval.']
    return '\n\n'.join(out)+'\n'


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('bundle',type=Path)
    parser.add_argument('--view',choices=['review','packet'],default='review')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=render(json.loads(args.bundle.read_text()),args.view)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(result)
    print(f'Wrote synthetic {args.view} view: {args.output}')
