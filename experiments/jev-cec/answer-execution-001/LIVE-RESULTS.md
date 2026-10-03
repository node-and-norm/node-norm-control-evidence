# Answer-level execution: first live result

The separately frozen answer-level contract retained 30 of 32 scheduled judgments. Two responses were partial and six fully eligible; all eight requests completed once. Whole-response acceptance on these same outputs would retain 24 judgments. This six-judgment difference describes the acceptance unit, not a model accuracy improvement.

Two answers failed the unchanged 0.00001 sum tolerance, each totaling 0.99: P1-V2-12-B-original action and P2-V2-12-B-explicit trajectory. Their eligible siblings remain in the analysis. There was no normalization, retry, replacement or transport/HTTP failure.

## Action comparison

| Pass | Card | Original | Explicit | Pair available |
| :--- | :--- | :--- | :--- | :--- |
| 1, primary | V2-12-A | not_reported | yes | Yes |
| 1, primary | V2-12-B | Excluded | yes | No |
| 2, secondary | V2-12-A | not_reported | yes | Yes |
| 2, secondary | V2-12-B | not_observable | yes | Yes |

Primary paired coverage is 1/2. Explicit action matches the proposed reference in 2/2 eligible answers at 2/2 coverage in each pass. Original action references remain unresolved and unscored. These transitions on two selected synthetic packets establish no accuracy gain against the original condition. The secondary pass is reported separately and cannot replace incomplete primary coverage.

## Remaining disagreements

For receipt, each condition in each pass matched 1/2 proposed labels at 2/2 coverage. For trajectory, each matched 1/2 at 2/2 coverage except pass-two explicit, which matched 1/1 at 1/2 coverage. Mitigation matched 2/2 at 2/2 coverage in all four condition-pass groups. The lower-coverage trajectory fraction must not be interpreted as improvement.

V2-12-B continues to assign `not_observable` to eligible receipt and trajectory answers, although the documented access restriction concerns the account outcome. The proposed reference keeps those dimensions `not_reported`. Clarifying the action does not settle that boundary under the frozen standard.

Action repetition agreed in 1/1 eligible original card with one excluded, and 2/2 explicit cards with none excluded. This is descriptive repetition on exposed material, not reliability in a population.

## Provenance and limits

Execution used clean commit `8021484a5cdacb683db4d9ffe1ef60b6c86ced22`, pinned `jev-1.13.0`, the frozen answer contract and unchanged question payloads. On 3 October 2026 UTC, the [official model page](https://docs.typesafe.ai/models) listed USD 0.042 per million input tokens, free output and request limits of 64,000 combined tokens and 32,000 for state plus the longest question. The dated preflight attestation is archived; no provider-page snapshot was saved.

Provider-reported usage was 19,460 input and 2,756 output tokens, estimated at USD 0.000817320 within the USD 1 cap. This is not an invoice. All eight provider request IDs are preserved. The [manifest](live-001/manifest.json) binds raw responses, requests, eligibility reasons, source snapshots and the [report](live-001/report.json). Archive verification, report reproduction and a configured-credential scan passed.

This is a new development run after earlier outputs informed the acceptance contract. Differences across runs can reflect different responses as well as different rules. Only the 30-versus-24 comparison on these same outputs isolates the acceptance-unit effect. Earlier scores and archives remain unchanged. No TAE/HIT validity, human performance or general classification claim follows.

## Decision

The runner demonstrated answer-level retention while preserving paired dependencies and unresolved references. Stop repeating this two-packet diagnostic. The next useful work is an offline design for structured, dimension-specific criteria and missingness boundaries, with option-order checks and a clear separation between development cases and any later evaluation set. Another live run requires a distinct prespecified question, not a desire for complete primary coverage.
