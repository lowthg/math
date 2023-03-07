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
#seed = 8
#seed = 19
seed = 32 # used for BM plot
seed = 33 # used for BB plot
bridge = True
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
    if bridge:
        a = (1 - t1) / (1 - t0)
        Xpath[i] = Xpath[i-1] * a + random.gauss(0, 1) * math.sqrt(dt*a)
    else:
        dX = random.gauss(0, 1) * math.sqrt(dt)
        Xpath[i] = Xpath[i-1] + dX
    sgn = np.sign(Xpath[i-1])

    if sgn != oldsgn:
        if i - i0 > maxi1 - maxi0:
            maxi0 = i0
            maxi1 = i
            maxsgn = oldsgn
        i0 = i - 1
        oldsgn = sgn

t0 = times[maxi0]
t1 = times[maxi1]
T = t0 + 0.4 * (t1 - t0)

Xpath = [x * maxsgn for x in Xpath]
extimes = [(t - t0)/(t1 - t0) for t in times[maxi0:maxi1]]
exX = [max(x, 0.0) for x in Xpath[maxi0:maxi1]]
minX = min(Xpath)
maxX = max(Xpath)
miny = minX - (maxX - minX) * 0.04
maxy = maxX + (maxX - minX) * 0.04

fig = plt.figure()
ax1 = fig.add_subplot(211)
# Xpath[maxi1:] = [-x for x in Xpath[maxi1:]]
ax1.plot(times[:maxi0+1], Xpath[:maxi0+1], linewidth=0.7, color='black')
ax1.plot(times[maxi1:], Xpath[maxi1:], linewidth=0.7, color='black')
ax1.plot(times[maxi0:maxi1+1], Xpath[maxi0:maxi1+1], linewidth=0.7, color='blue')
ax1.plot([0, times[-1]], [0, 0], linewidth=0.5, color='grey')
t0 = times[maxi0]
t1 = times[maxi1]
ax1.plot([0, times[-1]], [0, 0], linewidth=0.7, color='black')
ax1.plot([t0, t0], [miny, maxy], linewidth=0.5, color='grey', linestyle='--')
ax1.plot([t1, t1], [miny, maxy], linewidth=0.5, color='grey', linestyle='dashed')
ax1.plot([T,T], [miny, maxy], linewidth=0.5, color='grey', linestyle='dashed')
ax1.text(T-0.01, -0.09, '$T$')
ax1.text(t0-0.00, -0.08, '$\sigma$')
ax1.text(t1-0.015, -0.08, '$\\tau$')
ax1.text(0.23, 0.4, "$\\bf\\it X$", fontsize=13)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlim(0, times[-1])
ax1.set_ylim(miny, maxy)

ax = fig.add_subplot(212)

ax.plot(extimes, exX, label='B', linewidth=1, color='blue')
#ax.spines['left'].set_position('zero')
#ax.spines['right'].set_color('none')
#ax.spines['bottom'].set_position('zero')
#ax.spines['top'].set_color('none')
ax.set_xticks([0, 1])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, max(exX) * 1.04)
ax.text(0.3, 0.4, "$\\bf\\it B$", fontsize=13)
#ax.legend(loc='best')
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.margins(0, tight=True)
plt.show()
