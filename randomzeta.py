"""
plot riemann zeta
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import random



def zetaproduct(s, coeffs):
    result = 1 + 0j
    for u, p in coeffs:
        result /= 1.0 - u * (math.cos(p*s.imag) - 1j * math.sin(p*s.imag)) * math.exp(-p*s.real)
    return result


def zetafunc(s, logn):
    result = 1 + 0j
    sgn = -1
    for n in logn:
        result += (math.cos(n*s.imag) - 1j * math.sin(n*s.imag)) * math.exp(-n*s.real) * sgn
        sgn = -sgn
    log2 = math.log(2.0)
    result /= 1.0 - (math.cos(log2*s.imag)- 1j * math.sin(log2*s.imag)) * math.exp(log2*(1-s.real))
    return result


def listprimes(maxprime):
    primes = [2, 3]
    p = primes[-1]
    while True:
        p += 2
        if p > maxprime:
            break
        isprime = True
        for p2 in primes:
            if p2 * p2 > p:
                break
            if p % p2 == 0:
                isprime = False
        if isprime:
            primes.append(p)
    return primes


xmin = 0.65
xmax = 1.1
ymin = -5
ymax = 5
nx = 101
ny = 103
userandom = True

yoffset = 232

primes = listprimes(1000)

#random.seed(4)
random.seed(1)
#random.seed(13)

logprimes = [math.log(p) for p in primes]
uvec = []
for _ in primes:
    u = math.pi * 2 * random.random()
    uvec.append(math.cos(u) + 1j * math.sin(u))

uvec1 = [1+0j for _ in primes]

coeffs = [x for x in zip(uvec, logprimes)]
logn = [math.log(n) for n in range(2, 1000)]

xvals = np.linspace(xmin, xmax, nx)
if not userandom:
    ymin += yoffset
    ymax += yoffset
yvals = np.linspace(ymin, ymax, ny)

Z3 = np.ndarray(shape=(nx, ny))
Y3, X3 = np.meshgrid(yvals, xvals)


for i in range(0, nx):
    for j in range(0, ny):
        if userandom:
            z = zetaproduct(xvals[i] + yvals[j] * 1j, coeffs)
        else:
            z = zetafunc(xvals[i] + (yvals[j] + yoffset) * 1j, logn)
        Z3[i, j] = float(z.real)

fig = plt.figure()
ax = plt.axes(projection='3d', frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5) # coolwarm, Reds, summer
#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue')
ax.set_yticks([ymin, ymax])
ax.set_xticks([xmin, xmax])
#ax.set_ylim(xmin, xmax)
ax.set_xlabel('x', labelpad=-10)
ax.set_ylabel('y', labelpad=-10)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.view_init(30, -56)
plt.show()
