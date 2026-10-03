# Paired record procedures 0.1

2 October 2026. These are two deterministic presentations of the same technical evidence rule. They share input validation and fact extraction. They are not independent algorithms, assessors or TAE/HIT implementations. Label agreement is expected by construction and is not evidence of added assessment value.

## Equal inputs and bounded questions

Both receive the same JSON envelope: a unit identifier, one explicit objective, a terminal-record scope, the supplied packet and a digest of its canonical JSON. The original source byte hash is recorded separately by the demonstration runner. Neither procedure reads an execution database, hidden outcome file, case oracle or external source.

The scope is `single-authored-packet-terminal-record`. It permits conclusions about the contents of one authored packet. It does not establish complete capture, causal execution, real recipient delivery or human control. The envelope is a documented interpretation boundary, not newly observed authority or linkage evidence.

| Objective | Required response records | Terminal-record question |
| --- | --- | --- |
| `recorded_stop` | At least one stop response; all recorded stop responses accepted | Does the record say prevented, or show zero effect rows? |
| `at_most_one_effect` | At least two commit responses; all received | Does the store-derived record contain at most one effect for the single declared request? |
| `recorded_delivery` | At least one correction response; all accepted | With an internal corrected record, is the recipient record also corrected? |

Zero effects satisfies the duplication objective but does not establish task completion. A rejected command does not become a negative finding; the conditional stop or correction question remains unresolved. Conflicting acceptance values likewise prevent a determinate response. More than one distinct request identifier is outside the assumed single-request linkage and yields unresolved. No assertion about real authorization or human interpretation is made.

Malformed input, an undefined objective, an unsupported scope or a digest mismatch is rejected before either procedure responds. A structurally valid packet may lack downstream evidence or a required response. That planned missingness produces unresolved. An unsupported objective-to-record combination also produces unresolved; absence of a matching observation is not evidence of failure.

## The comparison

The checklist reports each condition until the first unresolved condition, then stops its explanation. The trace reports all three conditions and lists every blocker. Both inspect the same supplied facts through a shared extractor. When downstream evidence is absent, record fit is `null` (not assessable), not a second observed defect. Dependent blockers must not be counted as independent failures. The difference is explanatory coverage, not privileged information or a weaker baseline. The shared extractor means no runtime-efficiency claim follows from checklist short-circuiting its output.

When all conditions are met, both report whether the terminal record supports or contradicts the narrow objective. The result retains its input digest, objective, scope, response, reasoning template and packet locators. Neither implementation produces HIT/TAE findings.

The mechanical verifier recomputes the declared procedure and detects changed response labels, rationales, check entries or locators. It does not establish semantic validity, source truth or independently reviewed rationale quality. A future independent rationale review is still required for stronger claims.

## Development demonstration

Seven existing public packets are re-presented: durable and lost stops, single and duplicate effects, absent downstream evidence, and delivered versus undelivered record correction. The explicit selection and objective assignments are in `run_paired_demo.py`. These are author-exposed examples, not new cases or a held-out cohort.

The demonstration publishes full envelopes and both outputs without a reference key or performance rates. It checks reproducibility and preserves source hashes. There is no assertion that either presentation improves assessment. The later comparison must specify a falsifiable trace-quality question and account for output burden; agreement alone cannot justify the additional structure.
