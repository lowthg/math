"""
Rademacher sum near critical point
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import scipy.stats as stats


# plot results
# plt.rcParams.update({"text.usetex": True})

col1 = "grey"
col2 = "blue"
lw1 = 1.5
lw2 = 2



level = 1

lw = 1.5
ypath = 0

marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1, markersize=3)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1, markersize=3)
marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor=col2, markersize=3)
marker4 = dict(marker='o', markerfacecolor=col2, markeredgecolor=col2, markersize=3)

paths = {
    (1,1,1,-1),
    (1,1,-1,1),
    (1,-1,1,1),
    (-1,1,1,1)
}
allpaths = set()
for path in paths:
    for i in range(len(paths)):
        allpaths.add(path[0:i+1])

print(allpaths)


def plot_paths(a, ax, txt=True, adj=True):
    sigma = math.sqrt(np.inner(a, a))
    if adj or sigma > 1:
        a /= sigma
    yvals = [(0, ())]
    x = 0
    i = 1
    for ai in a:
        xnew = x + 1
        yvalsnew = []
        for y, path in yvals:
            for s in [-1, 1]:
                ynew = y + s * ai
                pathnew = path + (s,)
                if pathnew in allpaths:
                    ax.plot([x, xnew], [y, ynew], linewidth=lw1, color=col2, **marker3, clip_on=False, zorder=3)
                else:
                    ax.plot([x, xnew], [y, ynew], linewidth=lw1, color=col1, **marker1, clip_on=False)
                yvalsnew.append((ynew, pathnew))
#        ax.text((x+xnew)/2-0.06, (y+ynew)/2 + 0.04, '$a_{}$'.format(i))
        yvals = yvalsnew
        x = xnew
        i += 1


    ymax = 2.05
    ymin = -ymax

    for y in yvals:
        if y[1] in allpaths:
            ax.plot([x], [y[0]], linewidth=lw2, color=col2, **marker4, clip_on=False, zorder=3)
        else:
            ax.plot([x], [y[0]], linewidth=lw2, color=col1, **marker2, clip_on=False)

    if txt:
        ax.text(x+0.05, -a[0]+a[1]+a[2]+a[3], '$1$', ha='left', va='center')
        ax.text(x+0.05, a[0]-a[1]+a[2]+a[3], '$2$', ha='left', va='center')
        ax.text(x+0.05, a[0]+a[1]-a[2]+a[3], '$3$', ha='left', va='center')
        ax.text(x+0.05, a[0]+a[1]+a[2]-a[3], '$4$', ha='left', va='center')
    ax.text(0.5, 1.05, '$1$', ha='center', va='bottom')

    xmax = x + 0.1
    xmin = -0.05
    h = level * math.sqrt(sum([ai*ai for ai in a]))
    ax.plot([xmin, xmax], [1, 1], linewidth=lw1, linestyle='dashed', color='black')

    ax.set_xticks([])
    ax.set_yticks([])

#    ax.axis('off')
#    ax.set_frame_on(True)
#    ax.spines['top'].set_visible(False)
#    ax.spines['right'].set_visible(False)
#    ax.spines['left'].set_visible(False)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

fig = plt.figure()

ax = fig.add_subplot(221)
a0 = np.ones(4)/2
plot_paths(a0, ax, False)

ax = fig.add_subplot(222)
eps = np.array([0.09, 0.05, 0.0, -0.2]) - 0.0 # 1 up 3 dn
eps = np.array([0.0, -0.03, -0.07, -0.2]) - 0.0 # 1 up 3 dn
plot_paths(a0+eps, ax, False, adj=False)
print(1 - np.inner(a0+eps, a0+eps))

ax = fig.add_subplot(223)
eps = np.array([0.1, 0.04, -0.05, -0.13]) * 1  # 2 up 2 dn
plot_paths(a0+eps, ax, False)

ax = fig.add_subplot(224)
eps = np.array([0.15, -0.07, -0.11, -0.15]) * 1 # 3 up 1 dn
#eps = np.array([0.1, -0.0, -0.0, -0.0]) * 1 # 3 up 1 dn
plot_paths(a0+eps, ax, False)





plt.subplots_adjust(left=0.00, right=1, bottom=0.01, top=1, hspace=0, wspace=0)

#ax.legend(loc='upper right')
plt.show()