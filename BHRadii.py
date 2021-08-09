"""
Simulate black hole as concentric spheres of varying index of refraction
continuous IOR given by n(r) = (1+1/r)^3/(1-1/r)
do not require spheres of radius r <= r0 = 2 + sqrt(3) = 3.73, as light does not escape anyway.
given ratio of IOR of succesive spheres a > 1, solves radii satisfying
n(r) = a^i, i=1,2,...
as n0 = n(r0)  = 6(2-sqrt(3))=2.78, there are no spheres for a^i > 2.78
"""

import math

a = 1.001  # minimum index of refraction ratio
p = 1.05  # minimum radius ratio

rmin = 1

r0 = 2 + math.sqrt(3)
n0 = 6 * (2 * math.sqrt(3) - 3)
x0 = 3 - math.sqrt(3)

print("r0: ", r0)
print("n0: ", n0)

rvec = []

b = a
r_prev = 1e6
n_prev = 1.0

while b < n0:
    """
    for x=1+1/r need to solve x^3/(2-x)=b.
    Cubic: x^3 + bx - 2b = 0 over 1 < x < x0
    """
    u = math.sqrt(1 + b / 27) * b
    v = math.pow(u + b, 1/3)
    x = v - b / (3 * v)
    r = 1/(x-1)
    if r > r_prev / p:
        r = r_prev / p
    if r <= r0:
        break

    n = math.pow(1 + 1 / r, 3) / (1 - 1 / r)

#    print(b, ": ", )
    rvec.append((r / r0 * rmin, n/n_prev))
    b = n * a
    n_prev = n
    r_prev = r

print("Number of spheres: ", len(rvec))
i = 1
for (r, n) in rvec:
    print(i, "    ", r, "    ", n)
    i += 1
