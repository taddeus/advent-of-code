#!/usr/bin/env python3
import sys

def parse(f):
    graph = {}
    for line in f:
        a, b = line.rstrip().split('-')
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return graph

def paths(graph, may_dup):
    work = [(('start',), not may_dup)]
    distinct = 0
    while work:
        path, dup = work.pop()
        if path[-1] == 'end':
            distinct += 1
        else:
            for nb in graph[path[-1]]:
                if nb.isupper() or nb not in path:
                    work.append((path + (nb,), dup))
                elif not dup and nb != 'start':
                    work.append((path + (nb,), True))
    return distinct

graph = parse(sys.stdin)
print(paths(graph, False))
print(paths(graph, True))
