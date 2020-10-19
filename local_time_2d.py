"""
Plot Brownian motion and surface of local times
"""
import random
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math


npts = 100
ypts = 51
stride = 20
npts1 = (npts - 1) * stride + 1


times = np.linspace(0.0, 2.0, npts)
times1 = np.linspace(0.0, 2.0, npts1)
Xpath = np.zeros(npts1)
Xpath0 = np.zeros(npts)
# seed = 1
# seed = 7
# seed = 20

seed = 1

random.seed(seed)

Wmax = 0.0

for i in range(1, npts1):
    dX = random.gauss(0, 1) * math.sqrt(times1[i] - times1[i-1])
    Xpath[i] = Xpath[i-1] + dX

Xmin = np.amin(Xpath)
Xmax = np.amax(Xpath)
width = Xmax - Xmin
Xmin -= width * 0.05
Xmax += width * 0.05


yvals = np.linspace(Xmin, Xmax, ypts)

X3d = np.ndarray(shape=(npts, ypts))

Z3 = np.ndarray(shape=(npts, ypts))
Z31 = np.ndarray(shape=(npts1, ypts))

for j in range(0, ypts):
    Z3[0, j] = 0.0
    Z31[0, j] = 0.0

for i in range(0, npts):
    for j in range(0, ypts):
        Z3[i, j] = 0.0

for i in range(1, npts1):
    X0 = Xpath[i-1]
    X1 = Xpath[i]
    dt = times1[i] - times1[i-1]
    Z31[i, 0] = Z31[i, ypts - 1] = 0.0
    for j in range(1, ypts-1):
        y0 = 0.5 * (yvals[j-1] + yvals[j])
        y1 = 0.5 * (yvals[j+1] + yvals[j])
        if X0 > X1:
            (X0, X1) = (X1, X0)
        if y0 < X1 and X0 < y1:
            dL = (min(X1, y1) - max(X0, y0)) / (X1 - X0)
            dL *= dt
        else:
            dL = 0.0
        Z31[i, j] = Z31[i-1, j] + dL

zmax = 0.0
for i in range(0, npts):
    Xpath0[i] = Xpath[i * stride]
    for j in range(0, ypts):
        z = Z3[i, j] = Z31[i*stride, j]
        zmax = max(zmax, z)

X3, Y3 = np.meshgrid(yvals, times)


def f(x, y):
    return  x + y

#Z3 = f(X3, Y3)

zline = times * 0 + zmax + 0.02

print(Xmin)
fig = plt.figure()
plt.tight_layout(pad=0)
ax = plt.axes(projection='3d', frame_on='True')
ax.plot_surface(X3, Y3, Z3, cmap='cividis', edgecolor='grey')
ax.plot3D(Xpath0, times, zline, color='black')
#ax.plot_wireframe(X3, Y3, Z3, color='black')
ax.view_init(60, 35)
plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ax.plot(times, Xpath0, label='B', linewidth=1)
#
# ax.spines['left'].set_position('zero')
# ax.spines['right'].set_color('none')
# ax.spines['bottom'].set_position('zero')
# ax.spines['top'].set_color('none')
# ax.set_xticks([])
# ax.set_yticks([])
#
# ax.legend(loc='best')
# ax.margins(0, tight=True)
# plt.show()
