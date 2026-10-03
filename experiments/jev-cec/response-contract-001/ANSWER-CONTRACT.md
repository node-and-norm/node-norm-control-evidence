# Prospective answer eligibility contract 001

Future diagnostics should retain an independently usable answer when another answer fails. Adoption requires a new runner version and execution freeze. This specification changes the acceptance unit only; it retains absolute sum tolerance 0.00001. Existing runners and published results remain governed by their original rules.

## Decision sequence

1. Preserve response bytes and attempt metadata before interpretation. Reject duplicate JSON keys, nonfinite JSON constants and malformed JSON at envelope level. Check HTTP status, pinned model identity, expected answer identifiers and required usage accounting. An envelope failure prevents use of every answer. Preserve the reason and scheduled positions.
2. Check each expected answer independently: object shape, Choice type, choice membership, exact probability-label coverage, numeric values in [0,1] excluding booleans and nonfinite numbers, sum within tolerance, and selected choice at the maximum. Ties are permitted by this rule; retain the supplied choice and do not break ties to match a reference.
3. Record eligibility and reason per answer, including raw sum and discrepancy. A malformed answer excludes that answer. It does not exclude other answers after the envelope passes. Missing or unexpected identifiers remain an envelope failure in version 001, so missing keys do not silently alter the expected question set.
4. Apply downstream dependencies explicitly. An action transition requires both action answers to pass. A joint decision requiring four dimensions requires all four to pass. Every reported denominator must name that dependency and include the full scheduled count and exclusions.
5. Keep reference availability separate. An eligible answer with an unresolved reference may appear in a label transition but receives no agreement or correctness score. Keep uncertainty-based review routing separate from eligibility and the eight evidence labels.

Use machine-readable reasons such as `envelope_invalid`, `answer_shape`, `label_coverage`, `numeric_range`, `sum_outside_tolerance` and `choice_not_maximum`. A single response may contain several failures; retain all located reasons rather than just the first. This is a proposed research contract, not a claim that TypeSafe requires these rules.

## Reporting and operational boundaries

Preserve original probabilities without normalization. Report answer-level coverage alongside whole-response coverage under the same tolerance. Do not apply new acceptance retrospectively to official primary results. Label any historical sensitivity separately.

Retain the existing no-retry research policy, complete attempt accounting, cost reservation and stop rules for transport/HTTP failures, model mismatch and unavailable usage. These are experiment controls. They differ from ordinary application retry policies. Preserve allowlisted provider request identifiers in future execution without storing authorization headers or unrelated response headers.

The [precision audit](PRECISION.md) does not establish a new numerical tolerance. Implementation must test malformed envelopes, duplicate keys, missing identifiers, booleans, nonfinite values, ties, invalid individual answers, zero eligible pairs and unresolved references before adoption. A future live run must bind this contract, implementation and analysis to a clean source freeze. No existing live runner adopts the contract in this change.
