# CEC Jev execution protocol v1

3 October 2026. This protocol defines an exploratory model-reading exercise on the frozen [documentary challenge](../challenge-v1/README.md). No CEC model output has been observed. Reference judgments are AI-authored, public and independently unreviewed. Agreement measures consistency with that reference, not empirical accuracy or human benefit.

## Schedule and budget

Use model `jev-1.13.0` with the frozen questions unchanged. Make three passes through C01 to C12 in that order. Each request asks all three questions independently over the same packet. There are 36 scheduled requests and 108 scheduled determinations. Pass one is the primary descriptive comparison; passes two and three examine repeatability. Never select the best pass, combine votes into a preferred answer, or replace failures.

The proposed live transport is the official HTTP endpoint `https://api.typesafe.ai/v1/systemone`, using the Python standard library and no SDK. A later runner must record its Python version, code revision, request bytes, frozen input hashes and resolved model. Use a 30-second timeout and no automatic retries or redirects. Requests are sequential. Any timeout counts as an attempted request even if server execution is uncertain. Authentication, authorization, rate-limit or server failures stop the run; preserve the remaining schedule as not attempted. A malformed HTTP-success response is retained as invalid and does not trigger a retry.

The live-run spending ceiling is USD 1 for this schedule. TypeSafe's model page, checked on this date, lists USD 0.042 per million input tokens and a 64,000-token total request limit. Multiplying that limit by all 36 requests gives USD 0.096768 at the stated rate. This is a conservative planning calculation, not a billing guarantee or provider-enforced account cap. Before live dispatch, recheck pricing and limits; stop for a protocol amendment if they differ. Retain provider-reported input/output usage and running estimated charge. Missing usage stops further dispatch because spending cannot be accounted for. Do not infer zero usage for invalid or failed requests. The maximum request count remains binding even when the estimate is low.

No transport is implemented in this tranche. The budget and timeout are requirements for the live runner, not claims of an existing enforcement mechanism. The present command only produces the fixed schedule offline.

## Response acceptance

Preserve raw response bytes before parsing. Reject malformed JSON, duplicate object keys, nonfinite values, missing or different resolved model, missing or extra question IDs, wrong answer type, unknown choices, missing/extra probability labels, booleans posing as numbers, values outside [0,1], and a selected choice below the maximum-probability option. A tie at the maximum is permitted and remains visible.

Require the eight probabilities to sum to one within absolute tolerance 0.00001, with no relative tolerance and no normalization. Confidence is retained separately; it is not an evidence class or a permission to act. Input and output usage must be nonnegative integers. Additional top-level/provider metadata is preserved in the raw response but does not enter scoring.

Acceptance is at request level: one invalid answer makes all three determinations unavailable for the primary analysis. Retain valid-looking fields for a separately labeled diagnostic only. Never convert transport failure or invalid output into `unknown`, `not_reported`, or another evidence value. Model-version mismatch stops further dispatch in the future runner.

## Analysis fixed before outputs

Report attempted, not-attempted, HTTP-error, invalid and valid request counts against all 36 scheduled requests, and corresponding determination coverage against 108. Report first-pass class agreement as matches / valid determinations alongside valid / scheduled coverage (36 scheduled for that pass). Show eight-by-eight confusion counts overall and by dimension; absent reference classes have undefined recall, not zero. Report later passes separately.

For each valid determination, calculate multiclass Brier loss as the sum over eight labels of squared differences from the one-hot reference. Report the mean with its valid denominator, without dividing each loss by eight. Retain raw distributions and confidence. Do not fit calibration curves, choose a confidence threshold, or claim calibration from this small authored set.

For repeatability, report all-three-label agreement only where all three repetitions are valid; report eligible / 36 packet-dimension triplets and excluded triplets. Do not replace missing repetitions. Related stop and refund cases and their questions remain dependent. No population inference, confidence interval, composite score, pass/fail threshold or superiority claim is authorized.

Disagreements go into a separate review record with the original reference, output and locators. Candidate dispositions: model error, reference ambiguity, question defect, evidence wording defect, construct ambiguity, insufficient evidence or unresolved. No automatic adjudication; never overwrite original labels. This exercise closes no human-pilot decisions and creates no canonical corpus annotations.

## Records and next gate

The offline schedule contains payload hashes and a frozen-challenge hash. A future runner must create an exclusive output directory, save the complete schedule before dispatch, save each request before sending, preserve raw responses and status metadata, and write an exact artifact manifest including failures. Secrets and authorization headers never enter research artifacts. Use only these public synthetic payloads.

Commit this protocol and its validation tests before implementing or running live inference. Next is the bounded transport and analysis implementation, tested against an in-memory service before any API call. An interrupted live run remains preserved; a continuation requires an explicit record of which scheduled attempts remain, with no replay of attempted requests.

Provider references: [HTTP API](https://docs.typesafe.ai/api), [model limits and price](https://docs.typesafe.ai/models). Codex authored this protocol and software with AI assistance. Passing software tests establishes mechanical behavior only.
