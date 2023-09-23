"""
accuracy of discrete approximation to continuous barrier
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
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

concentration = 'ac'

ax.plot([], [], linewidth=2, color=col1, label='optimal bound')

if concentration == 'a':
    xmax = 1.2
    xmin = 0
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
elif concentration == 'c':
    xmin = 0
    xmax = 3/r2
    ax.plot([0, 1], [1, 1], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([0], [1], linewidth=2, color=col1, **marker2, clip_on=False, zorder=3)
    ax.plot([1, r2], [1/2, 1/2], linewidth=2, color=col1, **marker1)
    ax.plot([1], [1/2], linewidth=2, color=col1, **marker2)
    ax.plot([r2, r3], [1/4, 1/4], linewidth=2, color=col1, **marker1)
    ax.plot([r2], [1/4], linewidth=2, color=col1, **marker2)
    ax.plot([r3, 2], [1/8, 1/8], linewidth=2, color=col1, **marker1)
    ax.plot([r3], [1/8], linewidth=2, color=col1, **marker2)
    ax.plot([2, 3/r2], [9/128, 9/128], linewidth=2, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([2], [9/128], linewidth=2, color=col1, **marker2, clip_on=False, zorder=3)

    xvals = np.linspace(0, xmax, 200)
    yvals = [stats.norm.cdf(-x) * 2 for x in xvals]
    xvals2 = np.linspace(1, xmax, 100)
    yvals2 = [1/(x*x) for x in xvals2]
    ax.plot(xvals, yvals, linestyle='dashed', color='grey', label='Gaussian bound')
    ax.plot(xvals2, yvals2, linestyle='dashed', color='green', label='$x^{-2}$')

    ax.set_xticks([0, 1, r2, r3, 2], [0, 1, '$\\sqrt2$', '$\\sqrt3$', 2])
    ax.set_yticks([9/128, 1/8, 1/4, 1/2, 1], ['9/128', '1/8', '1/4', '1/2', 1])
    plt.subplots_adjust(left=0.08, right=0.99, bottom=0.05, top=0.98, hspace=0, wspace=0)
elif concentration == 'ac':
    xmin = -3/r2
    xmax = 1.2
    lw = 1.5
    marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1, markersize=5)
    marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1, markersize=5)
    ax.plot([1, xmax], [0, 0], linewidth=lw, color=col1, clip_on=False, zorder=3)
    ax.plot([1], [0], linewidth=lw, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([2/r6, 1], [7/64, 7/64], linewidth=lw, color=col1, **marker1)
    ax.plot([1], [7/64], linewidth=lw, color=col1, **marker2)
    ax.plot([1/r3, 2/r6], [1/8, 1/8], linewidth=lw, color=col1, **marker1)
    ax.plot([2/r6], [1/8], linewidth=lw, color=col1, **marker2)
    ax.plot([1/r5, 1/r3], [3/16, 3/16], linewidth=lw, color=col1, **marker1)
    ax.plot([1/r3], [3/16], linewidth=lw, color=col1, **marker2)
    ax.plot([1/r7, 1/r5], [29/128, 29/128], linewidth=lw, color=col1, **marker1)
    ax.plot([1/r5], [29/128], linewidth=lw, color=col1, **marker2)
    ax.plot([0, 1/r7], [1/4, 1/4], linewidth=lw, color=col1, **marker1, zorder=3)
    ax.plot([1/r7], [1/4], linewidth=lw, color=col1, **marker2, zorder=3)
    ax.plot([-1, 0], [1/2, 1/2], linewidth=lw, color=col1, **marker1)
    ax.plot([0], [1/2], linewidth=lw, color=col1, **marker2, zorder=3)
    ax.plot([-r2, -1], [3/4, 3/4], linewidth=lw, color=col1, **marker1, zorder=3)
    ax.plot([-1], [3/4], linewidth=lw, color=col1, **marker2, zorder=3)
    ax.plot([-r3, -r2], [7/8, 7/8], linewidth=lw, color=col1, **marker1)
    ax.plot([-r2], [7/8], linewidth=lw, color=col1, **marker2, zorder=3)
    ax.plot([-2, -r3], [15/16, 15/16], linewidth=lw, color=col1, **marker1, zorder=3)
    ax.plot([-r3], [15/16], linewidth=lw, color=col1, **marker2)
    ax.plot([-3/r2, -2], [247/256, 247/256], linewidth=lw, color=col1, **marker1, clip_on=False, zorder=3)
    ax.plot([-2], [247/256], linewidth=lw, color=col1, **marker2, zorder=3)
    ax.plot([0, 0], [0, 1], linewidth=0.5, color='grey', linestyle='dashed')
    ax.set_xticks([-3/r2, -2, -r3, -r2, -1, 0, 1/r7, 1/r5, 1/r3, 2/r6, 1],
                  ['$\\frac{-3}{\\sqrt2}$', -2, '$-\\sqrt3$', '$-\\sqrt2$', -1, 0, '$\\frac1{\\sqrt7}$',
                   '$\\frac1{\\sqrt5}$', '$\\frac1{\\sqrt3}$', '$\\frac2{\\sqrt6}$', 1], fontsize=8)
    ax.set_yticks([0, 7/64, 1/8, 3/16, 29/128, 1/4, 1/2, 3/4, 7/8, 15/16, 247/256],
                  [0, '7/64', '1/8', '3/16', '29/128', '1/4', '1/2', '3/4', '7/8', '15/16', '247/256'], fontsize=7)
    xvals = np.linspace(-3/r2, xmax, 200)
    yvals = [stats.norm.cdf(-x) for x in xvals]
    xvals2 = np.linspace(0, 1, 200)
    yvals2 = [(1-x*x)**2/6 for x in xvals2]
    xvals3 = np.linspace(-3/r2, -1, 200)
    yvals3 = [1 - 1/(2*x*x) for x in xvals3]
    ax.plot(xvals, yvals, linestyle='dashed', color='grey', label='Gaussian bound')
    ax.plot(xvals2, yvals2, linestyle='dashed', color='green', label='$(1-x^2)^2/6$')
    ax.plot(xvals3, yvals3, linestyle='dashed', color='purple', label='$1-x^{-2}/2$')

    plt.subplots_adjust(left=0.074, right=0.99, bottom=0.055, top=0.99, hspace=0, wspace=0)

ax.legend(loc='upper right')
ax.set_xlim(xmin, xmax)
ax.set_ylim(0, 1)
#ax.set_yticks([])
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()