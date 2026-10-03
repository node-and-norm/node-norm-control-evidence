# Four-question runner checkpoint

The separate v2 runner implements the [contract](PROTOCOL.md) for 90 requests and 360 scheduled determinations. It defaults to an in-memory mock service with uniform probabilities; mock agreement is plumbing arithmetic, not a model finding.

```sh
python experiments/jev-cec/execution-v2/v2_run.py --output build/cec-v2-mock
```

The output directory must be new. It contains the complete schedule, exact request/response bytes, attempts, code and input snapshots, metadata, report and a hash manifest. `v2_run.verify(Path(...))` checks the exact artifact set. The [freeze](freeze.json) covers the files listed by `v2_inputs.FILES`, including the experimental standard and normalized reference. The original v1 files and releases remain unchanged.

The report uses four-answer request-level acceptance, full coverage denominators, per-pass confusion counts and Brier sums, complete-triplet exclusions and paired contrasts. An invalid member makes the paired contrast unavailable. The intentional V2-14-B/V2-15-A duplicate is identified; the set has 29 unique packet states. There is no independent accuracy or generalization claim.

## Live gate

Live mode requires a clean committed checkout, unchanged frozen sources, an existing private credential supplied through `TYPESAFE_API_KEY`, and a JSON preflight checked on the execution date. Required fields are `checked_date_utc`, `input_usd_per_million` (string `0.042`), `output_usd_per_million` (string `0`), `request_token_limit` (64000), `max_requests` (90) and `max_usd` (string `1`). These values are an implementation compatibility condition, not a current provider-price assertion. Save the official pricing/limit evidence separately before execution; do not manufacture the attestation from this guide.

A changed price, limit or model requires amendment before dispatch. The client reserves a maximum-request input charge against the USD 1 ceiling, stops on unknown usage and never retries. The ceiling is not a provider-enforced account limit. This checkpoint makes no live request.

## Interpretation and next gate

Normalized reference values come from the exposed review and prevention proposals under standard 001. Frozen values remain contestable; a freeze preserves the comparison rather than validating it. The missingness and applicability decisions remain experimental. Human review requirements are still open.

Review the saved mock accounting and source hashes, recheck official service availability and prices, then run a separately identified live archive under the fixed contract. Preserve all failures and keep the first pass primary. Any subsequent amendment must keep this source freeze and earlier outputs recoverable in Git history.

## Preserved rehearsal

[mock-001](mock-001/manifest.json) was produced from clean implementation commit `758ea7c` with zero live requests. All 90 mock responses passed, and a repository test reproduces the report exactly from preserved response bytes and reference. This confirms mechanical accounting only. The uniform mock service does not assess the evidence or consult the key.

Archived source Markdown retains its original relative links for byte fidelity. It is excluded from repository navigation checks; use the current source tree for navigation. The archive reproduction test verifies all saved source hashes.
