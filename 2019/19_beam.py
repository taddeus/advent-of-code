#!/usr/bin/env python3
import sys
from collections import deque
from itertools import islice
from intcode import read_program, run

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
program = read_program(sys.stdin)
#print(sum(sum(row) for row in scan(program, 50, 50)))
print(sum(min(r, 50) - l for l, r in islice(bounds(program), 50) if l < 50))

# part 2
bx, by = find_box(program, 100)
print(bx * 10000 + by)
