# CEC Jev runner and analysis

[Execution protocol](PROTOCOL.md) / [Challenge set](../challenge-v1/README.md)

The runner implements the protocol's fixed schedule, sequential dispatch, stop rules, response validation and descriptive analysis. The protocol's earlier statement that transport was not yet implemented records its pre-implementation checkpoint; that document remains unchanged.

## Offline verification

From the repository root:

```sh
python experiments/jev-cec/run.py --mode mock --output build/cec-mock-new
python -m unittest discover -s tests -v
```

The mock always supplies a uniform eight-class distribution and chooses `unknown` at the resulting tie. It never reads the reference key. The report's arithmetic is deliberately uninformative about Jev performance. See [preserved mock report](mock-001/report.json). Its `live_requests_sent` is zero.

Tests simulate complete execution, invalid distributions, missing usage, different models, rate limits, timeouts, interruptions, budget exhaustion and altered artifacts. A substituted in-memory opener checks the official endpoint, method, request bytes, 30-second timeout and refusal to redirect. These checks do not establish live service compatibility.

## Live preflight

The live command reads `TYPESAFE_API_KEY` from the process environment. Never paste that value into research files, a command argument, a PR or chat. This implementation session found no credential in that environment. It made no live call.

Before live execution, check the provider's current price and limits against the protocol. Create a local JSON preflight with the current UTC check date and these exact fields:

```json
{
  "checked_date_utc": "YYYY-MM-DD",
  "input_usd_per_million": "0.042",
  "output_usd_per_million": "0",
  "request_token_limit": 64000,
  "max_requests": 36,
  "max_usd": "1"
}
```

The date placeholder must be replaced only after checking. This record is an operator attestation, not automatic verification of the provider's pricing or an account-level spending cap. The runner checks its date and values, reserves the maximum per-request estimate before dispatch and stops on missing usage. A server violating the documented token/billing limit could exceed the estimate; the runner then stops further requests. Unknown usage remains explicit.

```sh
python experiments/jev-cec/run.py --mode live --preflight /path/to/checked-preflight.json --output /path/to/new-private-run
```

Use a fresh directory. The fixed 36-request schedule includes all not-attempted rows after a stop. No continuation or retry command is implemented. An interrupted attempt is marked before dispatch; a timeout never implies the provider did not process it. Later continuation needs a separately reviewed record and must not replay attempted requests.

## Evidence preservation and review

The output contains the complete schedule, exact request and response bytes, statuses, durations, reported model and usage, reference and source snapshots, Python version, Git revision, working-tree state and a SHA-256 artifact manifest. Authorization headers are excluded. Transport exceptions retain only their class to avoid leaking credential-bearing exception text. Raw provider response bodies still require inspection before publication.

`run.verify(Path(...))` checks the exact artifact set and hashes. A checksum detects changes relative to that manifest; it is not a digital signature or independent custody record. The code snapshots identify the executed source even when the recorded checkout is dirty. Do not execute the preserved snapshots in place; use the corresponding repository version.

Each pass has its own agreement, valid/scheduled coverage, confusion counts, recall and mean multiclass Brier loss. Repeated-run agreement uses only complete triplets and reports exclusions. All mismatches remain `unresolved` review items with reference rationales and evidence IDs. An AI-authored reference can be wrong. No result automatically becomes a corpus annotation or closes a human-review decision.

Before publishing any live result, verify hashes, inspect raw responses for sensitive material, account for every scheduled attempt and report invalid outputs alongside valid-response agreement. Independent accuracy and human usefulness remain outside this synthetic exercise.
