# Rights ledger

Checked 2026-09-14 UTC. This is a source-intake decision record, not a blanket legal determination.

| Source | Inspected terms or evidence | Intake decision |
| --- | --- | --- |
| AIID | [Terms](https://incidentdatabase.ai/terms-of-use/) distinguish licensed snapshot collections from excluded report text. | Preserve IDs and links; inspect each snapshot license before importing fields. Report text redistribution blocked. |
| MIT Incident Tracker | [Methodology](https://airisk.mit.edu/ai-incident-tracker/incident-view) identifies AIID reports and LLM classification. | Links only for now; dataset-specific rights review pending. Preserve AIID lineage. |
| OECD AIM | [Disclosures](https://oecd.ai/en/incidents-methodology) reserve underlying third-party rights. | Discovery links only; no underlying article-text export. |
| Research literature | Publisher or repository pages reviewed for screening. | Bibliographic links and original short analysis only; no full-text redistribution authorized. |
| TAE / HIT | Methodological rules inspected; no case-label import. | Cite exact source files; source-specific license review required before copying research data. |
| CEC synthetic fixture | Created for this implementation. | Development export allowed; not empirical data. |

Each empirical source needs a machine-readable rights decision with scope, reviewer, date, attribution, restrictions, and the inspected terms version before any public export. Unknown rights block redistribution. A general repository license must not override upstream restrictions. The maintainer has not selected a blanket corpus license.
