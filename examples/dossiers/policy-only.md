[Example gallery](../README.md)

# Synthetic review dossier

> **Invented demonstration. No observed event, human judgment, or empirical finding.**

> **Review view exposes proposed controls and labels. Do not use it for blind enumeration or independent initial coding.**

## Event scope

| Event | Period | Scope note |
| :--- | :--- | :--- |
| Synthetic policy-only approval role | 2026-09-01T12:00:00Z | Invented scenario, not an observed evaluation. |

## Frozen packets

| Packet / event | Cutoff / version | Retrieval and omissions |
| :--- | :--- | :--- |
| PACKET&#95;1 / EVENT&#95;1 | 2026-09-03T00:00:00Z / synthetic-v1 | No retrieval performed; invented fixture. Implementation, permissions, runtime actions, and consequences intentionally absent. |

## Located evidence

| Evidence / source | Location | Observation | Applies from |
| :--- | :--- | :--- | :--- |
| EVID&#95;1 / SRC&#95;1 | Invented policy paragraph 1 | The invented policy assigns an operator authority to withhold approval. No implementation or runtime action is described. | 2026-09-01T12:00:00Z |

## Sources and dependence

Review views include all bundle source metadata; packet views include only sources connected to frozen evidence.

| Source | Role / family | Source date / retrieved | Version / rights |
| :--- | :--- | :--- | :--- |
| SRC&#95;1: Invented approval policy | synthetic / FAMILY&#95;1 | 2026-09-01T12:01:00Z / 2026-09-02T00:00:00Z | synthetic-v1 / synthetic |
| SRC&#95;2: Invented derivative summary | synthetic / FAMILY&#95;1 | 2026-09-02T00:00:00Z / 2026-09-02T00:00:00Z | synthetic-v1 / synthetic |

| From | Relation | To | Basis |
| :--- | :--- | :--- | :--- |
| SRC&#95;2 | derived&#95;from | SRC&#95;1 | The invented summary repeats the policy statement. |

<details>
<summary><strong>Source URLs and evidence-quality notes</strong></summary>


| Source | URL (as recorded) | Rights basis |
| :--- | :--- | :--- |
| SRC&#95;1 | https://example.invalid/synthetic/policy | Created solely as a software fixture. |
| SRC&#95;2 | https://example.invalid/synthetic/summary | Created solely as a software fixture. |

| Evidence | Dimension | Recorded assessment |
| :--- | :--- | :--- |
| EVID&#95;1 | directness | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | independence | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | traceability | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | temporal&#95;relevance | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | specificity | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | consistency | Synthetic demonstration; no empirical quality assessment. |
| EVID&#95;1 | completeness | Synthetic demonstration; no empirical quality assessment. |

</details>

## Proposed controls

| Control / event | Objective and opportunity | Functions / relevant period |
| :--- | :--- | :--- |
| CONTROL&#95;1 / EVENT&#95;1 | Require an operator approval before execution. A proposed action awaits release. | human&#95;oversight, authorization&#95;governance / 2026-09-01T12:00:00Z to 2026-09-01T12:01:00Z |

## Source claims

| Claim / source | Statement | Evidence IDs / status |
| :--- | :--- | :--- |
| CLAIM&#95;1 / SRC&#95;1 | The synthetic policy assigns approval authority. | EVID&#95;1 / preliminary |

## Initial judgments

Each value belongs to its stated packet. **Uncoded** means no annotation was supplied; it is a display label, never a missingness code.

### CONTROL&#95;1 · PACKET&#95;1

| Dimension | Value | Annotation / coder / kind / status | Evidence | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| formal&#95;authority | yes | ANN&#95;3 / SYNTHETIC&#95;1 / synthetic / sealed&#95;initial | EVID&#95;1 | The invented policy assigns the role approval authority. |
| intervention&#95;attempted | not&#95;reported | ANN&#95;1 / SYNTHETIC&#95;1 / synthetic / sealed&#95;initial | No cited item | The invented policy does not report an intervention. |
| intervention&#95;attempted | not&#95;reported | ANN&#95;2 / SYNTHETIC&#95;2 / synthetic / sealed&#95;initial | No cited item | The invented policy does not report an intervention. |

<details>
<summary><strong>Uncoded dimensions (15)</strong></summary>


declared, design&#95;adequacy, implemented, operating, trigger, action, propagation, trajectory&#95;effect, outcome&#95;mitigation, information, comprehension&#95;opportunity, intervention&#95;time, technical&#95;permission, institutional&#95;permission, alternatives. No value is inferred for these dimensions.

</details>

## Separate adjudication

| Adjudication | Initial records | Value | Reason |
| :--- | :--- | :--- | :--- |
| ADJ&#95;1 | ANN&#95;1, ANN&#95;2 | not&#95;reported | Synthetic agreement about packet silence on an attempt; no conclusion about whether one occurred. |

No human agreement or validity result can be calculated from these invented judgments.

<details>
<summary><strong>Integrity commitments</strong></summary>


| Packet | Content SHA-256 |
| :--- | :--- |
| PACKET&#95;1 | 4ecf51a5c7944d612ebb43a2066bf41c25ab4a324d4966cf6ee9bae08048c52f |

Packet hashes commit to supplied metadata, including the predefined control scope. They do not prove source-byte custody or reviewer non-exposure. Blind enumeration requires separately governed packet construction.

Input SHA-256: `20fb50574c452ebd97382e41f84ef6e45040425a47e4d13b043ea3086a179aa9`

</details>

**Development boundary:** this renderer accepts synthetic bundles only. Empirical display requires a reviewed projection, rights decisions, and research approval.
