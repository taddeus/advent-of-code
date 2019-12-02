#!/usr/bin/env python3
import sys
from collections import Counter

class Program:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children
        self.accweight = None

    @classmethod
    def parse(cls, f):
        parents = {}
        progs = {}
        for line in f:
            if '->' in line:
                left, right = line.rstrip().split(' -> ')
                children = right.split(', ')
            else:
                left = line.rstrip()
                children = []
            name, weight = left[:-1].split(' (')
            prog = cls(name, int(weight), children)
            for child in children:
                parents[child] = name
            progs[name] = prog

        for p in progs.values():
            p.children = [progs[child] for child in p.children]

        return next(p for name, p in progs.items() if name not in parents)

    def postorder(self):
        for child in self.children:
            yield from child.postorder()
        yield self

    def tower_weight(self):
        if self.accweight is None:
            self.accweight = self.weight + sum(c.tower_weight()
                                               for c in self.children)
        return self.accweight

    def find_unbalanced(self):
        for prog in self.postorder():
            weights = Counter(c.tower_weight() for c in prog.children)
            if len(weights) > 1:
                assert len(weights) == 2
                unba, ba = (p[1] for p in sorted((n, w) for w, n in weights.items()))
                u = next(c for c in prog.children if c.tower_weight() == unba)
                return u.weight + ba - unba

root = Program.parse(sys.stdin)
print(root.name)
print(root.find_unbalanced())
