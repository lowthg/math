from random import randrange


def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r >>= 1
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def inv(x):  # need 0 < x < p
    x1, x2 = (p, x % p)
    a1, a2 = (0, 1)
    while x2 != 0:
        c = x1 // x2
        x1, x2 = (x2, x1 - c * x2)
        a1, a2 = (a2, (a1 - c * a2) % p)
    return a1


def elliptic_add(P, Q):
    if P == ():
        return Q
    elif Q == ():
        return P
    elif P[0] == Q[0]:
        if P[1] == -Q[1] % p:
            return ()
        else:
            g = (P[0] * P[0] * 3 % p) * inv(P[1] * 2) % p
    else:
        g = (Q[1] - P[1]) * inv(Q[0] - P[0]) % p
    x = (g * g - P[0] - Q[0]) % p
    y = ((P[0] - x) * g - P[1]) % p
    return x, y


def elliptic_scale(P, n):
    if n == 0:
        return ()
    elif n == 1:
        return P
    else:
        Q = elliptic_scale(P, n >> 1)
        Q = elliptic_add(Q, Q)
        if n % 2 == 1:
            Q = elliptic_add(Q, P)
        return Q


# Point on bitcoin sep256k1 curve
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
xG = int('0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16)
yG = int('0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16)
nG = int('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)
omega = pow(-7, (p-1)//3, p)  # cube root of 3
print('omega =', hex(omega))  # check if -7 is a cube
print('omega3 =', omega * omega * omega % p)
assert ((xG * xG % p) * xG + 7) % p == yG * yG % p
print('p =', hex(p))
print('n =', hex(nG))
print('is p prime:', is_prime(p))
print('is n prime:', is_prime(nG))
print('G = (' + hex(xG) + ', ' + hex(yG) + ')')
P = elliptic_scale((xG, yG), nG)
print('n.G =', P)

# try random point
while True:
    xG = randrange(p)
    z = ((xG * xG % p) * xG + 7) % p
    yG = pow(z, (p+1)//4, p)
    if yG * yG % p == z:
        break

print('G = (' + hex(xG) + ', ' + hex(yG) + ')')
P = elliptic_scale((xG, yG), nG)
print('n.G =', P)
