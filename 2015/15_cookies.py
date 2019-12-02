#!/usr/bin/env python3
import sys
import re

def divide(amount, nbuckets):
    if nbuckets == 1:
        yield (amount,)
    else:
        for bucket in range(0, amount + 1):
            for rest in divide(amount - bucket, nbuckets - 1):
                yield (bucket,) + rest

def scores(ingredients, spoons):
    for buckets in divide(spoons, len(ingredients)):
        props = (max(sum(b * s for b, s in zip(buckets, stats)), 0)
                 for stats in zip(*ingredients))
        cap, dur, fla, tex, cal = props
        yield cap * dur * fla * tex, cal

ingredients = [tuple(map(int, re.findall(r'(-?\d+)', line)))
               for line in sys.stdin]
maxall = max500 = 0
for score, calories in scores(ingredients, 100):
    if score > maxall:
        maxall = score
    if calories == 500 and score > max500:
        max500 = score
print(maxall)
print(max500)
