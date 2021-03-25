"""
Plots Brownian motion, and associated brownian bridges on subintervals
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

class BMRange:
    """Sub-range of BM"""
    sim_val = 0.0

    def __init__(self, t0: float, t1: float, isbb: bool, dx: float, drift: float, color: str = "black"):
        self.t0 = t0
        self.t1 = t1
        self.isBB = isbb
        self.color = color
        npts = math.ceil((t1 - t0)/dx)
        self.times = np.linspace(t0, t1, npts + 1)
        self.Xpath = np.zeros(npts + 1)
        self.drift = drift

    def __str__(self):
        return "[{} {} {} {}]".format(self.t0, self.t1, self.isBB, self.color)

    def simulate(self):
        npts = len(self.times)
        self.Xpath[0] = self.sim_val
        for i in range(1, npts):
            dt = self.times[i] - self.times[i-1]
            self.Xpath[i] = self.Xpath[i-1] + random.gauss(0, math.sqrt(dt)) + drift * dt
        BMRange.sim_val = self.Xpath[-1]

    def linpath(self):
        return [self.t0, self.t1], [self.Xpath[0], self.Xpath[-1]]

    def bbpath(self):
        npts = len(self.times)
        c = self.t1 - self.t0
        b = math.sqrt(c)
        times = np.zeros(npts)
        Xpath = np.zeros(npts)
        x0 = self.Xpath[0]
        x1 = self.Xpath[-1]
        for i in range(npts):
            t = (self.times[i] - self.t0) / c
            times[i] = t
            Xpath[i] = (self.Xpath[i] - x1 * t - x0 * (1.0 - t))/b
        return times, Xpath

Tmax = 1.0
npts = 5000
seed = 1
drift = 0.2

ranges = [
    [.05,  0.25, "red"],
    [0.26, 0.5, "green"],
    [0.55, 0.75, "blue"],
    [0.8, 0.95, "purple"]
]

random.seed(seed)
dx = Tmax / (npts + 1)
xmin = 0.0
xmax = 0.0
rangeinfo = []
t1 = 0.0
for r in ranges:
    t0 = r[0]
    rangeinfo.append(BMRange(t1, t0, False, dx, drift))
    t1 = r[1]
    rangeinfo.append(BMRange(t0, t1, True, dx, drift, r[2]))
rangeinfo.append(BMRange(t1, Tmax, False, dx, drift))

for r in rangeinfo:
    r.simulate()
    xmin = min(xmin, min(r.Xpath))
    xmax = max(xmax, max(r.Xpath))
    print(r)

ymin = xmin + 0.05 * (xmin - xmax)
ymax = xmax + 0.05 * (xmax - xmin)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
for r in rangeinfo:
    color = r.color
    ax1.plot(r.times, r.Xpath, linewidth=1, color=color)
    if r.isBB:
        lint, linx= r.linpath()
        ax1.plot(lint, linx, linewidth=0.5, color=color)
        ax1.plot([lint[0], lint[0]], [ymin, ymax], linewidth=0.5, color=color)
        ax1.plot([lint[-1], lint[-1]], [ymin, ymax], linewidth=0.5, color=color)
        bbt, bbx = r.bbpath()
        ax2.plot(bbt, bbx, linewidth=1, color=color)
ax1.plot([0, Tmax], [0, 0], linewidth=.5, color="black")
ax2.plot([0, 1], [0, 0], linewidth=.5, color="black")
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
ax1.set_xlim(0, Tmax)
ax1.set_ylim(ymin, ymax)
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xlim(0, 1)
ax2.set_xticks([])
ax2.set_yticks([])

plt.show()

