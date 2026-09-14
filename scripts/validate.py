"""Validate a development bundle and research-relevant relational constraints."""
import argparse
import json
import hashlib
from datetime import datetime
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def packet_hash(data, packet):
    """Hash the packet scope, event, controls, evidence, and source metadata.

    This is an integrity commitment to supplied JSON, not proof of custody or
    integrity of third-party bytes. Claims and ratings are excluded from packets.
    """
    evidence = [r for r in data["evidence_item"] if r["id"] in packet["evidence_ids"]]
    source_ids = {r["source_id"] for r in evidence}
    # Include source lineage metadata as well as directly cited sources.
    while True:
        upstream = {r["to_source_id"] for r in data["provenance_relation"] if r["from_source_id"] in source_ids}
        if upstream <= source_ids:
            break
        source_ids |= upstream
    payload = {
        "scope": {k: v for k, v in packet.items() if k != "content_sha256"},
        "event": [r for r in data["event"] if r["id"] == packet["event_id"]],
        "control": [r for r in data["control"] if r["event_id"] == packet["event_id"]],
        "evidence": evidence,
        "sources": [r for r in data["source"] if r["id"] in source_ids],
        "relations": [r for r in data["provenance_relation"] if r["from_source_id"] in source_ids],
    }
    for key in ["event", "control", "evidence", "sources", "relations"]:
        payload[key] = sorted(payload[key], key=lambda row: row["id"])
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()

def validate(data):
    schema = json.loads((ROOT / "schemas/bundle.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    errors = [f"schema {list(e.path)}: {e.message}" for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)]
    if errors:
        return errors
    indexes = {}
    seen = set()
    for kind in schema["$defs"]:
        indexes[kind] = {}
        for row in data[kind]:
            if row["id"] in seen:
                errors.append(f"duplicate ID {row['id']}")
            seen.add(row["id"])
            indexes[kind][row["id"]] = row

    def ref(kind, identity):
        result = indexes[kind].get(identity)
        if result is None:
            errors.append(f"missing {kind} reference {identity}")
        return result

    for row in data["event"]:
        if row["synthetic"] != (data["mode"] == "synthetic"):
            errors.append("synthetic/empirical mixing")
    for row in data["source"]:
        if (row["role"] == "synthetic") != (data["mode"] == "synthetic"):
            errors.append("source mode mismatch")
        if (row["rights"] == "synthetic") != (data["mode"] == "synthetic"):
            errors.append("source rights mode mismatch")
        if row["source_date"] and stamp(row["source_date"]) > stamp(row["retrieved_at"]):
            errors.append("source date after retrieval")
    for row in data["control"]:
        ref("event", row["event_id"])
        if row["relevant_from"] and row["relevant_to"] and stamp(row["relevant_from"]) > stamp(row["relevant_to"]):
            errors.append("reversed control period")
    for row in data["evidence_item"]:
        ref("event", row["event_id"])
        ref("source", row["source_id"])
    for row in data["claim"]:
        control = ref("control", row["control_id"])
        ref("source", row["asserted_by_source_id"])
        for identity in row["evidence_ids"]:
            evidence = ref("evidence_item", identity)
            if evidence and control and evidence["event_id"] != control["event_id"]:
                errors.append("claim evidence from another event")
    for row in data["packet"]:
        ref("event", row["event_id"])
        if row["content_sha256"] != packet_hash(data, row):
            errors.append("packet content hash mismatch")
        if (row["cohort"] == "synthetic") != (data["mode"] == "synthetic"):
            errors.append("packet mode mismatch")
        for identity in row["evidence_ids"]:
            evidence = ref("evidence_item", identity)
            if evidence:
                if evidence["event_id"] != row["event_id"]:
                    errors.append("packet evidence from another event")
                source = ref("source", evidence["source_id"])
                if source and stamp(source["retrieved_at"]) > stamp(row["cutoff"]):
                    errors.append("packet contains evidence retrieved after cutoff")
    coding_keys = set()
    for row in data["annotation"]:
        control = ref("control", row["control_id"])
        packet = ref("packet", row["packet_id"])
        if packet and row["packet_sha256"] != packet["content_sha256"]:
            errors.append("annotation references another packet hash")
        if control and packet and control["event_id"] != packet["event_id"]:
            errors.append("annotation packet/event mismatch")
        if packet and stamp(row["coded_at"]) < stamp(packet["cutoff"]):
            errors.append("annotation predates packet freeze")
        if row["value"] in {"yes", "no", "partial", "conflicting"} and not row["evidence_ids"]:
            errors.append("substantive value requires evidence")
        for identity in row["evidence_ids"]:
            ref("evidence_item", identity)
            if packet and identity not in packet["evidence_ids"]:
                errors.append("annotation cites evidence outside frozen packet")
        if row["coder_kind"] == "ai" and (row["status"] != "proposal" or row["independent"]):
            errors.append("AI cannot supply independent sealed human ratings")
        if data["mode"] == "synthetic" and row["coder_kind"] != "synthetic":
            errors.append("synthetic fixture cannot impersonate a research coder")
        if data["mode"] == "empirical" and row["coder_kind"] == "synthetic":
            errors.append("synthetic coder in empirical bundle")
        key = tuple(row[k] for k in ["control_id", "packet_id", "dimension", "coder_id"])
        if key in coding_keys:
            errors.append("duplicate initial/proposal coding key")
        coding_keys.add(key)
    for row in data["adjudication"]:
        ratings = [ref("annotation", i) for i in row["annotation_ids"]]
        ratings = [r for r in ratings if r]
        if len({tuple(r[k] for k in ["control_id", "packet_id", "dimension"]) for r in ratings}) != 1:
            errors.append("adjudication mixes observations or packets")
        if len({r["coder_id"] for r in ratings}) != len(ratings):
            errors.append("adjudication requires distinct coders")
        for rating in ratings:
            if rating["status"] != "sealed_initial":
                errors.append("adjudication requires sealed initial ratings")
            if data["mode"] == "empirical" and (rating["coder_kind"] != "human" or not rating["independent"]):
                errors.append("empirical adjudication requires independent humans")
            if stamp(row["created_at"]) < stamp(rating["coded_at"]):
                errors.append("adjudication predates initial rating")
    graph = {identity: set() for identity in indexes["source"]}
    for row in data["provenance_relation"]:
        left = ref("source", row["from_source_id"])
        right = ref("source", row["to_source_id"])
        if row["from_source_id"] == row["to_source_id"]:
            errors.append("self provenance relation")
        if left and right and row["relation"] in {"derived_from", "aggregation_of"}:
            graph[left["id"]].add(right["id"])
        if left and right and row["relation"] == "independent_corroboration" and left["family_id"] == right["family_id"]:
            errors.append("same source family cannot be independent corroboration")
    def ancestors(identity, path=frozenset()):
        if identity in path:
            errors.append("cyclic source derivation")
            return set()
        found = set(graph[identity])
        for parent in graph[identity]:
            found |= ancestors(parent, path | {identity})
        return found
    lineage = {i: ancestors(i) | {i} for i in graph}
    for row in data["provenance_relation"]:
        if row["relation"] == "independent_corroboration":
            if lineage.get(row["from_source_id"], set()) & lineage.get(row["to_source_id"], set()):
                errors.append("shared upstream origin cannot corroborate independently")
    for row in data["derived_measure"]:
        for identity in row["adjudication_ids"]:
            ref("adjudication", identity)
    for row in data["release"]:
        if row["status"] == "approved" or row["approval_records"]:
            errors.append("empirical release approval is unavailable in development schema")
    return sorted(set(errors))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.bundle.read_text()))
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    raise SystemExit(bool(errors))
