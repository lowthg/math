"""
Plots Brownian motion, local time at 0, and the auxilliary BM
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

npts = 3001
times = np.linspace(0.0, 1.0, npts)
Xpath = np.zeros(npts)
seed = 5
seed = 9

random.seed(seed)

maxi0 = maxi1 = 0
maxsgn = 0
i0 = 0
len = 0.0
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
Xpath = [x * oldsgn for x in Xpath]
mtimes = [(t - t0)/(1 - t0) for t in times[i0:]]

mX = [max(x, 0.0) for x in Xpath[i0:]]

minX = min(Xpath)
maxX = max(Xpath)
miny = minX - (maxX - minX) * 0.04
maxy = maxX + (maxX - minX) * 0.04

fig = plt.figure()
ax1 = fig.add_subplot(211)
# Xpath[maxi1:] = [-x for x in Xpath[maxi1:]]
ax1.plot(times[:i0+1], Xpath[:i0+1], linewidth=1, color='black')
ax1.plot(times[i0:], Xpath[i0:], linewidth=1, color='blue')
ax1.plot([0, times[-1]], [0, 0], linewidth=0.5, color='grey')
ax1.plot([0, times[-1]], [0, 0], linewidth=0.7, color='black')
ax1.plot([t0, t0], [miny, maxy], linewidth=0.5, color='grey', linestyle='--')
ax1.plot([t1, t1], [miny, maxy], linewidth=0.5, color='grey', linestyle='dashed')
ax1.text(t0-0.00, -0.08, '$\\sigma$')
ax1.text(0.35, 0.3, "$\\bf\\it X$", fontsize=13)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlim(0, times[-1])
ax1.set_ylim(miny, maxy)

ax = fig.add_subplot(212)

ax.plot(mtimes, mX, label='B', linewidth=1, color='blue')

ax.set_xticks([0, 1])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, max(mX) * 1.04)
ax.text(0.37, 0.6, "$\\bf\\it B$", fontsize=13)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.margins(0, tight=True)
plt.show()
