# Review of the four-question live disagreements

The 62 mismatches form 30 card-dimension issues. This review checks every mismatch against the exact dispatched question and evidence. It identifies direct-evidence disagreements, conflict and missingness spreading between dimensions, and a packet-linkage ambiguity that also challenges the authored reference.

The [structured register](DISAGREEMENT-REVIEW.json) preserves each attempt, original choice, reference, exact evidence and question, and a provisional explanation. All dispositions remain unresolved. This is exposed AI analysis with access to the reference and prior outputs, not independent adjudication. No scores, reference labels or raw responses changed.

## What the evidence supports

V2-14-A states that W received R and that R cancelled J before execution. The model returned `not_reported` for both receipt and trajectory in all three valid passes. Under the frozen questions, absent account evidence does not remove those explicit statements. This is a direct disagreement with the intended dimension boundary. It does not show why the model produced the labels.

V2-04-B records receipt and a rejected settlement. The model marked receipt `conflicting` in all three passes. Rejection does not contradict receipt. V2-10-B likewise contains conflicting execution exports while preserving uncontested issuance and receipt, yet conflict extended to those propositions and mitigation. V2-07-B extends an issuance conflict into unreported later stages.

For V2-12-B, the account record is withheld while receipt and execution records are simply absent. The model applied `not_observable` to all three in its single valid pass. The standard makes barriers dimension-specific. Nevertheless, missingness precedence is an experimental operational choice; it has not been independently validated.

## Where the reference also needs scrutiny

V2-12-A/B says only that the console “issued R.” It does not explicitly associate R with J or define R as STOP. The scoped objective supplies the author's intended reading, but the question says scope is not observed evidence. The reference's `yes` therefore rests on implicit linkage. The model's alternative label is not automatically correct either. Preserve both and repair the packet explicitly in a future version if the intended test is issuance versus receipt.

The abbreviated R wording in original pair 02 deserves the same linkage inspection, although its receipt text also names J. A reference review should distinguish a complete human-readable context from an assumed machine-readable identity relationship.

V2-06-A and V2-15-B expose the boundary between `unknown` and `not_reported`: the packet provides an ambiguous identity or a competing route but no decisive result. The draft intentionally chooses `unknown`. Whether that distinction is clear and useful remains a construct question, not something model agreement can decide.

## Identical inputs, different outputs

The P1-V2-14-B and P1-V2-15-A request bytes are identical. Both responses were valid, but trajectory was `yes` for the first and `partial` for the second. The other three labels agreed. In passes two and three the V2-14-B response was invalid, preventing a complete valid comparison.

This is an observed consistency limit on one complete duplicate comparison. It does not establish a frequency, a provider-internal mechanism or a population reliability estimate. Local card IDs are not included in the request payload, so those IDs do not explain a prompt difference.

## Next experiment should isolate one question

Do not rerun this batch unchanged or silently normalize invalid outputs. A useful next diagnostic is a prospectively specified comparison of the frozen shared instructions with shorter dimension-specific instructions while holding evidence and proposed reference fixed. Inspect the runner's exact payloads first, preserve failed attempts, counterbalance request order and report every condition separately. Treat any such work as exposed prompt development.

Packet repairs should be a separate condition or version. Simultaneously changing instructions, evidence and labels would make their effects difficult to distinguish. The direct-evidence cases, duplicate baseline and incomplete competing-route comparison provide diagnostic targets, not an independent evaluation set. No additional inference is included in this review.
