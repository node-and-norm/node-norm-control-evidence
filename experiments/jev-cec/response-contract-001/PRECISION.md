# Offline numerical precision investigation

Exact decimal parsing reproduces all 19 probability-sum failures in the two reviewed archives. Switching from binary floating-point summation to decimal arithmetic therefore does not remove them under the existing tolerance.

The [audit script](precision.py) verifies response hashes and parses JSON decimal tokens without first converting them to binary floats. Its [located report](precision.json) covers 512 distributions: 480 from the instruction comparison and 32 from the packet-linkage diagnostic. The respective failure counts remain 14 and five at absolute tolerance 0.00001.

All 512 distributions contain probabilities within 0.000000000001 of a hundredth. Some raw JSON numbers retain small representation tails. This describes the received values. It does not establish the provider's internal precision, rounding direction, normalization procedure or generation mechanism.

## Hypothetical rounding bound

If an eight-option normalized distribution were independently rounded to the nearest hundredth, each entry's absolute rounding error would be at most 0.005. The triangle inequality gives a maximum sum discrepancy of 8 × 0.005 = 0.04. A 0.01 deficit is compatible with that hypothetical process.

Compatibility is not confirmation. Truncation, intermediate processing and other mechanisms can produce similar values. The bound also admits discrepancies larger than those observed, so adopting 0.04 solely to recover exclusions would lack a verified provider contract. No numerical tolerance is changed here, and no probabilities or confidence values are reconstructed.

## Conclusion for the next diagnostic

Proceed with the separately specified [answer eligibility contract](ANSWER-CONTRACT.md) while retaining the current tolerance until a prospective numerical policy is justified. Ask the provider about serialization precision, sum tolerance and the relationship between returned confidence and displayed probabilities before attributing these discrepancies to a service defect. No provider message was sent.

This investigation is post-output analysis of selected synthetic experiments. It provides no new model inference, accuracy estimate or validation of TAE and HIT.
