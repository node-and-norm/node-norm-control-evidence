# Development publication record

Prepared 2 October 2026. This package makes the authored experiment, development decisions and recorded outcomes inspectable. It does not approve an empirical corpus release or complete any TAE/HIT research gate.

## Placement and ownership

The existing Control Evidence Corpus repository provides a shared home for evidence infrastructure. This experiment lives under `experiments/us-control-sandbox/`, outside corpus data and schema exports. TAE and HIT retain their definitions, scoring rules and release processes. Their inspected revisions are listed in [the reconciliation record](RECONCILIATION.md). No change to either method is implied by this publication.

## What is preserved

The package includes the protocol candidate, contract review, application boundaries, source screening, NIST mapping, both executable suites, verification tests, original rehearsals, container runs, isolation evidence and source snapshots. The [run index](RUN-INDEX.md) distinguishes fixture outcomes, control objectives and verification checks. Historical source snapshots retain the wording and implementation used for those runs; current entry documents reconcile subsequent progress.

`PUBLICATION.json` records each imported file's original hash and, for distributed files, its public hash. Public log copies replace machine-specific study paths with `$STUDY_ROOT` and user-home paths with `$USER_HOME`. Such edits are identified individually. Raw originals remain in the local research archive. Saved outcome/packet manifests are unchanged and remain verifiable. No private correspondence, unrelated project files, credentials or conversation transcript is included.

Nine acquired reference documents are link-only: eight TAE/HIT files and the NIST AI RMF PDF. Their URLs, inspected versions and hashes are preserved in `references/manifest.json` and `references/nist/manifest.json`. Their full text remains local pending redistribution review. Reproduction of the authored simulations does not require those documents. The old source snapshots' references to local archives describe the original execution context.

## Assistance and review

The user authorized the research direction and repository publication. Codex assisted source inspection, scenario design, implementation, documentation and automated verification. This is not an independently reviewed study. Exact model build identifiers and inference settings were not captured in the development records and are not retrospectively asserted. No AI output is counted as an independent human assessment.

The development instructions called for preserving the original TAE/HIT workstreams, separating known execution outcomes from assessment evidence, retaining negative findings, and testing bounded U.S.-context questions without human participants. These decisions are recorded in the protocol, contract review and source register. Repository publication does not constitute human approval of scientific validity, empirical labels or legal conclusions.

## Limits and continuation

Sixteen conditions are public fixtures; their outputs cannot serve as untouched holdout evidence. Two recovery fixtures intentionally violate control objectives and are retained. The initial rehearsal lacks per-file artifact hashes; later runs add manifests. Temporary command-entry errors and the initial unavailable-runtime check were not retained as complete run folders, so this package does not claim an exhaustive tool-session transcript.

The next gate is synthetic-evidence admissibility under each method. Any future assessment requires rules fixed before scoring, separate outcome access, new case families and the specified review. A hosted model, external dataset or application framework needs its own justified role, provenance and limits.
