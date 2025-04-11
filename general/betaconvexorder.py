import numpy as np
import scipy.special
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import pylab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def putPrice(mean, c, x):
    if c > 1e-10:
        a = mean * c
        b = c - a
        return x * scipy.special.betainc(a, b, x) - mean * scipy.special.betainc(a+1, b, x)
    else:
        return x * (1-mean)


def var(mean, c, x, dt):
    dPdt = (putPrice(mean, c, x) - putPrice(mean, c + dt, x)) / dt
    c1 = c + dt/2
    a = mean * c1
    b = c1 - a
    dens = math.pow(x, a-1) * math.pow(1-x, b-1) / scipy.special.beta(a, b)
    return 2 * dPdt / dens


smax = 6.
smin = 1
ns = 200
nx = 300
dx = 1 / (nx+1)
mean = 0.2

svals = np.linspace(smin, smax, ns)
xvals = np.linspace(dx, 1-dx, nx)
ds = svals[1] - svals[0]

Z3 = np.ndarray(shape=(ns, nx))
X3, Y3 = np.meshgrid(xvals, svals)

for i in range(nx):
    for j in range(ns):
        Z3[j, i] = (putPrice(mean, svals[j], xvals[i]) - putPrice(mean, svals[j]+ds, xvals[i]))/ds
#        Z3[j, i] = (putPrice(mean, svals[j], xvals[i]-dx) + putPrice(mean, svals[j], xvals[i]+dx) - 2*putPrice(mean, svals[j], xvals[i]))/dx/dx
#        Z3[j, i] = var(mean, svals[j], xvals[i], ds) * math.pow(0.05+svals[j], 1.7)

print(mean)
fig = plt.figure()
ax = plt.axes(projection='3d')#, frame_on='True')
surf = ax.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5)#, rstride=1, cstride=1) # coolwarm, Reds, summer
#ax.plot_wireframe(X3, Y3, Z3, cmap='cividis', edgecolor='blue', cstride=1)
ax.set_xlim(0.0, 1.)
ax.set_ylim(smin, smax)
ax.set_title('mean = {}'.format(mean))
ax.set_ylabel('s')
ax.set_xlabel('x')

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.97, hspace=0, wspace=0)
ax.view_init(15, 70)

plt.show()
