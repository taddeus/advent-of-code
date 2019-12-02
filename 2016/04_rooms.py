#!/usr/bin/env python3
import sys
from collections import defaultdict


def parse(f):
    for line in f:
        name, rest = line.rstrip().rsplit('-', 1)
        sector, checksum = rest[:-1].split('[')
        yield name.replace('-', ''), int(sector), checksum


def is_real(name, checksum):
    count = defaultdict(int)
    for char in name:
        count[char] -= 1
    check = ''.join(sorted(count, key=lambda x: (count[x], x))[:5])
    return check == checksum


def decrypt(name, sector):
    return ''.join(chr((ord(c) - 97 + sector) % 26 + 97) for c in name)


rooms = list(parse(sys.stdin))
print(sum(s for n, s, c in rooms if is_real(n, c)))

for name, sector, checksum in rooms:
    if decrypt(name, sector) == 'northpoleobjectstorage':
        print(sector)
        break
