#!/usr/bin/env python3
import sys
from functools import partial, reduce

# get modular multiplicative inverse for prime p
def prime_modinv(p, mod):
    return pow(p, mod - 2, mod)

# get (a, b) coefficients for inverse linear index mapping functions ax+b
def inverse_functions(instructions, ncards):
    for line in reversed(instructions):
        if line == 'deal into new stack\n':
            yield -1, ncards - 1
        elif line.startswith('cut'):
            amount = int(line.split()[1])
            yield 1, amount
        else:
            increment = int(line.split()[-1])
            yield prime_modinv(increment, ncards), 0

# compose all inverse mappings into a single linear function
def inverse_function(instructions, ncards):
    functions = inverse_functions(instructions, ncards)
    return reduce(partial(fcompose, ncards), functions, (1, 0))

# compose linear functions ax+b and cx+d
def fcompose(mod, f, g):
    a, b = f
    c, d = g
    return c * a % mod, (c * b + d) % mod

# compute f(x) = ax+b
def fapply(f, x, mod):
    a, b = f
    return (a * x + b) % mod

# repeat ax+b n times
def frepeat(f, n, mod):
    if n == 0:
        return 1, 0
    if n == 1:
        return f
    half, odd = divmod(n, 2)
    g = frepeat(f, half, mod)
    gg = fcompose(mod, g, g)
    return fcompose(mod, f, gg) if odd else gg

def find_card(value, ncards, instructions):
    f = inverse_function(instructions, ncards)
    return next(i for i in range(ncards) if fapply(f, i, ncards) == value)

def card_at(index, ncards, nshuffles, instructions):
    f = inverse_function(instructions, ncards)
    fn = frepeat(f, nshuffles, ncards)
    return fapply(fn, index, ncards)

instructions = list(sys.stdin)
print(find_card(2019, 10007, instructions))
print(card_at(2020, 119315717514047, 101741582076661, instructions))
