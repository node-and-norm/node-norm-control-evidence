# Trace-quality stress evaluation: stress-001

2 October 2026. The full trace exposed three more material blockers than the short checklist across twelve authored packets, while producing 1,468 additional UTF-8 bytes. Their labels agreed on every valid packet. These observations quantify the shared procedures' output design; they do not establish improved assessment, independent validity or a human reading benefit.

## Recorded comparison

| Measure | Checklist | Full trace |
| --- | ---: | ---: |
| Valid packets processed | 12 | 12 |
| Deliberate invalid inputs rejected | 3 | 3 |
| Material blockers correctly represented | 9 / 12 | 12 / 12 |
| Incorrect check assertions | 0 / 24 | 0 / 36 |
| Locator errors | 0 / 27 | 0 / 39 |
| Check entries emitted | 24 | 36 |
| Dependent, unassessable conditions listed as blockers | 0 | 2 |
| Compact, sorted-key JSON output bytes | 8,035 | 9,503 |

The three omitted blockers occurred in the combined-gap stratum. Each checklist response stopped at its first unresolved condition. This is permitted by its declared design, not a violation of the checklist contract. The trace listed subsequent conditions. Two of its blocker labels referred to dependent unknowns; their explicit state remained null, and the audit did not count them as independent material failures.

Both procedures produced one supported-effect response, two supported-fault responses and nine unresolved responses. Labels matched the author-written reference key. The [machine report](runs/stress-001/report.json) retains all six label measures and their denominators. Those matches do not establish independent accuracy: the key and procedures share the same known contract and author exposure.

## Provenance and exposure

The initial plan and metric implementation were committed at `829b3ab9db651410a5f167483b8d5aa667fec518` before packet construction. The authored inputs, key, runner, tests and pre-run locator clarification were committed at `d51312ed463c8c47874ef0170873a2a947961907` before evaluation. The plan records the clarification; it was not introduced after seeing results.

The runner saved both procedures' outputs before opening the key. The author already knew the constructed records and expected states. Both the code and eventual public repository allow access to the key, so no independent blinding or access-control guarantee is claimed.

All fifteen units remain in the intake accounting. The malformed digest, unsupported scope and inconsistent-count inputs were rejected as planned. There were no unexpected intake results and no post-response exclusions or replacement cases. The full record contains inputs, the separate key, original responses, report and eight source/plan snapshots; its manifest covers twelve artifacts.

No new system execution generated these records. They are packet-level stress compositions and controls using already exposed mechanisms. The three identity variants are related, and the control stratum overlaps development examples. Treating twelve rows as twelve independent case families would overstate the evidence.

## What this supports

The complete trace exposes later blockers that a short explanation omits. It also emits more checks and more bytes. The result supports retaining both forms as inspectable development artifacts. It does not show that full traces should replace the checklist, save reviewer time, improve judgments or improve human control. No cost-benefit threshold or superiority claim is added after observing the counts.

The auditor checked reference states and prescribed locator sets without calling the procedures to derive expected values. That separation can catch implementation disagreement but is not independent methodological review. It did not judge the full semantic adequacy of free-form reasoning, authenticate the evidence, or validate the author-written key.

## Reproduction and next research decision

From the sandbox directory:

```sh
python3 -B verify_run.py trace-evaluation/runs/stress-001
python3 -B run_trace_evaluation.py --output build/trace-repeat-new --plan-commit 829b3ab9db651410a5f167483b8d5aa667fec518 --implementation-commit d51312ed463c8c47874ef0170873a2a947961907
```

The second command reruns the exposed set and requires a fresh folder. Commit arguments describe the original plan and pre-run checkpoint; source snapshots identify the bytes actually executed. A repeat is not a new independent study.

Before expanding the set, decide which larger claim merits testing. A bounded next option is a separately reviewed evidence-sufficiency key with more realistic linked records and conflicting record classes. A claim about reader usefulness requires an appropriate reader study; a model-based comparison requires its own model, prompt, access, repetition and cost plan. TAE/HIT findings remain disabled, and the original methods' research gates remain intact.
