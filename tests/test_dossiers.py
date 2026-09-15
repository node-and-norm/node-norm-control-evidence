"""Presentation must preserve uncertainty, separation, and untrusted source text."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_dossier import render
from validate import packet_hash,validate

class DossierTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'examples/synthetic.json').read_text())

    def refreeze(self):
        for p in self.data['packet']:
            p['content_sha256']=packet_hash(self.data,p)
            for a in self.data['annotation']: a['packet_sha256']=p['content_sha256']

    def test_packet_does_not_expose_interpretive_layers(self):
        self.data['control'][0]['objective']='SECRET_EXPECTED_CONTROL'
        self.data['claim'][0]['statement']='SECRET_SOURCE_CLAIM_OBJECT'
        self.data['annotation'][0]['rationale']='SECRET_INITIAL_RATING'
        self.data['adjudication'][0]['reason']='SECRET_ADJUDICATION'
        self.refreeze()
        result=render(self.data,'packet')
        self.assertNotIn('SECRET',result)
        self.assertNotIn('Initial judgments',result)
        self.assertIn('Located evidence',result)

    def test_uncoded_never_becomes_negative_or_missingness_label(self):
        self.data['annotation']=[];self.data['adjudication']=[]
        result=render(self.data)
        self.assertIn('Uncoded dimensions (17)',result)
        self.assertNotIn('not&#95;reported',result)
        self.assertNotIn('| no |',result)

    def test_render_is_inert_and_deterministic(self):
        self.data['evidence_item'][0]['observation']='<script>alert(1)</script> | [fake](https://bad.invalid)\n## forged'
        self.refreeze()
        first=render(self.data)
        self.assertEqual(first,render(copy.deepcopy(self.data)))
        self.assertNotIn('<script>',first)
        self.assertNotIn('[fake]',first)
        self.assertNotIn('\n## forged',first)
        self.assertIn('&#124;',first)

    def test_stale_packet_cannot_be_rendered(self):
        self.data['evidence_item'][0]['observation']='Changed after the packet was committed.'
        with self.assertRaisesRegex(ValueError,'packet content hash mismatch'): render(self.data)

    def test_empirical_display_stays_closed(self):
        self.data['mode']='empirical';self.data['event'][0]['synthetic']=False
        self.data['packet'][0]['cohort']='pilot'
        for s in self.data['source']: s.update(role='investigation',rights='metadata_only')
        self.data['annotation']=[];self.data['adjudication']=[]
        self.refreeze()
        self.assertEqual(validate(self.data),[])
        for view in ['review','packet']:
            with self.assertRaisesRegex(ValueError,'empirical publication'):render(self.data,view)

    def test_examples_retain_different_evidentiary_states(self):
        for name,dimension,value in [('synthetic.json','propagation','not_reported'),('override-confirmed.json','propagation','yes'),('policy-only.json','intervention_attempted','not_reported')]:
            data=json.loads((ROOT/'examples'/name).read_text())
            self.assertEqual(validate(data),[])
            self.assertEqual(data['annotation'][0]['dimension'],dimension)
            self.assertEqual(data['annotation'][0]['value'],value)
            self.assertIn('Invented demonstration',render(data))

if __name__=='__main__':unittest.main()
