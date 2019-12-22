#!/usr/bin/env python3
import sys
from functools import partial, reduce

# get (a, b) coefficients for inverse linear index mapping functions ax+b
def inverse_functions(instructions, ncards):
    for line in reversed(instructions):
        words = line.split()
        if words[0] == 'cut':
            yield 1, int(words[1])
        elif words[1] == 'into':
            yield -1, ncards - 1
        else:
            increment = int(words[-1])
            index_increment = pow(increment, ncards - 2, ncards)
            yield index_increment, 0

# compose linear functions ax+b and cx+d
def compose(mod, f, g):
    a, b = f
    c, d = g
    return c * a % mod, (c * b + d) % mod

# repeat ax+b n times
def repeat_linear(f, n, mod):
    if n == 0:
        return 1, 0
    if n == 1:
        return f
    half, odd = divmod(n, 2)
    g = repeat_linear(f, half, mod)
    g = compose(mod, g, g)
    return compose(mod, f, g) if odd else g

def card_at(index, ncards, nshuffles, instructions):
    functions = inverse_functions(instructions, ncards)
    invmap = reduce(partial(compose, ncards), functions, (1, 0))
    a, b = repeat_linear(invmap, nshuffles, ncards)
    return (index * a + b) % ncards

instructions = list(sys.stdin)
print(next(i for i in range(10007) if card_at(i, 10007, 1, instructions) == 2019))
print(card_at(2020, 119315717514047, 101741582076661, instructions))
