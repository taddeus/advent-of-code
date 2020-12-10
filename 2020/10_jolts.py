#!/usr/bin/env python3
import sys
from functools import lru_cache
from itertools import combinations

def diffs(adapters):
    prev = 0
    for jolts in adapters:
        yield jolts - prev
        prev = jolts
    yield 3

def mul_diffs(adapters):
    d = list(diffs(adapters))
    return d.count(1) * d.count(3)

def arrangements(adapters):
    graph = {}
    for a, b in combinations([0] + adapters, 2):
        if b - a <= 3:
            graph.setdefault(a, []).append(b)

    @lru_cache(maxsize=None)
    def walk(node):
        if node == adapters[-1]:
            return 1
        elif not graph[node]:
            return 0
        return sum(map(walk, graph[node]))

    return walk(0)

adapters = sorted(map(int, sys.stdin))
print(mul_diffs(adapters))
print(arrangements(adapters))
