#!/usr/bin/env python3
import sys


def count_mul(program):
    def get(arg):
        return int(arg) if arg.isdigit() or arg.startswith('-') else regs[arg]

    regs = {'a': 0, 'h': 0}
    muls = 0
    pc = 0

    while pc < len(program):
        opcode, a, b = program[pc]

        if opcode == 'set':
            regs[a] = get(b)
        elif opcode == 'sub':
            regs[a] -= get(b)
        elif opcode == 'mul':
            muls += 1
            regs[a] *= get(b)
        elif opcode == 'jnz':
            if get(a):
                pc += get(b) - 1

        pc += 1

    return muls


def primes_sieve(n):
    sieve = [1] * n
    for i in range(2, n):
        if sieve[i]:
            for m in range(i * i, n, i):
                sieve[m] = 0
    return sieve


def compute_h():
    # This emulates the program, which computes the number of non-primes between
    # b and c at intervals of 17
    b = 109900
    c = b + 17000 + 1

    is_prime = [1] * c
    for i in range(2, c):
        if is_prime[i]:
            for m in range(i * i, c, i):
                is_prime[m] = 0

    return sum(1 - is_prime[i] for i in range(b, c, 17))


program = [line.split() for line in sys.stdin]
print(count_mul(program))
print(compute_h())
