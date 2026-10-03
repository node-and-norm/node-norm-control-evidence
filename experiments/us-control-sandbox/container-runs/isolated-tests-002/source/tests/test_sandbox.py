import tempfile
import unittest
from pathlib import Path
from sandbox import CASES, execute, run

class Controls(unittest.TestCase):
    def test_acknowledgment_does_not_establish_effect(self):
        good, good_packet = execute(CASES['working-stop'])
        bad, bad_packet = execute(CASES['acknowledged-but-continues'])
        self.assertEqual(good_packet['events'], bad_packet['events'])
        self.assertNotEqual(good, bad)

    def test_withholding_does_not_change_execution(self):
        full, _ = execute(CASES['working-stop'])
        withheld, packet = execute(CASES['working-stop-missing-evidence'])
        self.assertEqual(full, withheld)
        self.assertIsNone(packet['downstream'])

    def test_boundary_and_late_commands_cannot_retroactively_stop(self):
        for at in (10, 11):
            case = dict(CASES['working-stop'], at=at)
            actual, packet = execute(case)
            self.assertEqual(actual['action'], 'executed')
            self.assertFalse(packet['events'][0]['accepted'])

    def test_unauthorized_command_rejected(self):
        actual, packet = execute(CASES['unauthorized-stop'])
        self.assertEqual(actual['action'], 'executed')
        self.assertFalse(packet['events'][0]['accepted'])

    def test_reproduction_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/'a', Path(tmp)/'b'
            self.assertEqual(run(a), run(b))
            for file in a.rglob('*.json'):
                self.assertEqual(file.read_bytes(), (b/file.relative_to(a)).read_bytes())
            with self.assertRaises(FileExistsError):
                run(a)

class EvidenceControls(unittest.TestCase):
    def test_recipient_effect_is_separate_from_internal_correction(self):
        good, a = execute(CASES['correction-delivered'])
        bad, b = execute(CASES['correction-not-delivered'])
        self.assertEqual(a['events'], b['events'])
        self.assertEqual(good['internal_record'], bad['internal_record'])
        self.assertNotEqual(good['recipient_record'], bad['recipient_record'])

    def test_observer_rejects_missing_database(self):
        import sqlite3
        from observer import observe
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(sqlite3.OperationalError):
                observe(Path(tmp)/'absent.sqlite')

    def test_outcome_not_taken_from_expected_label(self):
        case = dict(CASES['working-stop'], expected='executed')
        actual, _ = execute(case)
        self.assertEqual(actual['action'], 'prevented')

    def test_packet_does_not_include_case_oracle(self):
        for case in CASES.values():
            _, packet = execute(case)
            self.assertEqual(set(packet), {'events', 'downstream'})

    def test_artifact_tampering_detected(self):
        from verify_run import verify
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'run'
            run(root)
            self.assertGreater(verify(root), 0)
            packet = root/'assessment-packets'/'packet-001.json'
            packet.write_text('{}')
            with self.assertRaises(ValueError):
                verify(root)

if __name__ == '__main__':
    unittest.main()
