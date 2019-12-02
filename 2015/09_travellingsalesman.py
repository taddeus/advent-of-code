#!/usr/bin/env python3
import sys
import re
from itertools import permutations

graph = {}
for line in sys.stdin:
    src, dest, dist = re.match(r'(\w+) to (\w+) = (\d+)', line).groups()
    graph.setdefault(src, {})[dest] = int(dist)
    graph.setdefault(dest, {})[src] = int(dist)

def pathlength(path):
    length = 0
    for i, node in enumerate(path[:-1]):
        connections = graph[node]
        nextnode = path[i + 1]
        if nextnode not in connections:
            return
        length += connections[nextnode]
    return length

lens = list(filter(None, map(pathlength, permutations(graph))))
print(min(lens))
print(max(lens))
