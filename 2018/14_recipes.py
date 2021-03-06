#!/usr/bin/env python3
s = n = 440231
nb = bytes()
while s:
    s, d = divmod(s, 10)
    nb = bytes((d,)) + nb
scores = bytearray((3, 7))
a, b = 0, 1

while len(scores) <= 11 + n or nb not in scores[-8:]:
    sa = scores[a]
    sb = scores[b]
    s = sa + sb
    if s >= 10:
        scores.append(s // 10)
    scores.append(s % 10)
    a = (a + 1 + sa) % len(scores)
    b = (b + 1 + sb) % len(scores)

print(''.join(chr(x + ord('0')) for x in scores[n:n + 10]))
print(scores.rindex(nb))
