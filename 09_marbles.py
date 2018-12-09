#!/usr/bin/env python3
import sys
from collections import deque
from itertools import cycle

def play(nplayers, last):
    scores = [0] * nplayers
    circle = deque([0])

    for marble, player in zip(range(1, last + 1), cycle(range(nplayers))):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)

nplayers, lastmarble = map(int, sys.stdin.read().split()[::6])
print(play(nplayers, lastmarble))
print(play(nplayers, lastmarble * 100))
