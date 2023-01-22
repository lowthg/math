import random
from hashlib import sha256
import sympy

nbytes = 32
nbits = nbytes * 8
nmax = 2**nbits
r = 32
s = 10

for k in range(1000):
    p = 2**128 - 2**s * k + 1
    if sympy.isprime(p):
        print('p = 2^128 - {}.2^{} + 1'.format(k, s))
        break
else:
    raise "Could not find prime p"


index = random.getrandbits(s)
value = random.randbytes(16)
nonce = random.randbytes(16)
mp = []
for _ in range(s):
    mp.append(random.randbytes(32))

index = 443 # 110111011
value = bytes.fromhex('bb4f277c3363799eed6f2fcf487a96da')
nonce = bytes.fromhex('975f6b6b174df49c3af42206d3181233')
mp = [
    bytes.fromhex('97b41015e6b963781ab9dbebb68fdcb86e12fa7827f82cbcc5bc25947ecb33a8'),
    bytes.fromhex('b277289a3aebd0b7545e247599e4973312f8483dcd5336925589bec5f7d50623'),
    bytes.fromhex('7e7df590e1cc835dadb2eaeda189862ead27f61c1d2adaf25cce6f56b88a042a'),
    bytes.fromhex('e2863ca2f8622e0cbde1f4c9db8844534050f6d8410cd2f4bbb2dbc87dad5d25'),
    bytes.fromhex('f6462d385b254ea111d607450333ce577fa915592dd69c357b5e4a7800583339'),
    bytes.fromhex('7761a772580544d875067176f55f68b7b3a8f0d67e45ecc0635ab1e2700e1e09'),
    bytes.fromhex('c0059601a7d12e7da479651c42fff3e223bb3970234d322a4ba8f5c0edd42ecd'),
    bytes.fromhex('18e56a47d23de5ff37c909a5c8faeb197a7174ef7c2fed8123449688270154e2'),
    bytes.fromhex('42bd7bd0794085451fcf14274d02855f0fce975b8f0ae11ef096b90772f35fb7'),
    bytes.fromhex('e4d4cae75b2097f856878c6229eb67d8e60e4b28bb824ece1e18597bde30484e')
]
mr = bytes.fromhex('21124f1744293648120613fc60b805e24985d060f7cb4ccdaefc13c10a0d0cd3')

print("index = {}".format(index))
print("      = {:b}".format(index))



print('value = {}'.format(value.hex()))
print('nonce = {}'.format(nonce.hex()))


print('merkle proof = [')
for x in mp[:-1]:
    print('    {},'.format(x.hex()))
print('    {}'.format(mp[-1].hex()))
print(']')

h = sha256(value + nonce).digest()
print('h[0]  = SHA256(value|nonce)')
for i in range(len(mp)):
    str1 = ' ' if i < 9 else ''
    if (1 << i) & index == 0:
        h = sha256(h + mp[i]).digest()
        print('h[{}]{} = SHA256(h[{}]|mp[{}])'.format(i + 1, str1, i, i))
    else:
        h = sha256(mp[i] + h).digest()
        print('h[{}]{} = SHA256(mp[{}]|h[{}])'.format(i + 1, str1, i, i))

print('      = {}'.format(h.hex()))
print('root  = {}'.format(mr.hex()))
