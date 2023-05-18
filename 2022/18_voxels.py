#!/usr/bin/env python3
import sys

def neighbors(x, y, z):
    yield x - 1, y, z
    yield x + 1, y, z
    yield x, y - 1, z
    yield x, y + 1, z
    yield x, y, z - 1
    yield x, y, z + 1

def total_surface(voxels):
    return sum(nb not in voxels for xyz in voxels for nb in neighbors(*xyz))

def exterior_surface(voxels):
    w = max(x for x, _, _ in voxels) + 1
    h = max(y for _, y, _ in voxels) + 1
    d = max(z for _, _, z in voxels) + 1

    outside = {(-1, -1, -1)}
    visit = list(outside)
    while visit:
        for nb in neighbors(*visit.pop()):
            nx, ny, nz = nb
            if -1 <= nx <= w and -1 <= ny <= h and -1 <= nz <= d \
                    and nb not in outside and nb not in voxels:
                outside.add(nb)
                visit.append(nb)

    filled = {(x, y, z) for x in range(w) for y in range(h)
              for z in range(d) if (x, y, z) not in outside}
    return total_surface(filled)

voxels = {tuple(map(int, line.split(','))) for line in sys.stdin}
print(total_surface(voxels))
print(exterior_surface(voxels))
