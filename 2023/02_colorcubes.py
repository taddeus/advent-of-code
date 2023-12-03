#!/usr/bin/env python3
import sys

def parse(line):
    maximums = [0, 0, 0]
    for hand in line.split(': ', 1)[1].split('; '):
        for ty in hand.split(', '):
            amount, color = ty.split()
            i = ('red', 'green', 'blue').index(color)
            maximums[i] = max(maximums[i], int(amount))
    return maximums

games = list(map(parse, sys.stdin))
print(sum(i + 1 for i, game in enumerate(games)
          if all(real <= expect for real, expect in zip(game, (12, 13, 14)))))
print(sum(r * g * b for r, g, b in games))
