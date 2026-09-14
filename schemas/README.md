# Data contract 0.1.0

The bundle schema embeds standalone definitions for event, control, source, evidence_item, claim, packet, annotation, adjudication, provenance_relation, derived_measure, and release. All properties are explicit and required. Unknown times use null plus a note; unknown categorical evidence uses codebook values. Additional properties are rejected to prevent undeclared constructs from entering silently.

Regenerate JSON schemas with `python scripts/build_schemas.py`. The bundle validator also checks typed references, source derivation cycles, known shared origins, packet scope and hashes, timestamps, adjudication inputs, and separation of synthetic data. The packet hash covers supplied event, control, evidence, source, and lineage metadata. It does not certify original third-party bytes or prove that a holdout remained unread.

The schema preserves source-date, retrieval-time, valid-from, and correction/supersession relationships at the source layer. Richer object revision history and human approval attestations remain future extensions. Git history and retained packet versions are required until an audited append-only research store exists.

Validation cannot judge whether an evidence citation actually supports a statement, whether sources concealed shared origins, whether a human was independent, or whether a label is scientifically valid. Those gates require attributable review. The development exporter refuses every empirical bundle, even one that passes structural checks.
