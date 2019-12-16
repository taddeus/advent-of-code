#!/usr/bin/env python3
from collections import deque

def steal_left(n):
    elves = deque(range(1, n + 1))
    while len(elves) > 1:
        elves.rotate(-1)
        elves.popleft()
    return elves.pop()

def steal_opposite(n):
    elves = deque(range(1, n + 1))
    elves.rotate(-(len(elves) // 2))
    skip = len(elves) % 2
    while len(elves) > 1:
        elves.popleft()
        elves.rotate(-skip)
        skip = 1 - skip
    return elves.pop()

n = 3017957
print(steal_left(n))
print(steal_opposite(n))
