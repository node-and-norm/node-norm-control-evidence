# Pressure-test findings and decisions

Status: AI-assisted methodological review, 2026-09-14. This continues the preliminary seven-area screen in NOVELTY_REVIEW.md. It does not constitute independent scientific validation or an exhaustive novelty determination.

## What has been tested

The initial review covered AI control effectiveness, incident evidence, meaningful oversight, assurance cases, sociotechnical incident analysis, audit evidence, and post-incident observability. The repository also passed 16 software tests, including rejection of several invalid research-data states. Those checks establish behavior of the development implementation. They provide no evidence that humans can apply its constructs reliably.

This continuation inspected additional methods and limitations in four close works. Access failures and exact sections are recorded below. Full-text access does not mean every claim or citation in a paper has been independently verified.

## Closest-work findings

### Post-Deployment Accountability, Mumtaz et al., v3

Inspected PDF sections 3.1–3.3, 8–9, and Data & Code Availability, printed pages 6–8 and 19–20 (PDF indices 5–7 and 18–19). The method codes 480 incidents against nine provisions, includes insufficient evidence, and assesses applicability. Section 3.3 explicitly separates missing public documentation from noncompliance. Expert-ground-truth benchmarking remains future work in section 9. The availability statement links AIID; study-specific executable materials were not located in the inspected statement. Their existence elsewhere remains unresolved.

CEC cannot claim that evidence-aware post-deployment coding is new. Its candidate distinction is the validated event-control reconstruction procedure and its reusable provenance record. [Versioned PDF](https://arxiv.org/pdf/2605.16281v3).

### AI Forensics, Dehghantanha and Homayoun, v1

Inspected sections 3–4, especially 4.2–4.4. The paper explicitly connects investigator access, preservation, model-version attestation, reconstruction, and uncertainty. These are substantive overlaps with CEC. CEC should record access conditions and distinguish a metadata hash from custody of original evidence. The proposed corpus-level independent-coding study remains a candidate extension; absence of an equivalent dataset has not been established. [Versioned HTML](https://arxiv.org/html/2608.03520v1).

### From Incidents to Insights, Richards, Benn, and Zilka, v1

Inspected sections 3.1–3.2.4. The study analyzes 962 incidents and examines responses in 48 incidents through 638 associated reports. Two authors label harmed groups and cross-check consistency. The method explicitly limits inference to the observed database and explains why report counts reflect collection effort. Author cross-checking is not the external, blinded coding proposed for CEC, but multiple-person incident coding is already present in this literature. [Versioned HTML](https://arxiv.org/html/2505.04291v1).

### Lessons for Editors, Paeth et al., v1

Inspected the editorial-challenges sections on temporal ambiguity, multiplicity, and epistemic uncertainty. They identify difficulties defining event boundaries and recovering system details, including irretrievable records. CEC must measure disagreement in event and control enumeration before computing agreement on dimension values. This inspected 2024 preprint is distinct from the 2025 publisher version; their equivalence has not been checked. [Versioned HTML](https://arxiv.org/html/2409.16425v1).

## Retrieval limits

The accountability paper's HTML returned 404, but PDF text was accessible. Attempts to render three relevant pages through the web screenshot service returned cache errors. Findings above rely on extracted prose; no figure-derived estimates are used. The Beno SSRN page remains inaccessible through the tool. The oversight publisher page was reopened, but its full methods were not established from the returned page. The IEEE schema artifact remains unresolved. These gaps prevent closure of the novelty review.

## Adversarial assessment of CEC

| Challenge | Current finding | Required response |
| --- | --- | --- |
| Is this another annotation layer with familiar fields? | Plausible. Architecture alone cannot establish added research value. | Compare reviewer performance against simpler records using the same source packets. |
| Does more primary-source retrieval merely create more observable cases? | Retrieval effort can change the outcome being measured. | Separate representation effects from evidence-enrichment effects. |
| Can coders agree only because someone already chose the controls for them? | Current dimension agreement would miss that disagreement. | Independently enumerate controls and evaluate matching before dimension coding. |
| Do many controls in one event inflate precision? | Shared events and source families induce dependence. | Freeze event weighting, clustering, and sensitivity analyses. |
| Can a hash prove independent coding or an untouched holdout? | No. It establishes an integrity commitment to supplied content. | Require custody and access records plus attributable human attestations. |
| Are missingness categories consistently distinguishable? | Unknown. No empirical coding has occurred. | Test category confusions and retain failed constructs. |
| Can upstream uncertainty disappear in a downstream score? | The integration contract prohibits this, but production adapters are unfinished. | Audit downstream projections before empirical distribution. |

## Decision

Continue the research program under the existing Charter and Agenda. Keep novelty, reliability, criterion validity, and population-effectiveness claims closed. The next evidentiary contribution is a comparative pilot with independently assessed reconstruction quality and coding burden. A useful negative result would show that a simpler record performs equally well, or that the proposed distinctions cannot be applied consistently.
