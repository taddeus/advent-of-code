#!/usr/bin/env python3
import sys
from random import shuffle

def parse(f):
    ltrans, start = f.read().rstrip().split('\n\n')
    trans = {}
    for line in ltrans.split('\n'):
        key, val = line.split(' => ')
        trans.setdefault(key, []).append(val)
    return trans, start

def replace_one(mol, trans):
    for i, c in enumerate(mol):
        if c in trans:
            for repl in trans[c]:
                yield mol[:i] + repl + mol[i + 1:]
        elif i < len(mol) - 1:
            key = c + mol[i + 1]
            if key in trans:
                for repl in trans[key]:
                    yield mol[:i] + repl + mol[i + 2:]

def steps_to_e(target, trans):
    revtrans = {val: key for key, vals in trans.items() for val in vals}
    keys = list(revtrans)

    steps = 0
    mol = target
    while mol != 'e':
        oldsteps = steps

        shuffle(keys)
        for key in keys:
            n = mol.count(key)
            if n:
                steps += n
                mol = mol.replace(key, revtrans[key])

        if steps == oldsteps:
            steps = 0
            mol = target

    return steps

# part 1
trans, medicine = parse(sys.stdin)
print(len(set(replace_one(medicine, trans))))

# part 2
print(steps_to_e(medicine, trans))
