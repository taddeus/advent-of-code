#!/usr/bin/env python3
import sys
import re
claims = [tuple(int(col) for col in re.split(r'[#@, :x\n]', line) if col)
          for line in sys.stdin]
W = H = 1000

# part 1
grid = W * H * [0]

for patch, xl, yl, w, h in claims:
    for x in range(xl, xl + w):
        for y in range(yl, yl + h):
            grid[y * W + x] += 1

print(sum(int(cell > 1) for cell in grid))

# part 2
grid = W * H * [0]
intact = [False] + [True] * len(claims)

for patch, xl, yl, w, h in claims:
    for x in range(xl, xl + w):
        for y in range(yl, yl + h):
            prev = grid[y * W + x]
            if prev:
                intact[prev] = False
                intact[patch] = False
            else:
                grid[y * W + x] = patch

for patch, still_intact in enumerate(intact):
    if still_intact:
        print(patch)
        break
