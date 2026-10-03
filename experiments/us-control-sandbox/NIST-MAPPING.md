# Selected U.S. risk-management context

Mapping revision 0.1, 2 October 2026. Source pinned to NIST AI 100-1, AI RMF 1.0, January 2023, DOI 10.6028/NIST.AI.100-1. This does not claim to represent every subsequent NIST publication. The public source URL and locally acquired PDF digest are in references/nist/manifest.json. The full PDF remains in the local archive and is excluded from this public package.

This is an author-created mapping of development questions to selected provisions. It is not a NIST assessment, endorsement, compliance determination, certification or formal regulatory sandbox. No provision is marked satisfied. Page references below use printed page numbers; the corresponding PDF page is five higher.

| Provision and page | Brief source paraphrase | Our corresponding work | Evidence still needed |
| --- | --- | --- | --- |
| MAP 2.3, p. 27 | Document scientific integrity, evaluation design and data considerations. | PROTOCOL.md, CONTRACT-REVIEW.md and RECOVERY-DESIGN.md distinguish development fixtures from validation. | Prospective freeze, justified sampling and construct validity. |
| MAP 3.5, p. 27 | Define, assess and document human oversight processes. | Stop, authority-boundary and correction fixtures examine selected software mechanisms. | Actual institutional roles, usable authority and human comprehension or judgment. |
| MEASURE 2.1, p. 29 | Document test sets, metrics and evaluation tools. | Versioned fixtures, source snapshots, manifests and observed effect counts. | Held-out cases, defensible denominators and assessor agreement under a locked contract. |
| MEASURE 2.7, p. 30 | Evaluate and document security and resilience. | Restricted execution environment; restart and duplicate-request cases. | Threat model, concurrency, hostile inputs, power-loss behavior and production recovery. |
| MANAGE 2.4, p. 32 | Provide mechanisms and responsibilities to supersede or deactivate unsuitable systems. | Compare an accepted stop with downstream effects after worker replacement. | Responsible decision-makers, deployment-specific stop boundaries and acceptable residual risk. |
| MANAGE 4.1, p. 33 | Implement monitoring, override, incident response and recovery plans. | Correction-delivery fixtures and replay tests provide candidate checks. | Operating monitoring, affected-person feedback, recovery ownership and change governance. |

Source: [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf). The framework describes itself as voluntary (p. 2). These rows select narrow relationships; they do not measure framework coverage. A successful fixture cannot establish organizational compliance or the effectiveness of human oversight.

The study currently executes authored software without a model or human participant. MIT risk categories and incident sources help select failure mechanisms; they do not provide outcome labels. A later model or dataset adapter would require its own version, provenance, license, application boundary and admission decision. Adding a hosted model does not turn this exercise into a formal U.S. regulatory sandbox.
