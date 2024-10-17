import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import linalg


def calc_p1(p0, rates):
    M = np.diag(rates * -2) + np.diag(rates[1:], 1) + np.diag(rates[:-1], -1)
    print(M[0,0])
    print(rates[0])
    return np.matmul(linalg.expm(M), p0)


p0 = np.array([0.0, 1.0, 0.0])
p0 /= sum(p0)
rates = np.array([1.0, 1.0, 0.4])
n = len(p0)
i0 = 1

npts = 100
#a_vec = -np.log(np.linspace(1/npts, 1, npts))
a_vec = np.linspace(0, 4, npts)
print(a_vec)
amax = max(a_vec)

pout = [np.zeros(npts) for _ in range(n)]

for i in range(npts):
    rates[i0] = a_vec[i]
    p1 = calc_p1(p0, rates)
    for j in range(n):
        pout[j][i] = p1[j]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, amax)
ax.set_ylim(0, 1)
for i in range(n):
    color = 'red' if i == i0 else 'blue'
    ax.plot(a_vec, pout[i], color=color, lw=1, zorder=2)
    ax.plot([0, a_vec[-1]], [pout[i][-1], pout[i][-1]], color=color, ls='dashed', alpha=0.5)
    print(pout[i])
plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.99, hspace=0, wspace=0)

plt.show()
