"""
Plots a 2d normal
"""

import random
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from math import exp, pi, sqrt
import pylab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

xmax = 4.0
xpts = 101

xvals = np.linspace(-xmax, xmax, xpts)
Z3 = np.ndarray(shape=(xpts, xpts))
X3, Y3 = np.meshgrid(xvals, xvals)

c = 1.0 / sqrt(pi * 2)

for i in range(0, xpts):
    for j in range(0, xpts):
        r = xvals[i] * xvals[i] + xvals[j] * xvals[j]
        phi = exp(-r * 0.5) * c
        Z3[i, j] = phi

fig = plt.figure()
ax = plt.axes(projection='3d', frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5) # coolwarm, Reds, summer
#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zlim(0)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.99, hspace=0, wspace=0)
ax.view_init(20, 134)
plt.show()

