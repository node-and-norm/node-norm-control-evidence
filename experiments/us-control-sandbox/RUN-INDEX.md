# Development run index

Recorded on 2 October 2026 in America/New_York. Some engine timestamps fall on 3 October UTC. These are synthetic software executions, not independent observations of people or institutions. Repeated cases and cross-platform repeats are not additional independent samples.

| Record | What was exercised | Recorded result | Limitation |
| --- | --- | --- | --- |
| [Initial rehearsal](runs/rehearsal-001/manifest.json) | Seven in-memory conditions | 7 expected outcomes matched | Earlier implementation; no per-artifact manifest |
| [SQLite rehearsal](runs/rehearsal-002/manifest.json) | Nine stop/correction conditions | 9 expected outcomes matched | Simulated downstream store |
| [Basic container run](container-runs/isolated-001/result/manifest.json) | Same nine conditions under restrictions | 9 expected outcomes matched; JSON matched local run | Same authored fixtures |
| [Initial container tests](container-runs/isolated-tests-001/stderr.txt) | Twelve verification tests | 12 passed | Engineering checks only |
| [Isolation probes](isolation-runs/isolation-001/result.json) | Effective configuration and runtime restrictions | 8 configuration checks and 10 runtime probes passed | Not general adversarial escape resistance |
| [Local recovery run](runs/recovery-001/manifest.json) | Seven process-replacement/retry conditions | 7 expected outcomes matched; 5 control objectives met | Orderly worker replacement, no concurrent writes |
| [Container recovery run](container-runs/recovery-001/result/manifest.json) | Same seven recovery conditions | Same counts; all 8 semantic JSON files matched local output | Repeat, not new evidence about prevalence |
| [Expanded container tests](container-runs/isolated-tests-002/stderr.txt) | Nineteen verification tests | 19 passed | No validation of human judgment or TAE/HIT scores |

The recovery controls exposed the declared volatile-stop and duplicate-effect defects. Matching those expected failures is a successful fixture check while the control objective remains violated. A separate condition withholds evidence despite an effective stop. Its observer record does not authorize an assessor who lacks that record to conclude the stop worked.

Run `python3 -B verify_archive.py` from this directory to verify the five saved artifact manifests, the initial rehearsal's source hash and the expanded test suite's source snapshot hashes. The public-copy provenance manifest records editorial and path changes separately. All these hashes are change-detection aids, not signatures or proof of truth.

The original local and container records are development checkpoints. New executions must use fresh output directories and retain errors. The current protocol's complete-attempt preservation rule applies going forward; historical gaps are disclosed in [the publication record](PUBLICATION.md).

## Paired procedure demonstration

[development-001](procedure-runs/development-001/summary.json) re-presents seven previously published packets to the checklist and full-trace procedures. Their labels agree on all seven by the shared rule design. Thirteen artifacts, including input envelopes, both outputs and source snapshots, are retained under a manifest. There is no independent answer key or accuracy estimate. This adds no new study cases to the sixteen development conditions.
