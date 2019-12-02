#!/usr/bin/env python3
import sys

def valid(pp, match_anagrams):
    words = pp.split()
    if match_anagrams:
        words = [''.join(sorted(w)) for w in words]
    return len(set(words)) == len(words)

passphrases = [line.rstrip() for line in sys.stdin]
print(sum(int(valid(pp, False)) for pp in passphrases))
print(sum(int(valid(pp, True)) for pp in passphrases))
