# Offline acceptance-unit sensitivity

Keeping the frozen probability tolerance while evaluating each answer separately retains 49 additional judgments across the two named archives. This measures the effect of the acceptance unit on coverage. It establishes no improvement in model judgment.

This analysis was selected after inspecting outputs and the SDK contract. It is exploratory, not a replacement primary analysis. There are no new API calls, repaired probabilities, changed reference labels, alternative accuracy scores or tolerance changes.

## Fixed rule and changed unit

The numerical tolerance remains absolute 0.00001. Each answer must have the exact eight labels, finite bounded probability and confidence values, a valid Choice type and a selected label at the distribution maximum. Model identity, expected answer identifiers, HTTP success and nonnegative integer usage remain response-level prerequisites. The alternative accepts each passing answer even when another answer in the response fails. Original whole-response acceptance is taken from the archived attempt record.

The [script](sensitivity.py) verifies raw response hashes, preserves each judgment's location and produces the [complete report](sensitivity.json). Its envelope handling targets these two complete, JSON-readable archives. It is an analysis tool, not a new production validator for arbitrary malformed responses.

| Archive | Scheduled judgments | Original whole-response eligible | Alternative answer-level eligible | Newly eligible |
| :--- | ---: | ---: | ---: | ---: |
| Instruction comparison | 480 | 424 | 466 | 42 |
| Packet linkage | 32 | 20 | 27 | 7 |

These archives contain related, selected synthetic examples. The counts should not be interpreted as a population validity rate. Each newly eligible judgment passes the same numerical and answer checks; passing does not establish that its evidence classification is correct.

| Archive / pass / condition | Scheduled | Whole-response | Answer-level |
| :--- | ---: | ---: | ---: |
| Instruction / 1 / A | 120 | 108 | 117 |
| Instruction / 1 / B | 120 | 104 | 116 |
| Instruction / 2 / A | 120 | 108 | 117 |
| Instruction / 2 / B | 120 | 104 | 116 |
| Linkage / 1 / original | 8 | 4 | 6 |
| Linkage / 1 / explicit | 8 | 0 | 5 |
| Linkage / 2 / original | 8 | 8 | 8 |
| Linkage / 2 / explicit | 8 | 8 | 8 |

These are individual-judgment coverage counts. They are not counts of eligible action pairs and cannot substitute for paired comparison denominators. No previously unavailable primary comparison is promoted to an official result here.

## Recommendation

For the next independently specified diagnostic, separate response-envelope checks from answer-level eligibility. This avoids excluding a well-formed answer solely because an unrelated answer fails. Keep strict exclusions available as a parallel sensitivity view, disclose the changed rule prospectively and retain all raw bytes. Joint decisions must still require every answer they depend on; answer-level eligibility does not make an incomplete multi-answer decision usable.

Do not relax the numerical tolerance on the basis of these coverage gains. A separate precision investigation is needed before changing it, since the SDK's approximate-sum wording supplies no numerical bound. The original archives and published scores remain authoritative under their frozen protocols. This result supports reconsidering the acceptance unit, without resolving distribution precision or substantive evidence disagreements.
