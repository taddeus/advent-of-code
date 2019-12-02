#!/usr/bin/env python3
import sys
from operator import mul
from functools import reduce

def groups_with_sum(l, s):
    worklist = [(s, [], sorted(l))]
    while worklist:
        remain, group, picks = worklist.pop()
        for i, pick in enumerate(picks):
            if pick == remain:
                yield group + [pick]
            elif pick < remain:
                worklist.append((remain - pick, group + [pick], picks[i + 1:]))

def min_qe(weights, ngroups):
    groups = groups_with_sum(weights, sum(weights) // ngroups)
    return min((len(g), reduce(mul, g)) for g in groups)[1]

weights = list(map(int, sys.stdin))
print(min_qe(weights, 3))
print(min_qe(weights, 4))
