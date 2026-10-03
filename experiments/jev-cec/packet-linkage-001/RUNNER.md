# Packet-linkage runner

The runner implements the [prospective plan](PLAN.md) for eight requests. Mock mode exercises accounting and analysis without a provider connection. Outputs are plumbing checks and supply no model findings.

From the repository root:

```sh
python3 experiments/jev-cec/packet-linkage-001/linkage_run.py --output build/packet-linkage-mock
python3 -m unittest discover -s tests -p 'test_cec_linkage_runner.py' -v
```

The output directory must be new. It contains exact payloads and response bytes, the complete schedule, attempt status, source snapshots, metadata, descriptive report and an artifact hash manifest. `linkage_run.verify(path)` checks the artifact set and hashes. Source binding is checked before either mode runs.

Live mode additionally requires a clean committed checkout, the API key in `TYPESAFE_API_KEY`, and `--preflight` pointing to a JSON file recording the current UTC date, verified input/output prices, token ceiling, eight-request maximum and USD 1 cap. Recheck official provider documentation before execution. Never commit the key. No live execution is included in this implementation step.

Analysis leaves the original action reference and its agreement score null. It reports action transitions with their available denominator, explicit-condition agreement, secondary dimensions and pass-two repetition separately. Invalid responses exclude four judgments; missing attempts retain their scheduled positions. Stop conditions preserve raw output and produce a manifest. Probability repair and automatic retries are absent.

The [preserved mock rehearsal](mock-001/report.json) contains eight uniform mock responses and zero live requests. It was executed during implementation in a dirty checkout; exact source snapshots and hashes identify its inputs. It is not a clean live execution or research finding.
