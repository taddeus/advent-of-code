#!/usr/bin/env python3
from hashlib import md5
from itertools import count

def digest(index, salt, iters):
    hashed = salt + str(index)
    while iters > 0:
        hashed = md5(hashed.encode('ascii')).hexdigest()
        iters -= 1
    return hashed

def key_indices(salt, stretch):
    candidates = {}
    for index in count(0):
        conseq = prev = None
        three = None
        fives = set()

        for cur in digest(index, salt, stretch + 1):
            if cur == prev:
                conseq += 1
                if conseq == 3 and three is None:
                    three = cur
                elif conseq == 5:
                    fives.add(cur)
            else:
                conseq = 1
            prev = cur

        for five in fives:
            for candidate in candidates.pop(five, []):
                if index - candidate <= 1000:
                    yield candidate
        if three:
            candidates.setdefault(three, []).append(index)

def nth_key(n, salt, stretch):
    gen_keys = key_indices(salt, stretch)
    return max(next(gen_keys) for i in range(64))

salt = 'cuanljph'
print(nth_key(64, salt, 0))
print(nth_key(64, salt, 2016))
