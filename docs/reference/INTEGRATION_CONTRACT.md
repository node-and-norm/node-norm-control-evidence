# Downstream integration contract 0.1.0-dev

[Repository](../../README.md) / [Documentation](../README.md)

## Canonical ownership

CEC is the canonical empirical layer. TAE, HIT, and RGDS consume immutable releases and own their derived analyses. Proposed corrections return through reviewed changes with provenance; downstream code cannot silently update canonical records.

The repositories share the [Node & Norm organization](https://github.com/node-and-norm). Organization ownership does not change research authority, establish scientific validity, or make downstream outputs ground truth. CEC remains private development infrastructure; empirical consumption is a future contract, not an operational data feed. See the [organization migration record](ORGANIZATION_MIGRATION_2026-09-15.md).

## Required analysis provenance

Every analysis identifies corpus version, schema version and hash, input artifact hash, selected record IDs, filters, transformations, additional annotations, code revision, and limitations. Joins use stable IDs and versions. Human-readable titles are not identifiers. A later canonical adoption of a downstream construct requires separate validation and a migration record.

## Downstream uses

| Consumer | Potential use |
| :--- | :--- |
| [Trust Autonomy Evidence (TAE)](https://github.com/node-and-norm/trust-autonomy-evidence) | Evidence sufficiency and autonomy hypotheses |
| [Human Influence Telemetry (HIT)](https://github.com/node-and-norm/human-influence-telemetry) | Authority, information, intervention timing, permission, and propagation |
| [Regulated Gate Decision Support (RGDS)](https://github.com/node-and-norm/rgds) | Approval, escalation, residual-risk records, and decision authority |

These uses do not confer validity on downstream measures. The organization directory also links the governance framework, its method/profile, the historical independent study, and workflow infrastructure. Sharing an organization does not merge their versions, evidence, or release gates.

## Future site projection

The future site consumes a generated allowlist projection: release and schema identity, record IDs, event class, control functions, adjudicated dimension values with unresolved states, source links and locators approved for display, bounded interpretation, limitations, and correction links. It must not emit restricted source text, private coder details, sealed holdout contents, or AI proposals as established findings. Every display retains the evidence cutoff and release link. No score or legal-compliance badge is authorized.

## Development boundary

The development exporter handles only synthetic packets and labels them accordingly. Its output is a contract demonstration, not a site feed. Empirical release and site projection implementation remain gated by governance review. Breaking changes require a version change and migration guidance; old artifacts remain reproducible.
