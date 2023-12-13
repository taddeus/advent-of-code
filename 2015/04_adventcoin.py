#!/usr/bin/env python3
from hashlib import md5
from itertools import count

hashes = ((i, md5(b'iwrupvqb%d' % i).hexdigest()) for i in count(0))
print(next(i for i, h in hashes if h[:5] == '00000'))
print(next(i for i, h in hashes if h[:6] == '000000'))
