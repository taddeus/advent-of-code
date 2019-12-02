#!/usr/bin/env python3
import sys
from operator import and_, or_, lshift, rshift, inv

opmap = {'AND': and_, 'OR': or_, 'LSHIFT': lshift,
         'RSHIFT': rshift, 'NOT': inv}
WIRE, UNARY, BINARY, CONST = range(4)
imax = 1 << 16
wires = {}

def wrap(val):
    return (CONST, int(val)) if val.isdigit() else (WIRE, val)

for line in sys.stdin:
    left, res = line.rstrip().split(' -> ')
    parts = left.split()

    if len(parts) == 1:
        wires[res] = wrap(parts[0])
    elif len(parts) == 2:
        op, operand = parts
        wires[res] = UNARY, opmap[op], wrap(operand)
    elif len(parts) == 3:
        left, op, right = parts
        wires[res] = BINARY, wrap(left), opmap[op], wrap(right)

def underflow(i):
    return ((i + imax) % imax) & (imax - 1)

def compute(wire, cache):
    ty = wire[0]

    if ty == CONST:
        return wire[1]

    if ty == WIRE:
        x = wire[1]
        if x not in cache:
            cache[x] = compute(wires[x], cache)
        return cache[x]

    if ty == UNARY:
        op, operand = wire[1:]
        return underflow(op(compute(operand, cache)))

    assert ty == BINARY
    left, op, right = wire[1:]
    return underflow(op(compute(left, cache), compute(right, cache)))

a = compute(wires['a'], {})
print(a)
print(compute(wires['a'], {'b': a}))
