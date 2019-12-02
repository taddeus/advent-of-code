#!/usr/bin/env python3
from hashlib import md5

key = 'iwrupvqb'

d = b'xxx'
i = -1
while d[0] + d[1] > 0 or d[2] > 0xf:
    i += 1
    d = md5((key + str(i)).encode('ascii')).digest()
print(i)

while sum(d[:3]) > 0:
    i += 1
    d = md5((key + str(i)).encode('ascii')).digest()
print(i)
