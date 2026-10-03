# Response contract review

The archived failures are rejections under our research protocol. They cannot all be described as violations of a fully specified TypeSafe tolerance. The provider's SDK reference explicitly permits approximate probability sums, without defining the numerical tolerance. This distinction changes the interpretation of exclusions; the historical analyses remain unchanged.

Reviewed 3 October 2026. No new model requests, normalization, relabeling or rescoring.

## Documentation and implementation

| Source | Observed contract | Implication |
| :--- | :--- | :--- |
| [HTTP API](https://docs.typesafe.ai/api) and [Choice guide](https://docs.typesafe.ai/primitives/choice) | Probabilities sum to one; the selected option has maximal probability | Describes the intended distribution, without an explicit serialization tolerance |
| [Python response reference](https://docs.typesafe.ai/sdk/python/api/types/responses) | Probability values sum to “approximately 1” | Our 0.00001 tolerance is not a stated provider requirement |
| Python SDK 0.7.2, ChoiceAnswer definitions | Typed float mapping; inspected classes have no sum validator | Parsing an SDK object is distinct from our stricter research acceptance |
| Frozen CEC validator | Exact option set, finite bounded values, maximal choice, sum tolerance 0.00001, whole-response acceptance | Any failing answer excludes all answers in that response under the study contract |

The SDK source inspection used the published [0.7.2 package](https://pypi.org/project/typesafe-sdk/0.7.2/), wheel `typesafe_sdk-0.7.2-py3-none-any.whl`, SHA-256 `0a961148187d52e18276ed7f2d02617cfac48e3b97673cb631a8749397d43d1e`, verified against package metadata. Inspected `typesafe_sdk/_schemas/models.py` and `_core/response_types.py`: ChoiceAnswer declares a float mapping and the wrapper sets strict, frozen parsing. No sum check appears in those classes. This is static inspection, not a runtime SDK acceptance test or an exhaustive audit of every client path. No dependency was installed. The SDK documentation also exposes a request ID and raw HTTP response; our current transport retains response bodies but omits those response headers.

## What the saved responses show

The [located observations](observations.json) cover exactly the instruction-comparison and packet-linkage live archives. There are 19 failing distributions in 17 rejected responses: 14 in the instruction comparison and five in three packet-linkage responses. Each failing sum is approximately 0.99. This is not a corpus-wide service error rate; the cases are selected and related.

Whole-response acceptance excludes 68 judgments across these two archives, while 19 distributions fail the sum check. The other 49 satisfy the sum rule; that alone does not establish full validity or substantive correctness. These counts describe the cost of the chosen exclusion unit. They do not authorize changing the historical primary denominators.

A 0.01 deficit is compatible with some rounding schemes, but the inspected sources do not specify the scheme that generated these outputs. Do not claim confirmed rounding, provider fault, or a universal acceptable tolerance. Missing evidence, ambiguous classification, low confidence and serialization discrepancies require separate statuses.

## Recommended next contract

Prepare a separately versioned offline sensitivity protocol before calculating any alternative result. Preserve original bytes and official scores. Compare whole-response exclusion with answer-level eligibility while holding the numerical rule fixed first; investigate tolerance changes as a separate factor. Do not choose a tolerance because it restores a favorable result. A rounding-derived tolerance requires an explicit, justified precision assumption, clearly distinguished from provider confirmation.

Retain exact option coverage, finite bounded values, selected-label checks and model identity. Store raw sums and discrepancies beside every answer. Confidence-based routing should be a separate decision layer, with thresholds evaluated on suitable data. Any normalized distribution must be a derived artifact with its transformation disclosed; do not substitute it for the provider output or silently compute calibrated-loss claims from it.

For future live runs, capture allowlisted diagnostic headers such as the provider request ID, avoiding credentials and unrelated headers. A minimal provider question would ask about serialization precision, expected sum tolerance and whether SDK parsing applies normalization. No message has been sent to TypeSafe.

After this contract work, test structured, dimension-specific criteria with narrow propositions. The [structured-question guide](https://docs.typesafe.ai/primitives/advanced) and [citation cookbook](https://docs.typesafe.ai/cookbooks/citation_check) support separating exact source checks in code from semantic support judgments. Keep uncertainty routing outside the eight evidence labels. Evaluate option-order sensitivity separately, as recommended in the [model limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13). No cookbook threshold is adopted as a corpus standard.

The immediate correction is interpretive: “invalid” in the frozen reports means invalid under the stated study rule. TAE and HIT remain unchanged, and no empirical human-control claim follows from SDK compatibility.

The separate [acceptance-unit sensitivity](SENSITIVITY.md) now quantifies coverage under the unchanged numerical tolerance.
