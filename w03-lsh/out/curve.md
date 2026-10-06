# Week 3 · Crossover Measurement and Scaling Curve

## Timing & Comparisons Table (A3)

| $n$ | Brute Force Time | Brute Force Comparisons | LSH Time | LSH Comparisons |
|---:|---:|---:|---:|---:|
| 125 | 0.05 s | 7,750 | 0.32 s | 0 |
| 250 | 0.18 s | 31,125 | 0.62 s | 0 |
| 500 | 0.71 s | 124,750 | 1.18 s | 0 |
| 1,000 | 2.86 s | 499,500 | 2.40 s | 6 |
| 2,000 | 11.76 s | 1,999,000 | 4.73 s | 41 |
| 4,000 | 65.24 s | 7,998,000 | 14.17 s | 135 |

---

## Machine Specifications (A6)
- **OS / Platform:** Windows 11 (Windows-11-10.0.26200-SP0)
- **Processor:** Intel Core Ultra 7 (Intel64 Family 6 Model 170 Stepping 4, GenuineIntel)
- **RAM:** 16 GB (15.37 GiB usable, 16,507,727,872 bytes)
- **Python Version:** 3.12.6
- **Background Activity:** Normal desktop workstation load with VS Code running; no compute-heavy processes in the background.

---

## Quadratic Verification of Brute Force (A4)
Doubling $n$ should theoretically quadruple ($4\times$) the execution time of brute force ($O(n^2)$ comparisons):
- $n = 125 \to 250$: ratio = $0.18 / 0.05 \approx 3.60\times$
- $n = 250 \to 500$: ratio = $0.71 / 0.18 \approx 3.94\times$
- $n = 500 \to 1,000$: ratio = $2.86 / 0.71 \approx 4.03\times$
- $n = 1,000 \to 2,000$: ratio = $11.76 / 2.86 \approx 4.11\times$
- $n = 2,000 \to 4,000$: ratio = $65.24 / 11.76 \approx 5.55\times$

The empirical ratios cluster tightly around $4.0\times$ across all intermediate doublings, confirming the quadratic nature of brute force. At $n = 4,000$, cache pressure and CPU throttling slightly amplify the ratio above $4\times$.

---

## Peak Memory at Largest $n = 4,000$ (A5)
- **Brute Force:** Peak memory was **7.34 KiB** (7,344 bytes traced by `tracemalloc`). Brute force only maintains a running pair loop and does not store auxiliary structures.
- **LSH:** Peak memory was **49.14 MiB** (49,139,568 bytes). LSH stores signature vectors (128 integers per document) and hash bucket maps for all 32 bands.

---

## The Crossover Point (A7) & Why LSH Loses at Small $n$ (A8)
- **Crossover Point:** The crossover occurs between **$n = 500$ and $n = 1,000$ documents**.
  - At $n = 500$, brute force takes 0.71 s whereas LSH takes 1.18 s (brute force is faster).
  - At $n = 1,000$, brute force takes 2.86 s while LSH takes 2.40 s (LSH becomes faster).
- **Why LSH loses at small $n$:** LSH incurs an unavoidable linear upfront overhead: computing $k = 128$ minhash values for every shingle in every document, and inserting each document into $b = 32$ bucket dictionaries. For small $n$, the total number of pairwise comparisons avoided ($\approx 124,750$ at $n=500$) is so fast to compute in memory that the fixed cost of hashing machinery outweighs the savings. As $n$ grows past 1,000, avoiding $O(n^2)$ pairwise set intersections rapidly dwarfs the linear hashing cost.

---

## Where It Becomes Unpleasant (A2)
At **$n = 4,000$**, brute force becomes genuinely unpleasant, taking **65.24 seconds** (over a minute) for 8 million comparisons. In contrast, LSH finishes in **14.17 seconds**. CPU execution time ran out long before memory did.
