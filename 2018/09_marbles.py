#!/usr/bin/env python3
import sys
from collections import deque

def play(nplayers, nmarbles):
    scores = [0] * nplayers
    circle = deque([0])

    for marble in range(1, nmarbles + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % nplayers] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)

nplayers, nmarbles = map(int, sys.stdin.readline().split()[::6])
print(play(nplayers, nmarbles))
print(play(nplayers, nmarbles * 100))
