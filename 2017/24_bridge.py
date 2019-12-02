#!/usr/bin/env python3
import sys


def grow(length, strength, end, rest):
    for comp in rest:
        if end in comp:
            other_end = comp[1] if end == comp[0] else comp[0]
            yield from grow(length + 1, strength + sum(comp),
                            other_end, rest - {comp})

    yield length, strength


components = {tuple(map(int, line.split('/'))) for line in sys.stdin}
options = list(grow(0, 0, 0, components))
print(max(s for l, s in options))
print(max(options)[1])
