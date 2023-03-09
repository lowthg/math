"""
Plots Brownian meanders
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

npts = 3001
times = np.linspace(0.0, 1.0, npts)
Xpath = np.zeros(npts)
maxX = 0.0
paths = []
colors = 'bgrcmyk'

for seed in [5, 9, 10, 11, 12, 13, 15]:
    random.seed(seed)

    i0 = 0
    oldsgn = 0.0

    for i in range(1, npts):
        t0 = times[i-1]
        t1 = times[i]
        dt = t1 - t0
        dX = random.gauss(0, 1) * math.sqrt(dt)
        Xpath[i] = Xpath[i-1] + dX
        sgn = np.sign(Xpath[i-1])

        if sgn != oldsgn:
            i0 = i
            oldsgn = sgn

    t0 = times[i0]
    mtimes = [(t - t0)/(1 - t0) for t in times[i0:]]
    mX = [max(x * oldsgn, 0.0) for x in Xpath[i0:]]

    maxX = max(max(mX), maxX)
    paths.append((mtimes, mX))
    assert t0 < 0.8

maxy = maxX * 1.04

fig = plt.figure()
ax1 = fig.add_subplot(111)
i = 0
for mt, mX in paths:
    ax1.plot(mt, mX, linewidth=0.85, color=colors[i])
    i += 1

ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlim(0, 1)
ax1.set_ylim(0, maxy)

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax1.margins(0, tight=True)
plt.show()
