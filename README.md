# Node & Norm Control Evidence Corpus

Can an independent reviewer reconstruct whether an AI governance control had practical force from the evidence that survives a consequential event?

This repository implements the research infrastructure for that question. The analytical unit is an event-control observation. Sources, evidence, source claims, researcher annotations, adjudication, and derived measures remain separate.

Status: **0.1.0-dev, infrastructure only**. There are no human-coded empirical records, reliability findings, or validated effectiveness measures. The executable example is synthetic. No corpus release has been approved.

## Authority and navigation

- [Research Charter](RESEARCH_CHARTER.md) and [Research Agenda](RESEARCH_AGENDA.md) preserve the recovered governing drafts.
- [Continuation record](CONTINUATION.md) explains recovered state, precedence, and remaining gates.
- [Novelty review](NOVELTY_REVIEW.md) identifies overlap and open screening work.
- [Codebook](CODEBOOK.md), [sampling](SAMPLING_PLAN.md), [reliability](RELIABILITY_PLAN.md), and [validation](VALIDATION_PLAN.md) define the development protocol.
- [Source policy](SOURCE_POLICY.md) and [rights ledger](RIGHTS_LEDGER.md) govern evidence handling.
- [Integration contract](INTEGRATION_CONTRACT.md) governs TAE, HIT, RGDS, and later site exports.
- [Roadmap](ROADMAP.md) records the next unfinished work.

## Run locally

Python 3.11 or later and the pinned dependency in `requirements.txt` are required.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/validate.py examples/synthetic.json
python3 -m unittest discover -s tests -v
python3 scripts/export.py examples/synthetic.json --output build/synthetic-export.json
```

The exporter produces an explicitly synthetic development package with input and schema hashes. Empirical publication is deliberately unavailable in this development implementation. Passing software checks establishes data-contract behavior only.

Canonical research records will live in `data/`; development fixtures live in `examples/`. Release packages must be immutable and independently approved under GOVERNANCE.md. Source documents remain subject to their own rights.
