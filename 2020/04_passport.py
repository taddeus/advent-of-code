#!/usr/bin/env python3
import re
import sys

def parse(f):
    cur = {}
    for line in f:
        if line == '\n':
            yield cur
            cur = {}
        else:
            for pair in line.rstrip().split():
                key, val = pair.split(':')
                cur[key] = val
    if cur:
        yield cur

required = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')

def valid_basic(pp):
    return all(key in pp for key in required)

def valid_strict(pp):
    def isnum(key, lo, hi, suffix=''):
        val = pp[key]
        if not val.endswith(suffix):
            return False
        val = val[:len(val) - len(suffix)]
        return val.isdigit() and lo <= int(val) <= hi

    return valid_basic(pp) and \
           isnum('byr', 1920, 2002) and \
           isnum('iyr', 2010, 2020) and \
           isnum('eyr', 2020, 2030) and \
           (isnum('hgt', 150, 193, 'cm') or isnum('hgt', 59, 76, 'in')) and \
           re.match(r'#[0-9a-f]{6}$', pp['hcl']) is not None and \
           pp['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth') and \
           re.match(r'\d{9}$', pp['pid']) is not None


passports = list(parse(sys.stdin))
print(sum(map(valid_basic, passports)))
print(sum(map(valid_strict, passports)))
