# Instruction comparison 001: prospective development design

The v2 review found disagreements about explicitly stated evidence and ambiguity in the reference. This diagnostic asks whether a dimension-specific instruction package changes agreement and coverage when packet evidence, model, question identifiers, probability criteria and reference are held fixed.

Status: prospective offline design, no inference. The cases and candidate instructions were selected after inspecting v2 outputs. Results would describe exposed prompt development, not independent accuracy or generalization. There is no presumption that the candidate will outperform the baseline.

## Conditions and what changes

A uses the exact frozen v2 shared instructions. B uses [candidate-questions.json](candidate-questions.json). Only the four `instructions` strings change. Both conditions ask all four questions together, with the same eight criteria and the same packet. Proposed answers, local card IDs and condition names remain outside the API payload.

B reduces unrelated dimension-specific material and adds local clarification. This changes length, wording and emphasis together. It is not a test of instruction length alone or proof of a model-internal cause. It also explicitly states the competing-route reading that was implicit in the operational standard. The condition therefore tests an instruction package, not strict semantic equivalence. Reference ambiguities remain visible and are not repaired here.

| Rule | Candidate treatment |
| :--- | :--- |
| Documentary support and no invented links | Retained in every question |
| Source dependence, scope, conflict and missingness | Retained in shared concise text |
| Attempt versus receipt or benefit | Local to action |
| Receipt coverage and failed settlement | Local to propagation |
| System change and retrospective settlement evidence | Local to trajectory |
| Prevention chain and unresolved alternative route | Local to mitigation |
| Applicability | General rule retained; no-handoff example local to propagation |

## Schedule and budgets

Use all 30 cards in two passes. Within each pass, pair A and B requests for each card. For odd-numbered cards use AB in pass one and BA in pass two; even cards use BA then AB. This yields 120 requests, 480 scheduled determinations, 60 requests per condition, and equal first/second exposure for each condition. Card ordering stays deterministic. Adjacent pairs reduce long temporal separation but do not eliminate service drift or order effects.

V2-14-B and V2-15-A remain intentional duplicate packet states. There are 29 distinct states, not 30 independent cases. Request sequence and condition metadata must be retained separately from payloads. No retries, replacements, best-pass selection or optional early stopping based on scores.

Proposed client ceilings: 120 requests and USD 1, with sequential requests and 30-second timeout. Before any dispatch, verify official model availability, pricing and limits and reserve the maximum request cost. At the previously supported USD 0.042 per million input tokens and 64,000-token bound, the planning ceiling is USD 0.32256; current prices are not asserted. This preparer has no transport and enforces no live spending policy.

## Analysis before outputs

Primary descriptive comparison: pass one, report each condition's matches/valid alongside valid/120 scheduled judgments. Pass two is repetition, reported separately. For each card-dimension with both conditions valid, tabulate both-match, A-only-match, B-only-match and neither-match. Report the eligible denominator and exclusions against 120 per pass. A paired agreement difference may be calculated as (B-only minus A-only)/eligible, undefined when eligible is zero. Report individual condition coverage even when paired coverage is low.

An invalid response excludes all four judgments. Use unchanged v2 strict response acceptance and no probability repair. Invalid outputs never become evidence labels. Stop on transport/HTTP errors, unavailable usage or model mismatch; preserve unattempted positions. Retain all raw distributions and descriptive Brier sums by condition and pass. Do not pool passes to select a winner, infer population uncertainty or claim independent accuracy.

Report direct-evidence targets and disputed-reference cases only as named secondary descriptive subsets, with membership fixed before dispatch. Suggested membership for future freeze: direct-evidence targets V2-04-B propagation and V2-14-A propagation/trajectory; disputed-reference targets V2-12-A/B action and V2-15-B mitigation. Keep every case in the primary analysis. No adaptive subset selection.

## Before execution

The offline preparer validates the v2 freeze, builds both payload conditions and writes exact request hashes and the source-artifact hashes. That manifest identifies a preparation run, not a final study freeze.

Next implement the comparison runner and paired analysis, test counterbalanced accounting and failures using a local service, finalize the secondary subset membership, then freeze plan, candidate, source records, reference, implementation and budget contract at a clean commit. No source repair, reference relabeling or sensitivity normalization may be folded into this comparison. Those require separate versions.
