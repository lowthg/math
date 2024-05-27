"""
plots relating to int I(W > 0) dW
"""

import math
import random

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from scipy.stats import norm
import scipy.stats


showdensity = False
showpath = True

if showdensity:
    ax = plt.subplot(xlim=(-2,3), ylim=(0, 1.1))
    x = [_ * 0.01 - 2 for _ in range(501)]
    y = [norm.pdf(_) * 2/3 if _ > 0 else norm.pdf(2*_) * 8/3 for _ in x]
    ax.plot(x, y, color='blue')
    ax.fill_between(x, y, facecolor='blue', alpha=0.1)
    plt.show()

if showpath:
    random.seed(4)
    random.seed(7)
    random.seed(12)
    random.seed(13)
    random.seed(16)
    random.seed(21)
    random.seed(31)
    random.seed(47)
    ntimes = 20
    times = np.linspace(0, 1, ntimes)
    dt = times[1]
    wvals = np.zeros(ntimes)
    xvals = np.zeros(ntimes)

    qty0 = 1
    wpaths = [(qty0, [0], [0])]

    for i in range(1, ntimes):
        wvals[i] = wvals[i-1] + random.gauss(0, dt)
        if i == 1 and wvals[1] > 0:
            wvals[1] = -wvals[1]    # start on downtick
        qty = 1 if wvals[i] >= 0 else 0
        wpaths[-1][1].append(times[i])
        wpaths[-1][2].append(wvals[i])
        if qty != qty0 and i < ntimes - 1:
            wpaths.append((qty, [times[i]], [wvals[i]]))
        xvals[i] = xvals[i-1] + qty0 * (wvals[i] - wvals[i-1])
        qty0 = qty

    plt.rcParams.update({"text.usetex": True})
    fig = plt.figure()
    ax = fig.add_subplot(111)
    marker1 = dict(marker='o', markerfacecolor='white', markeredgecolor='blue', markersize=5)
    marker2 = dict(marker='o', markerfacecolor='blue', markeredgecolor='blue', markersize=5)

    ax.plot([0, 1], [0, 0], linewidth=1, color='grey', zorder=1, alpha=0.5)

    ax.plot([], [], linewidth=2, color='blue', label='$S$')
    ax.plot([], [], linewidth=2, color='green', label='$X=\\int1_{\\{S\\ge K\\}}dS$')
    ax.plot([], [], linewidth=2, color='red', label='$A=(S-K)_+-X$')
    ax.plot([], [], linewidth=1, alpha=0.5, color='grey', label='$K$')

    for path in wpaths:
        if path[0] == 1:
            ax.plot(path[1][:-1], path[2][:-1], linewidth=2, color='blue', zorder=3, alpha=1, **marker2, clip_on=False)
            ax.plot(path[1][-2:], path[2][-2:], linewidth=2, color='blue', zorder=2, alpha=1)
        else:
            pass
            ax.plot(path[1][:-1], path[2][:-1], linewidth=2, color='blue', zorder=3, alpha=1, ls='dashed', **marker1)
            ax.plot(path[1][-2:], path[2][-2:], linewidth=2, color='blue', zorder=2, alpha=1, ls='dashed')

    ax.plot(times, xvals, linewidth=2, color='green', zorder=1, alpha=1)
    ax.plot(times, np.maximum(wvals,0) - xvals, linewidth=2, color='red', zorder=1, alpha=1)
    ax.set_yticks([])
    ax.set_xticks([0, 1], [0, '$T$'])
    ax.set_xlim(0, 1)
    ax.legend(loc='upper left')

    plt.subplots_adjust(left=0.01, right=0.98, bottom=0.05, top=0.99, hspace=0, wspace=0)
    plt.show()

