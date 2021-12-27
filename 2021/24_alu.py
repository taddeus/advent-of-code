#!/usr/bin/env python3
import sys
from collections import namedtuple
from operator import add, mul, floordiv, mod, eq

Expr = namedtuple('Expr', 'opcode, left, right')
OPS = {'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': eq}

def parse(line):
    parts = line.split()
    if len(parts) == 2:
        operand = None
    elif parts[2].isdigit() or parts[2].startswith('-'):
        operand = int(parts[2])
    else:
        operand = parts[2]
    return parts[0], parts[1], operand

def simplify(e, conditions):
    lconst = isinstance(e.left, int)
    rconst = isinstance(e.right, int)

    if lconst and rconst:
        return int(OPS[e.opcode](e.left, e.right))
    elif lconst and e.opcode in ('add', 'mul', 'eql'):
        return simplify(Expr(e.opcode, e.right, e.left), conditions)

    if e.opcode == 'add':
        if e.right == 0:
            return e.left
        if e.left.opcode == 'add':
            return Expr('add', e.left.left, e.left.right + e.right)
    elif e.opcode == 'mul':
        if e.right == 0:
            return 0
        if e.right == 1:
            return e.left
    elif e.opcode == 'eql':
        offset = e.left.right
        if rconst or offset > 9:
            return 0
        conditions.append((e.left.left.left, e.right.left, offset))
        return 1
    elif e.opcode == 'div':
        return e.left if e.right == 1 else e.left.left.left
    elif e.opcode == 'mod':
        return e.left if e.left.left.opcode == 'inp' else e.left.right

    return e

def input_conditions(nomad):
    conditions = []
    regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    index = 0
    for opcode, reg, operand in nomad:
        if opcode == 'inp':
            regs[reg] = Expr('inp', index, None)
            index += 1
        else:
            if not isinstance(operand, int):
                operand = regs[operand]
            regs[reg] = simplify(Expr(opcode, regs[reg], operand), conditions)
    return conditions

def modelnum(conditions, largest):
    nr = [0] * 14
    for a, b, offset in conditions:
        nr[a] = 9 - max(offset, 0) if largest else 1 - min(offset, 0)
        nr[b] = nr[a] + offset
    return ''.join(map(str, nr))

conditions = input_conditions(map(parse, sys.stdin))
print(modelnum(conditions, True))
print(modelnum(conditions, False))
