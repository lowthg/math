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


print(cpath(3))
print(cpath(7))

npaths = 5
random.seed(1)

fig = plt.figure()
ax = fig.add_subplot(111)
xmax = 0
ymax = 0
ymin = 0

for i in range(npaths):
    n = random.randint(1, int(1e15))
    path = cpath(n)
    log0 = math.log(n)
    yvals = [math.log(x) - log0 for x in path]
    xvals = [x for x in range(len(yvals))]
    ax.plot(xvals, yvals, color='tab:blue')
    xmax = max(xmax, len(xvals) - 1)
    ymax = max(ymax, max(yvals))
    ymin = min(ymin, min(yvals))

ax.set_xlim(0, xmax)
ax.set_ylim(ymin, ymax)
plt.subplots_adjust(left=0.08, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)

plt.show()
