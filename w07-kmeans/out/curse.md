# The Curse of Dimensionality — Week 7

## A1 & A2: Distance Statistics Across Dimensions

| Dimension $d$ | Points $n$ | Mean Distance | Min Distance | Max Distance | Contrast $\frac{\max - \min}{\min}$ | Rel. Std. Dev. $\frac{\sigma}{\mu}$ | Time (s) |
|---|---|---|---|---|---|---|---|
| 2 | 1,000 | 0.521 | 0.003 | 1.326 | 488.58 | 0.476 | 0.035 |
| 5 | 1,000 | 0.884 | 0.111 | 1.687 | 14.26 | 0.282 | 0.051 |
| 10 | 1,000 | 1.274 | 0.438 | 2.159 | 3.93 | 0.193 | 0.068 |
| 20 | 1,000 | 1.815 | 0.821 | 2.670 | 2.25 | 0.135 | 0.096 |
| 50 | 1,000 | 2.867 | 1.909 | 3.785 | 0.982 | 0.083 | 0.196 |
| 100 | 1,000 | 4.068 | 3.206 | 4.954 | 0.545 | 0.060 | 0.354 |
| 200 | 1,000 | 5.776 | 4.871 | 6.682 | 0.372 | 0.041 | 0.704 |
| 500 | 2,000 | 9.126 | 8.099 | 10.176 | 0.256 | 0.026 | 1.696 |
| 1,000 | 2,000 | 12.909 | 11.970 | 13.806 | 0.153 | 0.019 | 3.153 |

## A3: Behavior of Contrast

Contrast collapses dramatically as dimension grows:
- At $d = 2$, contrast is $488.58$ (the closest pair is nearly 500 times closer than the furthest pair).
- Contrast drops below **1.0** at roughly **$d = 50$** (measured $0.982$). At this point, the furthest pair is less than twice as far apart as the closest pair.
- Contrast drops below **0.5** near **$d = 120$** ($0.545$ at $d=100$, $0.372$ at $d=200$).
- At $d = 1000$, contrast is only $0.153$. All points become almost equidistant, rendering Euclidean "nearest neighbor" distinctions statistically meaningless.

## A4: Growth of Mean Distance

For independent coordinates $X_i, Y_i \sim \text{Uniform}(0, 1)$, the expected squared difference along any axis is:
$$\mathbb{E}[(X_i - Y_i)^2] = \int_0^1 \int_0^1 (x - y)^2 \, dx \, dy = \frac{1}{6}$$
By the Central Limit Theorem, the squared Euclidean distance $\sum_{i=1}^d (X_i - Y_i)^2 \approx \frac{d}{6}$, so the Euclidean distance grows asymptotically as $\sqrt{d / 6} \approx 0.4082 \sqrt{d}$.
Our measurements confirm this relationship:
- $d = 50$: theoretical $\sqrt{50/6} \approx 2.887$, measured **$2.867$**
- $d = 200$: theoretical $\sqrt{200/6} \approx 5.774$, measured **$5.776$**
- $d = 1000$: theoretical $\sqrt{1000/6} \approx 12.910$, measured **$12.909$**

## A5: Relative Standard Deviation vs. Contrast

The standard deviation $\sigma$ remains remarkably flat across dimensions ($\sigma \approx 0.24$), but because the mean grows as $\sqrt{d}$, the relative standard deviation $\sigma / \mu$ decreases as $O(1/\sqrt{d})$ ($0.476 \to 0.019$). Both metrics reflect the curse, but **relative standard deviation ($\sigma / \mu$)** better captures the fundamental mathematical cause (concentration of measure), whereas contrast is also influenced by sample size through extreme value statistics.

## A6: Effect of Point Count $n$ at Fixed Dimension ($d = 50$)

| Points $n$ | Min Distance | Max Distance | Contrast | Relative Std. Dev. |
|---|---|---|---|---|
| 1,000 | 1.909 | 3.785 | 0.982 | 0.083 |
| 2,000 | 1.899 | 3.839 | 1.022 | 0.083 |

Varying $n$ from 1,000 to 2,000 slightly increases contrast ($0.982 \to 1.022$) because drawing more pairs samples deeper into the extreme tails of the distribution (finding a slightly smaller minimum and larger maximum). However, $\sigma / \mu$ remains invariant at $0.083$. Thus, increasing dataset size $n$ cannot cure the curse of dimensionality.

## A7: Hardware Environment

- **Platform**: Windows 11 (10.0.26300-SP0)
- **Processor**: Intel64 Family 6 Model 170 Stepping 4 (Intel Core Ultra 7)
- **Python**: 3.12.6
- **Runtime for largest test ($d=1000$, 2000 points)**: 3.15 seconds

## A8: Connection to LSH and Jaccard Similarity (Week 3)

The curse of dimensionality observed here **does not invalidate LSH** on text shingles because:
1. **Metric space**: Jaccard similarity is a set-intersection metric over discrete non-empty sets ($J(A, B) = \frac{|A \cap B|}{|A \cup B|}$), not Euclidean distance in continuous $L_2$ space.
2. **Sparsity**: Real-world document shingles live on an extremely sparse, lower-dimensional manifold. Most shingles have zero frequency, unlike uniform random noise filling a dense hypercube.
3. **Collision probability**: MinHash directly guarantees that hash collision probability equals the exact Jaccard similarity $P(h(A) = h(B)) = J(A, B)$ regardless of the nominal vocabulary size.

