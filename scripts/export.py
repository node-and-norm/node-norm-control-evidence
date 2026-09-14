"""Deterministic synthetic export. Scientific releases require a later approval path."""
import argparse
import hashlib
import json
from pathlib import Path
from validate import ROOT, validate

def canonical(data):
    return (json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()

def export(data):
    errors = validate(data)
    if errors:
        raise ValueError("; ".join(errors))
    if data["mode"] != "synthetic":
        raise ValueError("empirical publication requires human research and rights approvals; unavailable in development")
    schema = (ROOT / "schemas/bundle.schema.json").read_bytes()
    return {"artifact_type": "synthetic_development_demo", "schema_version": data["schema_version"],
            "schema_sha256": hashlib.sha256(schema).hexdigest(),
            "input_sha256": hashlib.sha256(canonical(data)).hexdigest(),
            "limitations": "Synthetic data; no empirical findings, reliability evidence, or scientific release.",
            "records": data}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = export(json.loads(args.bundle.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical(result))
    print(f"Wrote synthetic development export: {args.output}")
