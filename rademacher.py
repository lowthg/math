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
col1 = "grey"
col2 = "blue"
lw1 = 1.5
lw2 = 2

marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1)

ax.plot([], [], linewidth=2, color=col1, label='optimal bound')

a = [1/2, 1/3, 1/4, 1/7]
signs = [1, -1, 1, 1]
level = 1

yvals = [0]
x = 0
lw = 1.5
ypath = 0

marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1, markersize=5)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1, markersize=5)
marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor=col2, markersize=5)
marker4 = dict(marker='o', markerfacecolor=col2, markeredgecolor=col2, markersize=5)

i = 1
for sign, ai in zip(signs, a):
    xnew = x + 1
    yvalsnew = []
    for y in yvals:
        for ynew in [y - ai, y + ai]:
            ax.plot([x, xnew], [y, ynew], linewidth=lw1, color=col1, **marker1, clip_on=False)
            yvalsnew.append(ynew)
    ypathnew = ypath + ai * sign
    ax.plot([x, xnew], [ypath, ypathnew], linewidth=lw1, color=col2, **marker3, zorder=3)
    ax.text((x+xnew)/2-0.06, (y+ynew)/2 + 0.04, '$a_{}$'.format(i))
    yvals = yvalsnew
    x = xnew
    ypath = ypathnew
    i += 1

ymin = min(yvals)
ymax = max(yvals)

for y in yvals:
    ax.plot([x], [y], linewidth=lw2, color=col1, **marker2, clip_on=False)

ax.plot([x], [ypath], linewidth=lw2, color=col1, **marker4, zorder=3)

ax.text(x+0.05, ypath, '$Z$', ha='left', va='center')

h = level * math.sqrt(sum([ai*ai for ai in a]))
ax.plot([0, x], [h, h], linewidth=lw1, linestyle='dashed', color='black')
ax.plot([0, x], [-h, -h], linewidth=lw1, linestyle='dashed', color='black')

# xmin = -3/r2
# xmax = 1.2
#
# ax.plot([1, xmax], [0, 0], linewidth=lw, color=col1, clip_on=False, zorder=3)
# ax.plot([1], [0], linewidth=lw, color=col1, **marker1, clip_on=False, zorder=3)
# ax.plot([2/r6, 1], [7/64, 7/64], linewidth=lw, color=col1, **marker1)
# ax.plot([1], [7/64], linewidth=lw, color=col1, **marker2)
# ax.plot([1/r3, 2/r6], [1/8, 1/8], linewidth=lw, color=col1, **marker1)
# ax.plot([2/r6], [1/8], linewidth=lw, color=col1, **marker2)
# ax.plot([1/r5, 1/r3], [3/16, 3/16], linewidth=lw, color=col1, **marker1)
# ax.plot([1/r3], [3/16], linewidth=lw, color=col1, **marker2)
# ax.plot([1/r7, 1/r5], [29/128, 29/128], linewidth=lw, color=col1, **marker1)
# ax.plot([1/r5], [29/128], linewidth=lw, color=col1, **marker2)
# ax.plot([0, 1/r7], [1/4, 1/4], linewidth=lw, color=col1, **marker1, zorder=3)
# ax.plot([1/r7], [1/4], linewidth=lw, color=col1, **marker2, zorder=3)
# ax.plot([-1, 0], [1/2, 1/2], linewidth=lw, color=col1, **marker1)
# ax.plot([0], [1/2], linewidth=lw, color=col1, **marker2, zorder=3)
# ax.plot([-r2, -1], [3/4, 3/4], linewidth=lw, color=col1, **marker1, zorder=3)
# ax.plot([-1], [3/4], linewidth=lw, color=col1, **marker2, zorder=3)
# ax.plot([-r3, -r2], [7/8, 7/8], linewidth=lw, color=col1, **marker1)
# ax.plot([-r2], [7/8], linewidth=lw, color=col1, **marker2)
# ax.plot([-2, -r3], [15/16, 15/16], linewidth=lw, color=col1, **marker1)
# ax.plot([-r3], [15/16], linewidth=lw, color=col1, **marker2)
# ax.plot([-3/r2, -2], [247/256, 247/256], linewidth=lw, color=col1, **marker1, clip_on=False, zorder=3)
# ax.plot([-2], [247/256], linewidth=lw, color=col1, **marker2, zorder=3)
# ax.plot([0, 0], [0, 1], linewidth=0.5, color='grey', linestyle='dashed')
ax.set_xticks([])
ax.set_yticks([])

#              [0, '7/64', '1/8', '3/16', '29/128', '1/4', '1/2', '3/4', '7/8', '15/16', '247/256'], fontsize=7)
# xvals = np.linspace(-3/r2, xmax, 200)
# yvals = [stats.norm.cdf(-x) for x in xvals]
# xvals2 = np.linspace(0, 1, 200)
# yvals2 = [(1-x*x)**2/6 for x in xvals2]
# xvals3 = np.linspace(-3/r2, -1, 200)
# yvals3 = [1 - 1/(2*x*x) for x in xvals3]
# ax.plot(xvals, yvals, linestyle='dashed', color='grey', label='Gaussian bound')
# ax.plot(xvals2, yvals2, linestyle='dashed', color='green', label='$(1-x^2)^2/6$')
# ax.plot(xvals3, yvals3, linestyle='dashed', color='purple', label='$1-x^{-2}/2$')

ax.axis('off')
ax.set_frame_on(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)

#ax.legend(loc='upper right')
ax.set_xlim(0, x+0.09)
ax.set_ylim(ymin, ymax)
plt.show()