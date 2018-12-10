#!/usr/bin/env python3
import sys
import re

x, y, dx, dy = map(list, zip(*(map(int, re.findall(r'-?\d+', l)) for l in sys.stdin)))
h = 1 << 63
prevh = h + 1
t = -1
while h < prevh:
    prevh = h
    for i in range(len(x)):
        x[i] += dx[i]
        y[i] += dy[i]
    h = max(y) - min(y)
    t += 1

for i in range(len(x)):
    x[i] -= dx[i]
    y[i] -= dy[i]
points = set(zip(x, y))

print('message after', t, 'seconds:')
for py in range(min(y), max(y) + 1):
    print(''.join('#' if (px, py) in points else '.'
          for px in range(min(x), max(x) + 1)))
