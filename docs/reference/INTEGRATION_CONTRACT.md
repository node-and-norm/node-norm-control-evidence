# Downstream integration contract 0.1.0-dev

[Repository](../../README.md) / [Documentation](../README.md)

## Canonical ownership

CEC is the canonical empirical layer. TAE, HIT, and RGDS consume immutable releases and own their derived analyses. Proposed corrections return through reviewed changes with provenance; downstream code cannot silently update canonical records.

## Required analysis provenance

Every analysis identifies corpus version, schema version and hash, input artifact hash, selected record IDs, filters, transformations, additional annotations, code revision, and limitations. Joins use stable IDs and versions. Human-readable titles are not identifiers. A later canonical adoption of a downstream construct requires separate validation and a migration record.

## Downstream uses

TAE may examine evidence sufficiency and autonomy hypotheses. HIT may examine authority, information, intervention timing, permission, and propagation. RGDS may examine approval, escalation, residual-risk records, and decision authority. These uses do not confer validity on downstream measures.

## Future site projection

The future site consumes a generated allowlist projection: release and schema identity, record IDs, event class, control functions, adjudicated dimension values with unresolved states, source links and locators approved for display, bounded interpretation, limitations, and correction links. It must not emit restricted source text, private coder details, sealed holdout contents, or AI proposals as established findings. Every display retains the evidence cutoff and release link. No score or legal-compliance badge is authorized.

## Development boundary

The development exporter handles only synthetic packets and labels them accordingly. Its output is a contract demonstration, not a site feed. Empirical release and site projection implementation remain gated by governance review. Breaking changes require a version change and migration guidance; old artifacts remain reproducible.
