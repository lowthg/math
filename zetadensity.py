"""
Shows probability densities related to Riemann zeta
"""
from math import pi, exp
import numpy as np
import matplotlib.pyplot as plt


def psi(x, eps=0.001, maxn=10):
    if x < 1e-6:
        return 0
    if x < 1:
        return psi(1.0/x, eps, maxn) / (x * x * x)
    n = 1
    y = x * x
    p = 0.0
    while True:
        m = n * n
        e = exp(- pi * m * y)
        p += m * (pi * 2 * m * y - 3) * e
        if n > maxn and e < eps:
            break
        n += 1
    return pi * 4 * x * p


def phi2(x, eps=0.001, maxn=10):
    n = 1
    y = x * x
    p = 0.0
    while True:
        m = (n - 0.5)*(n - 0.5)
        e = exp(-m * y * pi)
        p += (pi * 2 * m * y - 1) * e
        if n > maxn and e < eps:
            break
        n += 1
    return y * 2 * p


def phi(x, eps=0.001, maxn=10):
    if x < 1e-6:
        return 0
    if x < 1:
        return phi2(1.0/x, eps, maxn)
    n = 1
    y = x * x
    p = 0.0
    sgn = 1
    while True:
        m = n * n
        e = exp(-m * y * pi)
        p += sgn * m * e
        if n > maxn and e < eps:
            break
        n += 1
        sgn = -sgn
    return pi * 4 * x * p

npts = 1000
maxx = 2.0

xvals = np.linspace(0, maxx, npts)
psivals = [psi(x) for x in xvals]
phivals = [phi(x) for x in xvals]

#plt.rcParams.update({"text.usetex": True})
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(xvals, phivals, linewidth=1, color='green', label='$\\Phi$')
ax.plot(xvals, psivals, linewidth=1, color='blue', label='$\\Psi$')
ax.fill_between(xvals, phivals, facecolor='green', alpha=0.08)
ax.fill_between(xvals, psivals, facecolor='blue', alpha=0.08)
plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.legend(loc='upper right')
ax.set_xlim(0, maxx)
ax.set_ylim(0, 2.2)
ax.set_yticks([0, 1, 2])
ax.set_xticks([0, 0.5, 1, 1.5, 2])
plt.show()
