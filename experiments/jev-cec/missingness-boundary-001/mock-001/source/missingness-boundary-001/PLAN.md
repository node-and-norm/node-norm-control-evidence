# Missingness boundary development design 001

Does an access restriction affect only the documentary proposition whose evidence is withheld? Earlier runs extended an account restriction into receipt and execution labels. This new offline design separates those three evidence conditions explicitly.

Status: exposed, AI-authored development design. No live requests, independent adjudication or held-out evaluation. The [eight packets](cards.json) cover all combinations of absent versus explicitly withheld records for receipt, execution and account consequence. Issuance is explicit and unchanged. Each relevant record's condition is named independently. Records are invented, and restriction means unavailable contents, not evidence of success or failure.

## Factors and proposed references

The [reference](reference.json) proposes `yes` for issuance; each other dimension is `not_reported` when its required information is absent without a reported barrier, and `not_observable` when that record is explicitly withheld. Each proposal cites its local evidence item. These are operational assumptions to inspect, not ground truth established by a model.

Eight packets produce twelve matched edges: for each of three restriction factors, four pairs differ in exactly that one factor. A desired transition changes the targeted dimension from not_reported to not_observable while the other dimensions retain their proposed labels. Report target transitions and unrelated-dimension changes separately. The edges share cards and are not independent observations.

Compare the frozen shared questions from the earlier archived request with [structured questions](candidate-questions.json). The candidate changes instruction organization, wording and missingness descriptions together. This tests an instruction package, not JSON structure alone. The packet conditions remain identical across packages.

Canonical option order is alphabetical by label. Reversed order is a separate secondary robustness condition; preserve actual serialized order, since sorting JSON keys would erase this manipulation. Candidate and baseline retain the same eight labels. Order is not a repetition pass and must not be reported as repeatability.

## Schedule and future analysis

The offline schedule contains 8 packets × 2 instruction packages × 2 option orders = 32 requests and 128 judgments. Within each order, alternate package order by card; reverse package order in the secondary block. Canonical is always the first block, so option-order findings remain confounded with time/block position and reversed package order. Treat these as diagnostic sensitivity observations, not an isolated causal order effect.

Primary descriptive outputs use canonical order only: per-dimension proposed-reference agreement with valid/scheduled coverage, the twelve target transitions and unrelated-dimension changes, each with eligible and excluded denominators. Compare packages only on jointly eligible judgments. Secondary reversed-order results retain their own denominators and are not pooled to choose a winner. For each package, a target edge requires its two target answers; a claim that all unrelated dimensions were stable requires all six corresponding answers. Report action stability separately.

Use the new answer-level contract, unchanged sum tolerance, and unresolved-reference exclusion if later review identifies an ambiguous proposal. Do not silently amend references after inference. No automatic decisions, population significance claims or TAE/HIT validation follow from these authored packets.

## Before execution

Run `python3 experiments/jev-cec/missingness-boundary-001/prepare.py --output build/missingness-boundary-001` from the repository root. The preparer has no network transport and emits an answer-free schedule with source hashes. Local card IDs and reference labels stay outside payloads. Payload hashes preserve option order.

Review reference ambiguity and candidate semantic changes before implementing a runner. Specify the complete paired analysis, budgets, stopping rules and a source freeze before dispatch; this preparation is not an execution freeze. A later evaluation set must be developed separately and kept out of tuning, with independence limitations disclosed. No private or independent holdout exists yet. Stop this development sequence if revisions merely fit these eight examples without resolving a defined boundary.

## Pre-execution review

The [wording and reference review](REVIEW.md) retains all 32 proposals conditionally and clarifies twelve withheld-record statements to avoid implying observed outcomes. Its edit ledger preserves the earlier text. Implementation should use the revised packets and disclose the three-label coverage and instruction-package differences.

## Execution contract

The implemented runner has a maximum of 32 sequential requests, a USD 1 client cap and 30-second per-request timeout. Live preflight must reverify pinned jev-1.13.0 availability, USD 0.042 per million input tokens, free output and the 64,000-token combined limit (plus 32,000 state/longest-question limit). These are supported configuration values to recheck, not a current-price assertion. Maximum configured reservation for 32 requests is USD 0.086016. No retry or score-based early stopping is permitted. Transport/HTTP failure, unavailable usage, model mismatch or exhausted reservation stops dispatch and preserves unattempted positions.

Eligibility follows answer contract 001. Located reasons, raw bytes and allowlisted request IDs are retained. The source freeze binds this reviewed design, references, runner and analysis. Encoding deliberately preserves key order, and each dispatched payload must match its scheduled byte hash. Canonical-order outcomes are primary; reversed-order outcomes remain separate. No block is treated as a repeatability estimate.
