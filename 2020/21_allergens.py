#!/usr/bin/env python3
import sys

def parse(f):
    for line in f:
        ingredients, allergens = line[:-2].split(' (contains ')
        yield ingredients.split(), allergens.split(', ')

def allergen_candidates(foods):
    candidates = {}
    known = set()
    for ingredients, allergens in foods:
        unknown = set(ingredients) - known
        for a in allergens:
            cand = candidates.get(a, None)
            if not cand:
                cand = candidates[a] = set(unknown)
            elif len(cand) > 1:
                cand &= unknown
            if len(cand) == 1:
                known |= cand
                unknown -= cand
    return candidates

def count_safe(foods, candidates):
    maybe_unsafe = set.union(*candidates.values())
    return sum(len(set(ing) - maybe_unsafe) for ing, _ in foods)

def translate_allergens(foods, candidates):
    unsafe = {}
    while candidates:
        found = {c.pop(): a for a, c in candidates.items() if len(c) == 1}
        unsafe.update(found)
        known = set(found)
        candidates = {a: c - known for a, c in candidates.items() if c}
    return sorted(unsafe, key=unsafe.__getitem__)

foods = list(parse(sys.stdin))
candidates = allergen_candidates(foods)
print(count_safe(foods, candidates))
print(','.join(translate_allergens(foods, candidates)))
