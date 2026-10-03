# Packet linkage diagnostic 001

Does explicitly identifying a stop request's target change how the frozen shared instructions classify documentary support? The preceding [validity review](../instruction-comparison-001/VALIDITY-REVIEW.md) identified an unstated link in pair 12. This diagnostic isolates a clarification of that link.

Status: prospective offline preparation. No requests have been sent. The cases were selected after examining earlier outputs and remain public synthetic development material. This is an AI-authored design, with no independent reference adjudication.

## Exactly what changes

Use the condition-A requests for V2-12-A and V2-12-B from the archived instruction comparison. [Source bindings](source-bindings.json) identify the exact original bytes. For each card, retain an original condition and create an explicit condition by replacing only the first sentence of E1:

| Condition | Issuance sentence |
| :--- | :--- |
| Original | The console issued R. |
| Explicit | The console issued stop request R targeting fee job J. |

All remaining evidence, scope, questions, criteria, model and payload fields remain identical. The wording adds both the stop-request identity and target association. It tests that clarification package; it cannot separate the effects of those two additions. Original archived requests and references are unchanged.

## Reference and analysis contract

The separate [reference](reference.json) records an unresolved action reference for each original packet and a proposed `yes` for each explicit packet. Unresolved is review metadata, never a ninth model choice. The original condition's action outputs receive no agreement score. Their historical labels remain in the previous experiment.

Primary output: pass-one action labels for each card and condition, with validity status. Tabulate each eligible original-to-explicit label transition. There are two scheduled pairs; report available/2 and unavailable/2. For explicit action only, report matches/valid and valid/2. A zero valid denominator is undefined, never zero agreement. Do not compute a paired accuracy gain against the unresolved original action reference.

Secondary output: for propagation, trajectory and mitigation, show each label beside its proposed reference by card and condition, with valid/2 coverage per dimension and condition. These labels remain respectively `not_reported`, `not_reported`, and either `not_reported` (A) or `not_observable` (B). Report cross-condition changes as possible spillover; the added sentence supplies no receipt or execution evidence. Do not pool these dimensions into a primary score.

Pass two repeats the same design, reported separately. Show within-condition action repetition for both cards, with eligible/2 and exclusions. Retain all probabilities but prescribe no Brier scoring against unresolved references, significance tests, population estimates, pooled winner or general accuracy claim. These two selected packets cannot validate TAE, HIT, human control or the classification standard.

## Schedule, acceptance and stopping rules

Two cards, two conditions and two passes produce eight requests and 32 scheduled judgments. Pass one uses original/explicit for A and explicit/original for B; pass two reverses each order. This balances order without eliminating drift or dependence. No adaptive additions, retries or replacements.

Use jev-1.13.0 and the unchanged strict four-answer response validator from the frozen comparison archive. A failed answer excludes its complete response. Preserve raw bytes, hashes, usage, timing, status and every unattempted schedule position. No normalization or answer-level salvage. Continue after an ordinary response-validation rejection; stop on transport/HTTP failure, model mismatch, missing usage or exhausted spending allowance.

Before dispatch, verify official model availability, limits and pricing, freeze the runner and analysis at a clean commit, and enforce an eight-request ceiling and USD 1 maximum budget with maximum-cost reservation before each request. Those are prospective limits; this offline preparer makes no network calls and enforces no live budget.

## Preparation and execution gate

Run `python3 experiments/jev-cec/packet-linkage-001/prepare.py --output build/packet-linkage-001` from the repository root. This writes an answer-free schedule plus hashes of the plan, reference, bindings and preparer. It refuses to overwrite an existing output directory. Local identifiers, proposed references and condition labels remain outside payloads.

Before a live run, implement and test the analysis for unresolved references, missing responses, strict whole-response exclusions, zero denominators and both passes. Exercise the bounded runner against a local mock service. Freeze the plan, source requests, validator, reference, runner and analysis together. The current preparation manifest is not an execution freeze or a result.
