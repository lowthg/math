import numpy as np
import matplotlib.pyplot as plt


def bosonprobs(n, p):
    yvals = np.zeros(n + 1)
    C = 0.0
    prob = pow(1.0 - p, n)
    a = p / (1.0 - p)
    for m in range(n+1):
        yvals[m] = prob
        C += prob
        prob *= a
    yvals /= C
    return yvals

fig = plt.figure()
ax = fig.add_subplot(111)

maxval = 1.0
p = 0.49
for n in [2, 50, 100, 200]:
    nvals = np.linspace(0.0, 1.0, n+1)
    yvals = bosonprobs(n, p) * (n+1)
    ax.plot(nvals, yvals, label='N = {}'.format(n), linewidth=1)
    maxval = max(maxval, yvals.max())

ax.set_xlim(0, 1)
ax.set_ylim(0, maxval * 1.05)
ax.set_yticks([])
ax.set_xticks([0, 0.5, 1])
ax.legend(loc='best')
plt.show()
