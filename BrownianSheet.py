"""
Plots a Brownian sheet
"""

import random
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math

xpts = 100
ypts = 100
seed = 52

random.seed(seed)
xvals = np.linspace(0.0, 1.0, xpts)
yvals = np.linspace(0.0, 1.0, ypts)
Z3 = np.ndarray(shape=(xpts, ypts))

sigma = math.sqrt((xvals[1] - xvals[0])*(yvals[1]-yvals[0]))

X3, Y3 = np.meshgrid(yvals, xvals)

for j in range(0, ypts):
    Z3[0, j] = 0.0

minz = 0.0
maxz = 0.0
for i in range(1, xpts):
    Z3[i, 0] = 0.0
    for j in range(1, ypts):
        Z3[i, j] = Z3[i-1, j] + Z3[i, j-1] - Z3[i-1, j-1] + random.gauss(0.0, sigma)
        minz = min(minz, Z3[i, j])
        maxz = max(maxz, Z3[i, j])

print(minz)
print(maxz)

fig = plt.figure()
ax = plt.axes(projection='3d', frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5)
ax.set_xlim(0.0, 0.99)
ax.set_ylim(0.01, 1)
ax.set_zlim(-0.6, 0.9)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])


#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue')
ax.view_init(46, -36)
plt.show()

