# Four-question execution contract v2

3 October 2026. Prospective development contract for the original sixteen successor cards, expansion 001's ten cards and prevention 001's four cards. Questions are those in development-v2/standard-001. This contract is documented before successor inference. The inputs are public, AI-authored and exposed to earlier model results. No independent accuracy or human-benefit claim is supported.

## Schedule and stopping

Three passes, in card-ID order, with all four questions in each request: 30 cards, 90 requests and 360 scheduled determinations. Pass one is primary, with 120 scheduled determinations. Later passes describe repetition; no voting, best-pass selection, replacement or retry. The duplicate baseline V2-14-B/V2-15-A stays in the schedule and is disclosed; there are 29 unique states, not 30 independent cases.

Use jev-1.13.0, sequential official-endpoint requests, 30-second timeout, no redirects or retries. Retain the whole schedule before dispatch. HTTP or transport failure, missing usage or resolved-model mismatch stops further requests. Malformed success responses with known usage remain invalid and may continue. Attempted requests are never replayed. Interruptions preserve partial records and unattempted schedule positions.

Ceilings are 90 requests and USD 1 estimated spend. Before dispatch, check current official availability, pricing and request limits and save dated evidence. Reserve a conservative maximum-request cost before each request and stop if it would exceed the ceiling. A price/model/limit change requires an explicit contract amendment. No rate is asserted as current here. This is a client estimate, not a provider-enforced billing cap. Unknown usage stops the run.

## Acceptance and arithmetic

Retain v1 strict acceptance, expanded to exactly four question IDs: reject duplicate JSON keys, nonfinite or Boolean numerical values, wrong model, missing/extra dimensions, wrong answer types, invalid labels, incomplete eight-class distributions, values outside [0,1], choices below maximum probability and invalid usage. Probabilities must sum to one within absolute 1e-5, relative tolerance zero. No normalization. Ties at the maximum are permitted. Preserve raw bytes before parsing.

One invalid answer makes all four determinations unavailable. Failures are statuses, never evidence labels. Retain confidence separately. Report all status counts against 90 requests and 360 determinations; per-pass denominators are 120 and per-dimension denominators 30. Report matches/valid together with valid/scheduled, confusion counts, reference-class recall and mean eight-class Brier sum without division by eight. Zero denominators remain undefined.

Report complete-triplet agreement across 120 card-dimension groups with exclusions. Separately identify the duplicate baseline; do not imply population precision from counts or compute confidence intervals. Pair contrasts are descriptive: report both labels and reference expectations when both requests are valid; otherwise mark the contrast unavailable. Never drop an invalid member and report the other as a successful contrast. Original and new packets remain in the primary report; do not choose a favorable subset.

All discrepancies remain unresolved review items. No rescoring of v1, canonical annotations, synthetic-to-empirical conversion, calibration claim or superiority threshold.

## Implementation and freeze gate

This tranche supplies an offline schedule only. The v1 runner remains a three-question implementation and must not execute this schedule. Before live work, implement and test four-question response validation, accounting, arithmetic, budget enforcement and interruption handling using an in-memory service.

Then freeze exact cards, questions, normalized proposed references, decision documents, implementation and analysis hashes together at a committed revision. The current schedule hashes request bytes but is not that full freeze. It must not be described as ready for dispatch. Preserve raw request/response bytes, attempts, source snapshots and a manifest in a new exclusive output directory; never record credentials. Publication requires artifact verification and a secret scan.
