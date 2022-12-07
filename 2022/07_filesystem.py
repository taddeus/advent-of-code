#!/usr/bin/env python3
import sys
from collections import defaultdict

def dirsizes(terminal):
    sizes = defaultdict(int)
    path = []
    def add_to_parent():
        curdir = sizes['/'.join(path)]
        path.pop()
        sizes['/'.join(path)] += curdir
    for line in terminal:
        if line.startswith('$ cd '):
            d = line[5:-1]
            if d == '..':
                add_to_parent()
            elif d != '/':
                path.append(d)
        elif line[0].isdigit():
            sizes['/'.join(path)] += int(line.split()[0])
    while path:
        add_to_parent()
    return sorted(sizes.values())

sizes = dirsizes(sys.stdin)
print(sum(size for size in sizes if size <= 100000))
print(next(size for size in sizes if size >= sizes[-1] - 40000000))
