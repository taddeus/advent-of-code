#!/usr/bin/env python3
import sys
from functools import reduce
from operator import mul, or_

def parse(f):
    rules = {}
    for line in f:
        if line == '\n':
            break
        field, ranges = line.rstrip().split(': ')
        rules[field] = valid = set()
        for rangestr in ranges.split(' or '):
            start, end = rangestr.split('-')
            valid |= set(range(int(start), int(end) + 1))

    assert next(f) == 'your ticket:\n'
    mine = tuple(map(int, next(f).split(',')))

    assert next(f) == '\n'
    assert next(f) == 'nearby tickets:\n'
    nearby = []
    for line in f:
        nearby.append(tuple(map(int, line.split(','))))

    return rules, mine, nearby

def filter_valid(rules, tickets):
    valid = []
    error_rate = 0
    for ticket in tickets:
        errors = [field for field in ticket
                  if not any(field in values for values in rules.values())]
        if errors:
            error_rate += sum(errors)
        else:
            valid.append(ticket)
    return error_rate, valid

def field_order(rules, tickets):
    order = [set(rules) for field in tickets[0]]
    for ticket in tickets:
        for field, names in zip(ticket, order):
            names -= {n for n in names if field not in rules[n]}

    known = {names.pop(): i for i, names in enumerate(order) if len(names) == 1}
    while len(known) != len(tickets[0]):
        for i, names in enumerate(order):
            names -= set(known)
            if len(names) == 1:
                known[names.pop()] = i
    return [n for i, n in sorted((i, n) for n, i in known.items())]

rules, mine, nearby = parse(sys.stdin)
error_rate, valid = filter_valid(rules, nearby)
print(error_rate)

order = field_order(rules, [mine] + valid)
departure = (mine[i] for i, n in enumerate(order) if n.startswith('departure'))
print(reduce(mul, departure))
