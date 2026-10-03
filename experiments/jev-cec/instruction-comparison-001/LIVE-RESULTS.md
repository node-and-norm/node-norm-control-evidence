# Instruction comparison: first live result

3 October 2026. The primary paired comparison showed no net agreement advantage for the candidate instructions: among 96 jointly valid judgments, A alone matched the reference 11 times and B alone matched it 11 times. Twenty-four of 120 scheduled pairs were unavailable. This is a descriptive result on exposed synthetic material, not evidence that the instruction packages are equivalent.

A is the frozen shared instruction package; B is the shorter dimension-specific package. Evidence, model, criteria and reference were held fixed. B changes wording, length and emphasis together. All 120 requests were attempted once, in the counterbalanced order: 106 valid responses and 14 probability-sum rejections. No retries, normalization, HTTP failures or transport failures occurred.

## Results with full denominators

| Pass | Condition | Matches / valid judgments | Valid / scheduled | Mean Brier sum |
| :--- | :--- | ---: | ---: | ---: |
| 1, primary | A, shared | 87 / 108 (80.6%) | 108 / 120 (90.0%) | 0.320454 |
| 1, primary | B, dimension-specific | 85 / 104 (81.7%) | 104 / 120 (86.7%) | 0.270958 |
| 2, repetition | A, shared | 85 / 108 (78.7%) | 108 / 120 (90.0%) | 0.347731 |
| 2, repetition | B, dimension-specific | 91 / 104 (87.5%) | 104 / 120 (86.7%) | 0.227790 |

| Pass | Both match | A only | B only | Neither | Unavailable | Paired difference (B minus A) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1, primary | 69 | 11 | 11 | 5 | 24 | 0 / 96 = 0 percentage points |
| 2, repetition | 71 | 7 | 14 | 4 | 24 | 7 / 96 = 7.3 percentage points |

Condition-only agreement uses different valid subsets. The paired table restricts comparison to the same eligible card-dimensions. One invalid response removes four judgments and makes their cross-condition pairs unavailable. Candidate coverage is lower in both passes. Lower candidate Brier means are conditional on valid responses with different composition; they do not settle the paired comparison or establish calibration.

The secondary pass favors B descriptively, but it does not replace the prespecified primary result. No pooled winner, significance test, population interval or superiority claim is introduced. The intentional duplicate baseline remains included; the 30 cards represent 29 distinct states and are related, authored examples.

## Secondary targets and repetition

The fixed direct-evidence subset had only one of three judgments available for each condition in pass one: A matched 0/1 and B 1/1. In pass two A matched 0/3 and B 1/1. Those different valid subsets prevent a complete test of the targeted boundary. The disputed-reference subset was also incomplete: pass one A 0/2, B 1/3; pass two A 0/1, B 0/1. These tiny selected subsets do not establish general improvement.

Within-condition two-pass label agreement was 95/100 eligible groups for A, with 20 excluded; B was 89/92, with 28 excluded. Repetition may preserve the same disagreement. All 76 reference mismatches remain unresolved in the [machine report](live-001/report.json).

## Provenance and execution

The [archive](live-001/manifest.json) preserves exact request and response bytes, source snapshots, attempts and report. Execution used clean revision `2a38153b777553313ea487e8305bb0bbda96782e` and the frozen comparison sources. Before dispatch, the [official model documentation](https://docs.typesafe.ai/models) listed jev-1.13.0 at USD 0.042 per million input tokens, free output, a 64,000-token combined limit and 32,000 for state plus the longest question. The requests were within these limits. The browser check is recorded here; metadata contains its dated preflight attestation, not a saved provider-page snapshot.

Provider-reported usage was 271,808 input tokens and 40,741 output tokens. The estimated charge was USD 0.011415936, within the USD 1 client ceiling; it is not an invoice. All invalid responses failed the unchanged probability-sum tolerance and remain unmodified.

Archive verification and a configured-credential scan passed. Response structures contained answers, model and usage. Report reproduction checks labels and counts exactly, permitting at most 1e-12 absolute difference for cross-version Brier arithmetic. These are mechanical checks, not independent research validation.

## Decision

Do not promote the candidate as an established improvement. The primary paired result supplies no net advantage, and incomplete coverage constrains both aggregate and targeted comparisons. Preserve both packages and their disagreements.

Pause further prompt tuning while reviewing the 14 response-validity failures and the known reference-linkage ambiguities. Any normalization analysis must be separately labeled and retain these original exclusions. Any packet repair must be a separate version. Repeated tuning on these public cases cannot establish independent accuracy; broader claims require a separate evaluation design.

The subsequent [response-validity and reference review](VALIDITY-REVIEW.md) traces the exclusions and specifies the next packet-linkage diagnostic.
