import json
from pathlib import Path
import shutil
import tempfile
import unittest
from build_evidence_appendices import ROOT, RUNS, appendix, documents, write, check


class EvidenceAppendices(unittest.TestCase):
    def packet(self, name):
        return json.loads((ROOT/'runs/rehearsal-002/assessment-packets'/name).read_text())

    def extract(self, packet):
        return appendix(packet, 'test-packet', 'test-digest')

    def test_acknowledgment_does_not_become_control_finding(self):
        good = self.extract(self.packet('packet-001.json'))
        bad = self.extract(self.packet('packet-002.json'))
        self.assertEqual(good['observations'][0], bad['observations'][0])
        self.assertNotEqual(good['observations'][1]['value'], bad['observations'][1]['value'])
        self.assertFalse(good['method_assessment']['hit_scoring_enabled'])
        self.assertFalse(good['method_assessment']['tae_scoring_enabled'])

    def test_missing_outcome_stays_unresolved(self):
        result = self.extract(self.packet('packet-005.json'))
        self.assertEqual(len(result['unresolved']), 1)
        self.assertEqual(result['unresolved'][0]['locator'], '/downstream')
        self.assertTrue(all(o['locator'].startswith('/events/') for o in result['observations']))

    def test_valid_rejected_response_is_preserved(self):
        result = self.extract(self.packet('packet-004.json'))
        self.assertIs(result['observations'][0]['value']['accepted'], False)

    def test_extra_conclusions_are_rejected(self):
        for extra in ('expected', 'score', 'human_authority', 'control_objective_met'):
            packet = self.packet('packet-001.json')
            packet[extra] = True
            with self.assertRaises(ValueError):
                self.extract(packet)

    def test_inconsistent_effect_record_is_rejected(self):
        with self.assertRaises(ValueError):
            self.extract({'events': [], 'downstream': {'effect_count': 2, 'request_ids': ['one']}})

    def test_string_boolean_is_rejected(self):
        packet = self.packet('packet-001.json')
        packet['events'][0]['accepted'] = 'false'
        with self.assertRaises(ValueError):
            self.extract(packet)

    def test_no_oracle_or_database_is_required(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for run in RUNS:
                (root/run).mkdir(parents=True)
                shutil.copyfile(ROOT/run/'manifest.json', root/run/'manifest.json')
                shutil.copytree(ROOT/run/'assessment-packets', root/run/'assessment-packets')
            self.assertEqual(documents(root), documents())
            damaged = root/RUNS[0]/'assessment-packets/packet-001.json'
            damaged.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'hash'):
                documents(root)

    def test_extra_packet_fails_inventory_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for run in RUNS:
                (root/run).mkdir(parents=True)
                shutil.copyfile(ROOT/run/'manifest.json', root/run/'manifest.json')
                shutil.copytree(ROOT/run/'assessment-packets', root/run/'assessment-packets')
            (root/RUNS[0]/'assessment-packets/extra.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'inventory'):
                documents(root)

    def test_reproduction_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'appendices'
            self.assertEqual(write(output), 16)
            self.assertEqual(check(output), 16)
            with self.assertRaises(FileExistsError):
                write(output)
            artifact = next(output.glob('*.json'))
            result = json.loads(artifact.read_text())
            result['method_assessment']['hit_scoring_enabled'] = True
            artifact.write_text(json.dumps(result))
            with self.assertRaises(ValueError):
                check(output)
