"""
reflected Rademacher sum
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import scipy.stats as stats

plt.rcParams.update({"text.usetex": True, "font.size": 14})
fig = plt.figure()
ax = fig.add_subplot(111)

col1 = 'blue'
marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1)
marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor='green')
marker4 = dict(marker='o', markerfacecolor='green', markeredgecolor='green')


xmax = 1.5
xvals = np.linspace(0, xmax, 100)
yvals = 1 - xvals * xvals

x = 0.21
x2 = 1.15
y2 = x2 * x2 - 1
n = math.floor(1/x)

ax.plot(xvals, yvals, linewidth=1.5, color='black')
ax.plot([0, xmax], [0, 0], linewidth=1, color='grey')

for i in range(n+1):
    y = 1 - i*i*x*x
    ax.plot([i*x, (i+1)*x], [y, y], linewidth=1.5, color='blue', **marker1, clip_on=False, zorder=3)
    ax.plot([i*x], [y], linewidth=1.5, color='blue', **marker2, clip_on=False, zorder=3)
    ax.plot([(i+1)*x, (i+1)*x], [y, 0], linewidth=1, color='grey', linestyle='dashed', clip_on=False, zorder=1)
    str = '$x$' if i == 0 else '${}x$'.format(i+1)
    ax.text((i+1)*x, -0.02, str, ha='center', va='top')

ax.plot([(n+1) * x, x2], [0, 0], linewidth=1.5, color='blue', **marker1, clip_on=False, zorder=2)
ax.plot([(n+1) * x], [0], linewidth=1.5, color='blue', **marker2, clip_on=False, zorder=3)

ax.text(x2, 0.04, '$y$', ha='center', va='bottom')
ax.plot([x2, xmax], [-y2, -y2], linewidth=1.5, color='blue', clip_on=False, zorder=2)
ax.plot([x2, x2], [-y2, 0], linewidth=1, color='grey', linestyle='dashed', clip_on=False, zorder=1)
ax.plot([x2], [-y2], linewidth=1.5, color='blue', **marker2, clip_on=False, zorder=3)
ax.text(x2, 1 - x2*x2-0.2, '$1-Y^2$', ha='center', va='top')

ax.set_xticks([])
ax.set_yticks([])

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)

#ax.legend(loc='upper right')
ax.set_xlim(0, xmax)
ax.set_ylim(yvals[-1], yvals[0] + 0.05)
plt.show()
