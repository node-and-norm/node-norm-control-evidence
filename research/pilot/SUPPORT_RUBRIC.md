# Documentary-support rubric: draft 0.1

[Repository](../../README.md) / [Pilot workbench](README.md)

The comparative pilot needs a repeatable way to assess whether a submitted conclusion follows from its frozen evidence packet. This draft supplies operational rules for decision P05. It is AI-assisted, unreviewed, and unavailable for confirmatory use until accountable humans approve the procedure. It changes no canonical construct or control-state value.

## Scope of a judgment

Assess one submitted proposition and conclusion about one event-control opportunity in a specified period. Record the packet ID and hash, exact proposition text, reviewer submission ID and hash, and rubric version. Split compound conclusions into separately identifiable propositions before assignment under a frozen segmentation rule. Preserve the original text and mapping; segmentation must not depend on which representation produced the response.

The support judgment concerns the inference permitted by the supplied evidence. The underlying world state may remain unknown. An allegation can support the proposition that an allegation was made; it does not by itself establish the alleged operation. Independent agreement about documentary support supplies no criterion truth about the event.

Use the existing [codebook](../../docs/methods/CODEBOOK.md) to interpret the submitted control-state value. The four labels below describe the support assessment and remain separate from that value.

| Support judgment | Operational rule |
| :--- | :--- |
| supported | The frozen packet warrants the submitted conclusion at its stated scope and certainty. The assessor identifies the evidence and reasoning, or the documented packet coverage supporting a bounded missingness statement. Material conflicting evidence is addressed. |
| unsupported | The assessor identifies a specific inferential defect: contradictory evidence, a scope or time mismatch, omitted material conflict, or a conclusion exceeding what the packet warrants. This includes an affirmative or negative control finding based only on silence. It does not mean the conclusion is false in the world. |
| unresolved | The assessor completes review but cannot determine whether the conclusion is warranted because a specific ambiguity in meaning, scope, or evidentiary interpretation remains. Record that ambiguity. This is not an automatic score for an unresolved control-state value. |
| not_assessed | No completed support assessment exists because of withdrawal, access failure, missing submission, conflict, or another procedural reason. Preserve the reason and assignment; do not treat this as an evidentiary finding. |

A well-supported `not_reported`, `unknown`, `not_observable`, or `conflicting` conclusion can receive `supported`. A generic assertion of uncertainty does not automatically earn support: inspect whether the packet actually permits a more specific conclusion under the frozen rule. `not_applicable` requires a mechanism-specific rationale. Partial conclusions must identify the supported component and the unresolved remainder.

## Assessment procedure

1. Confirm the assignment, rubric version, event-control period, packet hash, and sealed reviewer submission hash. An unavailable or mismatched artifact prevents assessment; record the reason.
2. Inspect exact evidence locators and relevant surrounding material within the same frozen packet. No external search or later source may silently augment this assessment. Log a proposed packet correction separately.
3. Check the proposition's subject, mechanism, opportunity, period, and strength against what the evidence establishes. Distinguish a declared role, implementation, operation, action, propagation, and outcome effect.
4. Trace repeated assertions to their source families. Multiple publishers repeating one record remain dependent. Unknown dependence remains unknown. An independence claim needs its own basis.
5. Check source version, event time, publication time, retrieval time, and evidence cutoff separately. A later investigation may describe earlier operation; its date alone establishes neither contemporaneous knowledge nor the mechanism's state.
6. Apply one support label and record a rationale with supporting and conflicting locators. For silence, identify packet coverage and retrieval limits. Unavailable evidence remains a missingness condition.
7. Seal the initial assessment with a timestamp and checksum before comparison. Preserve disagreement; any adjudication receives a separate record referencing every initial assessment and the reason for resolution.

## Independence and custody

A support assessor must be a different eligible human from the reconstructing reviewer and must satisfy the [reliability plan](../../docs/methods/RELIABILITY_PLAN.md). Record role acceptance, conflicts, case familiarity, and prior exposure under appropriate access. At least two eligible independent human initial assessments are required for support judgments used in primary published comparisons. AI drafting or suggested ratings cannot satisfy these roles.

Provide support assessors the common frozen packet and the submitted proposition, conclusion, and locators in a neutral layout. Withhold representation labels, hypotheses about the preferred view, other assessors' ratings, and adjudicated answers until sealing. Content may still reveal the representation; record suspected exposure and report this limitation. Do not remove evidentiary content to disguise a view.

Use the separate [support-assessment instrument](templates/support-assessment.csv). Its pseudonymous IDs link to access-controlled role and assignment records. The existing reconstruction worksheet has legacy support columns; leave those blank in new initial reviewer submissions. Preserve any existing submissions unchanged, then link support assessments by submission ID and hash. A later joined analysis table is derived data. A mutable shared CSV does not establish independent custody.

## Calibration examples

These invented examples illustrate the draft rules. They are development exposure and must never serve as untouched validation cases.

| Packet and submitted conclusion | Proposed support label | Reason |
| :--- | :--- | :--- |
| Policy assigns a reviewer; conclusion says runtime intervention occurred | unsupported | Assigned authority does not establish an action in the relevant period. |
| An override command is recorded; conclusion says propagation is unreported within the reviewed packet | supported | The conclusion is bounded to packet silence about downstream execution, assuming coverage was checked. |
| Same command; conclusion says propagation failed | unsupported | Silence supplies no affirmative evidence of failure. |
| Stop acknowledgement; conclusion says harm was prevented | unsupported | A downstream state change alone leaves mitigation and alternatives unresolved. |
| Two incompatible operational accounts; conclusion preserves conflict and cites both | supported | The conclusion retains the unresolved evidentiary conflict. |
| Three articles repeat one statement; conclusion calls them three independent confirmations | unsupported | The corroboration claim discards shared origin. |
| Ambiguous system identity prevents deciding whether a passage warrants the submitted value | unresolved | The assessor records the unresolved identity and its bearing on scope. |
| Assigned assessor cannot access the frozen packet | not_assessed | The procedure was not completed. |

## Reporting and decisions still open

Report counts for all four support categories by representation, including assignments with missing submissions or assessments. Preserve the submitted conclusion values alongside support labels. Cross-tabulate affirmative and negative conclusions against support judgments to expose unsupported certainty. Report well-supported unresolved control conclusions separately from unresolved support assessments.

The assignment register must supply the denominator, including nonresponse. Do not derive it only from completed CSV rows. Duplicate propositions, unenumerated opportunities, unmatched controls, and segmentation disagreements need separate coverage reporting. A method must not gain apparent performance by emitting many easy propositions or omitting difficult ones.

For any exploratory proportion, publish its numerator, denominator, exclusions, and missing counts. Zero denominators are undefined. Keep event-weighted and control-weighted summaries distinct; account for shared events, reviewers, assessors, and source families in the later analysis design. Do not pool synthetic calibration exercises with empirical observations.

Record preparation and review time as measured durations with a common timing rule; interruptions and unavailable measurements need reasons. The new support instrument records assessment seconds separately. Benefit, burden, allocation, precision, primary weighting, and acceptance thresholds remain open in P04 through P09. No composite score is introduced.

Before allocation, accountable humans must review the rubric, segmentation and coverage rules, assessor masking, timing, and storage procedure; trial them on disclosed development material; retain disagreements; and version any revision. P05 remains open until that decision and its evidence are recorded.
