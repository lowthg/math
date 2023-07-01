"""
Computes c = c(p) chosen such that discrete barrier condition
pX(t)+(1-p)X(s) + x |X(t) - X(s)| >= K
has zero expected overshoot
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from scipy.interpolate import make_interp_spline


p0 = 0.7311253

vals = [
    0.5,    0.87290,
    0.51,   0.87261,
    0.52,   0.87173,
    0.53,   0.87027,
    0.54,   0.86823,
    0.55,   0.86560,
    0.56,   0.86239,
    0.57,   0.85861,
    0.58,   0.854251,
    0.59,   0.84932,

    0.6,    0.84383,
    0.61,   0.83779,
    0.62,   0.83120,
    0.63,   0.82407,
    0.64,   0.81646,
    0.65,   0.808351,
    0.66,   0.79980,
    0.67,   0.790845,
    0.68,   0.781548,
    0.69,   0.77196,

    0.7,    0.76216,
    0.71,   0.75224,
    0.72,   0.742255,
    0.73,   0.73226,

    p0, p0
]

parr = []
carr = []
v = []
for i in range(0, len(vals), 2):
    v.append([vals[i], vals[i+1]])

v.sort(key=lambda a: a[0])

for i in range(len(v) - 1, 0, -1):
    parr.append(1-v[i][0])
    carr.append(v[i][1])
for i in range(len(v)):
    parr.append(v[i][0])
    carr.append(v[i][1])

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(n_steps, [1.14/math.sqrt(10*x) for x in n_steps], linewidth=2, color='black', alpha=0.7)
#ax.plot(n_steps, p_arr, linewidth=2, color='red')
#ax.plot(n_steps, p_arr - dev_arr * 2, linewidth=1, color='red')
#ax.plot(n_steps, p_arr + dev_arr * 2, linewidth=1, color='red')
p1 = 0.8
ax.set_xlim(1-p1, p1)
ax.set_ylim(2*p0-p1, 0.875)
#ax.set_xticks([])
#ax.set_yticks([])

#sigma = 0.7
#ax.text(0.5, 0.3, "$X$", fontsize=13)
#ax.text(0.12, k - 0.035, "$K$", fontsize=13)

ax.plot(parr, carr, linewidth=1, color='blue')
ax.plot([p0, p1], [p0, 2*p0-p1], linewidth=1, color='grey', linestyle='dashed')
ax.plot([1-p0, 1-p1], [p0, 2*p0-p1], linewidth=1, color='grey', linestyle='dashed')
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()