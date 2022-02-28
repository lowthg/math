import random
import numpy as np
import matplotlib.pyplot as plt
import math


def cpath(n, maxiter=10000):
    result = [n]
    for i in range(maxiter):
        if n % 2:
            n = (3 * n + 1) >> 1
        else:
            n = n >> 1
        result.append(n)
        if n == 1:
            return result
    raise Exception("max iterations exceeded")


def bmpath(n, mu, sigma, ymin):
    y = 0.0
    result = [y]
    for i in range(1, n):
        y += random.gauss(mu, sigma)
        result.append(y)
        if y < ymin:
            return result
    return result


print(cpath(3))
print(cpath(7))

npaths = 6
#random.seed(1)
random.seed(4)

fig = plt.figure()
ax = fig.add_subplot(111)
xmax = 0
ymax = 0
ymin = 0
nmax = int(1e15)
print(math.log2(nmax))

for i in range(npaths):
    n = random.randint(1, nmax)
    path = cpath(n)
    log0 = math.log2(n)
    yvals = [math.log2(x) - log0 for x in path]
    xvals = [x for x in range(len(yvals))]
    ax.plot(xvals, yvals, color='blue', zorder=1)
    xmax = max(xmax, len(xvals) - 1)
    ymax = max(ymax, max(yvals))
    ymin = min(ymin, min(yvals))

a = math.log2(3/2)
b = math.log2(1/2)
mu = (a + b) / 2
sigma = (a - b) / 2

for i in range(npaths):
    yvals = bmpath(xmax + 1, mu, sigma, ymin)
    xvals = [x for x in range(len(yvals))]
    ax.plot(xvals, yvals, color='tab:red', alpha=0.7, zorder=0)

xvals = [x for x in range(xmax + 1)]
yvals = [mu * x for x in xvals]
ax.plot(xvals, yvals, color='black', alpha=0.7, zorder=2, linewidth=2)

ax.set_xlim(0, xmax)
ax.set_ylim(ymin - (ymax - ymin) * 0.02, ymax + (ymax - ymin) * 0.02)
plt.subplots_adjust(left=0.08, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)

plt.show()
