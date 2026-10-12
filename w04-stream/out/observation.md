# Observations — Week 4

A Bloom filter cannot produce false negatives: each insertion sets to 1 the exact bit positions verified during membership lookup. The observed false positive rate of 0.755% closely matches the theoretical prediction of 0.860%.

The memory required by the exact set grows from 3.9 MB to 46.6 MB when the stream scales by 16x, whereas Flajolet-Martin remains strictly constant at 4.4 KB. Its distinct element estimate fluctuates within 0.58x to 1.15x of the true value, which is the expected tradeoff for fixed-size memory estimation.

With 10 bits per item, optimal hash count is k = 10 * ln(2) = 6.93, yielding 7 hashes. The theoretical floor is approximately 0.819%; our filter achieves 0.820% with zero false negatives. When n is unknown, underestimating leads to elevated false positives, while overestimating wastes memory budget.
