#!/usr/bin/env python3
import sys
from heapq import heappop, heappush
from itertools import chain, cycle

def read_grid(f):
    rows = [line.rstrip() for line in f]
    return list(chain.from_iterable(rows)), len(rows[0])

def build_graph(grid, w):
    def dfs(loc, prev, dist):
        nblocs = (loc - 1, loc + 1, loc - w, loc + w)
        neighbors = [nb for nb in nblocs if grid[nb] != '#']

        node = grid[loc]
        if node == '@' or node.isalpha() or len(neighbors) > 2:
            if node in doubles:
                seen = doubles[node]
                count = seen.setdefault(loc, len(seen))
                node += str(count)

            if prev is None:
                graph[node] = {}
            else:
                graph[prev][node] = dist
                graph.setdefault(node, {})[prev] = dist

            prev = node
            dist = 0

        if loc not in visited:
            visited.add(loc)
            for nb in neighbors:
                dfs(nb, prev, dist + 1)

    doubles = {'@': {}, '.': {}}
    graph = {}
    visited = set()
    for i, node in enumerate(grid):
        if node == '@':
            dfs(i, None, 0)
    return graph

def split_grid(grid, w):
    e = grid.index('@')
    grid[e - w - 1:e - w + 2] = '@#@'
    grid[e     - 1:e     + 2] = '###'
    grid[e + w - 1:e + w + 2] = '@#@'

def collect_from(graph, root, remkeys, keys, dist):
    inf = 100000000
    work = [(dist, remkeys, root, keys)]
    best_dists = {(root, keys): dist}

    def visit(node, dist, keys, remkeys):
        ident = node, keys
        if best_dists.get(ident, inf) > dist:
            best_dists[ident] = dist
            heappush(work, (dist, remkeys, node, keys))

    best = dist, remkeys, root, keys

    while True:
        while work:
            dist, remkeys, node, keys = heappop(work)
            if remkeys == 0:
                yield keys, dist
                return

            if remkeys < best[1] or (remkeys == best[1] and dist < best[0]):
                best = dist, remkeys, node, keys

            for nb, step in graph[node].items():
                if nb.islower() and nb not in keys:
                    nbkeys = ''.join(sorted(keys + nb))
                    visit(nb, dist + step, nbkeys, remkeys - 1)
                elif not nb.isupper() or nb.lower() in keys:
                    visit(nb, dist + step, keys, remkeys)

        dist, remkeys, node, keys = best
        newkeys, newdist = yield keys, dist
        newremkeys = remkeys - (len(newkeys) - len(keys))
        work.append((newdist, newremkeys, node, newkeys))

def collect_keys(graph):
    entrances = [node for node in graph if node[0] == '@']
    nkeys = sum(node.islower() for node in graph)
    bots = []
    keys = ''
    dist = 0

    for entrance in entrances:
        bot = collect_from(graph, entrance, nkeys - len(keys), keys, dist)
        bots.append(bot)
        keys, dist = next(bot)
        if len(keys) == nkeys:
            return dist

    for bot in cycle(bots):
        keys, dist = bot.send((keys, dist))
        if len(keys) == nkeys:
            return dist

# part 1
grid, w = read_grid(sys.stdin)
print(collect_keys(build_graph(grid, w)))

# part 2
split_grid(grid, w)
print(collect_keys(build_graph(grid, w)))
