# Convergence Analysis — Week 5

## A1 & A2: Iterations vs. Beta (1,200 nodes, tol = 1e-10)

| Beta | Iterations | Time (s) | Top 3 Nodes |
|---|---|---|---|
| 0.50 | 14 | 0.012 | p00009, p00001, p00006 |
| 0.70 | 17 | 0.013 | p00009, p00001, p00006 |
| 0.85 | 20 | 0.015 | p00009, p00001, p00006 |
| 0.95 | 23 | 0.021 | p00009, p00001, p00006 |
| 0.99 | 24 | 0.020 | p00009, p00001, p00006 |

## A3: Curve Shape and Asymptotic Behavior

As $\beta \to 1$, the number of iterations required to converge increases monotonically. In the PageRank power iteration equation $r^{(k+1)} = \beta M r^{(k)} + (1 - \beta) e / n$, the second eigenvalue of the Google matrix is bounded by $\beta$. Consequently, the error contraction per iteration is governed by $\beta^k$. As $\beta$ approaches 1, $\beta^k$ decays much more slowly ($\lim_{\beta \to 1} \ln \beta = 0$), requiring more matrix-vector passes to squeeze the L1 delta below $10^{-10}$.

## A4: Effect of Graph Size (1,200 vs 6,000 nodes, 5x scale)

| Nodes | Beta | Tol | Iterations | Time (s) |
|---|---|---|---|---|
| 1,200 | 0.85 | 1e-10 | 20 | 0.015 |
| 6,000 | 0.85 | 1e-10 | 22 | 0.105 |
| 1,200 | 0.95 | 1e-10 | 23 | 0.021 |
| 6,000 | 0.95 | 1e-10 | 24 | 0.115 |

- **Iteration count**: Remains virtually invariant to graph size (20 vs 22 for $\beta = 0.85$, 23 vs 24 for $\beta = 0.95$). This occurs because convergence rate is dictated by the spectral gap $1 - \beta$, which is independent of matrix dimension $N$.
- **Wall time**: Scales linearly with graph size and edge count ($0.015s \to 0.105s$, a ~7x increase corresponding to the ~5x increase in nodes and edges). Each power iteration performs work proportional to $O(|E| + |V|)$.

## A5: Effect of Tolerance ($10^{-6}$ vs $10^{-10}$)

| Tolerance | Beta | Nodes | Iterations | Time (s) |
|---|---|---|---|---|
| 1e-06 | 0.85 | 1,200 | 12 | 0.009 |
| 1e-10 | 0.85 | 1,200 | 20 | 0.015 |

Moving from $10^{-6}$ to $10^{-10}$ costs exactly 8 additional iterations for 4 decimal orders of magnitude, or roughly 2 iterations per extra digit of precision. This matches $\beta^2 = 0.85^2 \approx 0.72$ contracting error geometrically.

## A6: Top-10 Ranking Stability

- At $\beta = 0.50$, ranks 7 and 8 are `['p00000', 'p00004']`.
- At $\beta = 0.70, 0.85, 0.95, 0.99$, ranks 7 and 8 swap to `['p00004', 'p00000']`.
- The top 6 items (`p00009`, `p00001`, `p00006`, `p00005`, `p00003`, `p00002`) remain perfectly stable across all values of $\beta$. The first ranking change occurs between $\beta = 0.50$ and $\beta = 0.70$ on marginally distinguished nodes. Because relative ranks depend on link topology vs. uniform damping, tuning $\beta$ alters ranking of borderline pages.

## A7: Hardware Environment

- **Platform**: Windows 11 (10.0.26300-SP0)
- **Processor**: Intel64 Family 6 Model 170 Stepping 4 (Intel Core Ultra 7)
- **Python**: 3.12.6

