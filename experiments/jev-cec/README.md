# Jev request preparation for CEC

[Repository](../../README.md) / Jev preparation

Prepare inspectable model inputs from CEC's three existing synthetic examples. The [decision and next experiment](PLAN.md) explain where Jev might help and what remains untested.

From the repository root, using the existing pinned dependency:

```sh
python scripts/validate.py examples/synthetic.json
python experiments/jev-cec/prepare.py --output build/jev-cec-preparation
python -m unittest discover -s tests -v
```

Use a fresh output directory. Preparation saves exact inputs, requests, question definitions, codebook, plan, preparation code and artifact hashes. It creates three requests and nine questions. It sends nothing and produces no model answers or scores. Inspect the [preserved preparation manifest](prepared-001/manifest.json) and [requests](prepared-001/requests.json).

The eight choices retain CEC's distinction among `yes`, `no`, `partial`, `conflicting`, `unknown`, `not_reported`, `not_observable` and `not_applicable`. These are proposals under the existing codebook; they are separate from the pilot rubric's four support judgments and TAE's five-class experiment.

The original synthetic bundles include labels and are saved as provenance only. They must never be submitted wholesale to a model or given to an unexposed assessor. The prepared request omits those labels, but evidence wording and earlier exposure remain limitations. No blinding claim is made.

## Documentary challenge continuation

The [versioned challenge set](challenge-v1/README.md) adds twelve invented packets and a separate AI-authored reference key. It preserves 36 expectations before any CEC model inference. Run `python experiments/jev-cec/challenge.py check` to verify its hashes and references. This is development exposure; independent review and a live execution protocol remain outstanding.

## Execution contract

The [execution protocol v1](execution-v1/PROTOCOL.md) fixes three passes, a 36-request ceiling, a USD 1 spending ceiling for a future runner, whole-response validation and descriptive reporting rules. `python experiments/jev-cec/execution.py --output build/cec-schedule` prepares the schedule offline. The response validator rejects malformed distributions without normalization. No live transport is implemented yet.

## Runner continuation

The [runner guide](execution-v1/RUNNER.md) documents the implemented bounded transport, mock verification, live preflight and per-pass analysis. The earlier execution-contract milestone remains preserved. The [first live results](execution-v1/LIVE-RESULTS.md) preserve 31 valid and five invalid responses from 36 attempts, with unresolved disagreements.
