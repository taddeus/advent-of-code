#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def parse(inp):
    graph = {}
    for line in inp:
        left, right = line.split(': ')
        left_nbs = graph.setdefault(left, {})
        for node in right.split():
            left_nbs[node] = 1
            graph.setdefault(node, {})[left] = 1
    return graph

def cut(graph):
    added = {}
    weights = {v: 0 for v in graph}
    work = [(0, v) for v in graph]
    while work:
        weight, node = heappop(work)
        if weight == weights[node] and node not in added:
            added[node] = -weight
            for nb, nbweight in graph[node].items():
                weights[nb] -= nbweight
                heappush(work, (weights[nb], nb))
    rev = reversed(added)
    a, b = next(rev), next(rev)
    return a, b, added[a]

def merge(graph, a, b):
    a_nbs = graph.pop(a)
    b_nbs = graph.pop(b)
    graph[a + b] = ab_nbs = {}
    for nb, weight in a_nbs.items():
        if nb != b:
            del graph[nb][a]
            graph[nb][a + b] = ab_nbs[nb] = weight
    for nb, weight in b_nbs.items():
        if nb != a:
            del graph[nb][b]
            graph[nb][a + b] = ab_nbs[nb] = ab_nbs.get(nb, 0) + weight

def mincut(graph):
    # https://en.wikipedia.org/wiki/Stoer-Wagner_algorithm
    best = orig_len = len(graph)
    while len(graph) > 1:
        a, b, size = cut(graph)
        if size < best:
            best = size
            half = max(len(a), len(b)) // 3
        merge(graph, a, b)
    return half * (orig_len - half)

graph = parse(sys.stdin)
print(mincut(graph))
