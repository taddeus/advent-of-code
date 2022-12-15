#!/usr/bin/env python3
import sys
import re

def intervals(sensors, y):
    for sx, sy, bx, by in sensors:
        dx = abs(sx - bx) + abs(sy - by) - abs(sy - y)
        if dx >= 0:
            yield sx - dx, sx + dx

def coverage(sensors, y):
    l, r = zip(*intervals(sensors, y))
    beacons = len(set(bx for _, _, bx, by in sensors if by == y))
    return max(r) + 1 - min(l) - beacons

def border(x, y, radius):
    for dx in range(radius + 2):
        dy = radius + 1 - dx
        yield x + dx, y + dy
        yield x + dx, y - dy
        yield x - dx, y + dy
        yield x - dx, y - dy

def frequency(sensors, limit):
    rad = [(sx, sy, abs(sx - bx) + abs(sy - by)) for sx, sy, bx, by in sensors]
    for sensor in rad:
        for x, y in border(*sensor):
            if 0 <= x <= limit and 0 <= y <= limit and \
                    all(abs(x - sx) + abs(y - sy) > r for sx, sy, r in rad):
                return x * 4000000 + y

sensors = [tuple(map(int, re.findall(r'-?\d+', line))) for line in sys.stdin]
print(coverage(sensors, 2000000))
print(frequency(sensors, 4000000))
