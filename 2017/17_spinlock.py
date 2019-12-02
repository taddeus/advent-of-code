#!/usr/bin/env python3
from collections import deque

def spin(inserts, steps):
    buf = deque([0])
    for i in range(1, inserts + 1):
        buf.rotate(-(steps % len(buf) + 1))
        buf.appendleft(i)
    return buf

def after_zero(buf):
    while buf.popleft() != 0:
        pass
    return buf[0]

print(spin(2017, 386)[1])
print(after_zero(spin(50000000, 386)))
