#!/usr/bin/env python3
import sys

def parse(inp):
    rates = {}
    edges = {}
    for line in inp:
        _, node, _, _, flow, _, _, _, _, nbs = line.split(' ', 9)
        rates[node] = int(flow[5:-1])
        edges[node] = nbs.rstrip().split(', ')
    return rates, edges

def shortest_paths(edges):
    inf = 10000
    dist = {node: {nb: 1 for nb in nbs} for node, nbs in edges.items()}
    dist['start'] = {'AA': 0}
    for node in dist:
        dist[node][node] = 0
    for a, adist in dist.items():
        for b, bdist in dist.items():
            for c in dist:
                alt = bdist.get(a, inf) + adist.get(c, inf)
                if bdist.get(c, inf) > alt:
                    bdist[c] = alt
    return dist

def open_valves(rates, dist, time):
    def travel(released, time, pos, closed):
        yield released
        for dst in closed:
            t = time - dist[pos][dst] - 1
            if t >= 0:
                yield from travel(released + rates[dst] * t, t, dst, closed - {dst})

    valves = {node for node, rate in rates.items() if rate}
    return max(travel(0, time, 'start', valves))

rates, edges = parse(sys.stdin)
print(open_valves(rates, shortest_paths(edges), 30))
