#!/usr/bin/env python3
import sys
import re
import z3
from operator import itemgetter

bots = [tuple(map(int, re.findall(r'-?[0-9]+', line))) for line in sys.stdin]

# part 1
x, y, z, r = max(bots, key=itemgetter(3))
print(sum(int(abs(bx - x) + abs(by - y) + abs(bz - z) <= r)
          for bx, by, bz, br in bots))

# part 2
def zabs(x):
    return z3.If(x >= 0, x, -x)

def dist(xa, ya, za, xb, yb, zb):
    return zabs(xb - xa) + zabs(yb - ya) + zabs(zb - za)

# build an optimizing model with the solution and its intersections as variables
x, y, z = z3.Ints('x y z')
opt = z3.Optimize()

# maximize: number of intersecting bots
nisect = sum(z3.If(dist(bx, by, bz, x, y, z) <= br, 1, 0)
             for bx, by, bz, br in bots)
bestisect = opt.maximize(nisect)

# minimize: manhattan distance of solution to (0, 0, 0)
bestdist = opt.minimize(dist(x, y, z, 0, 0, 0))

assert opt.check() == z3.sat
#print(opt.model())
print('best teleportation point at %s from origin (%s nanobots in range)' %
      (bestdist.value(), bestisect.value()))
