"""
reflected Rademacher sum
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import scipy.stats as stats
import random


a = [1.1, 1, 0.9, 0.9, 0.9, 0.9, 0.83, 0.7, 0.7, 0.7] + [0.7] * 4 + [0.7] * 2
random.seed(7)
signs = [random.choice([-1, 1]) for _ in a]
signs = [-1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1]

xvals = [0]
yvals = [0]
for i in range(len(a)):
    xvals.append(i + 1)
    yvals.append(yvals[i] + signs[i]*a[i])

if yvals[-1] < 0:
    yvals = [-y for y in yvals]

#plt.rcParams.update({"text.usetex": True, "font.size": 14})
fig = plt.figure()
ax = fig.add_subplot(111)
xmin = 0
xmax = xvals[-1]
col1 = 'blue'
marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1)
marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor='green')
marker4 = dict(marker='o', markerfacecolor='green', markeredgecolor='green')

ax.plot(xvals, yvals, linewidth=1.5, color=col1, **marker1, clip_on=False, zorder=3)
ax.plot(xvals[-1], yvals[-1], linewidth=1.5, color=col1, **marker2, clip_on=False, zorder=3)

ax.plot([xmin, xmax], [0, 0], linewidth=1, linestyle='solid', color='grey')

x = a[0] * 2
u = yvals[-1] * 0.89723
v = u + x
x = v - u
k = u/2

xvals2 = []
yvals2 = []
hit = False
for i in range(len(yvals)):
    if not hit and yvals[i] > k:
        hit = True
        y2 = yvals[i]
    if hit:
        xvals2.append(xvals[i])
        yvals2.append(2 * y2 - yvals[i])

ax.plot(xvals2, yvals2, linewidth=1.5, color='green', **marker3, clip_on=False, zorder=2)
ax.plot(xvals2[-1], yvals2[-1], linewidth=1.5, color='green', **marker4, clip_on=False, zorder=3)

ax.plot([xmin, xmax], [u, u], linewidth=1.5, linestyle='dashed', color='black')
ax.plot([xmin, xmax], [v, v], linewidth=1.5, linestyle='dashed', color='black')
ax.fill_between([xmin, xmax], u, v, color='grey', alpha=0.3)
ax.plot([xmin, xmax], [x, x], linewidth=1.5, linestyle='dashed', color='black', zorder=1)
ax.plot([xmin, xmax], [-x, -x], linewidth=1.5, linestyle='dashed', color='black')
ax.fill_between([xmin, xmax], [-x, -x], [x, x], color='grey', alpha=0.3)
ax.plot([xmin, xmax], [k, k], linewidth=1, linestyle='dashed', color='grey')

ax.plot([xvals2[0], xvals2[0]], [0, yvals2[0]], linewidth = 0.5, color='grey')
ax.text(xmax * 0.2, -x, '$-x$', va='bottom', ha='center')
ax.text(xmax * 0.2, x, '$x$', va='bottom', ha='center')
ax.text(xmax * 0.2, k, '$u/2$', va='bottom', ha='center')
ax.text(xmax * 0.2, u, '$u$', va='bottom', ha='center')
ax.text(xmax * 0.2, v, '$u+x$', va='top', ha='center')
ax.text(xvals2[0], -0.05, '$N$', va='top', ha='center')
ax.text(xmax - 0.1, yvals[-1] + 0.1, '$Y$', va='center', ha='right')
ax.text(xmax - 0.15, yvals2[-1] - 0.2, '$Y\'$', va='center', ha='right')

ax.set_xticks([])
ax.set_yticks([])

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)

#ax.legend(loc='upper right')
ax.set_xlim(xmin, xmax)
ax.set_ylim(min(min(yvals), -x) *1.08, max(max(yvals),v) * 1.05)
plt.show()

