# Candidate Explosion Analysis — Week 6

## A1, A2 & A3: Support Threshold vs. Memory and Counters

| Support | Frequent Pairs | Peak Counters | Memory (MB) | Wall Time (s) | Growth Factor (Counters) |
|---|---|---|---|---|---|
| 400 | 249 | 10,585 | 1.1 MB | 1.29s | Baseline |
| 200 | 776 | 58,626 | 6.4 MB | 2.33s | 5.54x |
| 100 | 2,244 | 273,701 | 26.4 MB | 3.97s | 4.67x |
| 50 | 6,397 | 820,259 | 102.2 MB | 7.74s | 3.00x |
| 25 | 17,045 | 893,456 | 102.2 MB | 8.58s | Saturated |
| 12 | 43,116 | 893,456 | 102.8 MB | 8.14s | Saturated |

## A4: Counter Growth Rate

Counters grow significantly faster than doubling per halving. Halving support from 400 to 200 multiplied pair counters by 5.54x ($10,585 \to 58,626$). Halving again from 200 to 100 multiplied counters by 4.67x ($58,626 \to 273,701$). This super-linear explosion occurs because lowering the support threshold admits more items into $L_1$; the candidate pair space in Pass 2 scales quadratically as $\binom{|L_1|}{2} \approx \frac{1}{2} |L_1|^2$. Once nearly all active items pass the singleton threshold (at support $\le 25$), the candidate pool saturates at 893,456 pairs, holding over 102 MB in RAM purely for Python hash counters.

## A5: The Gap Between Candidates and Answers

At support 50:
- **Frequent pairs found (true answers)**: 6,397
- **Peak counters tracked in Pass 2**: 820,259
- **Wasted counter ratio**: $\frac{820,259 - 6,397}{820,259} = 99.22\%$

While the number of true frequent pairs grows smoothly from 249 to 6,397, the candidate counters explode to nearly a million. More than 99% of memory is squandered keeping counters for pairs that fail to meet the threshold. For any practitioner seeking "just a slightly lower threshold", this quadratic candidate explosion rapidly triggers out-of-memory crashes long before the result set becomes meaningfully large. This divergence is precisely why hash-filtering algorithms like PCY are essential.

## A6: Hardware Specifications

- **Platform**: Windows 11 (10.0.26300-SP0)
- **Processor**: Intel64 Family 6 Model 170 Stepping 4 (Intel Core Ultra 7)
- **RAM**: 16 GB
- **Python**: 3.12.6

