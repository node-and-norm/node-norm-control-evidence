# Reproduce the development artifacts

[Repository](../../README.md) / [Documentation](../README.md) / Reproducibility

**All executable outputs are synthetic development artifacts.** The workflow uses Python 3.11 or later and the pinned dependency in [requirements.txt](../../requirements.txt).

## Run from the repository root

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_schemas.py
python3 scripts/build_examples.py
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
python3 scripts/export.py examples/synthetic.json --output build/synthetic-export.json
```

| Step | Inspectable output | What it establishes |
| :--- | :--- | :--- |
| Schema generation | [Object contracts](../../schemas/README.md) | Reproducible definitions with explicit required fields |
| Example generation | [Gallery](../../examples/README.md) | Valid synthetic records and deterministic Markdown views |
| Documentation checks | Local link, fragment, and expansion-tag checks | Navigation consistency and balanced detail sections |
| Integrity tests | Validator and renderer behavior under adversarial inputs | Rejection of specific invalid data states and unsafe presentation |
| Export | `build/synthetic-export.json` | Labeled synthetic package with input and schema hashes |

## Render one view

```sh
python3 scripts/render_dossier.py examples/synthetic.json --view review --output build/review.md
python3 scripts/render_dossier.py examples/synthetic.json --view packet --output build/packet.md
```

Review views expose annotations. Packet views omit proposed controls, claims, ratings, and adjudication. Both are demonstration outputs; neither is an approved empirical publication interface. The [example guide](../../examples/README.md) explains the blinding limits.

## What a successful run cannot establish

| Research requirement | Why software checks cannot complete it |
| :--- | :--- |
| Source supports a proposition | A valid reference can still point to irrelevant or misleading content |
| Coders were independent | Identity fields and hashes do not establish actual non-exposure |
| A holdout remained untouched | A checksum needs custody, access records, and accountable people |
| Construct validity | Consistent labels may still measure the wrong concept |
| Redistribution rights | A field marked redistributable needs a source-specific reviewed basis |

The source-reconnaissance PDF stays in ignored local storage. Its committed metadata records the bytes retrieved, while redistribution of the source itself remains unapproved. No network retrieval occurs in the example-generation workflow.
