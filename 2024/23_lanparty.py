#!/usr/bin/env python3
import sys

def parse(f):
    network = {}
    for line in f:
        a, b = line.rstrip().split('-')
        network.setdefault(a, set()).add(b)
        network.setdefault(b, set()).add(a)
    return network

def max_cliques(graph):
    # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def bron_kerbosch(r, p, x):
        if not p and not x:
            yield ','.join(sorted(r))
        while p:
            v = p.pop()
            yield from bron_kerbosch(r | {v}, p & graph[v], x & graph[v])
            x.add(v)
    yield from bron_kerbosch(set(), set(graph), set())

network = parse(sys.stdin)
print(len(set(''.join(sorted((a, b, c)))
              for a, network_a in network.items()
              for b in network_a
              for c in network[b]
              if a in network[c] and 't' in a[0] + b[0] + c[0])))
print(max(max_cliques(network), key=len))
