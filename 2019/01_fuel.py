#!/usr/bin/env python3
import sys

def fuel(mass):
    return mass // 3 - 2

def fuelrec(mass):
    total = f = 0
    while f >= 0:
        total += f
        mass = f = fuel(mass)
    return total

masses = [int(line) for line in sys.stdin]
print(sum(map(fuel, masses)))
print(sum(map(fuelrec, masses)))
