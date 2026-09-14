"""Generate the standalone development schemas. No network resolution required."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = {"type": "string", "minLength": 1}
ID = {"type": "string", "pattern": "^[A-Z][A-Z0-9_-]+$"}
IDS = {"type": "array", "items": ID, "uniqueItems": True}
TIME = {"type": "string", "format": "date-time"}
NULLTIME = {"anyOf": [TIME, {"type": "null"}]}
HASH = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
VALUES = ["yes", "no", "partial", "conflicting", "unknown", "not_observable", "not_reported", "not_applicable"]
DIMENSIONS = ["declared", "design_adequacy", "implemented", "operating", "trigger", "action", "propagation", "trajectory_effect", "outcome_mitigation", "formal_authority", "information", "comprehension_opportunity", "intervention_time", "technical_permission", "institutional_permission", "alternatives", "intervention_attempted"]

def enum(values):
    return {"enum": values}

def obj(fields):
    return {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False}

def record(fields):
    return obj({"id": ID, **fields})

defs = {
    "event": record({"title": S, "event_class": enum(["incident", "hazard", "near_miss", "successful_intervention", "controlled_evaluation"]), "synthetic": {"type": "boolean"}, "occurred_at": NULLTIME, "time_note": S, "external_ids": {"type": "array", "items": S, "uniqueItems": True}}),
    "control": record({"event_id": ID, "objective": S, "opportunity": S, "functions": {"type": "array", "minItems": 1, "uniqueItems": True, "items": enum(["preventive", "detective", "restrictive_corrective", "recovery", "authorization_governance", "human_oversight"])}, "relevant_from": NULLTIME, "relevant_to": NULLTIME, "time_note": S}),
    "source": record({"url": {"type": "string", "format": "uri"}, "title": S, "role": enum(["primary_record", "institutional_statement", "investigation", "research", "news", "discovery", "synthetic"]), "source_date": NULLTIME, "retrieved_at": TIME, "version": S, "family_id": ID, "rights": enum(["unknown", "restricted", "metadata_only", "redistributable", "synthetic"]), "rights_basis": S}),
    "evidence_item": record({"event_id": ID, "source_id": ID, "locator": S, "observation": S, "valid_from": NULLTIME, "time_note": S, "quality": obj({k: S for k in ["directness", "independence", "traceability", "temporal_relevance", "specificity", "consistency", "completeness"]})}),
    "claim": record({"control_id": ID, "asserted_by_source_id": ID, "statement": S, "evidence_ids": {**IDS, "minItems": 1}, "status": enum(["alleged", "preliminary", "corroborated", "investigated", "adjudicated", "disputed", "corrected"]), "valid_from": NULLTIME}),
    "packet": record({"event_id": ID, "evidence_ids": IDS, "cutoff": TIME, "version": S, "cohort": enum(["synthetic", "pilot", "main", "holdout"]), "retrieval_log": S, "omissions": S, "content_sha256": HASH}),
    "annotation": record({"control_id": ID, "packet_id": ID, "packet_sha256": HASH, "dimension": enum(DIMENSIONS), "value": enum(VALUES), "evidence_ids": IDS, "rationale": S, "coder_id": ID, "coder_kind": enum(["human", "ai", "synthetic"]), "status": enum(["proposal", "sealed_initial"]), "independent": {"type": "boolean"}, "eligibility_record": S, "codebook_version": {"const": "0.1.0"}, "coded_at": TIME}),
    "adjudication": record({"annotation_ids": {**IDS, "minItems": 2}, "value": enum(VALUES), "reason": S, "adjudicator_id": ID, "created_at": TIME}),
    "provenance_relation": record({"from_source_id": ID, "to_source_id": ID, "relation": enum(["derived_from", "aggregation_of", "reports_same_claim", "independent_corroboration", "supersedes", "correction_of", "contradicts"]), "basis": S}),
    "derived_measure": record({"adjudication_ids": {**IDS, "minItems": 1}, "method": S, "code_revision": S, "value": {"type": ["number", "null"]}, "limitations": S}),
    "release": record({"version": S, "schema_version": {"const": "0.1.0"}, "status": enum(["development", "approved"]), "approval_records": IDS, "limitations": S}),
}

def generate():
    directory = ROOT / "schemas"
    directory.mkdir(exist_ok=True)
    for name, definition in defs.items():
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": name, **definition}
        (directory / f"{name}.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    fields = {"schema_version": {"const": "0.1.0"}, "mode": enum(["synthetic", "empirical"])}
    fields.update({name: {"type": "array", "items": {"$ref": f"#/$defs/{name}"}} for name in defs})
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$defs": defs, **obj(fields)}
    (directory / "bundle.schema.json").write_text(json.dumps(schema, indent=2) + "\n")

if __name__ == "__main__":
    generate()
