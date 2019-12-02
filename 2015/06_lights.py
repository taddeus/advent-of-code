#!/usr/bin/env python3
import sys
import re

ON, OFF, TOGGLE = 0, 1, 2
mapping = {'turn on': ON, 'turn off': OFF, 'toggle': TOGGLE}
pat = r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)'
actions = []
for line in sys.stdin:
    action, xa, ya, xb, yb = re.match(pat, line).groups()
    actions.append((mapping[action], int(xa), int(xb), int(ya), int(yb)))

# part 1
w = h = 1000
grid = w * h * [False]
for action, xa, xb, ya, yb in actions:
    for x in range(xa, xb + 1):
        for y in range(ya, yb + 1):
            i = y * w + x
            grid[i] = not grid[i] if action == TOGGLE else action == ON
print(sum(map(int, grid)))

# part 2
grid = w * h * [0]
for action, xa, xb, ya, yb in actions:
    for x in range(xa, xb + 1):
        for y in range(ya, yb + 1):
            i = y * w + x
            grid[i] = max(0, grid[i] + (1, -1, 2)[action])
print(sum(grid))
