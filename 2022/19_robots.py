#!/usr/bin/env python3
import sys
import re
from math import ceil

def parse_blueprint(line):
    ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = \
            map(int, re.findall(r'\d+', line)[1:])
    return (
        (0, geo_obs, 0, geo_ore),
        (0, 0, obs_clay, obs_ore),
        (0, 0, 0, clay_ore),
        (0, 0, 0, ore_ore),
    )

def max_geo(blueprint, time):
    work = [(time, (0, 0, 0, 0), (0, 0, 0, 1))]
    best = 0

    # We can only make 1 robot per turn so we should only produce the maximum of
    # any single material cost per turn.
    max_robots = [time] + [max(c[ty] for c in blueprint) for ty in range(1, 4)]

    while work:
        time, materials, robots = state = work.pop()
        final_geo = materials[0] + time * robots[0]

        # Best case we'll keep building a geo robot each turn from now on.
        # If even that is not enough to improve, ignore the state.
        if final_geo + sum(range(1, time)) < best:
            continue

        # Accumulate geodes in the remaining time, and try to improve by
        # building more robots.
        best = max(best, final_geo)

        for ty, cost in enumerate(blueprint):
            # Skip time until we have accumulated the material cost, then wait 1
            # turn for production. A very low default denominator approximates
            # infinite build time for robots requiring unproduced materials.
            build_time = 1 + max(ceil(max(c - m, 0) / (r or 0.0001))
                                 for c, m, r in zip(cost, materials, robots))
            if build_time < time and robots[ty] < max_robots[ty]:
                newmat = tuple(m + r * build_time - c
                               for c, m, r in zip(cost, materials, robots))
                newrobots = tuple(r + (i == ty) for i, r in enumerate(robots))
                work.append((time - build_time, newmat, newrobots))

    return best

blueprints = list(map(parse_blueprint, sys.stdin))
print(sum((i + 1) * max_geo(bp, 24) for i, bp in enumerate(blueprints)))
a, b, c = (max_geo(bp, 32) for bp in blueprints[:3])
print(a * b * c)
