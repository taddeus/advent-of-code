#!/usr/bin/env python3
import sys

def parse(f):
    graph = {}
    for line in f:
        a, b = line.rstrip().split('-')
        if b != 'start' and a != 'end':
            graph.setdefault(a, []).append(b)
        if a != 'start' and b != 'end':
            graph.setdefault(b, []).append(a)
    return graph

def paths(graph, may_dup):
    work = [('start', {'start'}, not may_dup)]
    distinct = 0
    while work:
        prev, visited, dup = work.pop()
        for nb in graph[prev]:
            if nb == 'end':
                distinct += 1
            elif nb.isupper() or nb not in visited:
                work.append((nb, visited | {nb}, dup))
            elif not dup:
                work.append((nb, visited, True))
    return distinct

graph = parse(sys.stdin)
print(paths(graph, False))
print(paths(graph, True))
