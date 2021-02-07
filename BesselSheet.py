"""
Plots a Brownian sheet
"""

import random
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import pylab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

seed = 4
seed = 5
#seed = 6
#seed = 8
#seed = 11
xpts = 100
ypts = 100
tmax = 40.0
amax = 8.0
plotmax = amax * 1

random.seed(seed)
xvals = np.linspace(0.0, tmax, xpts)
yvals = np.linspace(0.0, amax, ypts)
Z3 = np.ndarray(shape=(xpts, ypts))

X3, Y3 = np.meshgrid(yvals, xvals)

for j in range(0, ypts):
    Z3[0, j] = 0.0

def chi2(a, x):
    z = random.gammavariate(a/2, 2)
    u = random.random()
    rate = x / 2
    c0 = math.exp(-rate)
    c1 = c0
    for n in range(0, 20000):
        if u < c0:
            break
        c1 *= rate / (n+1)
        c0 += c1
        z = z + random.gammavariate(1, 2)
        if n > 19000:
            raise Exception('too many iterations')
#    z += x
    return z
#    return random.gauss(0.0, math.sqrt(a * x))

minz = 0.0
maxz = 0.0
for i in range(1, xpts):
    dt = xvals[i] - xvals[i-1]
    Z3[i, 0] = 0.0
    for j in range(1, ypts):
        da = yvals[j] - yvals[j - 1]
        Z3[i, j] = Z3[i, j-1] + chi2(da, (Z3[i-1, j] - Z3[i-1, j-1])/dt) * dt
        minz = min(minz, Z3[i, j])
        maxz = max(maxz, Z3[i, j])


for j in range(1, ypts):
    if yvals[j] > plotmax:
        for i in range(0, xpts):
            Z3[i, j] = pylab.NaN


fig = plt.figure()
ax = plt.axes(projection='3d', frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5) # coolwarm, Reds, summer
#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue')
ax.set_xlim(0.0, plotmax)
ax.set_ylim(tmax, 0)

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.view_init(20, 134)

fig2 = plt.figure()
ax2 = plt.axes(projection='3d', frame_on='False')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_zticks([])
eps = 1
for j in range(1, ypts):
    a = yvals[j]
    exvals = []
    avals = []
    tvals = []
    flag = False
    imax = 0
    for i in range(xpts-1, 0, -2):
        if Z3[i, j] - Z3[i, j-1] > eps:
            imax = i
            break
    truncate = False
    for i in range(0, xpts):
        dz = Z3[i, j] - Z3[i, j-1]
        if dz > eps and not flag:
            exvals.append(0.0)
            avals.append(a)
            tvals.append(xvals[i-1])
            flag = True
        if flag:
            exvals.append(dz)
            avals.append(a)
            tvals.append(xvals[i])
        if i >= imax:
            break
        truncate = i == imax
    if flag:
        if max(exvals) > 1:
            ax2.plot(avals, tvals, exvals, color='blue', linewidth=1)
    #    ax3.plot([z, z], [0, dtimes[-1]], [0, 0], color='black', linewidth=1)
            avals.append(a)
            exvals.append(0)
            if not truncate:
                tvals.append(tvals[-1])
            else:
                tvals.append(tvals[imax + 1])

            verts = [list(zip(avals, tvals, exvals))]
            art = Poly3DCollection(verts)
            art.set_alpha(0.4)
            art.set_color('grey')
            ax2.add_collection3d(art)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.view_init(20, 134)
ax2.view_init(20, 134)
ax2.set_xlim(0.0, plotmax)
ax2.set_ylim(tmax, 0)

plt.show()

