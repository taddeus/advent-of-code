#!/usr/bin/env python3
import sys
from functools import lru_cache

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

def make_grid(tiles, sz=10):
    tiles = dict(tiles)
    placed = {}
    unavail = set()

    @lru_cache(maxsize=None)
    def variants(ident):
        return list(fliprot(tiles[ident], sz))

    def place(ident, tile, x, y):
        tile_t = placed.get((x, y - 1), (None, None))[1]
        tile_b = placed.get((x, y + 1), (None, None))[1]
        tile_r = placed.get((x + 1, y), (None, None))[1]
        tile_l = placed.get((x - 1, y), (None, None))[1]

        if tile_t and tile_t[-sz:] != tile[:sz] or \
           tile_b and tile_b[:sz] != tile[-sz:] or \
           tile_r and tile_r[::sz] != tile[sz - 1::sz] or \
           tile_l and tile_l[sz - 1::sz] != tile[::sz]:
            return False

        placed[(x, y)] = ident, tile
        unavail.add(ident)
        for nb in ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)):
            if nb not in placed:
                for ident in tiles:
                    if ident not in unavail:
                        for variant in variants(ident):
                            if place(ident, variant, *nb):
                                break
        return True

    start = next(iter(tiles))
    place(start, tiles[start], 0, 0)

    minx = min(x for x, y in placed)
    miny = min(y for x, y in placed)
    maxx = max(x for x, y in placed) + 1
    maxy = max(y for x, y in placed) + 1
    return [[placed[(x, y)] for x in range(minx, maxx)]
            for y in range(miny, maxy)]

def stitch(grid, sz=10):
    return ''.join(tile[y + 1:y + sz - 1]
                   for row in grid
                   for y in range(sz, sz * sz - sz, sz)
                   for ident, tile in row)

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

grid = make_grid(parse(sys.stdin))
print(grid[0][0][0] * grid[0][-1][0] * grid[-1][0][0] * grid[-1][-1][0])
print(roughness(stitch(grid), len(grid) * 8))
