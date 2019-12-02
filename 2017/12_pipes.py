#!/usr/bin/env python3
import sys

def parse(f):
    graph = []
    for i, line in enumerate(f):
        left, right = line.rstrip().split(' <-> ')
        assert int(left) == i
        graph.append([int(nb) for nb in right.split(', ')])
    return graph

def find_groups(graph):
    def dfs(i, group):
        groups[i] = group
        for nb in graph[i]:
            if groups[nb] is None:
                dfs(nb, group)

    groups = [None] * len(graph)
    group = 0
    for start, known_group in enumerate(groups):
        if known_group is None:
            dfs(start, group)
            group += 1
    return groups

groups = find_groups(parse(sys.stdin))
print(sum(1 for g in groups if g == groups[0]))
print(len(set(groups)))
