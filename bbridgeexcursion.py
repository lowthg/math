"""
Plots Brownian motion, and associated brownian bridges on subintervals
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

seed = 4
seed = 6
npts = 1000

random.seed(seed)
times = np.linspace(0, 1, npts)
BBvals = np.zeros(npts)

for i in range(1, npts):
    dt = times[i] - times[i-1]
    BBvals[i] = BBvals[i-1] + random.gauss(0, np.sqrt(dt))
BM1 = BBvals[-1]
for i in range(1, npts - 1):
    BBvals[i] -= times[i] * BM1
BBvals[-1] = 0.0

imin = 0
imax = 0
BBmin = 0.0
BBmax = 0.0
for i in range(1, npts - 1):
    if BBvals[i] < BBmin:
        BBmin = BBvals[i]
        imin = i
    elif BBvals[i] > BBmax:
        BBmax = BBvals[i]
        imax = i

if BBmax + BBmin < 0:
    BBvals = [-x for x in BBvals]
    imin, imax = imax, imin
    BBmin, BBmax = -BBmax, -BBmin

BEvals = np.zeros(npts)
for i in range(1, npts - imin):
    BEvals[i] = BBvals[imin + i] - BBmin
for i in range(npts - imin, npts):
    BEvals[i] = BBvals[imin + i - npts] - BBmin

yminBB = BBmin + (BBmin - BBmax) * 0.05
ymaxBB = BBmax + (BBmax - BBmin) * 0.05
ymaxBE = (BBmax - BBmin) * 1.05

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.plot(times[:imin+1], BBvals[:imin+1], linewidth=1, color="blue")
ax1.plot(times[imin:], BBvals[imin:], linewidth=1, color="green")
ax1.plot([0, 1], [0, 0], linewidth=0.5, color="black")
ax2.plot(times[:npts - imin + 1], BEvals[:npts - imin + 1], linewidth=1, color="green")
ax2.plot(times[npts - imin:], BEvals[npts-imin:], linewidth=1, color="blue")
#ax1.plot([times[imin], times[imin]], [yminBB, ymaxBB], linewidth=0.5, color="grey")
#ax2.plot([times[npts - imin], times[npts - imin]], [0, ymaxBE], linewidth=0.5, color="grey")

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)


ax1.set_xlim(0, 1)
ax1.set_ylim(yminBB, ymaxBB)
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xlim(0, 1)
ax2.set_ylim(0, ymaxBE)
ax2.set_xticks([])
ax2.set_yticks([])

plt.show()
