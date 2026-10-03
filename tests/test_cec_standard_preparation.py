import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/'experiments/jev-cec/development-v2'
spec=importlib.util.spec_from_file_location('cec_standard',ROOT/'prepare_standard.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class StandardPreparationTests(unittest.TestCase):
    def test_complete_answer_free_projection(self):
        rows=list(m.requests())
        self.assertEqual(len(rows),26)
        self.assertEqual(len({i for i,r in rows}),26)
        for i,r in rows:
            self.assertEqual(set(r),{'model','state','questions'})
            self.assertEqual(set(r['state']),{'synthetic','scope','evidence'})
            self.assertEqual(set(r['questions']),m.DIMS)
            self.assertNotIn('expected',json.dumps(r['state']))
            self.assertNotIn('pair_id',r['state'])

    def test_reference_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for rel in ['cards.json','expansion-001/cards.json','standard-001/questions.json']:
                dst=p/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((ROOT/rel).read_bytes())
            self.assertEqual(list(m.requests(p)),list(m.requests()))
            (p/'proposed-reference.json').write_text('not valid JSON')
            self.assertEqual(list(m.requests(p)),list(m.requests()))

    def test_unexpected_answer_field_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'standard-001').mkdir()
            (p/'standard-001/questions.json').write_bytes((ROOT/'standard-001/questions.json').read_bytes())
            cards=json.loads((ROOT/'cards.json').read_text());cards[0]['expected']={'action':'yes'}
            (p/'cards.json').write_text(json.dumps(cards))
            with self.assertRaises(ValueError):list(m.requests(p))

    def test_preparation_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'prepared';m.prepare(out)
            index=json.loads((out/'index.json').read_text())
            self.assertEqual(index['status'],'offline_unfrozen')
            self.assertEqual(len(index['requests']),26)
            with self.assertRaises(FileExistsError):m.prepare(out)
