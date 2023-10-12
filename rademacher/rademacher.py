"""
accuracy of discrete approximation to continuous barrier
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import scipy.stats as stats



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

ax.set_xticks([])
ax.set_yticks([])


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