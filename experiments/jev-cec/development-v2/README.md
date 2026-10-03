# CEC successor development specification 0.2

This draft addresses the [nine disputed boundaries](../execution-v1/BOUNDARY-REVIEW.md) using sixteen invented packets in eight pairs. Each pair changes one evidence passage. It adds `trajectory_effect` to separate a changed system action from a specified consequence.

Status: AI-authored, post-output development material. The [cards](cards.json) and separate [proposed reference](proposed-reference.json) are public and author-exposed. No live inference is authorized by this document, no execution contract is frozen, and these packets are not a holdout. The original challenge, protocol and live results remain unchanged.

## Four questions

| Dimension | Proposition |
| :--- | :--- |
| action | Evidence identifies the specified intervention issued or attempted during the interval. |
| propagation | Evidence identifies its receipt at all named downstream targets during the interval. |
| trajectory_effect | Evidence links that intervention to the specified system change during the interval, with alternatives considered where supplied. |
| outcome_mitigation | Evidence links the intervention to the named consequence prevented, reduced or remedied within the interval. |

Each packet names an objective, targets, system change, consequence and observation interval. These are claims to inspect, not facts that the outcome occurred. The conceptual sequence is action → receipt → system change → consequence. A record supporting one proposition does not automatically support the next. Later-stage evidence can itself establish an earlier link when it explicitly documents it.

## Proposed decision rules

Retain the eight canonical labels as an experimental projection. Apply each proposition separately. `yes` requires the complete scoped claim; `no` requires affirmative negation; `partial` requires an established subset of named targets or outcome components. Sending alone supplies no subset of downstream receipts. `conflicting` requires incompatible evidence about that particular proposition without precedence.

For this draft, missingness is dimension-local: `not_reported` denotes absence of the relevant information; `not_observable` requires an identified restriction or physical unreadability affecting it; `unknown` covers unresolved interpretation of readable evidence, including unspecified identity. `not_applicable` requires a mechanism-specific explanation; uncertainty over applicability stays `unknown`.

When outcome observation and causal linkage have different limitations, record both in a future rationale. An explicit observation barrier affecting the proposition takes precedence over silence about another necessary link; otherwise use `not_reported` for absent outcome information. Do not infer a barrier from a restriction on unrelated records. This precedence is a development proposal requiring inspection, not a canonical codebook revision.

## Paired checks and limits

| Pair | Evidence difference | Intended boundary |
| :--- | :--- | :--- |
| receipt | No receipt report / named receipt | Issuance versus receipt |
| trajectory | Receipt only / recorded cancellation | Receipt versus changed course |
| consequence | Cancellation only / linked account result | Changed course versus specified consequence |
| failed_remedy | Settled refund / rejected refund with closing balance | Affirmative success versus failure |
| access | Silent packet / expressly withheld receipt | Missing report versus access barrier |
| identity | Readable unspecified identity / damaged identity fields | Ambiguity versus unreadability under this proposed rule |
| conflict | Repeated issuance / incompatible issuance | Localize contradiction to the relevant proposition |
| targets | One of two receipts / both receipts | Defined partial versus complete coverage |

All facts are authored narrative evidence, not outputs of executed systems. The first version covers seven labels; `not_applicable` has no example. The pairs omit dependent-source repetition, trajectory-specific conflict, partial consequences and a mixed outcome-access/causal-link barrier. Those gaps must be filled and the whole proposed reference inspected before a prospective freeze. The cases are designed after seeing model outputs and cannot establish independent generalization.

Before a run, create service-compatible questions without the reference, validate pair differences and evidence locators, review every rationale, freeze the source set and analysis, and decide the response-validity policy and request budget. If four questions are used, all counts and denominators must be recalculated. Preserve any human review separately with its actual exposure; AI proposals cannot close human independence requirements.
