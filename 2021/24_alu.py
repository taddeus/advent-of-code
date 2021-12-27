#!/usr/bin/env python3
import sys
from operator import add, mul, floordiv, mod, eq

OPS = {'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': eq}

def isoffset(e):
    return isinstance(e, Expr) \
            and e.opcode == 'add' \
            and isinstance(e.right, int) \
            and isinstance(e.left, Expr) \
            and e.left.opcode == 'inp'

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
            if rconst and self.left.opcode == 'add' and isinstance(self.left.right, int):
                return Expr('add', self.left.left, self.left.right + self.right)
        elif self.opcode == 'mul':
            if self.right == 0:
                return 0
            if self.right == 1:
                return self.left
        elif self.opcode == 'eql':
            if rconst:
                if self.left.opcode == 'inp' and self.right < 1 or self.right > 9:
                    return 0
            elif self.right.opcode == 'inp':
                if self.left.opcode == 'add' \
                        and isinstance(self.left.right, int) \
                        and self.left.right > 9:
                    return 0
                else:
                    assert isoffset(self.left)
                    index_a = self.left.left.left
                    offset = self.left.right
                    index_b = self.right.left
                    assert index_a < index_b
                    conditions.append((index_a, index_b, offset))
                    return 1
        elif self.opcode == 'div':
            if self.right == 1:
                return self.left
            if rconst and self.left.opcode == 'add' \
                    and isoffset(self.left.right) \
                    and self.left.left.opcode == 'mul' \
                    and self.left.left.right == self.right:
                return self.left.left.left
        elif self.opcode == 'mod':
            if self.left.opcode == 'add' and self.right == 26:
                return self.left if isoffset(self.left) else self.left.right

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
