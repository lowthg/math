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

b = 0.6 / x3[-1]
x3 = [z * b for z in x3]
c = (k - 0.2) / (y3[-1] - 0.2)
y3 = [z * c + 0.2 * (1 - c) for z in y3]

random.seed(15)
random.seed(39)
random.seed(42)
x4 = np.linspace(0.6, 0.75, 40)
dx2 = x4[1] - x4[0]
a *= c * math.sqrt(b * dx2 / dx)
y4 = np.zeros(40)
y4[0] = y3[-1]
for i in range(1, len(x4)):
    y4[i] = y4[i-1] + random.gauss((x4[i]-x4[i-1])*0, a)

p1 = (0.75, y4[-1])
p2 = None

print(x3)
for i in range(1, len(x3)):
    if x3[i] >= 0.5:
        u = (x3[i] - 0.5)/(x3[i] - x3[i-1])
        p2 = (0.5, u*y3[i-1] + (1-u)*y3[i])
        break

u = 0.6
p3 = (u * p1[0] + (1-u) * p2[0], u * p1[1] + (1-u) * p2[1])
p4 = (p3[0], 0.65)
ax.plot(x3, y3, linewidth=2, color='blue')
ax.plot(x4, y4, linewidth=2, color='blue')

plt.annotate(xy=(0.75, k), xytext=(0.75, y4[-1]), text='', arrowprops=dict(arrowstyle='<->'))
plt.annotate(xy=p3, xytext=p4, text='', arrowprops=dict(arrowstyle='<->'))
ax.text(0.755, (k + y4[-1])/2 - 0.02, "$-R$", fontsize=12)
ax.text(p3[0] - 0.03, p3[1] - 0.05, "$pX_{t_i}+(1-p)X_{t_{i-1}}$", fontsize=10)
ax.text(p4[0] - 0.13, p4[1] - 0.08, "$c|X_{t_i}-X_{t_{i-1}}|$", fontsize=10)
ax.text(0.76, p4[1]-0.01, "$M_i$", fontsize=12)

ax.plot([0, 1], [k, k], linewidth=1, color='grey', alpha=0.7, linestyle='dashed')
ax.plot([0.25, 0.25], [k, 1], linewidth=1, color='black')
ax.plot([0.5, 0.5], [k, 1], linewidth=1, color='black')
ax.plot([0.75, 0.75], [k, 1], linewidth=1, color='black')
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linewidth=1, color='grey', linestyle='dashed')
ax.plot([p4[0]-0.02, 0.75], [p4[1], p4[1]], linewidth=1, color='grey', alpha=0.7, linestyle='dashed')
ax.scatter([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='tab:blue')

plt.subplots_adjust(left=0.002, right=0.998, bottom=0.002, top=0.998, hspace=0, wspace=0)
plt.show()