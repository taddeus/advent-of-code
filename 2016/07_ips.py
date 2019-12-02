#!/usr/bin/env python3
import sys
from collections import deque


def sequences(ip, length):
    buf = deque()
    in_brackets = False
    for char in ip:
        if char in '[]':
            in_brackets = char == '['
            buf.clear()
        else:
            buf.append(char)
            if len(buf) == length:
                yield ''.join(buf), in_brackets
                buf.popleft()


def supports_tls(ip):
    has_abba = False
    for (a, b, c, d), in_brackets in sequences(ip, 4):
        if a != b and a == d and b == c:
            if in_brackets:
                return False
            has_abba = True
    return has_abba


def supports_ssl(ip):
    brack = set()
    nobrack = set()
    for (a, b, c), in_brackets in sequences(ip, 3):
        if a != b and a == c:
            if b + a in (nobrack if in_brackets else brack):
                return True
            (brack if in_brackets else nobrack).add(a + b)
    return False


ips = [line.rstrip() for line in sys.stdin]
print(sum(int(supports_tls(ip)) for ip in ips))
print(sum(int(supports_ssl(ip)) for ip in ips))
