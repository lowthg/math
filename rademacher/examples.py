"""
Rademacher sum near critical point
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import scipy.stats as stats


# plot results
plt.rcParams.update({"text.usetex": True})
plt.rc('text.latex', preamble=r'\usepackage{amsmath,amsfonts}')
col1 = "grey"
col2 = "blue"
lw1 = 1.5
lw2 = 2



level = 1

lw = 1.5
ypath = 0

marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor=col1, markersize=5)
marker2 = dict(marker='o', markerfacecolor=col1, markeredgecolor=col1, markersize=5)
marker3 = dict(marker='o', markerfacecolor='white', markeredgecolor=col2, markersize=5)
marker4 = dict(marker='o', markerfacecolor=col2, markeredgecolor=col2, markersize=5)


def plot_paths(a, ax, atxt='', ptxt=''):
    dx = 1./len(a)
    yvals = [(0, ())]
    x = 0
    i = 1
    for ai in a:
        xnew = x + dx
        yvalsnew = []
        for y, path in yvals:
            for s in [-1, 1]:
                ynew = y + s * ai
                pathnew = path + (s,)
                ax.plot([x, xnew], [y, ynew], linewidth=lw1, color=col2, **marker3)
                yvalsnew.append((ynew, pathnew))
        yvals = yvalsnew
        x = xnew
        i += 1
    props = dict(boxstyle='square', facecolor='white', linewidth=0.5)
    ax.text(0, 1.9, '$\\begin{{aligned}}&a={}\\\\&\\mathbb P(\\vert Z\\vert\\le1)={}\\end{{aligned}}$'.format(atxt, ptxt),
            ha='left', va='top', bbox=props, fontsize=12)

    ymax = 2.05
    ymin = -ymax

    for y in yvals:
        ax.plot([x], [y[0]], linewidth=lw2, color=col1, **marker4, clip_on=False)

    xmax = x + 0.1
    xmin = -0.05
    h = level * math.sqrt(sum([ai*ai for ai in a]))
    ax.plot([xmin, xmax], [1, 1], linewidth=lw1, linestyle='dashed', color='black')
    ax.plot([xmin, xmax], [-1, -1], linewidth=lw1, linestyle='dashed', color='black')

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
a = np.ones(1)
plot_paths(a, ax, '(1)', '1')

ax = fig.add_subplot(222)
a = np.ones(2)/math.sqrt(2)
a = np.array([4, 3])/5
plot_paths(a, ax, '(4, 3)/5', '1/2')

ax = fig.add_subplot(223)
a = np.array([12., 9, 8])/17
plot_paths(a, ax, '(12, 9, 8)/17', '3/4')

ax = fig.add_subplot(224)
a = np.array([1.,1,1, 1])/2
plot_paths(a, ax, '(1, 1, 1, 1)/2', '7/8')





plt.subplots_adjust(left=0.00, right=0.999, bottom=0.01, top=1, hspace=0, wspace=0)

#ax.legend(loc='upper right')
plt.show()