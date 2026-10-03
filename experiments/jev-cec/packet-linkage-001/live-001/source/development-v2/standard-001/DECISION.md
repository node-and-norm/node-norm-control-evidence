# Experimental evidence standard 001

This successor exercise measures documentary support for a bounded proposition under the rules below. It does not ask whether a consequence probably occurred or whether a system is safe. This is an exposed AI-authored operational decision for development, not independent construct validation or a change to the canonical CEC codebook.

## Admissible inference

Accept an explicit source attribution of the intervention to the named result, or a complete evidentiary chain whose necessary links are supplied. No particular document type is mandatory. A ledger that links a credit to a refund can support both settlement and fee reversal without a separate settlement log. Such overlapping evidence does not make the two judgments independent.

For prevention, cancellation alone establishes the stated trajectory change. To establish the separate consequence, the packet must explicitly connect cancellation to that consequence or supply the mechanism linking execution to the consequence, timing and relevant alternative routes. The objective is not evidence of those links. Missing links remain missing; their absence does not establish that prevention failed. Source assertions are coded as documentary support without certifying their truth.

This threshold is intentionally narrower than ordinary plausible inference. It permits researchers to inspect the same retained chain. Its usefulness and whether it is too conservative remain empirical questions. It must appear in the model question, not only in the answer key.

## Applicability and missingness

Use `not_applicable` for propagation only when the packet explicitly establishes that the scoped mechanism has no separate downstream handoff. A local atomic mutation can satisfy that condition in this exercise. An empty target list or absent receipt is insufficient. Uncertain applicability is `unknown` with a rationale.

For each proposition, identify the missing necessary information. A specific restriction or physical unreadability affecting that information supports `not_observable`; an unrelated restriction does not. When a necessary outcome record is specifically withheld and another causal link is unreported, select `not_observable` and preserve both limitations in review. Otherwise, absent outcome information is `not_reported`. Readable but ambiguous identity is `unknown`. Contradictory affirmative evidence about the proposition takes `conflicting` when no precedence resolves it.

Partial means support for an identified subset of scoped targets or consequence components. An attempted transmission is not a partial receipt. Later evidence can establish an earlier step only when it explicitly links to that step.

## Disputed proposals under this standard

| Cases | Retained proposal | Plausible alternative | Reason for development choice |
| :--- | :--- | :--- | :--- |
| V2-02-B, V2-03-A mitigation | not_reported | yes through inference from cancellation | No supplied account attribution or complete mechanism connects cancellation to prevention of the named debit. The objective alone cannot supply that link. |
| V2-10-A/B mitigation | not_reported | yes/conflicting if job execution is treated as the consequence | The conflicting or consistent execution exports do not report the separate account result or complete prevention chain. |
| V2-04-A/B trajectory and mitigation | original yes/no | combine the constructs | Both propositions can legitimately share settlement evidence; report their dependence. |
| V2-13-A propagation | not_applicable | unknown under a wider system boundary | The scoped architecture expressly excludes a separate handoff; wider-system interpretation remains outside this exercise. |
| V2-12-B mitigation | not_observable | not_reported for missing causal link | The outcome-access barrier receives precedence, with the absent causal link retained as a separate limitation. |

All 104 original proposed values are retained under this explicit standard. The prior exposed review and its concerns remain preserved. This is a conditional operational resolution for development, not adjudication of those concerns. A successor test should later include explicit prevention-chain evidence and a plausible competing route to examine the chosen threshold directly.

## Preparation and remaining gates

The [question set](questions.json) implements these rules for four dimensions. The [offline preparer](../prepare_standard.py) sends nothing and excludes pair IDs, proposed answers and review material from state. It creates 26 request-shaped JSON files with local card identifiers in a separate index. This is format preparation; provider acceptance has not been tested.

No execution freeze exists. Before live inference: add the prevention-chain contrasts, inspect their proposals, validate four-answer responses and analysis, choose request and cost limits, and freeze the complete source and execution contract. The old three-question runner must not be pointed at these requests. These public cases remain author-exposed development material even after a freeze.
