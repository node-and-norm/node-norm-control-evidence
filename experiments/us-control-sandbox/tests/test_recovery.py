import copy
import tempfile
import unittest
from pathlib import Path
from recovery import CASES, execute, run
from recovery_observer import observe
from verify_run import verify


class RecoveryChecks(unittest.TestCase):
    def execute_case(self, name, case=None):
        with tempfile.TemporaryDirectory() as temp:
            return execute(case or CASES[name], Path(temp)/'state.sqlite')

    def test_restart_loses_only_volatile_stop(self):
        good, good_packet, _ = self.execute_case('durable-stop-restart')
        bad, bad_packet, _ = self.execute_case('volatile-stop-restart')
        self.assertEqual(good_packet['events'], bad_packet['events'])
        self.assertEqual((good['effect_count'], bad['effect_count']), (0, 1))
        same_process, _, _ = self.execute_case('volatile-stop-without-restart')
        self.assertEqual(same_process['effect_count'], 0)

    def test_retry_counts_actual_effects(self):
        good, _, _ = self.execute_case('deduplicated-retry-after-restart')
        bad, _, _ = self.execute_case('duplicate-effect-after-restart')
        self.assertEqual(good['request_ids'], ['request-1'])
        self.assertEqual(bad['request_ids'], ['request-1', 'request-1'])

    def test_stop_blocks_repeated_commit(self):
        outcome, _, processes = self.execute_case('stop-blocks-repeated-commit')
        self.assertEqual(outcome['effect_count'], 0)
        self.assertEqual(len(processes), 3)

    def test_withholding_does_not_change_execution(self):
        good, _, _ = self.execute_case('durable-stop-restart')
        hidden, packet, _ = self.execute_case('durable-stop-withheld-evidence')
        self.assertEqual(good, hidden)
        self.assertIsNone(packet['downstream'])

    def test_expected_labels_do_not_drive_worker(self):
        case = copy.deepcopy(CASES['durable-stop-restart'])
        case.update(expected=99, maximum=99)
        observed, _, _ = self.execute_case('', case)
        self.assertEqual(observed['effect_count'], 0)

    def test_missing_store_is_not_success(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(sqlite3.OperationalError):
                observe(Path(temp)/'absent.sqlite')

    def test_manifest_and_failure_accounting(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'run'
            result = run(output)
            self.assertEqual((result['checks_passed'], result['checks_total'], result['control_objectives_met']), (7, 7, 5))
            self.assertGreater(verify(output), 0)
            with self.assertRaises(FileExistsError):
                run(output)
