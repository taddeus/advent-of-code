#!/usr/bin/env python3
import sys
from collections import Counter

TYPES = ([1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 2, 2],
         [1, 1, 3], [2, 3], [1, 4], [5])

def strength(hand, joker):
    variations = (hand.replace('J', c) for c in '23456789TQKA') \
                 if joker and 'J' in hand else [hand]
    ty = max(TYPES.index(sorted(Counter(v).values())) for v in variations)
    scores = [('23456789TJQKA', 'J23456789TQKA')[joker].index(c) for c in hand]
    return ty, scores

def rank(hands, joker):
    hands.sort(key=lambda h: strength(h[0], joker))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(hands))

hands = [(hand, int(bid)) for hand, bid in map(str.split, sys.stdin)]
print(rank(hands, False))
print(rank(hands, True))
