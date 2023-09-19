"""
accuracy of discrete approximation to continuous barrier
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


r7 = math.sqrt(7)
r5 = math.sqrt(5)
r6 = math.sqrt(6)
r3 = math.sqrt(3)
r2 = math.sqrt(2)

# plot results
plt.rcParams.update({"text.usetex": True})
fig = plt.figure()
ax = fig.add_subplot(111)
col1 = "blue"

marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1)

concentration = False

ax.plot([], [], linewidth=2, color=col1, label='optimal bound')

if concentration:
    xmax = 1.2
    ax.plot([0], [1], linewidth=2, color=col1, **marker2, clip_on=False, zorder=3)
    ax.plot([0, 1 / r7], [1 / 2, 1 / 2], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([1 / r7], [1/2], linewidth=2, color=col1, **marker2, zorder=3)
    ax.plot([1 / r7, 1 / r5], [29 / 64, 29 / 64], linewidth=2, color=col1, **marker1)
    ax.plot([1 / r5], [29/64], linewidth=2, color=col1, **marker2)
    ax.plot([1 / r5, 1 / r3], [3 / 8, 3 / 8], linewidth=2, color=col1, **marker1)
    ax.plot([1 / r3], [3/8], linewidth=2, color=col1, **marker2)
    ax.plot([1 / r3, 2 / r6], [1 / 4, 1 / 4], linewidth=2, color=col1, **marker1)
    ax.plot([2 / r6], [1 / 4], linewidth=2, color=col1, **marker2)
    ax.plot([2/r6, 1], [7/32, 7/32], linewidth=2, color=col1, **marker1)
    ax.plot([1], [7/32], linewidth=2, color=col1, **marker2)
    ax.plot([1, xmax], [0, 0], linewidth=2, color=col1, clip_on=False, zorder=3)
    ax.plot([1], [0], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)

    xvals = np.linspace(0, xmax, 200)
    yvals = [stats.norm.cdf(-x) * 2 for x in xvals]
    xvals2 = np.linspace(0, 1, 200)
    yvals2 = [(1-x*x)**2/3 for x in xvals2]
    ax.plot(xvals, yvals, linestyle='dashed', color='grey', label='Gaussian bound')
    ax.plot(xvals2, yvals2, linestyle='dashed', color='green', label='$(1-x^2)^2/3$')

    ax.set_xticks([0, 1/r7, 1/r5, 1/r3, 2/r6, 1], [0, '$\\frac1{\\sqrt7}$', '$\\frac1{\\sqrt5}$', '$\\frac1{\\sqrt3}$',
                                                   '$\\frac2{\\sqrt6}$', 1])
    ax.set_yticks([0, 7/32, 1/4, 3/8, 29/64, 1/2, 1], [0, '7/32', '1/4', '3/8', '29/64', '1/2', 1])
    ax.legend(loc='upper right')
else:
    xmax = 2
    ax.plot([0, 1], [1, 1], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([0], [1], linewidth=2, color=col1, **marker2, clip_on=False, zorder=3)
    ax.plot([1, r2], [1/2, 1/2], linewidth=2, color=col1, **marker1)
    ax.plot([1], [1/2], linewidth=2, color=col1, **marker2)
    ax.plot([r2, r3], [1/4, 1/4], linewidth=2, color=col1, **marker1)
    ax.plot([r2], [1/4], linewidth=2, color=col1, **marker2)
    ax.plot([r3, 2], [1/8, 1/8], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([r3], [1/8], linewidth=2, color=col1, **marker2, zorder=3)
    ax.plot([2], [9/128], linewidth=2, color=col1, **marker2, clip_on=False, zorder=3)

    xvals = np.linspace(0, xmax, 200)
    yvals = [stats.norm.cdf(-x) * 2 for x in xvals]
    xvals2 = np.linspace(1, xmax, 100)
    yvals2 = [1/(x*x) for x in xvals2]
    ax.plot(xvals, yvals, linestyle='dashed', color='grey', label='Gaussian bound')
    ax.plot(xvals2, yvals2, linestyle='dashed', color='green', label='$x^{-2}$')

    ax.set_xticks([0, 1, r2, r3, 2], [0, 1, '$\\sqrt2$', '$\\sqrt3$', 2])
    ax.set_yticks([9/128, 1/8, 1/4, 1/2, 1], ['9/128', '1/8', '1/4', '1/2', 1])
    ax.legend(loc='upper right')
    plt.subplots_adjust(left=0.08, right=0.99, bottom=0.05, top=0.98, hspace=0, wspace=0)


ax.set_xlim(0, xmax)
ax.set_ylim(0, 1)
#ax.set_yticks([])
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()