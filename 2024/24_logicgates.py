#!/usr/bin/env python3
import sys
from functools import reduce
from itertools import takewhile
from operator import and_, or_, xor

def parse(f):
    initial = {line[:3]: int(line[5])
               for line in takewhile(lambda line: line != '\n', f)}
    rules = {}
    for line in f:
        left, op, right, _, out = line.split()
        rules[out] = {'AND': and_, 'OR': or_, 'XOR': xor}[op], left, right
    return initial, rules

def evaluate(initial, rules):
    def value(name):
        if name in initial:
            return initial[name]
        op, left, right = rules[name]
        return op(value(left), value(right))
    return reduce(or_, (value(z) << int(z[1:]) for z in rules if z[0] == 'z'))

def construct_xy(op, i):
    return op, 'x%02d' % i, 'y%02d' % i

def construct_carry(i):
    carry = construct_xy(and_, i)
    if i == 0:
        return carry
    lhs = and_, construct_carry(i - 1), construct_xy(xor, i)
    return or_, lhs, construct_xy(and_, i)

def construct_z(i, initial):
    adder = construct_xy(xor, i)
    if i == 0:
        return adder
    carry = construct_carry(i - 1)
    if 'x%02d' % i not in initial:
        return carry
    return xor, carry, adder

def tostr(construct, rules):
    match construct:
        case op, left, right:
            op_str = {and_: '&', or_: '|', xor: '^'}[op]
            left, right = sorted((tostr(left, rules), tostr(right, rules)))
            return f'({left} {op_str} {right})'
        case str(node):
            return tostr(rules[node], rules) if node in rules else node

def find_incorrect(initial, rules):
    def expect(name, expected):
        if name in rules:
            op, left, right = rules[name]
            eop, eleft, eright = expected
            if op != eop:
                return {name}
            (lstr, left), (rstr, right) = sorted(((tostr(left, rules), left),
                                                  (tostr(right, rules), right)))
            if left in rules and right in rules:
                return expect(left, eleft) | expect(right, eright)
            if lstr != tostr(eleft, rules):
                return {left}
            if rstr != tostr(eright, rules):
                return {right}
        return set()
    return reduce(set.union, (expect(name, construct_z(int(name[1:]), initial))
                              for name in rules if name[0] == 'z'))

initial, rules = parse(sys.stdin)
print(evaluate(initial, rules))
print(','.join(sorted(find_incorrect(initial, rules))))
