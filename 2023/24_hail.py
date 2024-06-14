#!/usr/bin/env python3
import sys
import re
from itertools import combinations

def intersect2d(path1, path2, low, high):
    # https://stackoverflow.com/questions/563198
    x1, y1, _, dx1, dy1, _ = path1
    x2, y2, _, dx2, dy2, _ = path2
    rs = dx1 * dy2 - dy1 * dx2
    if rs:
        t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / rs
        u = ((x2 - x1) * dy1 - (y2 - y1) * dx1) / rs
        if t >= 0 and u >= 0:
            x = x1 + t * dx1
            y = y1 + t * dy1
            return low <= x <= high and low <= y <= high
    return False

def cross(u, v):
    a, b, c = u
    d, e, f = v
    return (b * f - c * e), (c * d - a * f), (a * e - b * d)

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def add(u, v):
    return tuple(a + b for a, b in zip(u, v))

def sub(u, v):
    return add(u, mul(-1, v))

def mul(scalar, v):
    return tuple(scalar * x for x in v)

def intersect_all(paths):
    # take 3 hailstones and use one as the origin for the other two:
    (q0, u0), (q1, u1), (q2, u2) = ((x[:3], x[3:]) for x in paths[:3])
    p1 = sub(q1, q0)
    p2 = sub(q2, q0)
    v1 = sub(u1, u0)
    v2 = sub(u2, u0)
    # now there exist some t1 and t2 such that p1+t1v1 and p2+t2v2 are
    # collinear, meaning their cross-product is zero:
    #   0 = p1+t1v1 x p2+t2v2
    #     = p1 x p2 + p1 x t2v2 + t1v1 x p2 + t1v1 x t2v2
    #     = p1 x p2 + t2(p1 x v2) + t1(v1 x p2) + t1t2(v1 x v2)
    # given that (a x b)*a = (a x b)*b = 0, take dot product with v2 to get t1:
    #   0 = v2*(p1 x p2) + t1v2*(v1 x p2)
    #   t1 = v2*(p2 x p1) / v2*(v1 x p2)
    # take dot product with v1 to get t2:
    #   0 = v1*(p1 x p2) + t2v1*(p1 x v2)
    #   t2 = v1*(p2 x p1) / v1*(p1 x v2)
    t1 = dot(v2, cross(p2, p1)) / dot(v2, cross(v1, p2))
    t2 = dot(v1, cross(p2, p1)) / dot(v1, cross(p1, v2))
    # use intersection times to compute intersection coordinates:
    intersect1 = add(q1, mul(t1, u1))
    intersect2 = add(q2, mul(t2, u2))
    # draw a line back through the intersection coordinates to get the origin:
    velocity = mul(1 / (t2 - t1), sub(intersect2, intersect1))
    origin = sub(intersect1, mul(t1, velocity))
    return int(sum(origin))

paths = [tuple(map(int, re.findall(r'-?\d+', line))) for line in sys.stdin]
print(sum(intersect2d(a, b, 2e14, 4e14) for a, b in combinations(paths, 2)))
print(intersect_all(paths))
