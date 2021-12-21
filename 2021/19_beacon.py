#!/usr/bin/env python3
import sys
from itertools import combinations, starmap
from collections import deque, Counter

def parse(f):
    for line in f:
        if line.startswith('---'):
            scan = []
        elif line == '\n':
            yield scan
        else:
            scan.append(tuple(map(int, line.split(','))))
    yield scan

def rotx(x, y, z):
    return x, -z, y

def rotz(x, y, z):
    return -y, x, z

ALL_ROTATIONS = (
    rotz, rotz, rotz,
    rotx,
    rotz, rotz, rotz,
    rotx,
    rotz, rotz, rotz,
    lambda x, y, z: (-x, -z, -y),
    rotz, rotz, rotz,
    rotx,
    rotz, rotz, rotz,
    lambda x, y, z: (x, z, -y),
    rotz, rotz, rotz,
)

def rotations(scan):
    yield scan
    for rot in ALL_ROTATIONS:
        scan = list(starmap(rot, scan))
        yield scan

def move(scan, dx, dy, dz):
    return [(x + dx, y + dy, z + dz) for x, y, z in scan]

def find_scanner(base, rotated_scans):
    for scan in rotated_scans:
        [(diff, count)] = Counter((x2 - x1, y2 - y1, z2 - z1)
                                  for x1, y1, z1 in scan
                                  for x2, y2, z2 in base).most_common(1)
        if count >= 12:
            return diff, move(scan, *diff)
    return None, None

def join(scans):
    joined = set(next(scans))
    remaining = deque(list(rotations(scan)) for scan in scans)
    scanners = [(0, 0, 0)]

    while remaining:
        rotated_scans = remaining.popleft()
        scanner, moved = find_scanner(joined, rotated_scans)
        if scanner:
            joined |= set(moved)
            scanners.append(scanner)
        else:
            remaining.append(rotated_scans)

    return joined, scanners

def max_distance(scanners):
    return max(abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)
               for (x1, y1, z1), (x2, y2, z2) in combinations(scanners, 2))

joined, scanners = join(parse(sys.stdin))
print(len(joined))
print(max_distance(scanners))
