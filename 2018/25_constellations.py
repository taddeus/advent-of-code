#!/usr/bin/env python3
import sys
from itertools import combinations, product

def dist(a, b):
    return sum(abs(y - x) for x, y in zip(a, b))


# iteratively make the first constellations
const = []
for line in sys.stdin:
    a = tuple(map(int, line.rstrip().split(',')))
    for c in const:
        if any(dist(a, b) <= 3 for b in c):
            c.append(a)
            break
    else:
        const.append([a])

# merge constellations where possible
prevlen = None

while len(const) != prevlen:
    prevlen = len(const)

    for i, j in combinations(range(prevlen), 2):
        c1 = const[i]
        c2 = const[j]
        if any(dist(a, b) <= 3 for a, b in product(c1, c2)):
            const[i] = c1 + c2
            const[j] = []

    const = list(filter(None, const))

print(len(const))
