import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate, packet_hash
from export import export, canonical

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/synthetic.json").read_text())

    def rejected(self, phrase):
        self.assertTrue(any(phrase in e for e in validate(self.data)), validate(self.data))

    def test_valid_fixture(self):
        self.assertEqual(validate(self.data), [])

    def test_missingness_is_not_no(self):
        self.data["annotation"][0]["value"] = "no"
        self.rejected("requires evidence")

    def test_packet_scope(self):
        self.data["packet"][0]["evidence_ids"] = []
        self.data["annotation"][0]["evidence_ids"] = ["EVID_1"]
        self.rejected("outside frozen packet")

    def test_duplicate_id(self):
        self.data["event"].append(copy.deepcopy(self.data["event"][0]))
        self.rejected("duplicate ID")

    def test_ai_not_human(self):
        self.data["annotation"][0]["coder_kind"] = "ai"
        self.rejected("AI cannot")

    def test_derivative_independence(self):
        self.data["provenance_relation"].append({"id": "REL_2", "from_source_id": "SRC_2", "to_source_id": "SRC_1", "relation": "independent_corroboration", "basis": "Different publisher, incorrectly assumed independent."})
        self.rejected("shared upstream")

    def test_cycle(self):
        self.data["provenance_relation"].append({"id": "REL_2", "from_source_id": "SRC_1", "to_source_id": "SRC_2", "relation": "derived_from", "basis": "Invalid cycle."})
        self.rejected("cyclic")

    def test_time_cutoff(self):
        self.data["source"][0]["retrieved_at"] = "2026-09-15T00:00:00Z"
        self.rejected("after cutoff")

    def test_adjudication_dimension_mismatch(self):
        self.data["annotation"][1]["dimension"] = "action"
        self.rejected("adjudication mixes")

    def test_false_approval(self):
        self.data["release"][0]["status"] = "approved"
        self.rejected("approval is unavailable")

    def test_unknown_field(self):
        self.data["annotation"][0]["control_failed"] = True
        self.rejected("schema")

    def test_export_deterministic_and_labeled(self):
        first = canonical(export(self.data))
        self.assertEqual(first, canonical(export(self.data)))
        self.assertIn(b"synthetic_development_demo", first)

    def test_export_refuses_empirical(self):
        self.data["mode"] = "empirical"
        self.data["event"][0]["synthetic"] = False
        self.data["packet"][0]["cohort"] = "pilot"
        for source in self.data["source"]:
            source["role"] = "news"
            source["rights"] = "unknown"
        for annotation in self.data["annotation"]:
            annotation["coder_kind"] = "human"
            annotation["independent"] = True
        self.data["packet"][0]["content_sha256"] = packet_hash(self.data, self.data["packet"][0])
        for annotation in self.data["annotation"]:
            annotation["packet_sha256"] = self.data["packet"][0]["content_sha256"]
        self.assertEqual(validate(self.data), [])
        with self.assertRaisesRegex(ValueError, "empirical publication"):
            export(self.data)

    def test_changed_packet_detected(self):
        self.data["evidence_item"][0]["observation"] = "A changed statement after coding."
        self.rejected("packet content hash mismatch")

    def test_wrong_annotation_hash(self):
        self.data["annotation"][0]["packet_sha256"] = "0" * 64
        self.rejected("another packet hash")

    def test_cross_event_claim(self):
        event = copy.deepcopy(self.data["event"][0])
        event["id"] = "EVENT_2"
        self.data["event"].append(event)
        self.data["evidence_item"][0]["event_id"] = "EVENT_2"
        self.rejected("claim evidence from another event")

if __name__ == "__main__":
    unittest.main()
