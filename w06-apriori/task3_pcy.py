#!/usr/bin/env python3
"""Week 6 · Task 3 — Make pass two fit.

Textbook §6.3 (PCY), §6.3.2 - §6.3.4.

`PlainApriori` does what Task 1 asked: use pass one to drop infrequent items,
then count every pair of surviving items. That is already much better than
counting all pairs. It is still not enough, because the surviving items are the
common ones, and the common ones appear together constantly.

The harness measures **the peak number of pair counters you held**, because
that is the thing that decides whether the algorithm runs at all. §6.3 is about
spending pass one's spare memory to shrink it.

    python3 bench.py
    python3 bench.py --yours

Correctness first: you must find exactly the same frequent pairs. Finding fewer
is not an optimisation.
"""
from collections import Counter
from itertools import combinations


class PlainApriori:
    """Pass one drops infrequent items. Pass two counts every surviving pair."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()
        for basket in baskets:
            counts.update(basket)
        frequent = {i for i, c in counts.items() if c >= self.support}

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(basket & frequent)
            for pair in combinations(items, 2):
                pair_counts[pair] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}


class YourAlgorithm:
    """Your frequent-pair finder.

        __init__(support)
        run(baskets) -> {frozenset({a, b}): count}
        .peak_counters -> the most pair counters you ever held at once

    Same pairs as the baseline. Fewer counters.

    Pass one only needs one integer per item, and there are not many items. The
    rest of your memory is sitting idle while you do it. §6.3 spends it: hash
    every pair you see in pass one into a fixed array of buckets, and count the
    buckets rather than the pairs.

    A bucket whose total is below the support threshold cannot contain a
    frequent pair. In pass two you skip every pair landing in such a bucket -
    and the bucket array collapses to a bitmap, one bit each, before you need
    the memory for counters.

    Two things to be careful of:

      * a bucket being frequent does not make its pairs frequent. It is a
        filter, not an answer
      * `peak_counters` is on your honour. Count the pair counters you hold at
        the same time. The bitmap is not a pair counter, but if you keep the
        full bucket counts alive into pass two, that is not free either -
        observation.md asks about it
    """

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        # PCY algorithm with bucket hashing in Pass 1, collapsed to a bitmap for Pass 2
        num_buckets = 1_000_003
        item_counts = Counter()
        buckets = [0] * num_buckets

        # Pass 1: count items and hash pairs to buckets
        for basket in baskets:
            item_counts.update(basket)
            items = sorted(basket)
            n_items = len(items)
            for i in range(n_items):
                ai = items[i] * 2003
                for j in range(i + 1, n_items):
                    h = (ai + items[j] * 997) % num_buckets
                    buckets[h] += 1

        frequent = {i for i, c in item_counts.items() if c >= self.support}
        # Collapse buckets into a compact bitmap (bytearray) before Pass 2
        bitmap = bytearray(1 if c >= self.support else 0 for c in buckets)
        del buckets

        # Pass 2: count pairs of frequent items only if their bucket is frequent
        pair_counts = Counter()
        self.peak_counters = 0

        for basket in baskets:
            items = sorted(basket & frequent)
            n_items = len(items)
            for i in range(n_items):
                ai = items[i] * 2003
                for j in range(i + 1, n_items):
                    h = (ai + items[j] * 997) % num_buckets
                    if bitmap[h]:
                        pair_counts[(items[i], items[j])] += 1
            if len(pair_counts) > self.peak_counters:
                self.peak_counters = len(pair_counts)

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}
