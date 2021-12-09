#!/usr/bin/env python3
import sys

def parse(content):
    w = content.find('\n') + 1
    return list(map(int, content.replace('\n', '9') + w * '9')), w

def visit(heights, w, i, visited):
    visited.add(i)
    return 1 + sum(visit(heights, w, nb, visited)
                   for nb in (i - 1, i + 1, i - w, i + w)
                   if heights[nb] < 9 and nb not in visited)

heights, w = parse(sys.stdin.read())
low = [i for i, height in enumerate(heights)
       if all(height < heights[nb] for nb in (i - 1, i + 1, i - w, i + w))]
print(sum(heights[i] + 1 for i in low))

a, b, c = sorted(visit(heights, w, i, set()) for i in low)[-3:]
print(a * b * c)
