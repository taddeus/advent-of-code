#!/usr/bin/env python3
import sys
from collections import Counter

coords = [tuple(map(int, line.split(', '))) for line in sys.stdin]
W = max(x for x, y in coords) + 1
H = max(y for x, y in coords) + 1

# part 1
grid = W * H * [-1]
dist = W * H * [W * H + 1]

for i, (x, y) in enumerate(coords):
    for j, d in enumerate(dist):
        dy, dx = divmod(j, W)
        newd = abs(dx - x) + abs(dy - y)
        if newd < d:
            dist[j] = newd
            grid[j] = i
        elif newd == d:
            grid[j] = -1

def is_edge(y, x): return y in (0, H - 1) or x in (0, W - 1)
edges = set(c for i, c in enumerate(grid) if is_edge(*divmod(i, W)))
edges.add(-1)
print(Counter(c for c in grid if c not in edges).most_common(1)[0][1])

# part 2
dist = W * H * [0]

for i, (x, y) in enumerate(coords):
    for j, d in enumerate(dist):
        dy, dx = divmod(j, W)
        dist[j] += abs(dx - x) + abs(dy - y)

print(sum(1 for d in dist if d < 10000))
