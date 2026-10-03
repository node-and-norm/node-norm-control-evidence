# CEC documentary challenge v1

[Preparation decision](../PLAN.md) / Challenge set

Twelve invented packets ask whether the supplied record establishes an action, its downstream propagation and a bounded mitigation. The [cards](cards.json) contain evidence only; the [reference key](reference-key.json) separately records 36 AI-authored expectations, rationales and locators. There are no model responses.

## Construction and interpretation

The 3 October 2026 preparation decision preceded this construction. Codex authored the cards and key together from CEC codebook 0.1.0, before any CEC Jev inference. The key was inspected for consistency with that codebook; no eligible independent human review occurred. The freeze commits to exact bytes after construction. It is internal version control, not independent preregistration or hidden holdout custody.

All events, timestamps, amounts, sources and records are invented. They are narrative representations of records, not outputs of newly executed systems. Every case uses a predefined control objective, opportunity and period. Evidence passages can make the intended classification explicit. IDs are local bookkeeping; repeated IDs across packets do not indicate a shared real event.

The first ten cards share a stop-command setting. The final two share a fee-refund setting. Do not treat twelve cards or 36 questions as independent observations from a population. No legal, behavioral, regulatory or institutional effectiveness claim is authorized.

| Card | Condition | Main distinction |
| :--- | :--- | :--- |
| C01 | Permission in policy | A role declaration leaves actions unreported |
| C02 | Console command | Sending leaves downstream receipt unreported |
| C03 | Matching acknowledgement | Propagation leaves mitigation separately assessable |
| C04 | Explicitly discarded request | Non-delivery has affirmative evidence |
| C05 | Incompatible worker exports | Conflict stays unresolved |
| C06 | Three reports, one origin | Repetition adds no receipt evidence |
| C07 | Different job, worker and date | Evidence must match the target scope |
| C08 | Withheld receipt records | A documented access barrier differs from silence |
| C09 | Unreadable linkage fields | Existing evidence can leave identity ambiguous |
| C10 | Two intended recipients, one receipt | An identified subset supports a partial conclusion |
| C11 | Refund linked to a posted credit | Mitigation is bounded to reversal of the named fee |
| C12 | Receipt followed by rejected refund | Propagation can coexist with absent remedy |

Seven of the eight codebook values occur in the authored key. `not_applicable` remains available in the questions but has no reference instance. Class coverage is uneven, particularly for mitigation. Report that limitation in any later evaluation. The repeated-source case tests resistance to overclaiming receipt, not successful inference of source dependence as a separate construct. There is no independent source-lineage performance measure.

## Reproduce requests without inference

From the repository root:

```sh
python experiments/jev-cec/challenge.py check
python experiments/jev-cec/challenge.py prepare --output build/cec-challenge-v1
```

Preparation verifies the freeze, validates card structure and copies only each card's state into a request alongside the frozen questions. It saves the packet ID outside the API payload, hashes each request and refuses to overwrite a folder. The answer key and condition names never enter requests. Verifying their hashes reads those files locally; it is not a blinding mechanism. All material is public and author-exposed.

The pinned candidate model and question wording are unchanged from the earlier preparation. No live client, automatic acceptance rule, result evaluator or corpus annotation writer is introduced. No API credentials are read. `requests_sent` remains zero.

## Review before inference

The next step is a versioned execution protocol and response-validation implementation, with an explicit request/repetition budget, maximum cost, SDK version, service-failure accounting and invalid-probability rules. That step must precede live CEC calls. Any challenge correction receives a successor version and an explanation; preserve this version and its key.

A disagreement can expose a model error, wording defect, construct ambiguity or reference error. Preserve the original response and reference, then record review separately. Never revise the key to improve an observed agreement rate. CEC's four documentary-support rubric values remain a separate assessment from these eight control-state values. None of the ten original pilot decisions is closed by this package.
