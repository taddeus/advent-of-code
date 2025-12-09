#!/usr/bin/env python3
import sys
from itertools import combinations

def area(xa, ya, xb, yb):
    return (abs(xa - xb) + 1) * (abs(ya - yb) + 1)

def fits(red, xa, ya, xb, yb):
    xmin, xmax = (xa, xb) if xa < xb else (xb, xa)
    ymin, ymax = (ya, yb) if ya < yb else (yb, ya)
    return not any(xmin < x < xmax and ymin < y < ymax for x, y in red)

def maxrect(half):
    a = half.pop()
    return max(area(*a, *b) for b in half if fits(half, *a, *b))

red = [tuple(map(int, line.split(','))) for line in sys.stdin]
print(max(area(*a, *b) for a, b in combinations(red, 2)))
print(max(maxrect(red[:249]), maxrect(red[-2:248:-1])))
