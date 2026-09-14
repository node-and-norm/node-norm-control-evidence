# Node & Norm Control Evidence Research Agenda

**Status:** Foundational research agenda  
**Program:** Node & Norm AI Assurance & Evaluation Lab  
**Research infrastructure:** Node & Norm Control Evidence Corpus  
**Planned repository:** `node-norm-control-evidence`

## Research Position

Node & Norm studies the gap between declared AI governance and demonstrated control.

Its empirical research asks whether available evidence can establish that a technical, organizational, or human control had practical force in a consequential AI-mediated event.

The research does not assume that policies, safeguards, approval gates, human reviewers, monitoring systems, or override mechanisms function merely because they are documented.

It asks what the evidence permits an independent reviewer to establish.

## Core Research Question

> Can an independent reviewer reconstruct whether an AI governance control had practical force from the evidence that survives a consequential event?

“Practical force” concerns whether the control was capable of affecting the relevant system state, action, decision, or consequence under the conditions that actually existed.

## Primary Contribution Hypothesis

The proposed contribution is not a new AI risk taxonomy, incident database, control catalog, audit framework, or theory of human oversight.

The contribution to be tested is a reproducible method and empirical corpus for reconstructing AI control operation from heterogeneous public evidence while preserving:

- source provenance and dependence;
- distinctions among claims, evidence, annotation, and inference;
- uncertainty and missingness;
- practical human authority;
- temporal relationships among events and interventions;
- control-specific operating conditions; and
- limits on the conclusions the evidence can support.

This remains a novelty hypothesis until the formal literature review is complete.

## Unit of Analysis

The primary analytical unit is the **event-control observation**.

A single event may contain several distinct control opportunities.

For example, one event may involve:

- an authorization control;
- a monitoring control;
- an automated restriction;
- a human approval gate;
- an escalation mechanism; and
- a recovery process.

Each control must be assessed separately.

The architecture is therefore:

**Event → Control Opportunity → Evidence Items → Claims → Annotations → Adjudicated Inference**

## Evidence Architecture

The research separates four epistemic layers.

**World state:** what actually happened.

**Evidence state:** what surviving records reveal.

**Annotation state:** what researchers code from those records.

**Inference state:** what the research protocol permits researchers to conclude.

The world state may remain unknown.

A missing record must never be transformed silently into a finding that a control was absent.

## Program I: Public Observability of AI Control Operation

The first empirical program will examine publicly documented AI incidents and hazards.

Its central question is:

> How often does the public record permit an independent researcher to resolve whether a relevant AI control was implemented, operating, capable of intervention, and consequential to the observed trajectory?

The initial study will measure observability rather than population-level control effectiveness.

Primary outcomes will include the proportion of event-control observations for which researchers can resolve:

- implementation;
- operation at the relevant time;
- triggering condition;
- intervention or control action;
- downstream propagation;
- effect on the trajectory;
- practical human authority where applicable; and
- evidentiary sufficiency for each conclusion.

No aggregate “trust score” will be assumed.

## Program II: Practical Human Control

Human oversight will be treated as an empirically testable system condition.

The research will examine whether designated humans possessed:

- relevant information;
- adequate comprehension opportunity;
- formal authority;
- practical authority;
- sufficient intervention time;
- technical permission;
- institutional permission;
- viable alternatives;
- usable intervention mechanisms; and
- downstream influence over execution.

This program will provide an external empirical substrate for Human Influence Telemetry and Trust, Autonomy & Evidence.

The corpus will not import HIT or TAE conclusions as ground truth.

Overlapping cases must be coded independently where they are used for validation.

## Program III: Evidence Preservation and Post-Incident Auditability

The program will identify which evidence is systematically absent after AI incidents.

Examples include:

- system versions;
- prompts and configuration;
- tool-call traces;
- model outputs;
- authorization state;
- timestamps;
- human-review records;
- override attempts;
- escalation records;
- downstream execution state;
- corrective actions; and
- evidence showing whether a control changed the outcome.

This research can support a later minimum evidence-preservation specification for consequential AI systems.

Such a specification must be derived from empirical missingness patterns rather than invented prospectively.

## Program IV: Prospective Validation

Retrospective public evidence cannot establish all aspects of control effectiveness.

Later research must therefore introduce controlled environments in which relevant ground truth is known.

Potential settings include:

- regulatory sandboxes;
- controlled agent evaluations;
- simulation environments;
- synthetic institutional workflows;
- red-team exercises; and
- cooperating organizational deployments.

These studies can test whether the retrospective reconstruction method identifies known control states correctly.

Prospective validation is required before claiming criterion validity.

## Corpus Development Design

Corpus development will proceed in stages.

### Development Pilot

Approximately 30 cases will be selected for codebook development.

Pilot cases may expose ambiguous definitions and motivate revisions.

They will not be treated as an untouched validation population.

All material codebook changes will be recorded.

### Frozen Main Protocol

After pilot completion:

- the research questions will be frozen;
- inclusion and exclusion rules will be frozen;
- the primary variables will be frozen;
- the coding manual will be versioned;
- the sampling procedure will be frozen;
- the primary analytical plan will be preregistered.

### Main Cohort

The target main cohort should be large enough to estimate principal descriptive quantities with useful precision while remaining feasible for deep documentary coding.

A provisional target of approximately 200 cases is appropriate for planning. Final sample size will be based on the declared primary estimands, sampling structure, expected clustering, missingness, and available coding capacity rather than an arbitrary round-number target.

### Holdout Cohort

A prespecified subset of cases will remain unavailable for construct revision.

The frozen method will be applied to this holdout without changing definitions in response to those cases.

Failure on the holdout is a research result.

## Reliability

Core observations supporting published conclusions will be independently coded by multiple human assessors.

Coders must be blind to one another's decisions before comparison.

Pre-adjudication ratings will be preserved permanently.

Reliability reporting will use statistics appropriate to each measurement scale and prevalence pattern rather than relying mechanically on one coefficient.

At minimum, reporting will retain:

- exact agreement;
- disagreement matrices;
- an appropriate chance-adjusted measure where estimable;
- adjudicated values;
- adjudication reasons; and
- construct-specific failure analysis.

Low agreement may indicate inadequate definitions rather than poor coders.

## Construct Validation

Construct development will distinguish:

**Content validity:** whether the variables capture the relevant mechanisms identified in literature and practice.

**Inter-rater reliability:** whether independent researchers can apply the definitions consistently.

**Convergent evidence:** whether independently coded findings align appropriately with related constructs from HIT, TAE, audit practice, safety engineering, or other methods.

**Discriminant evidence:** whether the method distinguishes conditions that should remain distinct, such as formal human presence and practical intervention authority.

**Criterion validity:** whether classifications match known control states in controlled or prospectively observed environments.

Criterion validity cannot be claimed from public historical reconstruction alone.

## Source Strategy

Incident databases are discovery and classification resources, not ground truth.

Candidate cases may originate from resources such as:

- AI Incident Database;
- OECD AI Incidents and Hazards Monitor;
- MIT AI Incident Tracker;
- AVID;
- regulatory databases;
- court records;
- government investigations;
- technical reports; and
- other documented sources.

Each case should then be enriched toward primary evidence wherever possible.

A database entry that derives from another database or news source does not constitute independent corroboration.

## Source Dependence

Each material source will receive provenance relationships.

Permitted relationships should include concepts equivalent to:

`primary_record`

`derived_from`

`reports_same_claim`

`independent_corroboration`

`aggregation_of`

`supersedes`

`contradicts`

`correction_of`

Evidence counts will not be interpreted as independent support until dependence has been assessed.

## Data Rights

The corpus will maintain a source-rights ledger.

Third-party source text will not be redistributed merely because it is publicly accessible.

Node & Norm will preferentially publish:

- stable external identifiers;
- bibliographic metadata;
- provenance relationships;
- researcher annotations;
- bounded quotations where legally appropriate;
- paraphrased evidentiary observations;
- derived variables; and
- links to source material.

Redistribution rules will be decided source by source.

## AI Assistance

AI may assist retrieval, deduplication, entity resolution, document triage, structured extraction, and validation.

AI-generated suggestions must remain identifiable.

Human assessors will establish the authoritative initial research labels supporting primary claims.

AI systems will not be represented as independent human raters.

A later research program may evaluate AI coding against the frozen human benchmark.

## Open Science

The project will maintain:

- versioned protocols;
- frozen research questions;
- machine-readable schemas;
- source manifests;
- annotation histories;
- preregistration where appropriate;
- analysis code;
- deterministic builds;
- claim-evidence maps;
- release manifests;
- AI-assistance records;
- authorship and contributor records;
- limitations;
- corrections;
- persistent release identifiers; and
- exact-version citation.

The public website will expose released research.

It will not become the canonical data store.

## Downstream Research Contract

TAE, HIT, RGDS, and later Node & Norm projects may consume released corpus versions.

They may create derived datasets and measures.

They may not silently alter canonical corpus records.

Every downstream analysis must identify:

- corpus release;
- schema version;
- record IDs;
- filters;
- transformations;
- additional annotations; and
- analytical code where applicable.

A construct developed downstream may enter a later canonical corpus version only after separate validation.

## Initial Publication Sequence

The first paper should address post-incident evidentiary observability.

A working research question is:

> What can public evidence establish about the operation of AI governance controls after consequential AI incidents?

A later paper should test practical human control.

A subsequent study should introduce controlled or prospective cases and evaluate whether retrospective classifications correspond to known system and control states.

Population-level claims about control effectiveness remain outside scope until an appropriate comparison design exists.

## Release Principle

Node & Norm will not reward dataset size at the expense of epistemic discipline.

A record that remains unresolved is preferable to a confident record unsupported by evidence.

A failed hypothesis is preferable to a post hoc explanation.

A smaller corpus with defensible provenance and reproducible judgments is preferable to a large corpus whose classifications cannot survive independent review.

The program succeeds only if another researcher can determine how Node & Norm reached a conclusion, reproduce the procedure, challenge the evidence, and identify precisely where reasonable disagreement remains.
