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

a = [0.8, 0.5]
h = 0.2
level = 1

b = [u-h for u in a]


x = 0
lw = 1.5
ypath = 0


marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor=col2, markersize=5)
marker4 = dict(marker='o', markerfacecolor=col2, markeredgecolor=col2, markersize=5)


def plot_paths(a0, a, x, labels=[], col='blue'):
    marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col, markersize=5)
    marker2 = dict(marker='o', markerfacecolor=col, markeredgecolor=col, markersize=5)
    yvals = [a0]
    i = 0
    for ai in a:
        xnew = x + 1
        yvalsnew = []
        for y in yvals:
            for ynew in [y - ai, y + ai]:
                ax.plot([x, xnew], [y, ynew], linewidth=lw1, color=col, **marker1, clip_on=False)
                yvalsnew.append(ynew)
        if i < len(labels):
            ax.text((x+xnew)/2-0.06, (y+ynew)/2, labels[i], ha='right', va='bottom')
        yvals = yvalsnew
        x = xnew
        i += 1
    for y in yvals:
        ax.plot([x], [y], linewidth=lw2, color=col, **marker2, zorder=3)


plot_paths(0, a, 0, ['$a_1$', '$a_2$'], col='blue')
plot_paths(h, b, 5, ['$b_1$'], col='black')
ax.text(6.5, 0.65, '$b_2$', ha='left', va='bottom')

z1 = a[0] + a[1]
z2 = a[0] - a[1]
z3 = -a[0] + a[1]
z4 = -a[0] - a[1]

y1 = h + b[0] + b[1]
y2 = h + b[0] - b[1]
y3 = h - b[0] + b[1]
y4 = h - b[0] - b[1]

ax.plot([2, 7], [z1, z1], linewidth=0.5, linestyle='dashed', color=col1)

path1 = [
    np.array([0, 1, 2, 3, 4, 5]),
    np.array([0, -2, -0.2, -2, -0.2, 1]) * h
]

path2 = [
    np.array([0, 1, 2, 3, 4]),
    np.array([0, 0.8, 0.1, -0.5, -0.2]) * h
]

for z, r in [(z1, -1), (z2, 1), (z3, 1), (z4, 1)]:
    ax.plot(path1[0] + 2, path1[1]*r + z, linewidth=lw1, color='blue', alpha=0.5)

ax.text(2.1, z1, '$z_1$', ha='left', va='top')
ax.text(2.1, z2, '$z_2$', ha='left', va='center')
ax.text(2.1, z3, '$z_3$', ha='left', va='center')
ax.text(2.1, z4, '$z_4$', ha='left', va='center')

for y, r in [(y1, -1), (y2, 1), (y3, 1), (y4, 1)]:
    ax.plot(path2[0] + 7, path2[1]*r + y, linewidth=lw1, color='blue', alpha=1)
    ax.plot([7], [y], marker='o', markerfacecolor='blue', markeredgecolor='blue', zorder=3, markersize=5)

ax.text(7.1, y1+0.02, '$z\'_1$', ha='left', va='center')
ax.text(7.1, y2, '$z\'_2$', ha='left', va='top')
ax.text(7.1, y3, '$z\'_3$', ha='left', va='top')
ax.text(7.1, y4, '$z\'_4$', ha='left', va='top')
ax.text(0.5, 1, '$1$', ha='center', va='bottom')

ax.text(3.4, z1+0.16, '$Z_1$', ha='center', va='center')
ax.text(3.4, z2-0.15, '$Z_2$', ha='center', va='center')
ax.text(3.4, z3-0.15, '$Z_3$', ha='center', va='center')
ax.text(3.4, z4-0.15, '$Z_4$', ha='center', va='center')
ax.text(9, y1+0.06, '$Z\'_1$', ha='center', va='center')
ax.text(9, y2+0.09, '$Z\'_2$', ha='center', va='center')
ax.text(9, y3-0.07, '$Z\'_3$', ha='center', va='center')
ax.text(9, y4+0.09, '$Z\'_4$', ha='center', va='center')


ax.plot([7, 7], [z4+h, z1], linewidth=0.5, linestyle='dashed', color='grey')
ax.text(7, 0, '$N$', ha='center', va='bottom')

plt.annotate(xy=(7, z1), xytext=(7, y1), text='', arrowprops=dict(arrowstyle='<->'))
ax.text(6.9, z1-0.04, '$h$', ha='right', va='top')

ax.plot(path2[0] + 7, path2[1]*r + z4+h, linewidth=lw1, color='blue', alpha=0.5, linestyle='dashed')

ax.plot([7], [z4+path1[1][-1]], marker='o', markerfacecolor='white', markeredgecolor='blue', zorder=3, markersize=5)

#ymin = min(yvals)
#ymax = max(yvals)


ax.plot([0, 11], [1, 1], linewidth=lw1, linestyle='dashed', color='black')
ax.plot([0, 11], [0, 0], linewidth=lw1, linestyle='dashed', color='grey', zorder=0)

ax.set_xticks([])
ax.set_yticks([])


ax.axis('off')
ax.set_frame_on(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.subplots_adjust(left=0.0, right=1, bottom=0, top=1, hspace=0, wspace=0)

ymax = z1 + max(-path1[1]) + 0.02
ax.set_xlim(-0.05, 11)
ax.set_ylim(-ymax, ymax)
plt.show()