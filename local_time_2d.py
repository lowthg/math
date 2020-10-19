"""
Plot Brownian motion and surface of local times
"""
import random
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math


npts = 400
ypts = 81
stride = 20
npts1 = (npts - 1) * stride + 1


times = np.linspace(0.0, 2.0, npts)
times1 = np.linspace(0.0, 2.0, npts1)
Xpath = np.zeros(npts1)
Xpath0 = np.zeros(npts)
# seed = 1
# seed = 7
# seed = 20

seed = 2
seed = 8
seed = 14

random.seed(seed)

Wmax = 0.0

for i in range(1, npts1):
    dX = random.gauss(0, math.sqrt(times1[i] - times1[i-1]))
    Xpath[i] = Xpath[i-1] + dX

Xmin = np.amin(Xpath)
Xmax = np.amax(Xpath)
width = Xmax - Xmin
#Xmin -= width * 0.05
#Xmax += width * 0.05


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
    if X0 > X1:
        (X0, X1) = (X1, X0)
    dt = times1[i] - times1[i-1]
    Z31[i, 0] = Z31[i, ypts - 1] = 0.0
    for j in range(1, ypts-1):
        y0 = 0.5 * (yvals[j-1] + yvals[j])
        y1 = 0.5 * (yvals[j+1] + yvals[j])
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

zline = times * 0 + zmax

x_scale=1.5
y_scale=1
z_scale=1

scale=np.diag([x_scale, y_scale, z_scale, 1.0])
scale=scale*(1.0/scale.max())
scale[3,3]=1.0

def short_proj():
  return np.dot(Axes3D.get_proj(ax), scale)

print(Xmin)
fig = plt.figure()
fig.subplots_adjust(top=1, bottom=0, left=0, right=1, wspace=0.1, hspace=0.1)
plt.tight_layout(pad=0)
plt.rcParams.update({"text.usetex": True})
ax = plt.axes(projection='3d', frame_on='True')
ax.get_proj=short_proj
ax.pbaspect = np.array([1,20,1])
ax.plot_surface(X3, Y3, Z3, cmap=cm.Reds, edgecolor='black', linewidth=0.1, zorder=-10)
ax.plot3D(Xpath0, times, zline, color='black', linewidth=0.7, zorder=20)
#ax.plot3D([0, 0], [0, times[-1]], [zline[0], zline[0]], color='grey', alpha=0.5, zorder=20)
ax.view_init(35, -74)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.set_xlabel('$x$', labelpad=-10)
ax.set_ylabel('$t$', labelpad=-10)
ax.set_zlabel('$L^x_t$', labelpad=-10, rotation=0)
ax.zaxis.set_rotate_label(False)
#ax.set_xlim(Xmin + width, Xmax - width)

# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ax.plot(times, Xpath0, label='B', linewidth=1)
#
# ax.spines['left'].set_position('zero')
# ax.spines['right'].set_color('none')
# ax.spines['bottom'].set_position('zero')
#ax.spines['top'].set_color('none')
# ax.set_xticks([])
# ax.set_yticks([])
#
# ax.legend(loc='best')
ax.margins(0, tight=True)

plt.show()
# plt.show()
