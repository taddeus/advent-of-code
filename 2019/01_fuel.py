#!/usr/bin/env python3
import sys

def fuel(mass):
    return mass // 3 - 2

def fuelrec(mass):
    f = fuel(mass)
    total = 0
    while f >= 0:
        total += f
        mass = f
        f = fuel(mass)
    return total

masses = [int(line) for line in sys.stdin]
print(sum(map(fuel, masses)))
print(sum(map(fuelrec, masses)))
