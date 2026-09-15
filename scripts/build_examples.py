"""Reproduce two contrasting synthetic bundles and all demonstration views."""
import copy
import json
from pathlib import Path
from validate import ROOT, packet_hash, validate
from render_dossier import render


def freeze(data):
    for packet in data['packet']:
        packet['content_sha256']=packet_hash(data,packet)
        for rating in data['annotation']:
            if rating['packet_id']==packet['id']: rating['packet_sha256']=packet['content_sha256']
    errors=validate(data)
    if errors: raise ValueError('; '.join(errors))
    return data


def rating(base, identity, dimension, value, rationale, evidence):
    row=copy.deepcopy(base)
    row.update(id=identity,dimension=dimension,value=value,rationale=rationale,evidence_ids=evidence)
    return row


def build():
    original=json.loads((ROOT/'examples/synthetic.json').read_text())
    confirmed=copy.deepcopy(original)
    confirmed['event'][0]['title']='Synthetic acknowledged stop with unresolved mitigation'
    confirmed['evidence_item'][0]['observation']='The invented trace records an override command and a downstream stop acknowledgement. Consequences and alternatives are not reported.'
    confirmed['packet'][0]['omissions']='Consequences and alternative trajectories intentionally absent.'
    confirmed['claim'][0]['statement']='The synthetic trace describes acknowledgement of a stop.'
    for a in confirmed['annotation']:
        a.update(value='yes',evidence_ids=['EVID_1'],rationale='The invented downstream acknowledgement documents propagation within this fixture.')
    confirmed['annotation'].append(rating(confirmed['annotation'][0],'ANN_3','outcome_mitigation','not_reported','No consequences or alternative trajectory are reported in the invented packet.',[]))
    confirmed['adjudication'][0].update(value='yes',reason='Synthetic agreement on propagation only; mitigation remains unresolved.')
    policy=copy.deepcopy(original)
    policy['event'][0]['title']='Synthetic policy-only approval role'
    policy['provenance_relation'][0]['basis']='The invented summary repeats the policy statement.'
    policy['source'][0].update(title='Invented approval policy',url='https://example.invalid/synthetic/policy')
    policy['evidence_item'][0].update(locator='Invented policy paragraph 1',observation='The invented policy assigns an operator authority to withhold approval. No implementation or runtime action is described.')
    policy['control'][0].update(objective='Require an operator approval before execution.',opportunity='A proposed action awaits release.',functions=['human_oversight','authorization_governance'])
    policy['claim'][0].update(statement='The synthetic policy assigns approval authority.')
    policy['packet'][0]['omissions']='Implementation, permissions, runtime actions, and consequences intentionally absent.'
    for a in policy['annotation']:
        a.update(dimension='intervention_attempted',rationale='The invented policy does not report an intervention.')
    policy['annotation'].append(rating(policy['annotation'][0],'ANN_3','formal_authority','yes','The invented policy assigns the role approval authority.',['EVID_1']))
    policy['adjudication'][0].update(reason='Synthetic agreement about packet silence on an attempt; no conclusion about whether one occurred.')
    bundles=[('override-unresolved','synthetic.json',original),('override-confirmed','override-confirmed.json',freeze(confirmed)),('policy-only','policy-only.json',freeze(policy))]
    for slug,name,data in bundles:
        if name!='synthetic.json': (ROOT/'examples'/name).write_text(json.dumps(data,indent=2)+'\n')
        for view,folder in [('review','dossiers'),('packet','packets')]:
            path=ROOT/'examples'/folder/(slug+'.md');path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('[Example gallery](../README.md)\n\n'+render(data,view))
    print('Reproduced 3 synthetic cases and 6 Markdown views.')

if __name__=='__main__': build()
