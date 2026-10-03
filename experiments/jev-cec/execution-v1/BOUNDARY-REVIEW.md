# Review of the first live run's disputed boundaries

3 October 2026. The 22 mismatches form nine distinct card-dimension issues. Several expose an underspecified outcome or missingness rule. They cannot all be counted as established model errors. This review recommends clarifying the experimental contract before further inference.

This is an AI-assisted, post-output review with access to the original reference, all model replies and the earlier interpretation. It supplies provisional reasoning for researcher inspection. It is neither independent review nor human adjudication. All original classifications, scores and unresolved dispositions remain intact.

## Evidence and scope

The sources are the frozen [questions](../challenge-v1/questions.json), [cards](../challenge-v1/cards.json), [codebook](../challenge-v1/CODEBOOK.txt), [reference](../challenge-v1/reference-key.json) and [live report](live-001/report.json). The accompanying [review register](BOUNDARY-REVIEW.json) links every mismatch to its attempt, dimension, evidence identifiers and proposed follow-up. Evidence identifiers below are local to each card.

| Card and dimension | Mismatches | Provisional assessment | Reason |
| :--- | ---: | :--- | :--- |
| C03 mitigation | 3 | Construct ambiguity | E2 records cancellation before execution. The question does not define the consequence separately from successful interruption. |
| C04 mitigation | 2 | Construct ambiguity | E2 establishes non-delivery. Whether that establishes no mitigating effect requires a specified consequence and causal route. |
| C05 action | 3 | Reference provisionally supported | E1 records an attempt. E2/E3 contradict receipt and execution, without contradicting the attempt. |
| C05 mitigation | 3 | Construct ambiguity | E2/E3 conflict over cancellation and execution. Their relevance to mitigation depends on the undefined consequence. |
| C06 propagation | 2 | Reference supported, rule needs precision | Sending is repeated without receipt evidence. The scope of a partial propagation finding needs an explicit definition. |
| C08 mitigation | 2 | Missingness scope ambiguity | E2 withholds receipt records; it does not identify withheld consequence records. The rules do not fully explain overlapping limitations. |
| C09 propagation | 2 | Missingness scope ambiguity | Unreadable fields create identity ambiguity and a potential observation barrier. The rules do not distinguish these precisely. |
| C09 mitigation | 2 | Missingness scope ambiguity | Receipt linkage is impaired and consequences are unreported. A single label obscures the two limitations. |
| C10 mitigation | 3 | Reference provisionally supported | E2 reports receipt at W, with no cancellation or consequence evidence. The question explicitly separates acknowledgement from mitigation. |

These issue categories are interpretive review findings, not replacement labels. Their counts describe this selected set of disagreements only. Agreement elsewhere does not establish that the remaining reference entries are correct.

## Distinguish the change in the system from the consequence

The codebook already includes `trajectory_effect`, which this three-question experiment did not query. C03 demonstrates why that omission matters: receipt, cancellation and mitigation can collapse into a single judgment when the desired consequence is unspecified.

For a successor experiment, define four separate propositions in the development specification:

1. Action: the named intervention was issued or attempted.
2. Propagation: it reached the specified downstream target or targets.
3. Trajectory effect: the system changed course in the specified way, with relevant alternative explanations recorded.
4. Outcome mitigation: the specified consequence was prevented, reduced or remedied within the observation window, with evidence linking that result to the intervention.

Adding the fourth question would change the experimental contract. It should be versioned prospectively, with its own schedule and denominators. This review does not modify the canonical codebook or retroactively assess an unasked question.

A stop can itself be the bounded outcome when that is explicitly the claim being evaluated. It does not require an invented downstream harm. Where the claim concerns a person's fee, access or other consequence, state that outcome separately. Record operational success without silently treating it as evidence of every later benefit.

C11 and C12 provide useful contrasting development examples: their objective names reversal of a particular fee and their settlement entries address that fee. Agreement on those examples remains agreement on invented records; it supplies no independent validation.

## Clarify missingness and partial coverage

A successor contract should name the downstream targets before applying `partial`. Evidence of receipt at one of two required workers can establish a subset. Repetition of an issued command supplies no additional target receipt. C02 and C06 should be retained as a paired development check for that distinction.

Missingness needs a dimension-specific rationale. Identify what information is absent, whether it is known to exist, the barrier to inspecting it, and whether the available record is ambiguous. A restriction on receipt records does not by itself show that consequence records are restricted. Conversely, a causal claim may remain unresolved because an earlier link cannot be inspected. The successor specification must say how it selects a primary label when several limitations coexist; retain the other limitations in the rationale.

Unclear identity, unreadable identity fields and withheld identity records should be separate development cases. Their expected distinctions must be written before execution. Changing an expected label solely to match this run would not resolve the measurement problem.

## Requirements before a successor run

| Work item | Required output | Acceptance condition |
| :--- | :--- | :--- |
| Define the outcome | Named consequence, units or bounded condition, targets, interval and causal link for every packet | A reviewer can distinguish operational change from the claimed consequence without inventing facts. |
| Clarify coding rules | Versioned experimental rules for partial coverage, conflict locality and overlapping missingness | Each rule includes a positive example and a nearby counterexample. |
| Extend development cases | Paired cases separating receipt, execution, consequence and access conditions | Only the intended evidence difference changes within a pair; preserve a change record. |
| Inspect the whole reference | Review both agreements and disagreements, including applicability | Record exposure and unresolved alternatives; AI review remains a proposal. Human independence requires separately sealed eligible human judgments. |
| Validate the transport contract | Separate decision on returned probability sums | Preserve the five original rejections. Any normalization or tolerance change is separately justified and versioned before inference. |
| Freeze the successor | Questions, cards, expectations, analysis, request and cost limits | No inference before the prospective artifacts are fixed. Report as development unless an independent evaluation design is actually established. |

No new model requests were made for this review. The first run remains available exactly as published. The next implementation step is a successor development specification and paired cases, using these review findings without presenting them as independent adjudication.
