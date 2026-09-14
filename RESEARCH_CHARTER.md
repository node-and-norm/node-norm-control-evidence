# Node & Norm Control Evidence Research Charter

**Status:** Research design draft  
**Artifact:** Node & Norm Control Evidence Corpus  
**Repository:** `node-norm-control-evidence`  
**Program:** Node & Norm AI Assurance & Evaluation Lab

## 1. Purpose

The Node & Norm Control Evidence program studies whether claims about AI governance controls can be substantiated by evidence of how those controls were designed, implemented, operated, and exercised in consequential sociotechnical systems.

The research begins from a distinction between the existence of governance and evidence of governance effectiveness.

Policies, approval procedures, human-review requirements, safeguards, monitoring systems, escalation mechanisms, access restrictions, evaluation gates, and override capabilities may all be documented. Their presence does not establish that they operated as intended when a consequential condition occurred.

The program therefore examines the evidentiary relationship among:

- system behavior;
- identified risks;
- institutional control claims;
- implemented controls;
- human authority and intervention capacity;
- observed outcomes;
- surviving operational evidence; and
- the conclusions that the available evidence can legitimately support.

The corpus is intended to provide reusable empirical infrastructure for Node & Norm research, including Trust, Autonomy & Evidence, Human Influence Telemetry, Regulated Gate Decision Support, and future assurance studies.

## 2. Primary Research Question

For publicly documented AI-related events, what evidence is available to establish whether relevant governance and technical controls were designed appropriately, implemented, operating during the relevant period, capable of influencing the system, and effective in addressing the risk they were intended to control?

## 3. Secondary Research Questions

The program will investigate several related questions.

How often can public evidence distinguish a declared control from an implemented and operating control?

Which forms of evidence provide the strongest basis for assessing control operation?

Where human oversight is present, what conditions determine whether the human possesses practical rather than merely formal decision authority?

Which control characteristics are associated with successful detection, restriction, escalation, correction, recovery, or human intervention?

Which aspects of AI incidents remain systematically unobservable after the event?

How frequently do institutional claims about safeguards exceed what the available evidence can substantiate?

Which governance concepts can independent researchers annotate reliably, and which remain too ambiguous for reproducible measurement?

How does evidentiary sufficiency vary by system type, domain, risk class, control class, institutional context, and source availability?

## 4. Epistemic Target

The corpus does not assume that public evidence provides complete access to the actual state of an AI system or organization.

For every case, the research distinguishes four layers:

**World state:** what actually occurred, which may remain partly unknowable.

**Evidence state:** documents, logs, records, testimony, investigations, technical artifacts, evaluations, and other surviving evidence.

**Annotation state:** structured observations made by researchers from that evidence.

**Inference state:** conclusions the research protocol permits on the basis of those observations.

A Node & Norm inference must never be represented as direct knowledge of the underlying world state unless the evidence warrants that conclusion.

The absence of evidence for a control is not evidence that the control did not exist.

A valid conclusion may therefore be:

> The available evidence does not establish that the control was implemented or operating at the relevant time.

That conclusion is materially different from:

> The control did not exist.

## 5. Units of Analysis

An incident is not the primary analytical unit for control research.

The principal unit will be an **event-control observation**.

One event may involve several relevant controls. Each control may have different evidence, owners, operational states, intervention mechanisms, and outcomes.

The hierarchy will therefore be:

**Event → Control Opportunity → Evidence Items → Claims → Annotations → Adjudicated Inference**

Human oversight may constitute one or more control opportunities within an event.

This structure prevents a complex incident from being reduced to a single binary assessment such as `control_failed = true`.

## 6. Event Classes

The evidence system must support more than harmful incidents.

Permitted event classes will include:

**Incident:** realized adverse consequence associated with an AI-enabled system.

**Hazard:** condition capable of producing harm where harm may not have occurred.

**Near miss:** consequential condition in which an adverse outcome was narrowly avoided.

**Successful intervention:** condition in which a control or human intervention demonstrably altered an undesirable trajectory.

**Controlled evaluation:** structured test, experiment, red-team exercise, field test, or other evaluation that produces evidence about control behavior.

These classes must remain analytically distinguishable.

Incident-only research may identify patterns among failures. It cannot by itself establish the effectiveness of a control because cases in which the control succeeds are systematically absent.

## 7. Control Model

Controls will be classified by function before their operating state is assessed.

Initial control classes are:

**Preventive controls:** prevent an unauthorized or unsafe condition from arising.

**Detective controls:** identify specified behavior, conditions, deviations, or failures.

**Restrictive or corrective controls:** constrain, interrupt, redirect, rollback, or otherwise alter system behavior.

**Recovery controls:** restore an acceptable state or mitigate consequences after failure.

**Authorization and governance controls:** determine whether actions, deployments, changes, escalations, or decisions may proceed and who possesses authority over them.

**Human oversight controls:** allocate observation, evaluation, intervention, override, escalation, appeal, or decision authority to human actors.

A control will not be forced into a universal runtime sequence.

Instead, applicable dimensions will include:

- control objective;
- risk addressed;
- design adequacy;
- evidence of implementation;
- evidence of operation during the relevant period;
- relevant triggering condition or decision point;
- action produced by the control;
- authority responsible for the action;
- observable effect on the system or decision;
- evidence of outcome mitigation;
- unresolved uncertainty.

## 8. Human Control

The mere presence of a human does not establish meaningful human control.

Human-control observations will initially examine:

- formal authority;
- information available;
- observability of relevant system behavior;
- time available to evaluate or intervene;
- technical permission to act;
- institutional permission to act;
- availability of alternatives;
- ability to pause, redirect, reject, override, or escalate;
- intervention attempted;
- system response;
- whether intervention affected the eventual trajectory or decision.

Derived measures of practical human control will not be introduced into the canonical corpus until their reliability and validity have been evaluated independently.

## 9. Evidence Model

Evidence will be represented as individual provenance-bearing objects rather than collapsed immediately into a single confidence score.

Evidence dimensions will include:

**Directness:** proximity of the evidence to the claimed system event or control operation.

**Independence:** whether the evidence provides an independent observation or derives from another cited source.

**Traceability:** ability to identify the origin and transformation history of the evidence.

**Temporal proximity:** relationship between the evidence and the time of the event.

**Specificity:** degree to which the evidence addresses the exact control, system behavior, or decision under examination.

**Consistency:** agreement or conflict with other available evidence.

**Completeness:** extent to which evidence needed to evaluate the claim is available.

A composite evidence score may be developed later. Raw dimensions must be retained even if a derived score is introduced.

## 10. Source Dependence

Multiple publications will not be treated automatically as independent corroboration.

The corpus will maintain a provenance graph identifying relationships such as:

original technical artifact → institutional statement → news report → incident database → derived classification → Node & Norm annotation.

Sources that ultimately derive from the same original assertion must be represented as dependent evidence.

The number of sources supporting a claim will therefore never serve as a substitute for source independence.

## 11. Source Hierarchy

Sources will be classified by their evidentiary role rather than publisher prestige alone.

Relevant source classes may include:

- operational logs and traces;
- configuration and audit records;
- reproducible technical evidence;
- court records;
- regulatory findings;
- government investigations;
- independent technical investigations;
- peer-reviewed empirical research;
- institutional disclosures;
- system and model documentation;
- credible investigative reporting;
- incident-database records;
- secondary reporting;
- first-person accounts;
- unverified public assertions.

The codebook will define how each source class may support particular claims.

No source category will automatically determine the truth of a claim.

## 12. Temporal Provenance

Understanding of an event may change as evidence becomes available.

The corpus will preserve historical state rather than overwrite earlier records.

Claims and evidence objects should support fields equivalent to:

`source_date`  
`retrieved_at`  
`valid_from`  
`supersedes`  
`correction_of`  
`evidentiary_status`

Possible evidentiary statuses include:

`alleged`  
`preliminary`  
`corroborated`  
`investigated`  
`adjudicated`  
`disputed`  
`corrected`

## 13. Missingness and Uncertainty

Unknown information is a research result.

Canonical categorical fields should support states appropriate to the construct, including:

`yes`  
`no`  
`partial`  
`conflicting`  
`unknown`  
`not_observable`  
`not_reported`  
`not_applicable`

The codebook must distinguish missing evidence from affirmative evidence of absence.

Researchers must record material disagreement among sources rather than resolving uncertainty implicitly.

## 14. Sampling Strategy

The initial corpus will begin with a structured candidate population assembled from recognized AI incident, hazard, vulnerability, and evaluation sources.

External identifiers will be preserved.

Duplicate or derivative records will be linked rather than treated as separate events.

The first empirical study will use a two-stage design.

### Stage A: Evidence-Availability Cohort

A stratified sample of publicly documented AI incidents will be selected according to predetermined rules.

This cohort will measure how much control-relevant evidence survives in ordinary public incident records.

Cases will not be excluded merely because control evidence is incomplete.

### Stage B: Control-Analysis Cohort

Cases meeting a predetermined evidentiary threshold will undergo deeper control analysis.

The relationship between Stage A and Stage B will remain visible so that selection into the richer evidentiary sample cannot be mistaken for population representativeness.

Sampling strata may include domain, system type, harm class, degree of autonomy, control type, and deployment context.

The final sampling procedure will be frozen before substantive analysis.

## 15. Prohibited Inferences

The corpus will not infer system risk from raw incident counts.

It will not rank organizations by safety using incident frequency without a defensible exposure denominator.

It will not treat absence of reported harm as evidence that a control is effective.

It will not infer causation from retrospective association alone.

It will not treat documentation of a policy as evidence of operating effectiveness.

It will not treat nominal human presence as evidence of practical human control.

It will not treat multiple derivative reports as independent corroboration.

## 16. Annotation Protocol

A pilot set will be coded before the main corpus.

Pilot coding will be used to identify ambiguous constructs, revise definitions, and determine whether proposed variables can be applied reproducibly.

Following the pilot, the codebook for the primary study will be version-frozen.

A predetermined portion of the corpus will be independently double-coded.

Disagreement will be preserved using separate fields for:

`coder_a_value`  
`coder_b_value`  
`adjudicated_value`  
`adjudication_reason`

Appropriate inter-rater reliability statistics will be reported according to the measurement level and structure of each construct.

Low reliability will be treated as evidence about the measurement model, not merely as annotator error.

## 17. Use of Artificial Intelligence in Research

AI systems may assist with:

- source discovery;
- document triage;
- entity resolution;
- candidate extraction;
- duplicate detection;
- taxonomy suggestions;
- formatting;
- schema validation; and
- reproducibility checks.

AI-generated classifications must be identifiable.

For variables supporting primary published findings, authoritative annotations in the initial research releases will require human review.

An AI system will not be presented as an independent human coder when calculating human inter-rater reliability.

Prompts, models, versions, and material AI-assisted research procedures will be documented where they may affect reproducibility or interpretation.

## 18. Ethics and Affected Persons

The corpus will minimize unnecessary personal information.

Individual identities will be retained only when necessary to understand the event, establish provenance, or accurately represent the public record.

Sensitive characteristics will not be inferred from indirect evidence.

Researchers will distinguish allegations from established findings.

Records involving vulnerable populations require heightened attention to minimization, context, and potential downstream harm.

A documented corrections and dispute process will allow material factual errors to be reviewed without permitting interested parties to erase supported findings.

## 19. Licensing and Redistribution

Every upstream dataset and source will receive a rights record describing:

- license;
- attribution requirements;
- redistribution permissions;
- derivative-data permissions;
- material restrictions;
- source URL or identifier; and
- retrieval date.

The corpus will distinguish Node & Norm annotations from third-party content.

Public accessibility will never be assumed to imply redistribution rights.

## 20. Reproducibility and Release

The GitHub repository will serve as the active research environment.

Machine-readable releases should support open, documented formats such as JSONL and Parquet alongside explicit schemas.

Dataset metadata should follow appropriate open-data standards.

Substantive releases should be archived immutably and assigned persistent identifiers.

Every published analysis must identify the exact corpus and schema version used.

The public Node & Norm website will present research records and findings but will not serve as the canonical research database.

## 21. Release Gate

A corpus release is not complete because a target number of records has been collected.

Release requires satisfactory completion of:

- schema validation;
- provenance validation;
- duplicate and source-dependence review;
- annotation-quality review;
- inter-rater reliability analysis where applicable;
- licensing and redistribution review;
- ethics review;
- unresolved-case review;
- reproducibility checks;
- documentation of known limitations;
- dataset documentation;
- changelog;
- machine-readable export validation.

Material failures at these gates must block release or be explicitly disclosed as unresolved limitations.

## 22. Research Integrity

Research questions, constructs, sampling decisions, and analytical rules must not be changed silently after results are known.

Where appropriate, confirmatory studies will be preregistered.

Exploratory findings must be identified as exploratory.

Negative results must be retained.

Hypotheses that fail will be reported as failures rather than reframed after analysis.

Corrections will be versioned publicly.

Node & Norm will apply to its own research the same evidentiary standards it asks institutions to apply to AI systems.

## 23. Scope of the First Study

The first study will primarily investigate **evidentiary observability of AI controls following documented incidents**.

It will not claim to establish population-level control effectiveness from incident data alone.


