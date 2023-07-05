"""
Plots Brownian motion and two meanders
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

npts = 3001
times = np.linspace(0.0, 1.0, npts)
Xpath = np.zeros(npts)
seed = 1
seed = 9
seed = 32

seed = 47
seed = 50

random.seed(seed)

i0 = 0
minX = 0.0

for i in range(1, npts):
    t0 = times[i-1]
    t1 = times[i]
    dt = t1 - t0
    dX = random.gauss(0, 1) * math.sqrt(dt)
    Xpath[i] = Xpath[i-1] + dX
    if Xpath[i] <= minX:
        minX = Xpath[i]
        i0 = i

t0 = times[i0]

maxX = max(Xpath)
miny = minX - (maxX - minX) * 0.04
maxy = maxX + (maxX - minX) * 0.04

fig = plt.figure()
ax1 = fig.add_subplot(211)
# Xpath[maxi1:] = [-x for x in Xpath[maxi1:]]
ax1.plot(times[:i0+1], Xpath[:i0+1], linewidth=1, color='blue')
ax1.plot(times[i0:], Xpath[i0:], linewidth=1, color='green')
ax1.plot([0, times[-1]], [0, 0], linewidth=0.5, color='grey')
ax1.plot([0, times[-1]], [0, 0], linewidth=0.7, color='black')
ax1.plot([t0, t0], [miny, 0], linewidth=0.5, color='grey', linestyle='--')
ax1.text(t0-0.01, 0.02, '$\\tau$')
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlim(0, times[-1])
ax1.set_ylim(miny, maxy)

ax = fig.add_subplot(212)

z1 = (Xpath[i0::-1] - minX) / math.sqrt(t0)
z2 = (Xpath[i0:] - minX) / math.sqrt(1-t0)
ax.plot(times[:i0 + 1] / t0, z1, linewidth=1, color='blue')
ax.plot((times[i0:] - t0) / (1-t0), z2, linewidth=1, color='green')

ax.set_xticks([0, 1])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, max(max(z1), max(z2)) * 1.04)
#ax.text(0.37, 0.6, "$\\bf\\it B$", fontsize=13)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.margins(0, tight=True)
plt.show()
