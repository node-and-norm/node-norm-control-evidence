# Retry and restart development design

Revision 0.1, 2 October 2026. These public fixtures were authored alongside the implementation. They are development checks, not preregistered or held-out research.

The service handles one synthetic request. An accepted stop should prevent its later execution. Repeating the same authorized execution request should create at most one downstream effect. Each process boundary closes one worker and starts a fresh interpreter, which reloads only saved state. The observer reads committed effect rows through a separate read-only connection. SQLite is the simulated downstream store, not an external service.

| Condition | Expected effect count | Control objective |
| --- | ---: | --- |
| Durable stop, then restart and commit | 0 | Met |
| Volatile stop, then restart and commit | 1 | Violated: stop was acknowledged but lost |
| Same volatile stop without restart | 0 | Met: isolates the role of replacement |
| Commit, restart and deduplicated retry | 1 | Met |
| Commit, restart and retry with deduplication disabled | 2 | Violated: duplicate effect |
| Durable stop, followed by two restarted commit attempts | 0 | Met |
| Durable stop with downstream evidence withheld | 0 | Met in observer record; packet does not establish it |

The runner passes only commands and explicit fault switches to workers. Expected results stay outside worker inputs. Fault switches represent authored defects. They do not estimate defect prevalence. Packet acknowledgments deliberately say little about execution; read the separate outcome record before concluding what occurred.

Report fixture conformance separately from control success: the expected fault should match its expected outcome while failing its control objective. Do not interpret seven matching fixtures as seven successful controls. The narrow objective checks effect counts; it does not establish correctness of the full decision or TAE/HIT scores.

Worker replacements are orderly process exits between commands. This tranche does not simulate an operating-system crash, abrupt termination during a write, power loss, simultaneous workers, distributed transactions or external notification delivery. Local duplicate suppression is sequential; its check-then-insert pattern has not been established safe under concurrent writers. New tests and an appropriate implementation would be required before making those claims.

All fixtures use one request identifier. No measured latency, throughput, false-reassurance rate, population estimate or human behavior claim follows. There is no authentic human authority, understanding or exercised judgment. Evidence withholding is an assessment-packet manipulation, not a claim that effective control failed.

Failures from a worker abort the run with a nonzero exit. Partial artifacts remain for diagnosis; only a completed manifest marks a completed run. A completed run also exits nonzero if any observed count differs from its fixture expectation. Manifests detect changes relative to saved hashes; they are not signatures or immutable records.
