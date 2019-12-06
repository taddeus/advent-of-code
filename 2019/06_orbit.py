#!/usr/bin/env python3
import sys

def read_graph(f):
    graph = {}
    for line in f:
        planet, moon = line.rstrip().split(')')
        graph.setdefault(planet, []).append(moon)
    return graph

def count_orbits(graph, root):
    def dfs(node, depth, vis):
        vis.add(node)
        return depth + sum(dfs(nb, depth + 1, vis)
                           for nb in graph.get(node, [])
                           if nb not in vis)
    return dfs(root, 0, set())

def shortest_path(graph, a, b):
    parents = {node: p for p, nodes in graph.items() for node in nodes}
    def find_root(node):
        yield node
        if node in parents:
            yield from find_root(parents[node])

    path_a = {node: dist for dist, node in enumerate(find_root(a))}
    for dist, node in enumerate(find_root(b)):
        if node in path_a:
            return path_a[node] + dist - 2

graph = read_graph(sys.stdin)
print(count_orbits(graph, 'COM'))
print(shortest_path(graph, 'YOU', 'SAN'))
