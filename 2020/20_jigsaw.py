#!/usr/bin/env python3
import sys
from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product

BOTTOM, RIGHT = range(2)

def parse(f):
    tile = ''
    for line in f:
        if line.startswith('Tile'):
            ident = int(line.split()[1][:-1])
        elif line == '\n':
            yield ident, tile
            tile = ''
        else:
            tile += line.rstrip()
    yield ident, tile

def print_tile(tile, sz, highlight=set()):
    for y in range(0, sz * sz, sz):
        print(''.join('O' if i in highlight else tile[i]
                      for i in range(y, y + sz)))
    print()

def vflip(tile, sz):
    return ''.join(tile[i:i + sz] for i in range((sz - 1) * sz, -1, -sz))

def lrotate(tile, sz):
    return ''.join(tile[sz - 1 - i::sz] for i in range(sz))

def fliprot(tile, sz):
    for variant in (tile, vflip(tile, sz)):
        yield variant
        for i in range(3):
            variant = lrotate(variant, sz)
            yield variant

def connections(a, b, sz):
    if a[:sz] == b[-sz:]: yield BOTTOM
    if a[::sz] == b[sz - 1::sz]: yield RIGHT

def make_graph(tiles, sz):
    variants = [(ident, set(fliprot(tile, sz))) for ident, tile in tiles]
    graph = {(i, v): defaultdict(set) for i, allv in variants for v in allv}
    for (ia, va), (ib, vb) in permutations(variants, 2):
        for a, b in product(va, vb):
            for side in connections(a, b, sz):
                graph[(ib, b)][side].add((ia, a))
    return graph

def find_grid(graph, sq):
    corner = next(i for (i, _), sides in graph.items() if not sides)
    worklist = deque(((), node) for node in graph if node[0] == corner)

    while worklist:
        grid, node = worklist.popleft()
        y, x = divmod(len(grid), sq)
        if y == 0 or node in graph[grid[-sq]][BOTTOM]:
            grid = grid + (node,)
            if x == sq - 1 and y == sq - 1:
                return grid
            neighbors = graph[node][RIGHT] if len(grid) % sq \
                        else graph[grid[-sq]][BOTTOM]
            for nb in neighbors:
                worklist.append((grid, nb))

def stitch(grid, sq, sz=10):
    return ''.join(tile[x + 1:x + sz - 1]
                   for i in range(0, sq * sq, sq)
                   for x in range(sz, sz * sz - sz, sz)
                   for ident, tile in grid[i:i + sq])

def findpat(tile, pattern, sz):
    diffs = [y * sz + x
             for y, line in enumerate(pattern)
             for x, char in enumerate(line)
             if char == '#']
    found = set()
    for variant in fliprot(tile, sz):
        for y in range(sz - len(pattern) + 1):
            for x in range(sz - len(pattern[0]) + 1):
                base = y * sz + x
                if all(variant[base + i] == '#' for i in diffs):
                    found |= {base + i for i in diffs}
        if found:
            return variant, found

def roughness(habitat, sz):
    monster = ('                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ')
    variant, monsters = findpat(habitat, monster, sz)
    return variant.count('#') - len(monsters)

sz, sq = 10, 12

tiles = list(parse(sys.stdin))
graph = make_graph(tiles, sz)
corners = set(i for (i, _), sides in graph.items() if not sides)
print(reduce(lambda a, b: a * b, corners))

grid = find_grid(graph, sq)
habitat = stitch(grid, sq, sz)
print(roughness(habitat, sq * (sz - 2)))
