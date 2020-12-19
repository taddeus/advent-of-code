#!/usr/bin/env python3
import regex
import sys

def parse(f):
    rules = {}
    for line in f:
        if line == '\n':
            break
        ident, rule = line.rstrip().split(': ')
        rules[int(ident)] = rule.replace('"', '')
    return rules, f.read().splitlines()

def match(rules, messages):
    def expand(word):
        return group(int(word)) if word.isdigit() else word
    def group(ident):
        return '(?:' + ''.join(map(expand, rules[ident].split())) + ')'
    reg = regex.compile(group(0))
    return sum(reg.fullmatch(m) is not None for m in messages)

rules, messages = parse(sys.stdin)
print(match(rules, messages))

rules[8] = '42 +'
rules[11] = '(?P<group> 42 (?&group)? 31 )'
print(match(rules, messages))
