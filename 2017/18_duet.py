#!/usr/bin/env python3
import sys
from collections import defaultdict, deque


def parse(f):
    def maybe_reg(op):
        return op if op.isalpha() else int(op)

    for line in f:
        parts = line.split()
        opcode = parts[0]
        a = maybe_reg(parts[1])
        b = maybe_reg(parts[2]) if len(parts) == 3 else None
        yield opcode, a, b


def run(program, progid, part1=False):
    def value(val):
        return regs[val] if isinstance(val, str) else val

    regs = defaultdict(int)
    regs['p'] = progid
    sent = deque()
    received = deque()
    pc = 0

    while pc < len(program):
        opcode, a, b = program[pc]

        if opcode == 'snd':
            sent.append(value(a))
        elif opcode == 'set':
            regs[a] = value(b)
        elif opcode == 'add':
            regs[a] += value(b)
        elif opcode == 'mul':
            regs[a] *= value(b)
        elif opcode == 'mod':
            regs[a] %= value(b)
        elif opcode == 'rcv' and part1:
            if value(a):
                yield sent[-1]
        elif opcode == 'rcv':
            while not received:
                received = yield sent
                sent = deque()
            regs[a] = received.popleft()
        elif opcode == 'jgz' and value(a) > 0:
            pc += value(b) - 1

        pc += 1


# part 1
program = list(parse(sys.stdin))
print(next(run(program, 0, True)))

# part 2
prog0 = run(program, 0)
prog1 = run(program, 1)
q0 = next(prog0)
q1 = next(prog1)
sent1 = len(q1)
while q0 or q1:
    q0, q1 = prog0.send(q1), prog1.send(q0)
    sent1 += len(q1)
print(sent1)
