"""
Plots fractional Brownian motion paths for different values of the Hurst parameter
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def bmpath(times, H, seed):
    np.random.seed(seed)
    npts = len(times)
    mean = np.zeros(shape=(npts,))
    cov = np.ndarray(shape=(npts, npts))
    for i in range(0, npts):
        t = times[i]
        cov[i, i] = math.pow(t, H * 2)
        for j in range(0, i):
            dt = t - times[j]
            cov[i, j] = cov[j, i] = (cov[i, i] + cov[j, j] - math.pow(dt, H * 2))/2
    return np.random.multivariate_normal(mean, cov)


def main():
    seed = 6

    times = np.linspace(0.0, 1.0, 600)
    path1 = bmpath(times, 0.25, seed)
    path2 = bmpath(times, 0.5, seed)
    path3 = bmpath(times, 0.75, seed)

    minx = min(min(path1), min(path2), min(path3))
    maxx = max(max(path1), max(path2), max(path3))

    gs = gridspec.GridSpec(1, 3)
    gs.update(hspace=0, wspace=0)

    for i, path in enumerate([path1, path2, path3]):
        ax = plt.subplot(gs[i])
        ax.plot(times, path, linewidth=0.8, color='black')
        ax.plot([0, 1], [0, 0], linewidth=1, color='grey', linestyle='dashed')
        minp = min(path)
        maxp = max(path)
        scale = max(minp / minx, maxp / maxx)
        ax.set_ylim(minx * scale, maxx * scale)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_xlim(0, 1)
        ax.margins(0)

    plt.show()


main()
