#!/usr/bin/env python3
import sys
from collections import deque

def parse(f):
    for deck in f.read().split('\n\n'):
        yield list(map(int, deck.splitlines()[1:]))

def play(a, b, rec):
    a = deque(a)
    b = deque(b)
    seen = set()

    while a and b:
        if rec:
            config = tuple(a) + (0,) + tuple(b)
            if config in seen:
                return True, a
            seen.add(config)

        ca = a.popleft()
        cb = b.popleft()

        if rec and ca <= len(a) and cb <= len(b):
            reca = [a[i] for i in range(ca)]
            recb = [b[i] for i in range(cb)]
            a_wins_round = play(reca, recb, True)[0]
        else:
            a_wins_round = ca > cb

        if a_wins_round:
            a.extend((ca, cb))
        else:
            b.extend((cb, ca))

    return bool(a), a or b

def score(a, b, rec):
    a_wins, deck = play(a, b, rec)
    return sum((len(deck) - i) * c for i, c in enumerate(deck))

a, b = parse(sys.stdin)
print(score(a, b, False))
print(score(a, b, True))
