#!/usr/bin/env python3
import sys
from collections import deque
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

def deploy_drone(program, x, y):
    return next(run(program, [y, x].pop, 1000))

def scan(program, w, h):
    return [[deploy_drone(program, x, y) for x in range(w)] for y in range(h)]

def bounds(program):
    left = 0
    right = 1
    y = 0
    while True:
        yield left, right
        y += 1
        left += 1
        while not deploy_drone(program, left, y):
            left += 1
        right += 1
        while deploy_drone(program, right, y):
            right += 1

def find_box(program, size):
    buf = deque([], size - 1)
    for y2, (left2, right2) in enumerate(bounds(program)):
        if len(buf) == size - 1:
            y1, left1, right1 = buf.popleft()
            if right1 - left2 >= size:
                return left2, y1
        buf.append((y2, left2, right2))

# part 1
program = list(map(int, sys.stdin.readline().split(',')))
grid = scan(program, 50, 50)
print(sum(sum(row) for row in grid))

# part 2
bx, by = find_box(program, 100)
print(bx * 10000 + by)
