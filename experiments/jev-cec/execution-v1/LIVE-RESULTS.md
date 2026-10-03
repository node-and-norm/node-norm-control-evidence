# CEC Jev first live run

3 October 2026 (America/New_York). The fixed 36-request schedule completed with 31 valid responses and five invalid responses. Primary-pass agreement with the AI-authored key was 24/33 valid determinations, with 33/36 coverage. This is an exploratory result on public synthetic packets, not an estimate of independent accuracy.

## Preserved execution

Run [live-001](live-001/manifest.json) used `jev-1.13.0`; every response reported that version. The tested implementation was committed and merged at `826d8f699c240caded6af9e988912bf58a3aaf04` before execution. Metadata records Python 3.9.6, a clean checkout, the current pricing/limits preflight and the start time. The [protocol](PROTOCOL.md), question set, challenge freeze, reference key and acceptance rules remained unchanged.

All 36 requests were attempted once. There were no retries, timeouts, HTTP failures, unattempted requests, model-version changes or unknown-usage records. The provider reported 69,009 input tokens and 9,210 output tokens. At the checked input-token rate, the estimated charge is USD 0.002898378; this is not an invoice. Raw request/response bytes and all attempt statuses remain in the archive.

## Results by pass

The first pass remains primary. Later passes describe repetition and are not replacements for it.

| Pass | Valid requests / scheduled | Matches / valid determinations | Valid determinations / scheduled | Mean multiclass Brier loss |
| :--- | ---: | ---: | ---: | ---: |
| 1, primary | 11 / 12 | 24 / 33 (72.7%) | 33 / 36 (91.7%) | 0.392448 |
| 2 | 12 / 12 | 28 / 36 (77.8%) | 36 / 36 (100%) | 0.371961 |
| 3 | 8 / 12 | 19 / 24 (79.2%) | 24 / 36 (66.7%) | 0.322375 |

The denominators differ because acceptance is at request level. A response with one invalid answer makes all three determinations unavailable for the primary analysis. The higher third-pass percentage does not establish improvement; a third of its scheduled determinations were unavailable.

Primary-pass matches by dimension were action 10/11, propagation 9/11 and mitigation 5/11. The [machine report](live-001/report.json) retains all distributions, per-pass confusion matrices, recall and undefined denominators. Brier loss uses the prespecified sum across eight classes without division by eight. The key contains no `not_applicable` example, so recall for that class is undefined.

Twenty-four of 36 packet-dimension triplets had valid responses in all three passes. Of those, 23 had the same label in all three. Twelve triplets were excluded for incomplete valid coverage. Repeated agreement can preserve the same disagreement with the reference; it does not establish correctness or calibration.

## Invalid responses

| Attempt | Affected answer | Sum of returned probabilities |
| :--- | :--- | ---: |
| P1-C01 | action | 0.99 |
| P3-C01 | propagation | 0.99 |
| P3-C04 | action | 0.99 |
| P3-C08 | propagation | 0.99 |
| P3-C09 | action | 0.99 |

Each sum violated the frozen absolute tolerance of 0.00001. Values were not normalized, relabeled or replaced. The observed sums are compatible with rounding, but the responses do not establish why it occurred. No explanation of the provider's internal mechanism is claimed. All five raw replies remain available for diagnosis. Changing tolerance after observing these results would require a separately labeled sensitivity analysis or a successor protocol, preserving this result.

## What the disagreements expose

There are 22 valid determination-level mismatches across the three passes, all retained as unresolved review records. They are repeated observations on related authored packets, not 22 independent failures.

- C03 received `yes` for mitigation in all three passes, while the reference says `not_reported`. The packet says the job was cancelled before execution but specifies no separate harm. Review whether the question and control objective adequately distinguish cancellation from mitigation before classifying this as a model error.
- C04 received `no` for mitigation in the first two valid passes, against `not_reported`. A discarded request establishes non-delivery; whether the wording invites a broader outcome conclusion needs review.
- C05 received `conflicting` for action as well as mitigation. The reference treats the console's attempted action as established despite incompatible downstream records. Review the separation of attempted action, downstream behavior and consequences.
- C06 received `partial` for propagation in passes one and three, and `not_reported` in pass two. Repeated reports of sending supply no additional receipt evidence under the reference. This is the only complete triplet whose label changed.
- C08 and C09 extended access-related missingness to mitigation. C09 also classified ambiguous receipt linkage as `not_observable` rather than the reference's `unknown`. Distinguishing unreadable fields from identity ambiguity may need clearer operational criteria.
- C10 received `partial` for mitigation in all three valid passes. As with C03, the reference separates partial propagation from consequences that the packet does not specify.

These are post-output observations and review questions. They are not adjudications. The reference can contain defects, and model confidence cannot settle them. No original key, response or reported score has been changed.

## Decision and next step

Keep Jev as an experimental proposal source with human inspection. This run does not support automatic acceptance of its classifications. The next useful task is an item-by-item review of the disputed distinctions, especially the meaning of mitigation in stop-command cases and the boundary between ambiguity and access barriers. Preserve that review separately, including author/AI exposure. Fix any confirmed defect in a successor question or challenge version before another prospective run.

The twelve cards share two invented settings and seven observed reference classes. They do not represent an application population, raw field evidence, an independent holdout or independent human ratings. No corpus annotation, TAE/HIT finding, research approval or live-site content changed.

## Publication checks

The copied archive matches its original manifest. Raw responses were inspected as structured model answers and usage, and a direct scan found no occurrence of the configured credential in any artifact. The report is reproduced from saved raw responses and the frozen key by a repository test. Recalculated Brier values permit absolute floating-point differences up to 1e-12 because summation order can vary between Python processes. Counts, labels and other values must match exactly; archive hashes and response acceptance rules remain unchanged. These checks establish artifact consistency and mechanical reproduction, not source authenticity or scientific validity.
