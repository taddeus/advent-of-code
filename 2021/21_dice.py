#!/usr/bin/env python3
import sys
from itertools import cycle
from functools import lru_cache

def move(pos, score, amount):
    pos = (pos + amount - 1) % 10 + 1
    return pos, score + pos

def practice(a, b):
    players = [(a, 0), (b, 0)]
    die = cycle(range(1, 101))
    rolls = 0
    while True:
        for player, (pos, score) in enumerate(players):
            roll = next(die) + next(die) + next(die)
            rolls += 3
            pos, score = players[player] = move(pos, score, roll)
            if score >= 1000:
                otherpos, otherscore = players[1 - player]
                return rolls * otherscore

def play(a, b):
    @lru_cache(maxsize=None)
    def wins(a, b):
        awins = bwins = 0
        for x in range(1, 4):
            for y in range(1, 4):
                for z in range(1, 4):
                    pos, score = roll_a = move(*a, x + y + z)
                    if score >= 21:
                        awins += 1
                    else:
                        roll_bwins, roll_awins = wins(b, roll_a)
                        awins += roll_awins
                        bwins += roll_bwins
        return awins, bwins
    return max(wins((a, 0), (b, 0)))

a, b = (int(line.split(': ')[-1]) for line in sys.stdin)
print(practice(a, b))
print(play(a, b))
