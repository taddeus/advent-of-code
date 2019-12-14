#!/usr/bin/env python3
from functools import reduce
from hashlib import md5
from heapq import heappop, heappush

def doors_open(path):
    a, b = md5(path.encode('ascii')).digest()[:2]
    quads = a >> 4, a & 0xf, b >> 4, b & 0xf
    return tuple(i for i, quad in enumerate(quads) if quad > 0xa)

def walk(passcode):
    dx = 0, 0, -1, 1
    dy = -1, 1, -0, 0
    work = [(len(passcode), 6, 0, 0, passcode)]
    while work:
        pathlen, dist, x, y, path = heappop(work)
        if dist == 0:
            yield path[len(passcode):]
        else:
            for door in doors_open(path):
                newx = x + dx[door]
                newy = y + dy[door]
                if 0 <= newx < 4 and 0 <= newy < 4:
                    newdist = dist - dx[door] - dy[door]
                    newpath = path + 'UDLR'[door]
                    heappush(work, (len(newpath), newdist, newx, newy, newpath))

walker = walk('gdjjyniy')
print(next(walker))
print(len(reduce(lambda a, b: b, walker)))
