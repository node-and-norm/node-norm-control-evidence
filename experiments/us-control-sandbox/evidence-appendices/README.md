# Technical evidence appendices

These sixteen appendices describe the nine basic and seven recovery packets already published. Each observation points to a JSON field and preserves its recorded value. Source hashes identify the inspected packet bytes; the source revision is the earlier publication commit.

They contain no TAE stage findings, HIT scores or integrity ratings. The [admissibility decision](../ADMISSIBILITY.md) explains the boundary. The exact packet selection is development material, and all source cases and outcomes are already public.

| Contrast to inspect | What the records establish |
| --- | --- |
| [Working stop packet](v0.1/rehearsal-002-packet-001.json) and [ineffective stop packet](v0.1/rehearsal-002-packet-002.json) | Both response records say accepted. Their supplied downstream action states differ. |
| [Missing downstream evidence](v0.1/rehearsal-002-packet-005.json) | The packet omits the downstream result. The appendix preserves an unresolved proposition without concluding failure or success. |
| [Single effect after retry](v0.1/recovery-001-recovery-004.json) and [duplicate effects](v0.1/recovery-001-recovery-005.json) | The supplied effect counts and request identifiers differ. Neither record establishes a human decision. |

The builder uses no outcome files, expected labels or database queries. It preserves contradictions that exist across record classes; it rejects structurally malformed or internally inconsistent packet fields. A stored state is still an authored record, not an independently corroborated institutional event.

Reproduce or check these files using the commands in the [sandbox README](../README.md#evidence-eligibility-checkpoint). No new case was executed to create these appendices. Their generation is evidence preparation, not an assessment study or new validation sample.
