#!/usr/bin/env python3
import sys
from collections import deque

def breed(fish, days):
    state = deque([0] * 9)
    for to_breed in fish:
        state[to_breed] += 1

    for day in range(days):
        breeding = state.popleft()
        state[-2] += breeding
        state.append(breeding)

    return sum(state)

fish = list(map(int, sys.stdin.readline().split(',')))
print(breed(fish, 80))
print(breed(fish, 256))
