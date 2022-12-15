#!/usr/bin/env python3
import sys
import re

def ranges(sensors, y):
    intervals = set()

    def pop_overlapping(a, b):
        for other in intervals:
            c, d = other
            if a <= d and c <= b:
                intervals.remove(other)
                return min(a, c), max(b, d)

    for sx, sy, bx, by in sensors:
        dist = abs(sx - bx) + abs(sy - by) - abs(sy - y)
        if dist >= 0:
            interval = sx - dist, sx + dist
            new = pop_overlapping(*interval)
            while new:
                interval = new
                new = pop_overlapping(*interval)
            intervals.add(interval)

    return intervals

def coverage(sensors, y):
    covered = sum(r - l + 1 for l, r in ranges(sensors, y))
    beacons = len(set(bx for _, _, bx, by in sensors if by == y))
    return covered - beacons

def frequency(sensors, ymax):
    for y in range(ymax + 1):
        r = ranges(sensors, y)
        if len(r) == 2:
            (a, _), (b, _) = r
            return (max(a, b) - 1) * 4000000 + y

sensors = [tuple(map(int, re.findall(r'-?\d+', line))) for line in sys.stdin]
print(coverage(sensors, 2000000))
print(frequency(sensors, 4000000))
