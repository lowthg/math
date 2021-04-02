"""
Plots Brownian motion, and associated brownian bridges on subintervals
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

seed = 1
npts = 5000
interval_colors = ['red', 'green', 'blue', 'purple']
nintervals = len(interval_colors)
tmax = 1.0
drift = -0.2

random.seed(seed)
times = np.linspace(0, tmax, npts)
BMvals = np.zeros(npts)

intervals = []
ileft = 1
tleft = 0

for i in range(1, npts):
    t0 = times[i-1]
    t1 = times[i]
    dt = t1 - t0
    B0 = BMvals[i-1]
    B1 = B0 + random.gauss(0, np.sqrt(dt)) + drift * dt
    BMvals[i] = B1
    if i > 1 and B0 * B1 < 0:
        t = (B1 * t0 - B0 * t1)/(B1 - B0)
        intervals.append([ileft, i, tleft, t])
        ileft = i
        tleft = t

intervals.sort(key=lambda x: x[2] - x[3])
intervals = intervals[:4]
intervals.sort(key=lambda x: x[0])

ileft = 0
tleft = 0.0
paths = []
for i, interval in enumerate(intervals):
    paths.append([ileft, interval[0], tleft, interval[2], 'black', False])
    paths.append(interval + [interval_colors[i], True])
    ileft = interval[1]
    tleft = interval[3]
paths.append([ileft, npts, tleft, tmax, 'black', False])

for i, path in enumerate(paths):
    pathtimes = list(times[path[0]:path[1]])
    pathvals = list(BMvals[path[0]:path[1]])
    if i < nintervals * 2:
        pathtimes += [path[3]]
        pathvals += [0.0]
    if i > 0:
        pathtimes = [path[2]] + pathtimes
        pathvals = [0.0] + pathvals
    path += [pathtimes, pathvals]

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
for path in paths:
    ax1.plot(path[6], path[7], linewidth=0.7, color=path[4])
    if path[5]:
        pathtimes = path[6]
        t0 = pathtimes[0]
        t1 = pathtimes[-1]
        dt = t1 - t0
        c = 1/math.sqrt(dt)
        pathtimes = [(t - t0)/(t1 - t0) for t in pathtimes]
        pathvals = [c * abs(x) for x in path[7]]
        ax2.plot(pathtimes, pathvals, linewidth=1, color=path[4])

ax1.plot([0, times[-1]], [0, 0], linewidth=0.5, color="black")

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)

ax1.set_xlim(0, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xlim(0, 1)
ax2.set_ylim(0)
ax2.set_xticks([])
ax2.set_yticks([])

plt.show()
