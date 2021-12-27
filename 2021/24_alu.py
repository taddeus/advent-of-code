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

def simplify(e, constraints):
    lconst = isinstance(e.left, int)
    rconst = isinstance(e.right, int)

    if lconst and rconst:
        return int(OPS[e.opcode](e.left, e.right))
    elif lconst and e.opcode in ('add', 'mul', 'eql'):
        return simplify(Expr(e.opcode, e.right, e.left), constraints)

    if e.opcode == 'add':
        # a + 0 -> a
        # (a + 1) + 2 -> a + 3
        if e.right == 0:
            return e.left
        if e.left.opcode == 'add':
            return Expr('add', e.left.left, e.left.right + e.right)
    elif e.opcode == 'mul':
        # a * 0 -> 0
        # a * 1 -> a
        if e.right == 0:
            return 0
        if e.right == 1:
            return e.left
    elif e.opcode == 'eql':
        # ((a % 26) + larger_than_9) == inp[i] -> 0
        # (inp[i] + offset) == inp[j] -> 1, record constraint (i, j, offset)
        offset = e.left.right
        if rconst or offset > 9:
            return 0
        constraints.append((e.left.left.left, e.right.left, offset))
        return 1
    elif e.opcode == 'div':
        # a / 1 -> a
        # ((a * 26) + b) / 26 -> a
        return e.left if e.right == 1 else e.left.left.left
    elif e.opcode == 'mod':
        # (inp[i] + smaller_than_17) % 26 -> inp[i] + smaller_than_17
        # ((a * 26) + b) % 26 -> b
        return e.left if e.left.left.opcode == 'inp' else e.left.right

    return e

def input_constraints(nomad):
    constraints = []
    regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    index = 0
    for opcode, reg, operand in nomad:
        if opcode == 'inp':
            regs[reg] = Expr('inp', index, None)
            index += 1
        else:
            if not isinstance(operand, int):
                operand = regs[operand]
            regs[reg] = simplify(Expr(opcode, regs[reg], operand), constraints)
    return constraints

def modelnum(constraints, largest):
    nr = [0] * 14
    for a, b, offset in constraints:
        nr[a] = 9 - max(offset, 0) if largest else 1 - min(offset, 0)
        nr[b] = nr[a] + offset
    return ''.join(map(str, nr))

constraints = input_constraints(map(parse, sys.stdin))
print(modelnum(constraints, True))
print(modelnum(constraints, False))
