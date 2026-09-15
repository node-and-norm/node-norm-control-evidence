[Example gallery](../README.md)

# Synthetic review dossier

> **Invented demonstration. No observed event, human judgment, or empirical finding.**

> **Review view exposes proposed controls and labels. Do not use it for blind enumeration or independent initial coding.**

## Event scope

| Event | Period | Scope note |
| :--- | :--- | :--- |
| Synthetic override with missing execution record | 2026-09-01T12:00:00Z | Invented scenario, not an observed evaluation. |

## Frozen packets

| Packet / event | Cutoff / version | Retrieval and omissions |
| :--- | :--- | :--- |
| PACKET&#95;1 / EVENT&#95;1 | 2026-09-03T00:00:00Z / synthetic-v1 | No retrieval performed; invented fixture. Execution acknowledgement intentionally absent. |

## Located evidence

| Evidence / source | Location | Observation | Applies from |
| :--- | :--- | :--- | :--- |
| EVID&#95;1 / SRC&#95;1 | Invented trace line 1 | An override command is described; no execution acknowledgement is supplied. | 2026-09-01T12:00:00Z |

## Sources and dependence

Review views include all bundle source metadata; packet views include only sources connected to frozen evidence.

| Source | Role / family | Source date / retrieved | Version / rights |
| :--- | :--- | :--- | :--- |
| SRC&#95;1: Invented trace description | synthetic / FAMILY&#95;1 | 2026-09-01T12:01:00Z / 2026-09-02T00:00:00Z | synthetic-v1 / synthetic |
| SRC&#95;2: Invented derivative summary | synthetic / FAMILY&#95;1 | 2026-09-02T00:00:00Z / 2026-09-02T00:00:00Z | synthetic-v1 / synthetic |

| From | Relation | To | Basis |
| :--- | :--- | :--- | :--- |
| SRC&#95;2 | derived&#95;from | SRC&#95;1 | The invented summary repeats the trace description. |

<details>
<summary><strong>Source URLs and evidence-quality notes</strong></summary>


| Source | URL (as recorded) | Rights basis |
| :--- | :--- | :--- |
| SRC&#95;1 | https://example.invalid/synthetic/trace | Created solely as a software fixture. |
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
| CONTROL&#95;1 / EVENT&#95;1 | Allow an operator to interrupt an action. An action is pending approval. | human&#95;oversight, restrictive&#95;corrective / 2026-09-01T12:00:00Z to 2026-09-01T12:01:00Z |

## Source claims

| Claim / source | Statement | Evidence IDs / status |
| :--- | :--- | :--- |
| CLAIM&#95;1 / SRC&#95;1 | The synthetic trace describes an override attempt. | EVID&#95;1 / preliminary |

## Initial judgments

Each value belongs to its stated packet. **Uncoded** means no annotation was supplied; it is a display label, never a missingness code.

### CONTROL&#95;1 · PACKET&#95;1

| Dimension | Value | Annotation / coder / kind / status | Evidence | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| propagation | not&#95;reported | ANN&#95;1 / SYNTHETIC&#95;1 / synthetic / sealed&#95;initial | No cited item | The synthetic packet has no downstream execution record. |
| propagation | not&#95;reported | ANN&#95;2 / SYNTHETIC&#95;2 / synthetic / sealed&#95;initial | No cited item | The synthetic packet has no downstream execution record. |

<details>
<summary><strong>Uncoded dimensions (16)</strong></summary>


declared, design&#95;adequacy, implemented, operating, trigger, action, trajectory&#95;effect, outcome&#95;mitigation, formal&#95;authority, information, comprehension&#95;opportunity, intervention&#95;time, technical&#95;permission, institutional&#95;permission, alternatives, intervention&#95;attempted. No value is inferred for these dimensions.

</details>

## Separate adjudication

| Adjudication | Initial records | Value | Reason |
| :--- | :--- | :--- | :--- |
| ADJ&#95;1 | ANN&#95;1, ANN&#95;2 | not&#95;reported | Demonstrates a separate adjudication object; no human adjudication occurred. |

No human agreement or validity result can be calculated from these invented judgments.

<details>
<summary><strong>Integrity commitments</strong></summary>


| Packet | Content SHA-256 |
| :--- | :--- |
| PACKET&#95;1 | 1bb4b906cdd93330cd05f5a58063f307171da08a972a860f7e298e0694cc27e8 |

Packet hashes commit to supplied metadata, including the predefined control scope. They do not prove source-byte custody or reviewer non-exposure. Blind enumeration requires separately governed packet construction.

Input SHA-256: `1409508baae195c007316091134e77b1dee599da02b85411a8664b56e53c710d`

</details>

**Development boundary:** this renderer accepts synthetic bundles only. Empirical display requires a reviewed projection, rights decisions, and research approval.
