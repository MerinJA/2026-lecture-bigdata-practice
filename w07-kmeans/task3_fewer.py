#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """Your k-means.

        __init__(k, max_iter=50)
        run(points, initial_centroids, distance) -> (labels, centroids)

    Same starting centroids, same `distance` function - which is counted. That
    counter is your score.

    The idea, from §7.3 and the triangle inequality:

        if a point is much closer to its current centroid than that centroid
        moved, and than any other centroid could have come, then it cannot have
        changed cluster, and you do not have to measure anything

    Keeping enough bookkeeping to make that test cheap, without keeping so much
    that the bookkeeping costs more than the distances, is the task.

    You may call `distance` on two centroids, and those calls are counted too -
    which is the correct accounting, since that is real work. There are k of
    them and n points, and k is much smaller than n. That asymmetry is the
    whole opening.
    """

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter
        self.iterations = 0

    def run(self, points, initial_centroids, distance):
        k = self.k
        n = len(points)
        centroids = [tuple(c) for c in initial_centroids]
        labels = [0] * n
        u = [0.0] * n
        l = [[0.0] * k for _ in range(n)]

        # Initial pass: compute exact distance from each point to every centroid
        for i, p in enumerate(points):
            best_d, best_j = float("inf"), 0
            for j, c in enumerate(centroids):
                dist = distance(p, c)
                l[i][j] = dist
                if dist < best_d - 1e-12:
                    best_d, best_j = dist, j
            labels[i] = best_j
            u[i] = best_d

        for it in range(1, self.max_iter + 1):
            self.iterations = it
            new_centroids = _means(points, labels, k, centroids)

            # Distances each centroid moved
            deltas = [distance(c, nc) for c, nc in zip(centroids, new_centroids)]
            if max(deltas) < 1e-12:
                centroids = new_centroids
                break

            # Precompute pairwise distances between all centroids
            c_dist = [[0.0] * k for _ in range(k)]
            s = [float("inf")] * k
            for j1 in range(k):
                for j2 in range(j1 + 1, k):
                    cd = distance(new_centroids[j1], new_centroids[j2])
                    c_dist[j1][j2] = cd
                    c_dist[j2][j1] = cd
                    if cd < s[j1]:
                        s[j1] = cd
                    if cd < s[j2]:
                        s[j2] = cd
            s = [0.5 * val for val in s]

            # Update upper and lower bounds based on centroid movement
            for i in range(n):
                u[i] += deltas[labels[i]]
                for j in range(k):
                    l[i][j] = max(0.0, l[i][j] - deltas[j])

            centroids = new_centroids
            changed = False

            for i, p in enumerate(points):
                cur = labels[i]
                # Test 1: if upper bound <= half distance to nearest other centroid
                if u[i] <= s[cur]:
                    continue

                r = True  # whether u[i] is an upper bound rather than exact
                for j in range(k):
                    if j == cur:
                        continue
                    if u[i] <= l[i][j] or u[i] <= 0.5 * c_dist[cur][j]:
                        continue
                    if r:
                        exact_d = distance(p, centroids[cur])
                        u[i] = exact_d
                        l[i][cur] = exact_d
                        r = False
                        if exact_d <= l[i][j] or exact_d <= 0.5 * c_dist[cur][j]:
                            continue

                    dist = distance(p, centroids[j])
                    l[i][j] = dist
                    if dist < u[i] - 1e-12:
                        cur = j
                        labels[i] = j
                        u[i] = dist
                        changed = True

            if not changed:
                break

        return labels, centroids
