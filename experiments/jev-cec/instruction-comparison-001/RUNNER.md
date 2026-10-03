# Instruction comparison runner

The comparison runner implements the [prospective plan](PLAN.md) with 120 requests, 480 scheduled judgments and fixed secondary subsets. The [source freeze](freeze.json) binds both instruction conditions, inherited evidence and reference, runner and analysis. The uniform mock does not consult the reference.

```sh
python experiments/jev-cec/instruction-comparison-001/comparison_run.py --output build/comparison-mock
```

Use a new directory. Saved records include the full ordered schedule, request bytes, response bytes, source snapshots, metadata, per-condition results, paired records and an exact hash manifest. `comparison_run.verify` checks the archive. Each paired comparison requires valid responses from both conditions; missing members stay unavailable. Pass one remains primary. Two-pass repetition is descriptive and separate for each condition.

Live mode requires a clean checkout and the dated preflight fields used by v2, with `max_requests` set to 120. The supported configuration is USD 0.042 per million input tokens, free output and a 64,000-token combined limit; recheck the official service before attesting these values. USD 1 is the client spending ceiling. The runner never retries or repairs responses. Store credentials privately; do not include them in research artifacts.

This implementation changes no packet or reference. Candidate wording, length and emphasis vary together. All cases remain exposed development material; agreement cannot establish independent accuracy. Source snapshots retain original relative Markdown links and are verified as archived bytes rather than navigable documentation.
