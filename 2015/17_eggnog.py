#!/usr/bin/env python3
import sys
from itertools import combinations

def combs(boxes, cap):
    indices = list(range(len(boxes)))
    for l in range(len(boxes), 0, -1):
        fits = 0
        trynext = False
        for picks in combinations(indices, l):
            s = sum(boxes[i] for i in picks)
            if s == cap:
                fits += 1
            trynext |= s > cap
        if not trynext:
            break
        yield l, fits

comb = list(combs(list(map(int, sys.stdin)), 150))
print(sum(c[1] for c in comb))
print(comb[-1][1])
