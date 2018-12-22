#!/usr/bin/env python3
import sys
from heapq import heapify, heappush, heappop

def parse(regex):
    graph = {}
    branches = []
    dirs = {'N': (0, -1), 'W': (-1, 0), 'S': (0, 1), 'E': (1, 0)}
    cur = (0, 0)

    assert regex[0] == '^' and regex[-1] == '$'
    for c in regex[1:-1]:
        if c == '(':
            branches.append(cur)
        elif c == ')':
            cur = branches.pop()
        elif c == '|':
            cur = branches[-1]
        else:
            dx, dy = dirs[c]
            x, y = cur
            vertex = x + dx, y + dy
            graph.setdefault(cur, []).append(vertex)
            graph.setdefault(vertex, []).append(cur)
            cur = vertex

    return graph

def shortest_paths(graph, source):
    inf = 1 << 32
    dist = {v: inf for v in graph}
    dist[source] = 0
    Q = [(dist[v], v) for v in graph]
    heapify(Q)

    while Q:
        udist, u = heappop(Q)
        if udist > dist[u]:
            continue
        for v in graph[u]:
            alt = udist + 1
            if alt < dist[v]:
                dist[v] = alt
                heappush(Q, (alt, v))

    return dist

regex = sys.stdin.readline().rstrip()
graph = parse(regex)
dist = shortest_paths(graph, (0, 0))
print(max(dist.values()))
print(sum(int(d >= 1000) for d in dist.values()))
