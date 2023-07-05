"""
accuracy of discrete approximation to continuous barrier
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.interpolate as interp


def is_hit(ntimes, dt, level, adj_coeffs):
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
    m = len(adj_coeffs)
    a2hit = np.zeros(m)
    for _ in range(ntimes):
        x1 = x + random.gauss(0, s)
        p = math.exp(a * (level - x) * (level - x1))
        ctsNotHit *= 1 - p
        if max(2*x1-x, 2*x - x1) >= adjlevel:
            allhit = True
            if x1 >= adjlevel:
                adjhit = 1.0
                if x1 >= level:
                    hit = 1.0
                    ctsNotHit = 0
                else:
                    allhit = False
            else:
                allhit = False
            for i, (p,c) in enumerate(adj_coeffs):
                if a2hit[i] == 0:
                    m1 = p * x1 + (1-p) * x + c * abs(x1 - x)
                    if m1 >= level:
                        a2hit[i] = 1
                    else:
                        allhit = False
            if allhit:
                break
        x = x1

    return hit, 1.0 - ctsNotHit, adjhit, a2hit


def get_discrete_diff(npaths, n_steps, dt, level, adj_coeffs):
    print('nsteps =', n_steps)
    hits = 0.0
    hits2 = 0.0
    adjhits = 0.0
    adjhits2 = 0.0
    a2hits = np.zeros(len(adj_coeffs))
    a2hits2 = np.zeros(len(adj_coeffs))
    for _ in range(npaths):
        hit, chit, adjhit, a2hit = is_hit(n_steps, dt, level, adj_coeffs)
        x = chit - hit
        hits += x
        hits2 += x * x
        y = chit - adjhit
        adjhits += y
        adjhits2 += y * y
        z = -a2hit + chit
        a2hits += z
        a2hits2 += z * z

    hits /= npaths
    hits2 /= npaths
    stddev = math.sqrt((hits2 - hits * hits) / npaths)
    adjhits /= npaths
    adjhits2 /= npaths
    adjdev = math.sqrt((adjhits2 - adjhits * adjhits) / npaths)
    a2hits /= npaths
    a2hits2 /= npaths
    a2dev =np.sqrt((a2hits2 - a2hits * a2hits) / npaths)
    return hits, stddev, adjhits, adjdev, a2hits, a2dev


p0 = 0.7311253

adj_coeffs = [
    (0, 2*p0-1),
    (0.5, 0.87290),
    (1, 2 * p0 - 1),
]


vol = 1
t_exp = 1
level = 0.66

npaths = 10000000

n_steps = list(range(10, 30, 1))+list(range(30,40,2))+list(range(40,80,5))+list(range(80,201,10))
n_steps = list(range(10, 200, 10))
n_steps = list(range(10, 30, 2))+list(range(30,40,4))+list(range(40,80,10))+list(range(80,201,20))

showadj = True

p_arr = np.zeros(len(n_steps))
dev_arr = np.zeros(len(n_steps))
p2_arr = np.zeros(len(n_steps))
dev2_arr = np.zeros(len(n_steps))
p3_arr = []
dev3_arr = []
for i in range(len(adj_coeffs)):
    p3_arr.append(np.zeros(len(n_steps)))
    dev3_arr.append(np.zeros(len(n_steps)))

y3max = 0
for i, n in enumerate(n_steps):
    dt = t_exp / n
    p, dev, p2, dev2, p3, dev3 = get_discrete_diff(npaths, n, dt, level, adj_coeffs)
    p_arr[i] = p
    dev_arr[i] = dev
    p2_arr[i] = p2
    dev2_arr[i] = dev2
    for j in range(len(adj_coeffs)):
        p3_arr[j][i] = p3[j]
        dev3_arr[j][i] = dev3[j]
        y3max = max(y3max, p3[j])

print(p_arr)
print(p2_arr)
for i in range(len(adj_coeffs)):
    print("p = {}".format(adj_coeffs[i][0]))
    print(p3_arr[i])

ymax = max(p_arr)
# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
#if True:
#    ax.plot(n_steps, p_arr, linewidth=2, color='red', label='discrete')
    #ax.plot(n_steps, p_arr - dev_arr * 2, linewidth=1, color='red')
    #ax.plot(n_steps, p_arr + dev_arr * 2, linewidth=1, color='red')
ax.set_xlim(min(n_steps), max(n_steps))
if True:
#    ax.set_ylim(min(0, min(p2_arr)), max(0, max(p_arr)))
    ax.set_ylim(min(0, min(p2_arr)), 0.01)
    ax.plot(n_steps, p2_arr, linewidth=2, color='blue', label='shifted')
    ax.plot([n_steps[0], n_steps[-1]], [0, 0], linewidth=1, color='grey', linestyle='dashed')

for j in range(len(adj_coeffs)):
    ax.plot(n_steps, p3_arr[j], linewidth=2, label='p = {}'.format(adj_coeffs[j][0]))

ax.legend(loc='upper right')

#    ax.plot(n_steps, p2_arr - dev2_arr * 2, linewidth=1, color='blue')
#    ax.plot(n_steps, p2_arr + dev2_arr * 2, linewidth=1, color='blue')
#    ax.plot(n_steps, [-0.03/x for x in n_steps], linewidth=2, color='black', alpha=0.7)
#ax.set_xticks([])
#ax.set_yticks([])
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()