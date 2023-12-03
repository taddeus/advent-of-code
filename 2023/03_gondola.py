#!/usr/bin/env python3
import sys

def parse(inp):
    numbers = []
    nmap = {}
    symbols = {}
    for y, line in enumerate(inp):
        num = ''
        for x, char in enumerate(line):
            if char.isdigit():
                num += char
                nmap[(x, y)] = len(numbers)
            else:
                if num:
                    numbers.append(int(num))
                    num = ''
                if char not in '.\n':
                    symbols[(x, y)] = char
    return numbers, nmap, symbols

def neighbors(x, y):
    for nx in (x - 1, x, x + 1):
        for ny in (y - 1, y, y + 1):
            if nx != x or ny != y:
                yield nx, ny

def gear_ratios(numbers, nmap, symbols):
    for (x, y), symbol in symbols.items():
        if symbol == '*':
            nb_nrs = set(nmap[nxy] for nxy in neighbors(x, y) if nxy in nmap)
            if len(nb_nrs) == 2:
                a, b = nb_nrs
                yield numbers[a] * numbers[b]

numbers, nmap, symbols = parse(sys.stdin)
partnrs = set(nmap.get(nxy, -1) for x, y in symbols for nxy in neighbors(x, y))
print(sum(numbers[i] for i in partnrs if i >= 0))
print(sum(gear_ratios(numbers, nmap, symbols)))
