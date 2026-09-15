[Example gallery](../README.md)

# Synthetic review dossier

> **Invented demonstration. No observed event, human judgment, or empirical finding.**

> **Review view exposes proposed controls and labels. Do not use it for blind enumeration or independent initial coding.**

## Event scope

| Event | Period | Scope note |
| :--- | :--- | :--- |
| Synthetic acknowledged stop with unresolved mitigation | 2026-09-01T12:00:00Z | Invented scenario, not an observed evaluation. |

## Frozen packets

| Packet / event | Cutoff / version | Retrieval and omissions |
| :--- | :--- | :--- |
| PACKET&#95;1 / EVENT&#95;1 | 2026-09-03T00:00:00Z / synthetic-v1 | No retrieval performed; invented fixture. Consequences and alternative trajectories intentionally absent. |

## Located evidence

| Evidence / source | Location | Observation |
| :--- | :--- | :--- |
| EVID&#95;1 / SRC&#95;1 | Invented trace line 1 | The invented trace records an override command and a downstream stop acknowledgement. Consequences and alternatives are not reported. |

## Sources and dependence

Review views include all bundle source metadata; packet views include only sources connected to frozen evidence.

| Source | Role | Family |
| :--- | :--- | :--- |
| SRC&#95;1: Invented trace description | synthetic | FAMILY&#95;1 |
| SRC&#95;2: Invented derivative summary | synthetic | FAMILY&#95;1 |

| From | Relation | To | Basis |
| :--- | :--- | :--- | :--- |
| SRC&#95;2 | derived&#95;from | SRC&#95;1 | The invented summary repeats the trace description. |

<details>
<summary><strong>Source URLs and evidence-quality notes</strong></summary>


| Source / field | Recorded value |
| :--- | :--- |
| SRC&#95;1 / url | https://example.invalid/synthetic/trace |
| SRC&#95;1 / source&#95;date | 2026-09-01T12:01:00Z |
| SRC&#95;1 / retrieved&#95;at | 2026-09-02T00:00:00Z |
| SRC&#95;1 / version | synthetic-v1 |
| SRC&#95;1 / rights | synthetic |
| SRC&#95;1 / rights&#95;basis | Created solely as a software fixture. |
| SRC&#95;2 / url | https://example.invalid/synthetic/summary |
| SRC&#95;2 / source&#95;date | 2026-09-02T00:00:00Z |
| SRC&#95;2 / retrieved&#95;at | 2026-09-02T00:00:00Z |
| SRC&#95;2 / version | synthetic-v1 |
| SRC&#95;2 / rights | synthetic |
| SRC&#95;2 / rights&#95;basis | Created solely as a software fixture. |

| Evidence | Dimension | Recorded assessment |
| :--- | :--- | :--- |
| EVID&#95;1 | valid&#95;from | 2026-09-01T12:00:00Z |
| EVID&#95;1 | time&#95;note | Synthetic timestamp. |
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
| CLAIM&#95;1 / SRC&#95;1 | The synthetic trace describes acknowledgement of a stop. | EVID&#95;1 / preliminary |

## Initial judgments

Each value belongs to its stated packet. **Uncoded** means no annotation was supplied; it is a display label, never a missingness code.

### CONTROL&#95;1 · PACKET&#95;1

| Dimension | Value | Annotation |
| :--- | :--- | :--- |
| propagation | yes | ANN&#95;1 |
| propagation | yes | ANN&#95;2 |
| outcome&#95;mitigation | not&#95;reported | ANN&#95;3 |

<details>
<summary><strong>Judgment provenance, evidence, and rationale</strong></summary>


**ANN&#95;1**

| Field | Recorded value |
| :--- | :--- |
| coder&#95;id | SYNTHETIC&#95;1 |
| coder&#95;kind | synthetic |
| status | sealed&#95;initial |
| independent | False |
| eligibility&#95;record | Fixture only; no person or independent rating. |
| evidence&#95;ids | EVID&#95;1 |
| rationale | The invented downstream acknowledgement documents propagation within this fixture. |
| codebook&#95;version | 0.1.0 |
| coded&#95;at | 2026-09-03T01:00:00Z |

**ANN&#95;2**

| Field | Recorded value |
| :--- | :--- |
| coder&#95;id | SYNTHETIC&#95;2 |
| coder&#95;kind | synthetic |
| status | sealed&#95;initial |
| independent | False |
| eligibility&#95;record | Fixture only; no person or independent rating. |
| evidence&#95;ids | EVID&#95;1 |
| rationale | The invented downstream acknowledgement documents propagation within this fixture. |
| codebook&#95;version | 0.1.0 |
| coded&#95;at | 2026-09-03T01:00:00Z |

**ANN&#95;3**

| Field | Recorded value |
| :--- | :--- |
| coder&#95;id | SYNTHETIC&#95;1 |
| coder&#95;kind | synthetic |
| status | sealed&#95;initial |
| independent | False |
| eligibility&#95;record | Fixture only; no person or independent rating. |
| evidence&#95;ids |  |
| rationale | No consequences or alternative trajectory are reported in the invented packet. |
| codebook&#95;version | 0.1.0 |
| coded&#95;at | 2026-09-03T01:00:00Z |

</details>

<details>
<summary><strong>Uncoded dimensions (15)</strong></summary>


declared, design&#95;adequacy, implemented, operating, trigger, action, trajectory&#95;effect, formal&#95;authority, information, comprehension&#95;opportunity, intervention&#95;time, technical&#95;permission, institutional&#95;permission, alternatives, intervention&#95;attempted. No value is inferred for these dimensions.

</details>

## Separate adjudication

| Adjudication | Initial records | Value | Reason |
| :--- | :--- | :--- | :--- |
| ADJ&#95;1 | ANN&#95;1, ANN&#95;2 | yes | Synthetic agreement on propagation only; mitigation remains unresolved. |

No human agreement or validity result can be calculated from these invented judgments.

<details>
<summary><strong>Integrity commitments</strong></summary>


| Packet | Content SHA-256 |
| :--- | :--- |
| PACKET&#95;1 | 55893e2e572d9628b89e8e47f4df62c092d2f6a53d1cc3fba208e00c4976f98e |

Packet hashes commit to supplied metadata, including the predefined control scope. They do not prove source-byte custody or reviewer non-exposure. Blind enumeration requires separately governed packet construction.

Input SHA-256: `a7918de68c17e34e510e1b9fa3e7db28dca76ceaba2bf9785504720899df796e`

</details>

**Development boundary:** this renderer accepts synthetic bundles only. Empirical display requires a reviewed projection, rights decisions, and research approval.
