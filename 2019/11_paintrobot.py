#!/usr/bin/env python3
import sys
from operator import add, mul, lt, eq

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

def paint(firmware, color):
    robot = run(firmware, lambda: color, 1000)
    painted = set()
    white = set()
    x = y = 0
    dx, dy = 0, -1
    for make_white in robot:
        painted.add((x, y))
        (white.add if make_white else white.discard)((x, y))
        dx, dy = (-dy, dx) if next(robot) else (dy, -dx)
        x += dx
        y += dy
        color = int((x, y) in white)
    return white, len(painted)

def draw(coords):
    xmin = min(x for x, y in coords)
    xmax = max(x for x, y in coords)
    ymin = min(y for x, y in coords)
    ymax = max(y for x, y in coords)

    grid = [[0] * (xmax - xmin + 1) for y in range(ymin, ymax + 1)]
    for x, y in coords:
        grid[y - ymin][x - xmin] = 1

    for row in grid:
        print(''.join(' @'[c] for c in row))

firmware = list(map(int, sys.stdin.read().split(',')))
white, npainted = paint(firmware, 0)
print(npainted)
white, npainted = paint(firmware, 1)
draw(white)
