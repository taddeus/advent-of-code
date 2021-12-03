#!/usr/bin/env python3
from collections import deque

def spin(inserts, steps):
    buf = deque([0])
    for i in range(1, inserts + 1):
        buf.rotate(-steps % len(buf))
        buf.append(i)
    return buf

def spin_at(target, inserts, steps):
    pos = last = 0
    for i in range(1, inserts + 1):
        pos = (pos + steps) % i + 1
        if pos == target:
            last = i
    return last

steps = 386
print(spin(2017, steps)[0])
print(spin_at(1, 50000000, steps))
