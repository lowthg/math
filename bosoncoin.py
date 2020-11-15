import random
import numpy as np
import matplotlib.pyplot as plt
import math


def binomialprobs(n):
    yvals = np.zeros(n + 1)
    prob = pow(0.5, n)
    for m in range(n+1):
        yvals[m] = prob
        prob *= (n-m) / (m+1)
    return yvals



fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot([0, 1], [1, 1], label='Uniform', linewidth=1)

maxval = 1.0
for n in [2, 10, 100, 500]:
    nvals = np.linspace(0.0, 1.0, n+1)
    yvals = binomialprobs(n) * (n+1)
    ax.plot(nvals, yvals, label='N = {}'.format(n), linewidth=1)
    maxval = max(maxval, yvals.max())

ax.set_xlim(0, 1)
ax.set_ylim(0, maxval * 1.05)
ax.set_yticks([])
ax.set_xticks([0, 0.5, 1])
ax.legend(loc='best')
plt.show()
