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

def scan(program, w, h):
    def deploy_drone(x, y):
        return next(run(program, [y, x].pop, 1000))
    return [[deploy_drone(x, y) for x in range(w)] for y in range(h)]

def draw(grid):
    for row in grid:
        print(''.join('.#O'[x] for x in row))

program = list(map(int, sys.stdin.readline().split(',')))
grid = scan(program, 50, 50)
draw(grid)
print(sum(sum(row) for row in grid))
