# Research sandbox checkpoint, 2 October 2026

## Completed

Current TAE/HIT revisions verified; eight method references pinned and hashed. HIT specification, schema, handbook, catalog and replication boundaries reviewed. Synthetic application and actor boundaries documented. Three incident candidates screened, with source posture and limitations preserved.

The nine-case basic rehearsal runs in a pinned Linux arm64 container through Colima. The recorded environment passed eight configuration checks and ten runtime restriction probes. Original nine outcomes matched the local rehearsal.

NIST-MAPPING.md revision 0.1 ties six selected AI RMF 1.0 provisions to study questions and outstanding evidence. The January 2023 PDF is archived locally; its source URL and digest are published. This is an author-created contextual mapping; no provision is marked satisfied.

Seven additional retry/restart fixtures are implemented and verified locally and in the same restricted container. Five met their control objective. Two deliberately faulty cases exposed lost stop state and duplicate execution. All seven matched expected outcomes. Seven assessment packets and the outcome report matched across environments; twenty-one artifacts in each run verified against their manifests. All nineteen verification tests passed locally and in the container.

New records: runs/recovery-001; container-runs/recovery-001; container-runs/isolated-tests-002. Source snapshots and fixture definitions accompany outcomes. RECOVERY-DESIGN.md explains the comparisons and limits.

## Environment

Colima 0.9.1, Docker client 29.2.1 and Lima 2.0.3. The dedicated profile uses two CPUs and 2 GiB memory while running. No login startup service was enabled and the default Docker context was not replaced. The VM is stopped after verification; its image and records are preserved. ENVIRONMENT.md holds restart instructions and the image digest.

Restrictions are demonstrated for authored code and the recorded configuration, not general adversarial escape resistance. Worker replacement is orderly process exit and reload, not abrupt machine failure or distributed application execution.

## Research boundaries

All sixteen cases are public development fixtures. No held-out study, TAE/HIT scoring, human-judgment validation, independent review, formal regulatory participation, empirical publication or production integration has occurred. This package publishes development code, documentation and records only. Existing TAE/HIT workstreams remain unchanged.

Rite Aid/AIID 619 is retained for source-informed test design with FTC allegations labeled. Tempe is a boundary reference. Air Canada is deferred. FTC PDF text was reviewed through the browser, but direct archiving returned HTTP 403; no complete frozen incident packet is claimed.

No Hugging Face dataset, hosted model or LangChain application has been evaluated. These remain a later, justified application layer with provenance, licensing and an admission boundary. Current source connections supply test-design context, not behavioral outcome data.

## Next gates

1. Complete source packets and prospective assessment admissibility; synthetic permission does not establish human authority.
2. Define how a permitted assessment should distinguish justified findings, false reassurance and unresolved evidence. Do not derive these classifications from the simulator's hidden answer key.
3. Design new held-out case families, separate assessor access from outcome access and freeze the study protocol before evaluation.
4. Add concurrency, interrupted writes or external-service integration only with explicit new objectives and failure models.

High reasoning is appropriate for source and contract decisions. Medium is sufficient for implementation against settled acceptance rules. Additional model review does not constitute independent validation.
