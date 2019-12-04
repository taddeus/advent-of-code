#!/usr/bin/env python3
def get_groups(pw):
    prev = 10
    group = 1
    groups = []
    while pw:
        d = pw % 10
        if d > prev:
            return []
        if d == prev:
            group += 1
        else:
            groups.append(group)
            group = 1
        prev = d
        pw //= 10
    groups.append(group)
    return groups

pmin, pmax = 240920, 789857
relaxed = strict = 0
for n in range(pmin, pmax + 1):
    groups = list(get_groups(n))
    relaxed += int(any(group >= 2 for group in groups))
    strict += int(2 in groups)
print(relaxed)
print(strict)
