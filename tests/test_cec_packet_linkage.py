import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'experiments/jev-cec/packet-linkage-001'
spec = importlib.util.spec_from_file_location('packet_linkage', FOLDER / 'prepare.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PacketLinkageTests(unittest.TestCase):
    def test_only_issuance_sentence_changes(self):
        rows = module.schedule()
        self.assertEqual(len(rows), 8)
        for pass_id in (1, 2):
            for card in ('V2-12-A', 'V2-12-B'):
                pair = {r['condition']: r['payload'] for r in rows if r['pass'] == pass_id and r['card_id'] == card}
                explicit = copy.deepcopy(pair['explicit'])
                explicit['state']['evidence'][0]['text'] = explicit['state']['evidence'][0]['text'].replace(module.NEW, module.OLD, 1)
                self.assertEqual(explicit, pair['original'])
                self.assertEqual(set(explicit), {'model', 'questions', 'state'})
                self.assertEqual(set(explicit['state']), {'evidence', 'scope', 'synthetic'})
        self.assertEqual([r['condition'] for r in rows], ['original','explicit','explicit','original','explicit','original','original','explicit'])

    def test_unresolved_reference_stays_outside_payload(self):
        refs = json.loads((FOLDER / 'reference.json').read_text())['conditions']
        for card in ('V2-12-A', 'V2-12-B'):
            self.assertIsNone(refs['original'][card]['action']['label'])
            self.assertEqual(refs['explicit'][card]['action']['label'], 'yes')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'prepared'
            module.prepare(path)
            manifest = json.loads((path / 'manifest.json').read_text())
            self.assertEqual(manifest['requests_sent'], 0)
            self.assertEqual(manifest['scheduled_judgments'], 32)
            with self.assertRaises(FileExistsError):
                module.prepare(path)
