# Packet-linkage diagnostic: first live result

The primary pass has no eligible paired action comparison: both explicit-condition responses and one original-condition response failed strict probability-sum validation. The secondary pass produced two valid transitions to `yes` after clarification. These secondary observations do not replace the unavailable primary comparison or establish a general improvement.

All eight requests were attempted once: five valid responses, three invalid, zero retries and zero transport or HTTP failures. Response-level exclusion removed 12 of 32 scheduled judgments. Original action references remain unresolved and unscored.

## Action results

| Pass | Card | Original action | Explicit action | Paired availability |
| :--- | :--- | :--- | :--- | :--- |
| 1, primary | V2-12-A | not_reported | Invalid response | Unavailable |
| 1, primary | V2-12-B | Invalid response | Invalid response | Unavailable |
| 2, secondary | V2-12-A | not_reported | yes | Available |
| 2, secondary | V2-12-B | not_observable | yes | Available |

Primary paired coverage is 0/2; explicit action coverage is 0/2 and agreement is undefined. Original coverage is 1/2. Secondary paired coverage is 2/2; explicit action matches its proposed reference in 2/2 valid judgments at 2/2 coverage. The original outputs have no agreement score because their action reference is unresolved.

The clarification adds both stop-request identity and target association. The secondary transitions describe responses to that package on two selected, exposed synthetic packets. They cannot identify which added phrase mattered, estimate general accuracy or show that the original labels were correct.

## Later-stage evidence and repetition

In the primary pass, the only valid original response (V2-12-A) matched all three later-stage proposed labels. Both explicit responses were excluded.

In pass two, V2-12-A returned `not_reported` for receipt, trajectory and mitigation under both conditions, matching the proposed reference. V2-12-B returned `not_observable` for all three under both conditions. Its account-outcome restriction supports that proposed mitigation label, but the reference assigns `not_reported` to receipt and trajectory because their records are absent without a stated access restriction. Thus each condition matched 1/2 receipt labels, 1/2 trajectory labels and 2/2 mitigation labels, each at 2/2 coverage.

The clarified action label did not resolve the later-stage missingness disagreements. This observation concerns the supplied packets and experimental standard; it provides no explanation of the provider's internal mechanism.

Original action repetition agreed in 1/1 eligible card, with 1/2 excluded. Explicit action repetition had 0/2 eligible cards and is undefined. Invalid distributions remain untouched. No normalization, rerun, pooled winner or new reference label was introduced.

## Provenance

Execution used clean revision `1134ac20a02ba790cfa130c5b55624c1bb693443`, the frozen sources and pinned model `jev-1.13.0`. On 3 October 2026 UTC, the [official model documentation](https://docs.typesafe.ai/models) listed USD 0.042 per million input tokens, free output, a 64,000-token request ceiling and 32,000 for state plus the longest question. The dated preflight attestation is preserved; no provider-page snapshot was saved.

Provider-reported usage was 19,460 input and 2,756 output tokens. Estimated charge was USD 0.000817320, within the USD 1 cap; this is not an invoice. The runner completed without a stop condition. A configured-credential scan and archive hash verification passed.

The [archive manifest](live-001/manifest.json) binds requests, raw responses, metadata, source snapshots and the [report](live-001/report.json). Reproduction checks the saved analysis exactly. These mechanical checks do not supply independent adjudication or empirical validation of TAE or HIT.

## Decision

Retain this diagnostic as incomplete primary evidence, with the secondary transitions visible. Further prompt or packet tuning should wait for a separately specified response-validity investigation: repeated sum failures now prevent the planned primary comparison. A future sensitivity analysis may inspect answer-level acceptance or normalization, but must retain the original exclusions and state that its rules were chosen after these outputs. No further live run is justified by a desire to obtain a complete or favorable primary result.

The subsequent [response-contract review](../response-contract-001/REVIEW.md) qualifies these exclusions against the SDK documentation and preserves the original analysis.
