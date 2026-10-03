"""Boundary tests for optional offline CEC request preparation."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cec_prepare', ROOT / 'experiments/jev-cec/prepare.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from validate import packet_hash


class PreparationTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / 'examples/synthetic.json').read_text())

    def rehash(self, data):
        value = packet_hash(data, data['packet'][0])
        data['packet'][0]['content_sha256'] = value
        for row in data['annotation']:
            row['packet_sha256'] = value

    def test_answer_objects_and_titles_do_not_enter_request(self):
        data = self.fixture()
        original = module.prepare(data)
        data['event'][0]['title'] = 'ANSWER CUE'
        data['packet'][0]['omissions'] = 'ANSWER CUE'
        data['claim'][0]['statement'] = 'ANSWER CUE'
        for row in data['annotation']:
            row['rationale'] = 'ANSWER CUE'
        self.rehash(data)
        self.assertEqual(original, module.prepare(data))
        self.assertNotIn('ANSWER CUE', json.dumps(original))
        self.assertNotIn('annotation', original['state'])

    def test_evidence_change_changes_request(self):
        data = self.fixture()
        old = module.prepare(data)
        data['evidence_item'][0]['observation'] = 'A stop acknowledgement is supplied.'
        self.rehash(data)
        self.assertNotEqual(old, module.prepare(data))

    def test_bad_hash_and_empirical_mode_rejected(self):
        data = self.fixture()
        data['packet'][0]['content_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            module.prepare(data)
        data = self.fixture()
        data['mode'] = 'empirical'
        with self.assertRaisesRegex(ValueError, 'synthetic'):
            module.prepare(data)

    def test_multiple_controls_and_missing_packet_rejected(self):
        data = self.fixture()
        data['packet'] = []
        with self.assertRaises(ValueError):
            module.prepare(data)
        data = self.fixture()
        control = copy.deepcopy(data['control'][0])
        control['id'] = 'CONTROL_2'
        data['control'].append(control)
        self.rehash(data)
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            module.prepare(data)

    def test_linked_source_family_preserved(self):
        data = self.fixture()
        # A packet that cites the derivative must retain its upstream family.
        data['evidence_item'][0]['source_id'] = 'SRC_2'
        self.rehash(data)
        state = module.prepare(data)['state']
        self.assertEqual({s['id'] for s in state['sources']}, {'SRC_1', 'SRC_2'})
        self.assertEqual({s['family_id'] for s in state['sources']}, {'FAMILY_1'})
        self.assertEqual(state['source_relations'][0]['relation'], 'derived_from')

    def test_all_codebook_values_and_three_separate_questions(self):
        request = module.prepare(self.fixture())
        self.assertEqual(set(request['questions']), {'action', 'propagation', 'outcome_mitigation'})
        schema = json.loads((ROOT / 'schemas/annotation.schema.json').read_text())
        for q in request['questions'].values():
            self.assertEqual(set(q['criteria']), set(schema['properties']['value']['enum']))
        self.assertEqual(request['model'], 'jev-1.13.0')

    def test_export_hashes_reproducibility_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'a'
            manifest = module.export(folder)
            self.assertEqual(manifest['requests_sent'], 0)
            self.assertIsNone(manifest['model_resolved'])
            self.assertEqual(manifest['requests_prepared'], 3)
            self.assertEqual(set(p.name for p in folder.iterdir()), set(manifest['artifacts']) | {'manifest.json'})
            for name, sha in manifest['artifacts'].items():
                self.assertEqual(module.digest((folder / name).read_bytes()), sha)
            with self.assertRaises(FileExistsError):
                module.export(folder)
            self.assertEqual(manifest, module.export(Path(tmp) / 'b'))

    def test_preserved_preparation_artifact_set_and_hashes(self):
        folder = ROOT / 'experiments/jev-cec/prepared-001'
        manifest = json.loads((folder / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'prepared-only')
        self.assertEqual(manifest['requests_sent'], 0)
        self.assertEqual({p.name for p in folder.iterdir()}, set(manifest['artifacts']) | {'manifest.json'})
        for name, sha in manifest['artifacts'].items():
            self.assertEqual(module.digest((folder / name).read_bytes()), sha)
