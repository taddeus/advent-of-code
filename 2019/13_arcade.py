#!/usr/bin/env python3
import sys
from itertools import islice
from operator import add, mul, lt, eq
from time import sleep

def run(p, get_input, memsize=0):
    def decode_param(offset):
        return p[pc + offset], modes // (10 ** (offset - 1)) % 10

    def pload(offset):
        param, mode = decode_param(offset)
        return param if mode == 1 else p[param + relbase * mode // 2]

    def pstore(offset, value):
        param, mode = decode_param(offset)
        p[param + relbase * mode // 2] = value

    opmap = {1: add, 2: mul, 7: lt, 8: eq}
    p = p + [0] * memsize
    pc = relbase = 0

    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        if opcode in (1, 2, 7, 8):
            pstore(3, opmap[opcode](pload(1), pload(2)))
            pc += 4
        elif opcode == 3:
            pstore(1, get_input())
            pc += 2
        elif opcode == 4:
            yield pload(1)
            pc += 2
        elif opcode == 5:
            pc = pload(2) if pload(1) else pc + 3
        elif opcode == 6:
            pc = pload(2) if not pload(1) else pc + 3
        elif opcode == 9:
            relbase += pload(1)
            pc += 2

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
    ypaddle = next(y for y, row in enumerate(grid) if 3 in row)
    xball = xpaddle = 0
    ball_right = True
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
                    ball_right = x > xball
                    xball = x
                if verbose:
                    draw(grid, score)
                    sleep(.003)
    except (StopIteration, ValueError):
        return score

# part 1
code = list(map(int, sys.stdin.read().split(',')))
outp = list(run(code, lambda: 0, 1000))
print(outp[2::3].count(2))

# part 2
code[0] = 2
print(play(code, '-v' in sys.argv))
