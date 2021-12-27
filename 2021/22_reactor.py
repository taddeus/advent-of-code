#!/usr/bin/env python3
import sys
import re
from itertools import starmap

def clamp(n, nmin, nmax):
    return max(min(n, nmax), nmin)

def split(start, end, point):
    sx, sy, sz = start
    ex, ey, ez = end
    px, py, pz = point
    yield (sx, sy, sz), (px, py, pz)
    yield (px, sy, sz), (ex, py, pz)
    yield (sx, py, sz), (px, ey, pz)
    yield (px, py, sz), (ex, ey, pz)
    yield (sx, sy, pz), (px, py, ez)
    yield (px, sy, pz), (ex, py, ez)
    yield (sx, py, pz), (px, ey, ez)
    yield (px, py, pz), (ex, ey, ez)

class Cuboid:
    def __init__(self, on, start, end):
        self.on = on
        self.start = start
        self.end = end
        self.children = []

    def split(self, point):
        for start, end in split(self.start, self.end, point):
            child = Cuboid(self.on, start, end)
            if child.size():
                self.children.append(child)

    def toggle(self, subset):
        if subset.size():
            if self.children:
                for child in self.children:
                    child.toggle(subset.clamp(child))
            elif subset.on != self.on:
                if subset.start == self.start:
                    if subset.end == self.end:
                        self.on = subset.on
                    else:
                        self.split(subset.end)
                        self.children[0].on = subset.on
                else:
                    self.split(subset.start)
                    self.children[-1].toggle(subset)

    def size(self):
        dx, dy, dz = (r - l for l, r in zip(self.start, self.end))
        return dx * dy * dz

    def count_on(self):
        if self.children:
            return sum(child.count_on() for child in self.children)
        return self.on * self.size()

    def clamp(self, to):
        start = tuple(starmap(clamp, zip(self.start, to.start, to.end)))
        end = tuple(starmap(clamp, zip(self.end, to.start, to.end)))
        return Cuboid(self.on, start, end)

def parse(line):
    xmin, xmax, ymin, ymax, zmin, zmax = map(int, re.findall(r'-?\d+', line))
    start = xmin, ymin, zmin
    end = xmax + 1, ymax + 1, zmax + 1
    return Cuboid(line.startswith('on'), start, end)

def reboot(instructions, reactor):
    for cuboid in instructions:
        reactor.toggle(cuboid.clamp(reactor))
    return reactor.count_on()

def stretch(dist):
    return Cuboid(False, (-dist, -dist, -dist), (dist + 2, dist + 2, dist + 2))

instructions = list(map(parse, sys.stdin))
print(reboot(instructions, stretch(50)))
print(reboot(instructions, stretch(100000)))
