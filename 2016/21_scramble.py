#!/usr/bin/env python3
import sys
from collections import deque

def scramble(password, instructions, unscramble=False):
    pw = deque(password)
    if unscramble:
        instructions = reversed(instructions)
    for words in instructions:
        if words[0] == 'swap':
            index = pw.index if words[1] == 'letter' else int
            i = index(words[2])
            j = index(words[5])
            pw[i], pw[j] = pw[j], pw[i]
        elif words[0] == 'rotate':
            if words[1] == 'based':
                i = pw.index(words[-1])
                if unscramble:
                    oldi = i
                    while (2 * oldi + 1 + (oldi >= 4)) % len(pw) != i:
                        oldi = (oldi - 1) % len(pw)
                        pw.rotate(-1)
                    continue
                index = i + 1 + (i >= 4)
            elif words[1] == 'left':
                index = -int(words[2])
            else:
                index = int(words[2])
            pw.rotate(-index if unscramble else index)
        elif words[0] == 'reverse':
            start, end = map(int, words[2::2])
            while start < end:
                pw[start], pw[end] = pw[end], pw[start]
                start += 1
                end -= 1
        elif words[0] == 'move':
            src, dst = map(int, words[2::3])
            if unscramble:
                src, dst = dst, src
            letter = pw[src]
            del pw[src]
            pw.insert(dst, letter)
    return ''.join(pw)

instructions = [line.split() for line in sys.stdin]
print(scramble('abcdefgh', instructions))
print(scramble('fbgdceah', instructions, True))
