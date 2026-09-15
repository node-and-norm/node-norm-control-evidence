# Node & Norm organization migration

[Repository](../../README.md) / [Documentation](../README.md)

**Completed 2026-09-15 UTC.** Seven public repositories transferred from `mj3b` to [Node & Norm](https://github.com/node-and-norm). Each retained its repository identity and separate research scope. CEC remains private.

## Canonical locations

| Repository | Role | Validation after migration |
| :--- | :--- | :--- |
| [Trust Autonomy Evidence](https://github.com/node-and-norm/trust-autonomy-evidence) | Evidence and autonomy research | [Passed](https://github.com/node-and-norm/trust-autonomy-evidence/actions/runs/34926525899) |
| [Human Influence Telemetry](https://github.com/node-and-norm/human-influence-telemetry) | Human authority and intervention research | [Passed](https://github.com/node-and-norm/human-influence-telemetry/actions/runs/34926326046) |
| [RGDS](https://github.com/node-and-norm/rgds) | Reference implementation | [Passed](https://github.com/node-and-norm/rgds/actions/runs/34926328182) |
| [RGDS AI Governance](https://github.com/node-and-norm/rgds-ai-governance) | AI Assistance Governance method/profile | [Passed](https://github.com/node-and-norm/rgds-ai-governance/actions/runs/34926330072) |
| [RGDS Independent Study](https://github.com/node-and-norm/rgds-independent-study) | Historical exploratory study | [Build and deployment passed](https://github.com/node-and-norm/rgds-independent-study/actions/runs/34926332457) |
| [Governed Decision Intelligence](https://github.com/node-and-norm/governed-decision-intelligence) | Governance framework | [Passed](https://github.com/node-and-norm/governed-decision-intelligence/actions/runs/34926333834) |
| [Applied AI Research Translator](https://github.com/node-and-norm/applied-ai-research-translator) | Research workflow infrastructure | [Passed](https://github.com/node-and-norm/applied-ai-research-translator/actions/runs/34926335811) |

The [organization profile](https://github.com/node-and-norm/.github/blob/main/profile/README.md) provides a public directory and distinguishes research maturity from organizational affiliation. Software validation is not empirical validation.

## Preservation and integration checks

| Item | Verified result |
| :--- | :--- |
| Repository identity | All seven retained their GitHub repository IDs and public visibility. Old repository API addresses resolve to the corresponding new locations. |
| Existing history | Branch and tag commit targets matched immediately before and after transfer. Subsequent administrative commits update current navigation. |
| Releases | All 46 existing release records retained their IDs and attached asset identities, names, sizes, and available digests. No release was recreated or tag moved. |
| Attribution | Existing authors, licenses, and DOI identifiers retained. Active citation repository addresses updated where permitted by release integrity constraints. |
| TAE frozen files | Its README and citation file are covered by the release manifest. Their exact original bytes were restored after validation identified the constraint. Current locations appear in its separate `REPOSITORY_LOCATION.md`. |
| Dependencies | AI Governance now checks out RGDS from the organization while retaining the exact pinned commit. |
| Archival integration | Five existing Zenodo release webhook configurations retained their IDs, active states, and event subscriptions. Future release delivery was not tested; no test archive was created. |
| Local working copies | Migration checkouts use the new organization remotes. Unrelated local checkouts were not inventoried. |

## Study address

The independent study is deployed at **[node-and-norm.github.io/rgds-independent-study](https://node-and-norm.github.io/rgds-independent-study/)**. The deployed page responds and contains the updated canonical and repository links.

The previous `mj3b.github.io/rgds-independent-study/` Pages address does not automatically redirect. Current navigation and relevant repository homepages use the new address. Historical references remain preserved and may still contain the former address.

## Boundaries

The public Node & Norm website and repositories outside the seven listed projects were not modified. CEC's `v0.1.0-dev` release remains unchanged. No empirical records, private source packets, or holdout material were published. The [downstream integration contract](INTEGRATION_CONTRACT.md) continues to govern future reuse.
