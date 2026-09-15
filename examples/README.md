# Example gallery

[Repository](../README.md) / Examples

**Three invented cases. One inspectable evidence model.** These bundles exercise the software and explain its distinctions. No person supplied an independent rating, and none of the cases is an observed evaluation.

| Case | Research distinction illustrated | Annotated review | Source packet | Machine record |
| :--- | :--- | :--- | :--- | :--- |
| Unresolved override | An attempted action can leave propagation unreported | [Dossier](dossiers/override-unresolved.md) | [Packet](packets/override-unresolved.md) | [JSON](synthetic.json) |
| Acknowledged stop | Propagation can be documented while mitigation remains unreported | [Dossier](dossiers/override-confirmed.md) | [Packet](packets/override-confirmed.md) | [JSON](override-confirmed.json) |
| Policy-only authority | Assigned authority does not settle whether intervention was attempted | [Dossier](dossiers/policy-only.md) | [Packet](packets/policy-only.md) | [JSON](policy-only.json) |

## Two views, different uses

| View | Contains | Appropriate use |
| :--- | :--- | :--- |
| Review dossier | Evidence, source claims, proposed controls, initial synthetic labels, separate adjudication | Inspect the representation and review traceability |
| Source packet | Event scope, frozen evidence, source metadata and dependence; no proposed controls or labels | Demonstrate how an enumeration interface can withhold prior judgments |

> [!WARNING]
> A review dossier reveals labels. It must not be given to a reviewer whose initial judgment is supposed to be independent. The packet projection alone does not establish blinding: source content, titles, prior familiarity, access logs, and assignment procedures also matter.

## Read a value carefully

`not_reported` describes silence in the reviewed packet. `no` requires affirmative evidence for negation. **Uncoded** appears only in the display when a dimension has no annotation; it is never inserted into the research data as a value. The [codebook](../docs/methods/CODEBOOK.md) defines the full vocabulary.

<details>
<summary><strong>Regenerate the gallery</strong></summary>

```sh
python3 scripts/build_examples.py
```

Run from the repository root. The original fixture is the baseline; the builder creates two contrasting bundles, recalculates their packet commitments, validates them, and generates all six views. CI detects drift between the checked-in gallery and the generator.

</details>

For a source-based example, read the separate [Tempe reconnaissance note](../research/reconnaissance/tempe.md). It has no empirical labels and cannot be pooled with these fixtures.
