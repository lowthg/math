"""
show probability density of max B - max X
"""

import math
import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.special as special

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


xvals = np.linspace(0, 3.5, 400)
#random.seed(2)


beta = -special.zeta(0.5)/math.sqrt(2*math.pi)
print(beta)
xplot = (xvals[1:] + xvals[:-1])/2
xplot2 = [0] + list(xplot)
xmax = 3
fig = plt.figure()
ax = fig.add_subplot(111)

ymax = 0

n_sim = 1000
n_sim2 = 1000
for i in range(1):
    pvals = np.zeros(len(xvals)-1)
    for _ in range(n_sim2):
        pvals += conditional_dist(n_sim, xvals)
    pvals /= n_sim2
    print(sum(xplot * pvals * xvals[1]))
    pvals2 = [1.5*pvals[0] - 0.5*pvals[1]] + list(pvals)
    ax.plot(xplot2, pvals2, linewidth=2, color='green', label='R')
    ymax = max(max(pvals), ymax)

ax.fill_between(xplot2, pvals2, facecolor='green', alpha=0.08)
ax.plot([beta, beta], [0, ymax], linewidth=0.5, color='black', linestyle='dashed')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
plt.show()

