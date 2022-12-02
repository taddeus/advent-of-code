#!/usr/bin/env python3
import sys

def score(them, me):
    return me + 1 + 3 * (them == me) + 6 * ((me - them) % 3 == 1)

games = [('ABC'.index(line[0]), 'XYZ'.index(line[2])) for line in sys.stdin]
print(sum(score(them, me) for them, me in games))
print(sum(score(them, (them + outcome - 1) % 3) for them, outcome in games))
