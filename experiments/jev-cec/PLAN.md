# Jev and CEC: preparation decision, 3 October 2026

Jev is a candidate for proposing evidence classifications that a researcher can inspect. The first CEC task is to distinguish a recorded action, its downstream propagation and mitigation of consequences. These are separate propositions in the existing codebook. A model response remains an AI proposal, even when its confidence is high.

## Relationship to the existing research

CEC preserves dated sources, locators, source dependence, missingness and separate judgments. TAE and HIT own their respective methods and derived assessments. The [shared sandbox](../us-control-sandbox/README.md) supplies scripted development records, and its recent trace exercise measures explanation coverage under shared rules. It does not establish whether a model can read documentary evidence correctly.

The TAE [research status](https://github.com/node-and-norm/trust-autonomy-evidence/blob/main/RESEARCH_STATUS.md) and [Jev guide](https://github.com/node-and-norm/trust-autonomy-evidence/blob/main/docs/jev-experiments.md), inspected in the local TAE checkout on this date, record live synthetic experiments and a later collaborative review. Reuse their handling of version identity, invalid responses, raw probabilities, exposure and preserved disagreement. Their five-class assessment labels and results do not transfer to CEC's eight evidence classes. TAE work remains at its existing stopping point.

## Bounded implementation now

`prepare.py` validates the three existing public synthetic demonstrations and prepares one request per packet, with three Choice questions. It preserves the predefined control period, located observations and linked source-family metadata. It excludes rating objects, adjudication, source-claim objects, event titles, quality ratings and omission commentary. Input and request hashes are separate. The original input is saved for local inspection alongside the request; only the request would enter a future API call.

This projection tests a predefined control scope. It cannot test independent control enumeration. Evidence consists of already interpreted synthetic observations, not raw operational logs or an untouched documentary sample. Wording may make the intended distinction easy. All three examples are public and author-exposed; the nine questions are dependent development checks, not nine independent cases.

The preparation command has no network client, credentials, live mode, evaluator or corpus-write operation. It does not claim a Jev connection has been tested. Its manifest records zero requests sent and an unknown resolved model. The selected candidate model is `jev-1.13.0`, as listed by TypeSafe on this date.

## Proposed next experiment

The research question is whether model proposals preserve evidence boundaries when the supplied wording supports different states. A useful challenge set would include:

| Condition | Distinction to test |
| :--- | :--- |
| Policy only | Assigned authority does not establish an attempted action |
| Command without downstream record | Missing propagation evidence does not establish failure |
| Command and downstream acknowledgement | Recorded propagation leaves mitigation separately assessable |
| Affirmative downstream failure | Contrary evidence differs from silence |
| Incompatible accounts | Conflict remains visible |
| Multiple reports with one origin | Repetition does not establish independent confirmation |
| Record about another time or component | Scope mismatch limits support |
| Withheld record versus no mention | Access barriers differ from packet silence |

These rows are a proposed construction plan. No new challenge cases or expected classifications have been frozen. Review the draft [support rubric](../../research/pilot/SUPPORT_RUBRIC.md) alongside the [codebook](../../docs/methods/CODEBOOK.md) before constructing that set. Support judgments and control-state classes answer different questions and must remain separate.

Before a live CEC experiment, record a versioned question set and reference key, construction exposure, invalid-response rules, model/SDK versions, request count, repetitions, cost cap and handling of service failures. Keep all attempts; do not silently normalize invalid distributions or retry until a preferred answer appears. The prior TAE probability-sum failures make this a concrete implementation requirement. Preserve valid-response coverage alongside class agreement and confusion counts. Keep evidence uncertainty separate from model probability and service failure.

A separate, later comparison can test whether displaying proposals improves a person's review. It needs actual measured burden and preserved unaided judgments before exposure. CEC's original pilot still requires eligible independent humans; this preparation closes none of its ten open protocol decisions. Solo AI-assisted development is possible while those research gates remain open.

## What would justify continued use

Proceed if the model can be evaluated on a bounded semantic task with a reviewable reference and retained failure cases. Stop or revise if it repeatedly converts silence into failure, treats acknowledgement as remedy, or adds more review burden than its proposals justify. No numerical acceptance threshold has been chosen, and no performance claim follows from preparing valid requests.

A source-selection experiment could later ask Jev to rank candidate passages. Deterministic code would still resolve IDs and hashes. Candidate coverage would need testing, because a model cannot select omitted evidence. Neither selection nor classification authenticates a source or independently validates a control.

## Provider basis and disclosure

Official documentation consulted on 3 October 2026: [Choice](https://docs.typesafe.ai/primitives/choice), [citation-checking pattern](https://docs.typesafe.ai/cookbooks/citation_check), [models](https://docs.typesafe.ai/models), [confidence](https://docs.typesafe.ai/confidence), and [Python client](https://docs.typesafe.ai/sdk/python/api/clients/sync). Choice returns labels, distributions and confidence; it does not supply a narrative rationale. The citation cookbook's demonstration and automatic-acceptance threshold are not CEC validation and are not adopted here.

Codex prepared the code, questions and this decision with AI assistance. There has been no independent methodological review of this CEC extension, no live CEC Jev call, no human rating, no change to canonical annotations, and no empirical release.
