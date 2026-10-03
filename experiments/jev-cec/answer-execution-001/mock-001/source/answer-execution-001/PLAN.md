# Answer-level execution 001

This separately versioned runner implements [answer contract 001](../response-contract-001/ANSWER-CONTRACT.md) on the existing eight-position packet-linkage schedule. Question payloads, proposed references and numerical tolerance remain fixed. Original runners and archives are unchanged.

Status: implementation and mock verification only. No live execution is included. Reusing exposed packets is development work and cannot establish independent accuracy. Any future run must state this changed acceptance unit prospectively and must not substitute its results for the earlier primary comparison.

Envelope failures exclude every answer. Individual answer failures produce located reasons and raw sums; eligible siblings remain available. Request statuses distinguish valid, partial and invalid responses. The analysis reports individual eligibility and whole-response coverage separately. Action pairs require both action answers, repetition requires both passes, and unresolved references remain unscored. Each multi-dimension downstream decision must declare its dependencies and require all of them; this runner does not authorize such decisions.

The primary pass, secondary dimensions and repetition follow the packet-linkage plan. No pooled winner, probability normalization or changed tolerance is introduced. Validity reasons are diagnostic metadata, never additional evidence labels. Raw response bytes, source snapshots and allowlisted provider request IDs are retained. No authorization or unrelated response headers are stored.

The maximum is eight sequential requests, USD 1, no retries. Live mode requires a clean checkout and same-day verified pricing/limits preflight. Existing stop rules apply to transport/HTTP failures, model mismatch, unavailable usage and budget exhaustion. Source hashes bind the inherited packet design and this implementation before any dispatch.

Run the mock with `python3 experiments/jev-cec/answer-execution-001/answer_run.py --output build/answer-execution-mock`. A new output directory is required. Mock output is plumbing evidence only. No provider request should be made merely to replace an incomplete or unfavorable historical result.
