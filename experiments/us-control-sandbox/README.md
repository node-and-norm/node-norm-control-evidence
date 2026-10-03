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
