#!/usr/bin/env python3
import sys
from itertools import islice
from time import sleep
from intcode import read_program, run

def makegrid(game):
    x, y, ident = islice(game, 3)
    coords = []
    while x != -1:
        coords.append((x, y, ident))
        x, y, ident = islice(game, 3)
    score = ident

    width = max(x for x, y, ident in coords) + 1
    height = max(y for x, y, ident in coords) + 1
    grid = [[0] * width for y in range(height)]
    for x, y, ident in coords:
        grid[y][x] = ident

    return grid, score

def draw(grid, score):
    print('\033c', end='')
    for row in grid:
        print(''.join(' @x_o'[c] for c in row))
    print('score:', score)

def play(code, verbose):
    game = run(code, lambda: xball - xpaddle, 1000)
    grid, score = makegrid(game)
    xpaddle = xball = 0
    if verbose:
        draw(grid, score)
    try:
        while True:
            x, y, ident = islice(game, 3)
            if x == -1:
                score = ident
            else:
                grid[y][x] = ident
                if ident == 3:
                    xpaddle = x
                elif ident == 4:
                    xball = x
                if verbose:
                    draw(grid, score)
                    sleep(.003)
    except (StopIteration, ValueError):
        return score

# part 1
code = read_program(sys.stdin)
outp = list(run(code, lambda: 0, 1000))
print(outp[2::3].count(2))

# part 2
code[0] = 2
print(play(code, '-v' in sys.argv))
