"""Checks for the frozen, offline documentary challenge."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cec_challenge', ROOT / 'experiments/jev-cec/challenge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ChallengeTests(unittest.TestCase):
    def test_frozen_set_and_coverage_limits(self):
        cards, questions = m.check()
        self.assertEqual(len(cards), 12)
        self.assertEqual(set(questions), m.DIMS)
        key = json.loads((m.FOLDER / 'reference-key.json').read_text())
        observed = {j['value'] for row in key for j in row['judgments'].values()}
        self.assertEqual(observed, m.LABELS - {'not_applicable'})

    def test_tampered_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'set'
            shutil.copytree(m.FOLDER, folder)
            with (folder / 'cards.json').open('a') as f:
                f.write(' ')
            with self.assertRaisesRegex(ValueError, 'Freeze mismatch'):
                m.check(folder)

    def test_key_cannot_change_request_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'set'
            shutil.copytree(m.FOLDER, folder)
            before = m.prepare(root / 'a', folder)
            key = json.loads((folder / 'reference-key.json').read_text())
            key[0]['condition'] = 'SECRET ANSWER HINT'
            key[0]['judgments']['action']['rationale'] = 'SECRET ANSWER HINT'
            (folder / 'reference-key.json').write_bytes(m.encode(key))
            freeze = json.loads((folder / 'freeze.json').read_text())
            freeze['artifacts']['reference-key.json'] = m.sha((folder / 'reference-key.json').read_bytes())
            (folder / 'freeze.json').write_bytes(m.encode(freeze))
            after = m.prepare(root / 'b', folder)
            self.assertEqual(before, after)
            self.assertNotIn('SECRET ANSWER HINT', json.dumps(after))

    def test_reject_label_fields_empirical_duplicate_and_bad_reference(self):
        cards, _ = m.check()
        for change in ('label', 'empirical', 'duplicate', 'source'):
            bad = copy.deepcopy(cards)
            if change == 'label':
                bad[0]['state']['expected'] = 'yes'
            elif change == 'empirical':
                bad[0]['state']['synthetic'] = False
            elif change == 'duplicate':
                bad[1]['id'] = bad[0]['id']
            else:
                bad[0]['state']['evidence'][0]['source_id'] = 'MISSING'
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.validate_cards(bad)

    def test_preserve_silence_barrier_conflict_and_partial_separately(self):
        key = {r['id']:r for r in json.loads((m.FOLDER / 'reference-key.json').read_text())}
        expected = {'C02':'not_reported','C04':'no','C05':'conflicting','C08':'not_observable','C09':'unknown','C10':'partial'}
        for identity, value in expected.items():
            self.assertEqual(key[identity]['judgments']['propagation']['value'], value)
        self.assertEqual(key['C11']['judgments']['outcome_mitigation']['value'], 'yes')
        self.assertEqual(key['C12']['judgments']['propagation']['value'], 'yes')
        self.assertEqual(key['C12']['judgments']['outcome_mitigation']['value'], 'no')

    def test_output_provenance_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            rows = m.prepare(out)
            manifest = json.loads((out / 'manifest.json').read_text())
            self.assertEqual(manifest['requests_sent'], 0)
            self.assertEqual(manifest['questions_prepared'], 36)
            self.assertEqual(manifest['requests_sha256'], m.sha((out / 'requests.json').read_bytes()))
            for row in rows:
                self.assertEqual(set(row['payload']), {'model', 'state', 'questions'})
                self.assertEqual(manifest['payload_sha256'][row['card_id']], m.sha(m.encode(row['payload'])))
            with self.assertRaises(FileExistsError):
                m.prepare(out)
