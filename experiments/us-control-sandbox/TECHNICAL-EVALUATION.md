# Technical-evidence evaluation rules 0.1

Prepared 2 October 2026, before new case construction. This is a versioned development evaluation contract. It is not a preregistered study, an independent assessment, a human-participant protocol or a TAE/HIT scoring extension. No evaluation results are reported in this document.

## Question and unit

Can an evidence-processing procedure distinguish a documented technical effect, a documented technical fault and insufficient evidence, without using the hidden execution outcome?

One unit is one packet version, one specified control objective and one bounded observation period. Frame the objective positively and narrowly, such as preventing a specified commitment after an applicable stop, avoiding an additional effect on a retry, or delivering a specified correction to the simulated recipient store. Establish request identity, command applicability, ordering and the observation cutoff before asking whether the objective was met. Rejection of an inapplicable command is not automatically a control fault.

Every packet states its objective and relevant boundary. Human authority, understanding and judgment remain outside this technical contract. The [admissibility decision](ADMISSIBILITY.md) still governs any proposed TAE/HIT application.

## Two answer records

The execution record describes what happened in the simulated system. Keep it unavailable to the evaluator. The evidence-sufficiency key describes what a specified packet can support about the stated objective. These records must remain separate.

For each unit, the evidence-sufficiency key must preserve source hashes, exact locators, the positive objective, scope and timing, known evidence restrictions, contradictions, a rationale and its author/review/exposure status. Its compact scoring projection has one reference state:

| Reference state | Admission rule |
| --- | --- |
| `supported_effect` | Applicable, linked records support the stated objective over the declared boundary; no unresolved material conflict changes that conclusion. |
| `supported_fault` | Applicable, linked records support a violation of that objective over the declared boundary; no unresolved material conflict changes that conclusion. |
| `unresolved` | The packet lacks a necessary linkage, state, applicable authority-to-command setting, timing boundary or observation, or contains a material unresolved conflict. |

These are technical-evidence states, not HIT findings or TAE stage states. A stored field can support a claim about that record. A claim about actual execution additionally needs the predeclared evidence-generation and completeness assumptions. The key must state which claim is being assessed. An acknowledgment alone cannot establish the downstream effect; a missing record alone cannot establish failure.

A malformed packet, undefined objective, corrupted provenance or unresolvable question boundary is excluded during intake with a named reason. Keep these exclusions in the cohort ledger and report their counts. Do not convert them to `unresolved` merely to include them in a convenient denominator. Ordinary planned missingness belongs in valid unresolved cases. The scoring projection cannot perform this substantive admission review.

## Evaluator response and rationale

The evaluator returns `effect_supported`, `fault_supported` or `unresolved`, with a bounded rationale and packet locators. It may not infer missing content from case names, sources outside the declared packet, the answer key or the simulated outcome. Missing, duplicated, malformed or out-of-cohort responses invalidate the run for scoring; they are operational failures, not justified uncertainty.

The metric calculator consumes only the compact labels after responses are fixed. It does not judge a rationale, authenticate a key or decide whether a citation actually supports a proposition. A separate rationale review must reject unsupported claims even when the submitted label happens to match. Label agreement alone is not sufficient evidence of sound assessment.

## Measures and denominators

All measures report numerator and denominator. A zero denominator yields `null`, meaning not estimable, never zero performance or success. An empty overall cohort is invalid. Report the full three-by-three matrix and all measures; there is no composite score.

| Measure | Numerator | Denominator |
| --- | --- | --- |
| Unsupported reassurance | `effect_supported` responses where the key is fault or unresolved | All fault and unresolved units |
| Missed documented fault | Any response other than `fault_supported` where the key is fault | All supported-fault units |
| Appropriate uncertainty | `unresolved` response where the key is unresolved | All unresolved units |
| Unsupported negative conclusion | `fault_supported` responses where the key is effect or unresolved | All effect and unresolved units |
| Unnecessary abstention | `unresolved` responses where the key is determinate | All supported-effect and supported-fault units |
| Supported-effect recognition | `effect_supported` response where the key is effect | All supported-effect units |

A fault answered as an effect enters both unsupported reassurance and missed documented fault. Categories overlap and must not be summed as a total error rate. An all-unresolved procedure has perfect appropriate-uncertainty performance but misses every supported fault and recognizes no supported effect. The matrix makes that behavior visible.

Counts are descriptive for the declared cohort. Deterministic repeats are reproducibility checks. Correlated variants of one scenario remain one family for later uncertainty analysis; they do not become independent evidence merely because they produce separate rows. No population rate, confidence interval or universal safety threshold is justified by these fixtures.

## Comparison design to fix before cases

Compare a simple deterministic checklist with the candidate evidence-processing procedure on paired units. Both receive the same objective, boundary and admissible facts. Any representation change must preserve information content; disclose added structure and access to raw evidence. Both outputs are fixed before the key is revealed. The checklist must use linkage, applicability, observation and contradiction checks, not a rule that treats acknowledgment as success.

Implement and version both procedures before constructing new case families. Do not use the current appendix extractor as a scored assessor: it preserves observations and does not make these conclusions. Evaluate label agreement and rationale adequacy separately. No incremental value, usability or independent validity claim follows from two author-written procedures agreeing with an author-written key.

## Fixed failure handling and prospective gates

For software regression fixtures with known reference labels, every matrix cell and denominator must calculate exactly. This is an arithmetic-correctness requirement, not a field-performance threshold. A calculator must reject missing, duplicate or unexpected units and unknown labels. It never reads the hidden execution record.

Before a new study run, fix the cohort and family split, inclusion/exclusion ledger, evidence-generation assumptions, full key with locators/rationales, evaluator versions, comparison, response/rationale format, operational failure policy and any claim-specific acceptance thresholds. Record these in the versioned run plan before output inspection. None are silently supplied by this calculator.

For a researcher-only study without an independent custodian, describe new cases as author-exposed evaluation cases. They may be withheld from an automated evaluator, but cannot establish independent blinding or an untouched researcher holdout. The current sixteen public fixtures are development examples only. Later independent custody or review must be attributable to actual eligible people.

An invalid run retains inputs, error details and exclusion history. Repair creates a new attempt and records the change; never drop difficult units after seeing responses. No automatic overall pass or method validation is produced.

## Status and next deliverable

`evaluation_rules.json` fixes the label vocabulary and metric contract; `evaluate_evidence.py` implements its arithmetic. The tests exhaust the nine combinations of three reference and three response states and challenge omissions, duplicate units and abstention. These are calculator checks, not evaluations of TAE, HIT or an AI model.

The paired procedures and a candidate run plan are now implemented in PROCEDURES.md and RUN-PLAN.md. Their verifier checks mechanical consistency, not independent rationale quality. Complete the trace-quality criteria, cohort and access plan before a new evaluation. Only then construct new case families and record who can access the packets, evidence-sufficiency key and execution record. Changes to these rules require a new version and a visible deviation record after any evaluation exposure.
