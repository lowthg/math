"""
show probability density of overshoot R
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.special as special
import random

pdf = stats.norm.pdf
cdf = stats.norm.cdf


def conditional_dist(n_sim, xvals):
    X = np.zeros(n_sim)
    M = 0
    m = len(xvals)
    for i in range(1, n_sim):
        X[i] = X[i-1] + random.gauss(0,1)
        M = max(X[i], M)

    pvals = np.ones(m)
    X -= M

    for i in range(1, n_sim):
        pvals *= 1 - np.exp(-(xvals - X[i]) * (xvals - X[i-1]) * 2)

    pvals[-1] = 1

    return (pvals[1:] - pvals[:-1]) / (xvals[1:] - xvals[:-1])


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
beta = -special.zeta(0.5)/math.sqrt(2*math.pi)
print(beta)
M, N = transition(m, n, h1, h2)


v = np.zeros(m)
v[m-1] = 1
M2 = np.matrix(np.zeros(shape=[10,10]))
print('solving...')
p = N * np.matrix(np.linalg.solve(np.identity(m) - M, v)).transpose()
parr = [p[i, 0]/h2 for i in range(n)]
xplot = np.linspace(h2/2, nwidth-h2/2, n)
print(sum([a*b*h2 for a,b in zip(xplot, parr)]))

xplot2 = [0] + list(xplot)
parr2 = [1.5*parr[0]-0.5*parr[1]] +list(parr)
ymax = max(parr)
xmax=2

plt.rcParams.update({"text.usetex": True, "font.size": 14})
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(xplot2, parr2, linewidth=2, color='blue', label='overshoot')
ax.fill_between(xplot2, parr2, facecolor='blue', alpha=0.08)

if True:
    xvals = np.linspace(0, 3.5, 400)
    random.seed(3)

    xplot = (xvals[1:] + xvals[:-1]) / 2
    xplot2 = [0] + list(xplot)

    n_sim = 1000
    n_sim2 = 1000
    print('simulating...')
    for i in range(1):
        pvals = np.zeros(len(xvals) - 1)
        for _ in range(n_sim2):
            pvals += conditional_dist(n_sim, xvals)
        pvals /= n_sim2
        print(sum(xplot * pvals * xvals[1]))
        pvals2 = [1.5 * pvals[0] - 0.5 * pvals[1]] + list(pvals)
        ymax = max(max(pvals), ymax)

    ax.plot(xplot2, pvals2, linewidth=2, color='green', label='excess max')
    ax.fill_between(xplot2, pvals2, facecolor='green', alpha=0.08)

ax.legend(loc='upper right')
ax.text(beta, -0.02, '$\\beta$'.format(i), va='top', ha='center')
plt.subplots_adjust(left=0.06, right=0.98, bottom=0.05, top=0.99, hspace=0, wspace=0)

ymax *= 1.05
ax.plot([beta, beta], [0, ymax], linewidth=0.5, color='black', linestyle='dashed')

ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
ax.set_xticks([0, 0.5, 1, 1.5, 2])
plt.show()
