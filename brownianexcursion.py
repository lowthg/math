"""
Plots Brownian motion, local time at 0, and the auxilliary BM
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

npts = 3001
times = np.linspace(0.0, 2.0, npts)
Xpath = np.zeros(npts)
seed = 4

random.seed(seed)

maxi0 = maxi1 = 0
maxsgn = 0
i0 = 0
len = 0.0
oldsgn = 0.0

for i in range(1, npts):
    dX = random.gauss(0, 1) * math.sqrt(times[i] - times[i-1])
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

extimes = [(t - t0)/(t1 - t0) for t in times[maxi0:maxi1]]
exX = [max(x * maxsgn, 0.0) for x in Xpath[maxi0:maxi1]]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(extimes, exX, label='B', linewidth=1)

ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.set_xticks([0, 1])
ax.set_yticks([])
ax.set_xlim(0, 1)

#ax.legend(loc='best')
ax.margins(0, tight=True)
plt.show()
