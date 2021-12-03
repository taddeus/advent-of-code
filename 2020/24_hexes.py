#!/usr/bin/env python3
import sys

DIFFS = {'e': (1, 0), 'w': (-1, 0), 'se': (0, -1),
         'sw': (-1, -1), 'ne': (1, 1), 'nw': (0, 1)}

def walk(line):
    x = y = 0
    vert = ''
    for char in line.rstrip():
        if char in 'sn':
            vert = char
        else:
            dx, dy = DIFFS[vert + char]
            x += dx
            y += dy
            vert = ''
    return x, y

def flip(coords):
    tiles = {}
    for xy in coords:
        tiles[xy] = not tiles.get(xy, False)
    return [xy for xy, black in tiles.items() if black]

def evolve(black, days):
    black = set(black)
    for day in range(days):
        makewhite = set()
        white = {}
        for x, y in black:
            nbs = [(x + dx, y + dy) for dx, dy in DIFFS.values()]
            black_nbs = sum(nb in black for nb in nbs)
            if black_nbs == 0 or black_nbs > 2:
                makewhite.add((x, y))
            white.update({nb: white.get(nb, 0) + 1
                          for nb in nbs if nb not in black})
        black -= makewhite
        black |= {xy for xy, black_nbs in white.items() if black_nbs == 2}
    return black

black = flip(map(walk, sys.stdin))
print(len(black))
print(len(evolve(black, 100)))
