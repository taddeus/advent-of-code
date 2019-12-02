#!/usr/bin/env python3
import fileinput
masses = [int(line) for line in fileinput.input()]

def fuel(mass):
    return int(mass / 3) - 2

def fuelrec(mass):
    f = fuel(mass)
    total = 0
    while f >= 0:
        total += f
        mass = f
        f = fuel(mass)
    return total

print(sum(map(fuel, masses)))
print(sum(map(fuelrec, masses)))
