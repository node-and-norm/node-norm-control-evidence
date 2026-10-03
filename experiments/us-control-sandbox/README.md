# TAE/HIT prospective research sandbox

Development checkpoint, 2 October 2026. Published within the Control Evidence Corpus repository as a separate experiment; its outputs are outside the empirical corpus. Two authored suites contain sixteen conditions: nine basic intervention/correction conditions and seven retry/restart conditions. TAE and HIT remain unscored. No confirmatory study, human-behavior validation or regulatory participation is claimed.

Run from this directory with Python 3.9 or later, choosing new output names:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B sandbox.py --output runs/basic-next
python3 -B recovery.py --output runs/recovery-next
```

The basic suite tests stop effectiveness, timing, permission, missing evidence and correction delivery to a simulated recipient record. The recovery suite launches separate worker processes to test saved stops and duplicate requests. Its observer counts committed effects. It does not test concurrent workers or crashes during writes.

Nineteen verification tests passed locally and in the pinned, network-disabled container. All seven recovery fixtures matched expectations in both environments; five met their narrow control objective and two exposed deliberate defects. Eight JSON files, comprising seven packets and the outcome report, matched across environments. Both manifests verified twenty-one artifacts. Earlier runs are preserved.

- [Study checkpoint](STATUS.md): completed work and next gates.
- [Publication record](PUBLICATION.md): AI assistance, public-copy changes and source rights.
- [Run index](RUN-INDEX.md): preserved attempts, results and their verification limits.
- [NIST mapping](NIST-MAPPING.md): six selected AI RMF 1.0 provisions, pages and outstanding evidence.
- [Recovery design](RECOVERY-DESIGN.md): conditions, objectives and process-replacement limits.
- runs/recovery-001/ and container-runs/recovery-001/: local and container outcomes.
- container-runs/isolated-tests-002/: full nineteen-test container report and source snapshots.
- ENVIRONMENT.md: restrictions, pinned image and restart instructions.

The container launcher accepts `--suite basic`, `--suite recovery` or `--suite tests`. It requires a pinned image and unique run name; specify the study context as shown in ENVIRONMENT.md. It does not fall back to host execution.

Verify artifacts with `python3 -B verify_run.py runs/recovery-001`. Hashes detect changes relative to a manifest, not malicious rewriting of both artifacts and manifest. They are not signatures or immutable ledgers. Compare semantic outcomes across runtimes; SQLite bytes can vary.

Outcome and assessment files are separated by directory, not access control. Source and expected results are public. There is no assessor blinding or independent evaluation. Scripted actors cannot establish human comprehension, authority or exercised judgment. The original methods' workstreams are preserved; see PROTOCOL.md, RECONCILIATION.md, CONTRACT-REVIEW.md and APPLICATION-BOUNDARY.md.

TAE owns its [control protocol](https://github.com/node-and-norm/trust-autonomy-evidence); HIT owns its [assessment contract](https://github.com/node-and-norm/human-influence-telemetry). This experiment supplies candidate evidence for future admissibility review. Its records are not imported into CEC schemas, assessed under either method, or approved for an empirical release.

## Evidence eligibility checkpoint

[The admissibility decision](ADMISSIBILITY.md) permits a technical appendix for each supplied packet. A full TAE/HIT assessment needs an eligible human/institutional boundary and the required evidence. The appendix format records observations and unresolved downstream evidence with scoring disabled.

[Sixteen reproducible appendices](evidence-appendices/README.md) are generated solely from the saved packet bytes and their recorded hashes. The builder does not read expected case labels, databases or hidden outcome files. It cannot establish the truth or completeness of the supplied record.

```sh
python3 -B build_evidence_appendices.py --check --output evidence-appendices/v0.1
python3 -B build_evidence_appendices.py --output build/appendices-new
```

The second command requires a new directory. The evidence-eligibility checkpoint added nine boundary tests, bringing that checkpoint to twenty-eight tests. The prior nineteen-test container checkpoint remains an unchanged historical record; the new appendix checks run locally and in repository CI.

## Technical-evaluation rules

[Technical-evidence evaluation 0.1](TECHNICAL-EVALUATION.md) defines the unit, evidence-sufficiency key, response labels, six separate measures, denominators and invalid-run handling before new case construction. It does not score TAE or HIT. The calculator checks submitted label arithmetic; it cannot validate a rationale or the reference key.

The compact key is a JSON list of objects containing `unit_id` and `reference`; responses contain `unit_id` and `response`. Every key unit needs exactly one response. The permitted labels are in [evaluation_rules.json](evaluation_rules.json). Full key rationales, locators and excluded units remain in separate study records; these projections cannot replace them.

```sh
python3 -B evaluate_evidence.py --key build/key-projection.json --responses build/responses.json --output build/scoring-attempt-001
```

Use your declared study projections and a fresh output directory. Failed attempts retain available input bytes and an error record and return a nonzero exit. Successful arithmetic records the rule, evaluator and input hashes. No overall pass, scientific validation or composite score is emitted. No cohort has been evaluated under these rules yet; nine calculator tests bring the sandbox suite to thirty-seven tests.

## Paired procedure checkpoint

The [procedure specification](PROCEDURES.md) and [candidate run plan](RUN-PLAN.md) define a short checklist and a complete trace using the same facts and rules. Their shared implementation means label agreement is expected and supplies no independent validation or comparative accuracy result.

The [preserved development demonstration](procedure-runs/development-001/summary.json) reuses seven public packets. It includes the envelopes, both outputs, source locators and hashes, and source snapshots. No new study cases or reference key were created. Eight new tests bring the sandbox suite to forty-five tests.

```sh
python3 -B run_paired_demo.py --output build/paired-attempt-new
python3 -B verify_run.py procedure-runs/development-001
```

The first command needs a fresh directory. The next research-design task is to specify trace-quality measures and burden, fix the cohort and access plan, then create new author-exposed case families. Independent blinding is not claimed.
