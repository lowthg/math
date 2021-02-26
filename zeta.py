"""
plot riemann zeta
"""

import random
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from math import exp, pi, sqrt
import pylab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpmath import zeta, mp
mp.dps = 6

xmin = 0.65
xmax = 0.85

ymin = 500
yrange = 10
ymax = ymin + yrange
nx = 101
ny = 103

xvals = np.linspace(xmin, xmax, nx)
yvals = np.linspace(ymin, ymax, ny)
Z3 = np.ndarray(shape=(nx, ny))
Y3, X3 = np.meshgrid(yvals, xvals)

print(X3.shape)
print(Y3.shape)
print(Z3.shape)
print(X3)

for i in range(0, nx):
    for j in range(0, ny):
        z = zeta(xvals[i] + yvals[j] * 1j)
        Z3[i, j] = float(z.real)

fig = plt.figure()
ax = plt.axes(projection='3d', frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5) # coolwarm, Reds, summer
#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue')
ax.set_yticks([ymin, ymax])
ax.set_xticks([xmin, xmax])
#ax.set_ylim(xmin, xmax)
ax.set_xlabel('x', labelpad=-10)
ax.set_ylabel('y', labelpad=-10)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.view_init(30, -56)
plt.show()
