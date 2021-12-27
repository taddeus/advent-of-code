#!/usr/bin/env python3
import sys
from operator import add, mul, floordiv, mod, eq

OPS = {'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': eq}

class Expr:
    def __init__(self, opcode, left, right):
        self.opcode = opcode
        self.left = left
        self.right = right

    def reduce(self, conditions):
        lconst = isinstance(self.left, int)
        rconst = isinstance(self.right, int)

        if lconst and rconst:
            return int(OPS[self.opcode](self.left, self.right))
        elif lconst and self.opcode in ('add', 'mul', 'eql'):
            return Expr(self.opcode, self.right, self.left).reduce(conditions)

        if self.opcode == 'add':
            if self.right == 0:
                return self.left
            if self.left.opcode == 'add':
                right = self.left.right + self.right
                return Expr('add', self.left.left, right)
        elif self.opcode == 'mul':
            if self.right == 0:
                return 0
            if self.right == 1:
                return self.left
        elif self.opcode == 'eql':
            offset = self.left.right
            if rconst or offset > 9:
                return 0
            conditions.append((self.left.left.left, self.right.left, offset))
            return 1
        elif self.opcode == 'div':
            return self.left if self.right == 1 else self.left.left.left
        elif self.opcode == 'mod':
            if self.left.left.opcode == 'inp':
                return self.left
            return self.left.right

        return self

def parse(line):
    parts = line.split()
    if len(parts) == 2:
        operand = None
    elif parts[2].isdigit() or parts[2].startswith('-'):
        operand = int(parts[2])
    else:
        operand = parts[2]
    return parts[0], parts[1], operand

def input_conditions(program):
    conditions = []
    regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    index = 0
    for opcode, reg, operand in program:
        if opcode == 'inp':
            regs[reg] = Expr('inp', index, None)
            index += 1
        else:
            if not isinstance(operand, int):
                operand = regs[operand]
            regs[reg] = Expr(opcode, regs[reg], operand).reduce(conditions)
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
