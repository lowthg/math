"""
accuracy of discrete approximation to continuous barrier
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def is_hit(ntimes, dt, level):
    """
    returns (is hit, prob cts interpolation hits)
    """
    x = 0.0
    s = math.sqrt(dt)
    a = -2 / dt
    hit = 0.0
    adjhit = 0.0
    adjlevel = level - 0.5826 * s
    ctsNotHit = 1.0
    for _ in range(ntimes):
        x1 = x + random.gauss(0, s)
        if x1 >= adjlevel:
            adjhit = 1.0
            if x1 >= level:
                hit = 1.0
                ctsNotHit = 0
                break
        p = math.exp(a * (level - x) * (level - x1))
        ctsNotHit *= 1 - p
        x = x1

    return hit, 1.0 - ctsNotHit, adjhit


def get_discrete_diff(npaths, n_steps, dt, level):
    print('nsteps =', n_steps)
    hits = 0.0
    hits2 = 0.0
    adjhits = 0.0
    adjhits2 = 0.0
    for _ in range(npaths):
        hit, chit, adjhit = is_hit(n_steps, dt, level)
        x = chit - hit
        hits += x
        hits2 += x * x
        y = chit - adjhit
        adjhits += y
        adjhits2 += y * y

    hits /= npaths
    hits2 /= npaths
    stddev = math.sqrt((hits2 - hits * hits) / npaths)
    adjhits /= npaths
    adjhits2 /= npaths
    adjdev = math.sqrt((adjhits2 - adjhits * adjhits) / npaths)
    return hits, stddev, adjhits, adjdev


vol = 1
t_exp = 1
level = 0.66

npaths = 100000

n_steps = list(range(10, 30, 1))+list(range(30,40,2))+list(range(40,80,5))+list(range(80,201,10))

showadj = True

p_arr = np.zeros(len(n_steps))
dev_arr = np.zeros(len(n_steps))
p2_arr = np.zeros(len(n_steps))
dev2_arr = np.zeros(len(n_steps))

for i, n in enumerate(n_steps):
    dt = t_exp / n
    p, dev, p2, dev2 = get_discrete_diff(npaths, n, dt, level)
    p_arr[i] = p
    dev_arr[i] = dev
    p2_arr[i] = p2
    dev2_arr[i] = dev2

print(p_arr)
print(p2_arr)

ymax = max(p_arr)
# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
if not showadj:
    ax.plot(n_steps, p_arr, linewidth=2, color='red', label='discrete')
    #ax.plot(n_steps, p_arr - dev_arr * 2, linewidth=1, color='red')
    #ax.plot(n_steps, p_arr + dev_arr * 2, linewidth=1, color='red')
ax.set_xlim(min(n_steps), max(n_steps))
if showadj:
    ax.set_ylim(min(0, min(p2_arr)), max(0, max(p2_arr)))
    ax.plot(n_steps, p2_arr, linewidth=2, color='blue', label='shifted')
    ax.plot([n_steps[0], n_steps[-1]], [0, 0], linewidth=1, color='grey', linestyle='dashed')
    ax.legend(loc='upper right')
    ax.plot(n_steps, p2_arr - dev2_arr * 2, linewidth=1, color='blue')
    ax.plot(n_steps, p2_arr + dev2_arr * 2, linewidth=1, color='blue')
    ax.plot(n_steps, [-0.03/x for x in n_steps], linewidth=2, color='black', alpha=0.7)
else:
    ax.set_ylim(0)
    ax.plot(n_steps, [1.14/math.sqrt(10*x) for x in n_steps], linewidth=2, color='black', alpha=0.7)
#ax.set_xticks([])
#ax.set_yticks([])
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()