# Missingness runner

[Design](PLAN.md) · [Reference review](REVIEW.md) · [Mock report](mock-001/report.json) · [Manifest](mock-001/manifest.json)

The runner implements 32 ordered requests, answer-level eligibility, per-dimension agreement and twelve dependent edges per instruction package and option-order block. Target transitions require two target answers; stability across unrelated dimensions requires all six relevant answers. Package comparisons use jointly eligible judgments. Canonical results are primary; reversed-order results remain separate.

Run `python3 experiments/jev-cec/missingness-boundary-001/boundary_run.py --output build/missingness-mock` from the repository root. The directory must be new. Default mode uses uniform mock responses. Live mode additionally requires a clean checkout, verified same-day preflight and the existing private credential in the environment. See the plan for cost and stop limits.

The preserved mock contains 32 uniform responses and zero live requests. Its dirty development-checkout status is disclosed in metadata; exact source snapshots and hashes identify its implementation. It demonstrates arithmetic and archive plumbing, not model performance. Tests separately exercise perfect synthetic fixtures, a single failed answer, unavailable pairs, interruption, budget exhaustion and option-order preservation.

No existing experiment is rescored. Historical validators and raw outputs remain unchanged.
