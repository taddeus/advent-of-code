#!/usr/bin/env python3
import sys
import re


def parse(f):
    p, v, a = [], [], []
    for line in f:
        nums = list(map(int, re.findall(r'-?[0-9]+', line)))
        p += nums[:3]
        v += nums[3:6]
        a += nums[6:]
    return p, v, a


def closest_after_steps(p, v, a, steps):
    p = p.copy()
    v = v.copy()
    for step in range(steps):
        for i in range(len(p)):
            v[i] += a[i]
            p[i] += v[i]
    p = list(map(abs, p))
    d = [sum(p[i:i + 3]) for i in range(0, len(p), 3)]
    return d.index(min(d))


def not_collided_after_steps(p, v, a, steps):
    p = p.copy()
    v = v.copy()
    collided = [False] * len(p)

    for step in range(steps):
        for i in range(len(p)):
            if not collided[i]:
                v[i] += a[i]
                p[i] += v[i]

        seen = {}
        for i in range(0, len(p), 3):
            if not collided[i]:
                pos = tuple(p[i:i + 3])
                seen.setdefault(pos, []).append(i)

        for indices in seen.values():
            if len(indices) > 1:
                for i in indices:
                    collided[i] = True
                    collided[i + 1] = True
                    collided[i + 2] = True

    return collided.count(False) // 3


# part 1
p, v, a = parse(sys.stdin)
print(closest_after_steps(p, v, a, 500))

# part 2
print(not_collided_after_steps(p, v, a, 500))
