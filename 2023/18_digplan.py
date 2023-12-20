#!/usr/bin/env python3
import sys
from itertools import pairwise

def parse(inp):
    DXDY = (1, 0), (0, 1), (-1, 0), (0, -1)
    for line in inp:
        direction, distance, color = line.split()
        normal_instruction = DXDY['RDLU'.index(direction)], int(distance)
        color_instruction = DXDY[int(color[7])], int(color[2:7], 16)
        yield normal_instruction, color_instruction

def follow(instructions):
    x = y = 0
    for (dx, dy), distance in instructions:
        x += dx * distance
        y += dy * distance
        yield x, y

def dig(instructions):
    x, y = zip(*follow(instructions))
    v = len(x)
    area = abs(sum(x[i] * y[(i + 1) % v] - y[i] * x[(i + 1) % v]
                   for i in range(v))) // 2  # Shoelace formula
    outer = sum(abs(bx - ax + by - ay)
                for (ax, ay), (bx, by) in pairwise(zip(x + x[:1], y + y[:1])))
    inner = area - outer // 2 + 1  # Pick's theorem
    return outer + inner

normal, color = zip(*parse(sys.stdin))
print(dig(normal))
print(dig(color))
