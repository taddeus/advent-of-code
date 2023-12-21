#!/usr/bin/env python3
import sys
import re

def parse_rule(rule):
    if ':' not in rule:
        return 0, (1, 4000), rule
    left, op, right, _, destination = re.split('([<>:])', rule)
    rating = 'xmas'.index(left)
    rating_range = (1, int(right) - 1) if op == '<' else (int(right) + 1, 4000)
    return rating, rating_range, destination

def parse(inp):
    flows = {}
    for line in inp:
        if line == '\n':
            break
        flow, rule_strings = line[:-2].split('{')
        flows[flow] = list(map(parse_rule, rule_strings.split(',')))
    parts = [tuple(map(int, re.findall(r'\d+', line))) for line in inp]
    return flows, parts

def at(ranges, i, lower, upper):
    return *ranges[:i], (lower, upper), *ranges[i + 1:]

def naccept(ranges, flows, flow):
    if flow == 'R':
        return 0
    if flow == 'A':
        x, m, a, s = (upper - lower + 1 for lower, upper in ranges)
        return x * m * a * s
    acc = 0
    for i, (imin, imax), dst in flows[flow]:
        rmin, rmax = ranges[i]
        lower = max(rmin, imin)
        upper = min(rmax, imax)
        if upper >= lower:
            acc += naccept(at(ranges, i, lower, upper), flows, dst)
            if rmin < imin:
                acc += naccept(at(ranges, i, rmin, imin - 1), flows, flow)
            if rmax > imax:
                acc += naccept(at(ranges, i, imax + 1, rmax), flows, flow)
            break
    return acc

flows, parts = parse(sys.stdin)
print(sum(sum(p) for p in parts if naccept(tuple(zip(p, p)), flows, 'in')))
print(naccept(((1, 4000),) * 4, flows, 'in'))
