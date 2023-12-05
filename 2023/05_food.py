#!/usr/bin/env python3
import sys
from itertools import chain

def parse(inp):
    yield list(map(int, next(inp).split()[1:]))
    yield [[list(map(int, line.split())) for line in par.split('\n')[1:]]
           for par in inp.read().strip().split('\n\n')]

def apply(maps, start, end):
    for dst, src, mapsize in maps:
        delta = dst - src
        mapend = src + mapsize
        r = start, end
        if src <= start < mapend:
            if end <= mapend:
                yield start + delta, end + delta
                return
            else:
                yield start + delta, dst + mapsize
                start = mapend
        elif src < end <= mapend:
            yield dst, end + delta
            end = src
        elif start < src and end > mapend:
            yield from apply(maps, start, src)
            yield dst, dst + mapsize
            start = mapend
    yield start, end

def min_location(seeds, steps):
    ranges = seeds
    for maps in steps:
        ranges = list(chain.from_iterable(apply(maps, *r) for r in ranges))
    return min(start for start, end in ranges)

seeds, steps = parse(sys.stdin)
print(min_location([(s, s + 1) for s in seeds], steps))
ranges = [(s, s + size) for s, size in zip(seeds[::2], seeds[1::2])]
print(min_location(ranges, steps))
