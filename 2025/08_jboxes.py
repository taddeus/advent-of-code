#!/usr/bin/env python3
import sys
from heapq import nlargest
from itertools import combinations

def squared_distance(xa, ya, za, xb, yb, zb):
    return (xa - xb) ** 2 + (ya - yb) ** 2 + (za - zb) ** 2

def connect(boxes, nfirst):
    pairs = sorted((squared_distance(*a, *b), i, j)
                   for (i, a), (j, b) in combinations(enumerate(boxes), 2))
    circuits = [{i} for i in range(len(boxes))]
    for p, (_, i, j) in enumerate(pairs):
        circuits[i].update(circuits[j])
        for k in circuits[j]:
            circuits[k] = circuits[i]
        if p == nfirst - 1:
            uniq = {id(c): c for c in circuits}
            a, b, c = nlargest(3, uniq.values(), key=len)
            largest = len(a) * len(b) * len(c)
        if len(circuits[i]) == len(boxes):
            return largest, boxes[i], boxes[j]

boxes = [tuple(map(int, line.split(','))) for line in sys.stdin]
largest, last1, last2 = connect(boxes, 1000)
print(largest)
print(last1[0] * last2[0])
