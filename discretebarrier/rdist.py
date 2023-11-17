"""
show probability density of overshoot R
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.special as special

pdf = stats.norm.pdf
cdf = stats.norm.cdf


def transition(m, n, h1, h2):
    """
    Returns M, N
    M is mxm transition matrix from X_{t-1} to X_t restricted to X_t > 0
    N is mxn transition matrix from X_{t-1} to X_t restricted to X_t < 0
    m points for X_t > 0 step h1
    n points for X_t < 0 step h2
    """
    M = np.matrix(np.zeros(shape=[m, m]))
    N = np.matrix(np.zeros(shape=[n, m]))

    p = np.zeros(2*m-1)
    for i in range(2*m-1):
        j = i - m
        p[i] = cdf(j*h1 + h1/2)-cdf(j*h1 - h1/2)

    for i in range(m):
        x = h1 * i + h1/2
        for j in range(m-1):
            M[j, i] = p[j-i+m]
        M[m-1, i] = cdf(x - h1*(m-1))

        for j in range(n-1):
            y = h2 * j
            N[j, i] = cdf(x+y+h2) - cdf(x+y)
        N[n-1, i] = cdf(-x-h2*(n-1))

    return M,N


mwidth = 6
nwidth = 3.5
m = 400
n = 100
h1 = mwidth / m
h2 = nwidth / n
M, N = transition(m, n, h1, h2)

v = np.zeros(m)
v[m-1] = 1
M2 = np.matrix(np.zeros(shape=[10,10]))
print('solving...')
p = N * np.matrix(np.linalg.solve(np.identity(m) - M, v)).transpose()
parr = [p[i, 0]/h2 for i in range(n)]
xplot = np.linspace(h2/2, nwidth-h2/2, n)
print(sum([a*b*h2 for a,b in zip(xplot, parr)]))
beta = -special.zeta(0.5/math.sqrt(2*math.pi))

xplot = [0] + list(xplot)
parr = [1.5*parr[0] - 0.5*parr[1]] + parr

ymax = max(parr)*1.1
xmax=3
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([beta, beta], [0, ymax], linewidth=0.5, color='black', linestyle='dashed')
ax.plot(xplot, parr, linewidth=2, color='blue', label='R')
ax.fill_between(xplot, parr, facecolor='blue', alpha=0.08)
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
plt.show()
