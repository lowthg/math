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
Lpath = np.zeros(npts)
Wpath = np.zeros(npts)
Mpath = np.zeros(npts)
seed = 1

random.seed(seed)

Wmax = 0.0

for i in range(1, npts):
    dX = random.gauss(0, 1) * math.sqrt(times[i] - times[i-1])
    Xpath[i] = Xpath[i-1] + dX
    sgn = np.sign(Xpath[i-1])
    Wpath[i] = Wpath[i-1] - sgn * dX
    Mpath[i] = max(Mpath[i-1], Wpath[i])
    if Xpath[i] > 0.0 > Xpath[i-1]:
        dL = Xpath[i]
    elif Xpath[i] < 0.0 < Xpath[i-1]:
        dL = -Xpath[i]
    else:
        dL = 0.0
    Lpath[i] = Lpath[i-1] + 2 * dL

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(times, Xpath, label='B', linewidth=1)
ax.plot(times, Mpath, label='L', linewidth=1.5, color='black')
ax.plot(times, Wpath, label='W', linewidth=0.3, color='grey')

ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.set_xticks([])
ax.set_yticks([])

ax.legend(loc='best')
ax.margins(0, tight=True)
plt.show()
