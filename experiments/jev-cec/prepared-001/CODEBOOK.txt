# Development codebook 0.1.0

[Repository](../../README.md) / [Documentation](../README.md) / Codebook

Each annotation records one dimension of one event-control observation, packet version, coder identity and kind, provenance-bearing evidence IDs, rationale, and coding time. Human authoritativeness requires an eligible human's own initial judgment, sealed before comparison. AI suggestions remain proposals.

## Values

| Value | Decision rule |
| --- | --- |
| yes | Evidence affirmatively supports the complete proposition in the specified period. |
| no | Evidence affirmatively supports its absence or negation. An unsuccessful document search is insufficient. |
| partial | Evidence establishes an identified subset of the proposition; state which part remains unsupported. |
| conflicting | Material sources support incompatible readings which the coding rule cannot resolve. |
| unknown | Available evidence leaves the proposition unresolved after recorded retrieval. |
| not_reported | The reviewed packet does not report the information; this is a statement about the packet. |
| not_observable | The required state cannot be resolved within the documented access conditions; explain the barrier. |
| not_applicable | The proposition has no role for this control mechanism; give a mechanism-specific reason. |

Use conflicting before unknown when there is affirmative conflict. Use not_reported for silence, not_observable for an identified access barrier, and unknown for residual uncertainty. Never impute a no value from these categories. Applicability itself may be uncertain; use unknown and explain it.

## Dimensions and affirmative evidence

| Dimension | Required proposition |
| --- | --- |
| declared | A dated policy or statement assigns this control objective. |
| design_adequacy | A stated criterion and operating assumptions support this design; no global safety judgment. |
| implemented | Configuration, deployment record, or sufficiently specific evidence places the mechanism in the system. |
| operating | Evidence places that mechanism in operation during the relevant period. |
| trigger | Evidence establishes the applicable condition or decision point. |
| action | Evidence identifies the action produced or attempted. |
| propagation | Evidence traces action to the downstream component or decision. |
| trajectory_effect | Evidence identifies a change in trajectory and relevant alternative explanations. |
| outcome_mitigation | Evidence connects control action to mitigation; association alone leaves this unresolved. |
| formal_authority | A role had assigned authority over this decision. |
| information | The role could access the relevant information at that time. |
| comprehension_opportunity | Presentation, training, and time allowed assessment; do not infer mental state. |
| intervention_time | The intervention window accommodated the required action; retain timing evidence in rationale. |
| technical_permission | Interfaces and permissions permitted the action. |
| institutional_permission | Organizational rules permitted the action without contradicting authority requirements. |
| alternatives | A viable alternative action was available. |
| intervention_attempted | Evidence records a human attempt. |

## Procedure

1. Freeze event scope, retrieval cutoff, codebook version, and packet.
2. Independently enumerate objectives, mechanisms, opportunities, and relevant periods. Retain hypothetical opportunities as such, and preserve unmatched controls.
3. Trace sources to their origins and record inaccessible material. Supply identical evidence to each eligible coder.
4. Code applicability before substantive values. Use exact evidence locators; explain uncertainty and access barriers.
5. Seal initial submissions before comparison. Record exposure, conflicts, and coder identity under the independence procedure.
6. Compare and adjudicate in separate records. Never overwrite initial annotations.

## Boundary examples

| Evidence | Defensible distinction | Inspect |
| :--- | :--- | :--- |
| Policy assigns approval authority | A declaration leaves implementation and operation unresolved without supporting records | [Policy-only dossier](../../examples/dossiers/policy-only.md) |
| Override command without downstream acknowledgement | An action can be recorded while propagation is `not_reported` in the packet | [Unresolved override](../../examples/dossiers/override-unresolved.md) |
| Command and downstream stop acknowledgement | Propagation can resolve while consequences and mitigation remain unreported | [Acknowledged stop](../../examples/dossiers/override-confirmed.md) |
| Three articles repeating one institutional statement | Repetition preserves one assertion family; publisher count does not establish independence | [Source policy](../policies/SOURCE_POLICY.md) |
| Always-on permission boundary | Operation need not involve a discrete trigger | [Constructs](CONSTRUCTS.md) |

The linked cases are synthetic teaching and software artifacts. They supply no empirical validity evidence.


Quantitative timing and construct-specific thresholds require pilot amendments before they become canonical structured measures. This codebook does not authorize a composite score.
