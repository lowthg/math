import random
from hashlib import sha256
import sympy

import sys

print(sys.version_info)

nbytes = 32
nbits = nbytes * 8
nmax = 2**nbits
r = 32
s = 30
N = 2**s

for k in range(1000):
    p = 2**128 - 2**s * k + 1
    if sympy.isprime(p):
        print('p = 2^128 - {}.2^{} + 1'.format(k, s))
        break
else:
    raise "Could not find prime p"

for x in range(1000):
    w = pow(x, (p-1)//N, p)
    a = pow(w, N//2, p)
    if a == p - 1:
        print(x)
        print(w)
        break
else:
    raise "Could not find w"

print("w = {}".format(hex(w)))

if False:
    values = [random.randrange(p) for _ in range(N)]
    nonces = [random.randbytes(16) for _ in range(N)]

    merkle = [None] * (s + 1)
    merkle[s] = [None] * N
    for i in range(N):
        merkle[s][i] = sha256(values[i].to_bytes(16) + nonces[i]).digest()

    for j in range(s, 0, -1):
        M = 2**(j-1)
        merkle[j - 1] = [None] * M
        for i in range(M):
            merkle[j-1][i] = sha256(merkle[j][2*i] + merkle[j][2*i + 1]).digest()

    root = merkle[0][0]
    print("Merkle root = {}".format(root.hex()))

    index = int.from_bytes(sha256(root).digest()) & (N - 1)

    print("Index = {}".format(index))
    print("      = {:010b}".format(index))

    value = values[index]
    nonce = nonces[index]
    print("Value = {}".format(value.to_bytes(16).hex()))
    print("Nonce = {}".format(nonce.hex()))

    proof = []
    for j in range(s, 0, -1):
        i = (index >> (s - j)) ^ 1
        proof.append(merkle[j][i])

    print("Merkle proof = [")
    for i in range(len(proof)):
        print("    {}{}".format(proof[i].hex(), ',' if i < s - 1 else ''))
    print("]")

    h = sha256(value.to_bytes(16) + nonce).digest()
    print('h = SHA256(value|nonce)')
    for i in range(s):
        if index & (1 << i) == 0:
            h = sha256(h + proof[i]).digest()
            print('h = SHA256(h|mp[{}])'.format(i))
        else:
            h = sha256(proof[i] + h).digest()
            print('h = SHA256(mp[{}]|h)'.format(i))

    print('  = {}'.format(h.hex()))
