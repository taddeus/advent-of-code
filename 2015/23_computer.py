#!/usr/bin/env python3
import sys

def parse(f):
    def cast(op):
        return int(op) if op[0] in '+-' else op

    for line in f:
        opcode, ops = line.rstrip().split(' ', 1)
        if ',' in ops:
            op1, op2 = ops.split(', ')
            yield opcode, cast(op1), cast(op2)
        else:
            yield opcode, cast(ops), None

def run(program, a):
    regs = {'a': a, 'b': 0}
    pc = 0
    while pc < len(program):
        opcode, op1, op2 = program[pc]
        if opcode == 'hlf':
            regs[op1] //= 2
        elif opcode == 'tpl':
            regs[op1] *= 3
        elif opcode == 'inc':
            regs[op1] += 1
        elif opcode == 'jmp':
            pc += op1 - 1
        elif opcode == 'jie':
            if regs[op1] % 2 == 0:
                pc += op2 - 1
        elif opcode == 'jio':
            if regs[op1] == 1:
                pc += op2 - 1
        pc += 1
    return regs['b']

program = list(parse(sys.stdin))
print(run(program, 0))
print(run(program, 1))
