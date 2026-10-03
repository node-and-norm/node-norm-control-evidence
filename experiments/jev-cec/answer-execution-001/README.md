# Answer-level runner

[Plan and limits](PLAN.md) · [Mock report](mock-001/report.json) · [Manifest](mock-001/manifest.json)

This runner implements the prospective answer contract with unchanged numerical tolerance. Failed answers remain excluded while eligible siblings can be analyzed. Pair and repetition eligibility follow the required individual answers. Unresolved references remain unscored.

The archived mock contains eight uniform mock responses, 32 eligible mock answers and zero live requests. It was executed in a dirty development checkout. Exact source snapshots and hashes identify the implementation; this is plumbing verification, not a live finding. Tests separately inject partial responses and malformed envelopes.

Future execution requires the frozen sources and live preflight. No existing result is reclassified or replaced by this implementation.
