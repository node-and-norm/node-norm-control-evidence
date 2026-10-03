# Four-question live development run 001

3 October 2026. All 90 requests were attempted once: 76 responses were valid and 14 invalid. The primary pass matched 76 of 92 valid judgments, with 92 of 120 scheduled judgments available. These are comparisons with an exposed AI-authored reference, not independent accuracy estimates.

## Execution and preflight

The run used clean committed revision `d7985dea64d368046978017f038fba3324abaae7` and the frozen v2 inputs. Before dispatch, the [official model page](https://docs.typesafe.ai/models) listed jev-1.13.0, USD 0.042 per million input tokens, free output, a 64,000-token combined limit and a 32,000-token state-plus-longest-question limit. The small synthetic requests were within these limits. This note records the browser check; the archive metadata preserves the dated preflight attestation, not an archived copy of the provider page.

The estimated input-token charge was USD 0.009191322, within the USD 1 ceiling; this is not an invoice. There were no retries, HTTP errors, transport errors or unattempted requests. [The archive](live-001/manifest.json) preserves request and response bytes, attempts, source snapshots, usage and the exact report. No probabilities or labels were repaired.

## Results with coverage

| Pass | Valid requests | Matches / valid judgments | Valid / scheduled judgments | Mean Brier sum |
| :--- | ---: | ---: | ---: | ---: |
| 1, primary | 23 / 30 | 76 / 92 (82.6%) | 92 / 120 (76.7%) | 0.313850 |
| 2 | 27 / 30 | 85 / 108 (78.7%) | 108 / 120 (90.0%) | 0.337219 |
| 3 | 26 / 30 | 81 / 104 (77.9%) | 104 / 120 (86.7%) | 0.344038 |

One invalid answer excludes all four judgments in its request. Thirteen responses failed probability-sum acceptance; one failed because the selected label was below the maximum returned probability. These are validation diagnoses, not explanations of the provider's internal behavior. All raw replies remain preserved.

Provider-reported usage was 218,841 input tokens and 30,633 output tokens. Of 180 scheduled pair-dimension contrasts, 128 were available and 52 unavailable because at least one member was invalid.

Primary-pass matches by dimension were action 18/23, propagation 19/23, trajectory effect 18/23 and mitigation 21/23. The [report](live-001/report.json) retains confusion matrices, absent-class denominators, all distributions and paired contrasts. Brier loss sums across eight classes without division by eight and remains relative to the authored reference.

Seventy-six of 120 card-dimension groups had three valid repetitions; 71 of those retained the same label. Forty-four groups were excluded from that repeatability calculation. These are dependent repetitions on public synthetic material. The intentionally identical V2-14-B and V2-15-A baseline remains in the analysis; there are 29 unique states across 30 cards.

## Questions exposed by the run

All 62 mismatches remain unresolved. Several concern explicit source statements: V2-12-A records issuance, yet action was classified as `not_reported` in all passes; V2-14-A records receipt and cancellation, yet those dimensions were `not_reported` in all passes. This warrants examining whether the long shared instructions or dimension boundaries obscure the specific proposition. It does not establish that mechanism as the cause.

Conflict also spread beyond the proposition directly contradicted. V2-10-B's execution exports conflict, while its issuance and receipt statements are uncontested; the model marked all three as conflicting in each pass. The frozen code and packet should be inspected together before attributing this exclusively to the model.

The competing-route case V2-15-B was invalid in the first two passes. Its sole valid mitigation judgment was `not_reported`, against the proposed `unknown`. It therefore supplies no complete repeated test of that boundary. Successful-looking aggregate mitigation agreement must not conceal that coverage gap.

No comparison here establishes improvement over v1. The questions, cases, number of dimensions and valid-response composition changed. No confidence threshold, pooled superiority statistic or selected-pass result is introduced.

## Decision

Keep Jev outputs as inspectable proposals. Review the direct-evidence disagreements and missingness/conflict scope before designing any new prompt or sensitivity analysis. Preserve this run as the prospective result under the frozen standard. A later normalization or wording experiment must be separately identified, without replacing these failures or reference judgments.

The archive was verified against its manifest, inspected for response structure and scanned for the configured credential before publication. Mechanical reproduction does not validate the reference or establish practical human control. No TAE/HIT finding, canonical annotation or empirical release gate changed.

The reproduction test requires exact labels, counts and other fields, with absolute tolerance 1e-12 only for Brier arithmetic across Python versions. Saved reports and response acceptance rules are unchanged.
