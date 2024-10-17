import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import linalg


def calc_p1(p0, rates):
    M = np.diag(rates * -2) + np.diag(rates[1:], 1) + np.diag(rates[:-1], -1)
    return np.matmul(linalg.expm(M), p0)


p0 = np.array([1.0, 1.0])
p0 /= sum(p0)

npts = 80
rates1d = -np.log(np.linspace(1/npts, 1, npts))
#rates1d = np.linspace(0, 20.0, npts)
rates1d = np.power(rates1d, 2.5) + rates1d
res = [[None] * npts for _ in range(npts)]

fig = plt.figure()
ax = fig.add_subplot(111)

x = []
y = []
for i in range(npts):
    for j in range(npts):
        rates = np.array([rates1d[i], rates1d[j]])
        res[i][j] = calc_p1(p0, rates)
        x.append(res[i][j][0])
        y.append(res[i][j][1])

lw = 0.2
col = 'blue'
for i in range(npts):
    ax.plot([res[i][j][0] for j in range(npts)], [res[i][j][1] for j in range(npts)], color=col, lw=lw, zorder=1)
for j in range(npts):
    ax.plot([res[i][j][0] for i in range(npts)], [res[i][j][1] for i in range(npts)], color=col, lw=lw, zorder=1)

#plt.scatter(x, y, color='blue', s=0.6, zorder=2)

ax.set_xlim(0)
ax.set_ylim(0)
plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.99, hspace=0, wspace=0)

plt.show()