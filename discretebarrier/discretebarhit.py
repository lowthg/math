"""
accuracy of discrete approximation to continuous barrier
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from scipy.interpolate import make_interp_spline


k = 0.5

# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(n_steps, [1.14/math.sqrt(10*x) for x in n_steps], linewidth=2, color='black', alpha=0.7)
#ax.plot(n_steps, p_arr, linewidth=2, color='red')
#ax.plot(n_steps, p_arr - dev_arr * 2, linewidth=1, color='red')
#ax.plot(n_steps, p_arr + dev_arr * 2, linewidth=1, color='red')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

sigma = 0.7
ax.text(0.5, 0.3, "$X$", fontsize=13)
ax.text(0.12, k - 0.035, "$K$", fontsize=13)
ax.text(0.36, k + 0.03, "$\\delta t$", fontsize=10)
ax.text(0.63, k + 0.01, "$\\sim\\delta t/2$", fontsize=10)
ax.text(0.75, k-0.15, "$\\sim\\sigma\\sqrt{\\delta t/2}$", fontsize=10)
plt.annotate(xy=(0.75, k), xytext=(0.75, k-math.sqrt(0.15) * sigma), text='', arrowprops=dict(arrowstyle='<->'))
plt.annotate(xy=(0.25, k + 0.02), xytext=(0.5, k + 0.02), text='', arrowprops=dict(arrowstyle='<->'))
plt.annotate(xy=(0.6, k), xytext=(0.75, k), text='', arrowprops=dict(arrowstyle='<->'))
x1 = np.linspace(0, 0.15, 50)
y1 = np.sqrt(x1) * 0.7

dx = 1/200
x3 = [0]
y3 = [0.2]
random.seed(14)
a = sigma / math.sqrt(200)
j = 0
for i in range(200):
    x3.append(x3[-1] + dx)
    y3.append(y3[-1] + random.gauss(0, a))
    if y3[-1] > k:
        break

a = 0.6 / x3[-1]
x3 = [z * a for z in x3]
a = (k - 0.2) / (y3[-1] - 0.2)
y3 = [z * a + 0.2 * (1 - a) for z in y3]

ax.plot(x3, y3, linewidth=2, color='blue')

ax.plot(x1 + 0.6, y1 + k, linewidth=2, color='blue', alpha=0.7, linestyle = 'dashed')

ax.plot(x1 + 0.6, y1 + k, linewidth=2, color='blue', alpha=0.7, linestyle = 'dashed')
ax.plot(x1 + 0.6, -y1 + k, linewidth=2, color='blue', alpha=0.7, linestyle = 'dashed')

ax.plot([0, 1], [k, k], linewidth=1, color='grey', alpha=0.7, linestyle='dashed')
ax.plot([0.25, 0.25], [k, 1], linewidth=1, color='black')
ax.plot([0.5, 0.5], [k, 1], linewidth=1, color='black')
ax.plot([0.75, 0.75], [k, 1], linewidth=1, color='black')
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()