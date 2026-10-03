# Paired-case expansion and reference review 001

The development set now contains 26 packets in thirteen pairs. Ten new packets address the five documented coverage gaps. All 104 proposed judgments, including the original agreements, have a separate [review record](reference-review.json) with evidence locators, reasoning and any remaining construct issue.

This is exposed AI review, conducted after reading the earlier outputs and reference. It is not independent human adjudication. Original cards and proposed labels remain unchanged; there is no new model run or revised performance score.

## Added pairs

| Pair | Change | What it tests |
| :--- | :--- | :--- |
| 09, dependent repetition | One quotation becomes three quotations of the same source | Repetition adds no receipt evidence. |
| 10, trajectory conflict | Consistent execution export becomes an incompatible export | Conflict attaches to execution without erasing the uncontested attempt and receipt. |
| 11, partial consequence | One linked fee credit becomes two | Partial versus complete named outcomes; later-stage evidence may establish settlement. |
| 12, overlapping missingness | Unreported outcome becomes a specifically withheld outcome | Record missing causal linkage and outcome access separately; apply the proposed label precedence. |
| 13, applicability | Local atomic mechanism becomes a remote command mechanism | No separate handoff versus an applicable handoff lacking receipt evidence. |

The [new cards](cards.json) contain only scope and invented evidence. Their [proposed reference](proposed-reference.json) is stored separately with a rationale for each dimension. IDs continue the original series. Within each pair only E2 changes; scope and E1 remain constant. Pair 13 deliberately changes the described mechanism, so it is an applicability contrast, not a causal estimate from equivalent mechanisms.

All eight labels now occur somewhere in the proposed set. This does not provide balanced coverage of each label within every dimension, broad domain coverage, or evidence of generalization. The cases remain concentrated in authored fee and stop-command narratives.

## Findings from reviewing all proposed answers

1. Original V2-02-B and V2-03-A mitigation remain contestable. Cancellation before execution may logically prevent the specifically named debit from that job. A demand for an additional account record is a documentary evidence threshold, which must be stated and justified. Merely calling the outcome a separate dimension does not settle the inference. The new trajectory-conflict pair inherits this issue.
2. Original refund pair 04 uses settlement as the system change and fee reversal as the consequence. Those propositions overlap. The pair remains useful for affirmative failure, but their agreement cannot demonstrate independent measurement of two constructs.
3. The new partial-consequence pair checks the reverse inference: a linked credit can establish settlement even if a separate settlement record is absent. A rule demanding one particular document for each dimension would incorrectly discard that evidence.
4. Physical unreadability and access restriction are grouped under the draft's `not_observable` rule. The original identity pair supports that intended contrast, but this remains a proposed operational definition requiring research review.
5. The applicability pair depends on a stated mechanism boundary. A local atomic control can lack a separate downstream handoff; that interpretation must not turn an empty target list or missing receipt into `not_applicable` by default.

The structured review preserves proposed labels and records open issues without supplying replacements. “Provisionally supported under draft” means internally defensible under the stated reading. It does not certify the reference as correct.

## Decision before freezing

Keep execution unfrozen. Resolve the cancellation-to-consequence evidence threshold and mechanism-specific applicability first. Document whether the study measures documentary support under a specified standard or broader warranted inference. That choice changes the question, reference rationale and interpretation of agreement.

Next, revise the experimental wording with an explicit change record, inspect alternate labels for the flagged cases and prepare service-compatible inputs without answers. Freeze the final questions, cases, reference, acceptance rules, analysis and request budget together. Later tests on these publicly exposed cases remain development tests. Independent claims require a separate design and actual independent review.

No original experiment archive, canonical codebook, TAE/HIT assessment or scientific release gate changed. The eight-class coverage is a design inventory, not a measured result.
