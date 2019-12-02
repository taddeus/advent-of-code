#!/usr/bin/env python3
import sys
from operator import add, sub, gt, ge, lt, le, eq, ne
from collections import defaultdict

ops = { 'inc': add, 'dec': sub}
tests = {'>': gt, '>=': ge, '<': lt, '<=': le, '==': eq, '!=': ne}

def parse(f):
    for line in f:
        inst, cond = line.rstrip().split(' if ')
        outreg, op, opnd = inst.split()
        treg, t, tconst = cond.split()
        yield outreg, ops[op], int(opnd), treg, tests[t], int(tconst)

regs = defaultdict(int)
allmax = 0
for outreg, op, opconst, testreg, test, testconst in parse(sys.stdin):
    if test(regs[testreg], testconst):
        regs[outreg] = op(regs[outreg], opconst)
    curmax = max(regs.values())
    allmax = max(allmax, curmax)
print(curmax)
print(allmax)
