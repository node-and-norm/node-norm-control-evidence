# Initial external-source coverage register

Reviewed 2 October 2026. Author/AI-selected mappings for development planning. These mappings are not MIT classifications of our cases and imply no endorsement. No bulk dataset or incident packet has been imported.

Source: [MIT AI Risk Repository](https://airisk.mit.edu/risks), Domain Taxonomy, categories 2.2, 5.2, 7.3 and 7.4. The source taxonomy concerns security, agency, capability and transparency. Our mapping uses these as coverage prompts, not causal findings or prevalence estimates.

| Category locator | Proposed test connection | Coverage boundary |
|---|---|---|
| 2.2 | Unauthorized stop rejected | Does not test adversarial intrusion or full security |
| 5.2 | Working versus ineffective stop | No measurement of experienced human agency |
| 7.3 | Correction fails to reach recipient | One synthetic propagation failure |
| 7.4 | Acknowledgment versus observable outcome; withheld record | Evidence availability only, not model interpretability |

Human overreliance (5.1) remains outside the scripted pilot. Fairness, discrimination, environmental effects and other taxonomy domains are untested. This small mapping is not comprehensive AI-risk coverage.

[AI Incident Database snapshot guidance](https://incidentdatabase.ai/research/snapshots/) was reviewed for versioned access and incident-specific attribution. Three candidates are now screened, with decisions in INCIDENT-SCREENING.md. Selection rule: a bounded decision with identifiable actors, reported intervention or correction, and accessible primary evidence about effects. Exclude examples supported only by a summary or where the record cannot distinguish acknowledgment from consequence. Preserve uncertainty and source dependence. Record rejection reasons.

Next source gate: complete the screened candidates’ source packets; verify primary sources, licensing and redistribution rights; freeze source identifiers, retrieval dates and hashes; distinguish documentary conclusions from researcher-authored simulations. Only then import a dataset or public evidence packet. Hugging Face and LangChain remain optional technical choices, with no integrations claimed.

## Screening update

Three incident candidates were screened. Rite Aid/AIID 619 is retained for source-informed design with allegations explicitly labeled; Tempe is a boundary reference; Air Canada is deferred. See INCIDENT-SCREENING.md for primary-source locators and retrieval limits. The earlier pending-selection statements describe the initial checkpoint. No bulk dataset or complete incident packet has been imported.
