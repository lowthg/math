from sympy import symbols, plot_implicit, Eq, plot_parametric
from math import sqrt, pow, fabs
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data
u = np.linspace(0, 2 * np.pi, 30)
v = np.linspace(0, np.pi, 30)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

a = -1.5
b = 2
u = np.linspace(-b * 4, b * 4, 40)
v = np.linspace(-b * 4, b * 4, 40)
z2 = np.outer(np.ones(np.size(u)), np.ones(np.size(u))) * a
y2 = np.outer(u, np.ones(np.size(v)))
x2 = np.outer(np.ones(np.size(u)), v)
u = np.linspace(0, np.pi, 50)
z3 = np.zeros(np.size(u))
x3 = np.sin(u)
y3 = np.cos(u)
z4 = np.zeros(np.size(u))
x4 = -np.sin(u)
y4 = np.cos(u)

#    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))  # aspect ratio is 1:1:1 in data space
ax.set_box_aspect((np.ptp([-1,1]), np.ptp([-1,1]), np.ptp([-1,1])))  # aspect ratio is 1:1:1 in data space
ax.set_xlim(-b, b)
ax.set_ylim(-b, b)
ax.set_zlim(-b, b)
ax.axis('off')
# Plot the surface
ax.plot_wireframe(x2, y2, z2, alpha=0.6, color='grey', zorder=-1)
#ax.plot_wireframe(x, y, z, alpha=1, color='blue', zorder=0, linewidth=0.3)
ax.plot_surface(x, y, z, cmap=cm.Blues, alpha=0.5, shade=True, vmin=-3, vmax=1.5, zorder=0, linewidth=1, color='grey')
#ax.plot_surface(x2, y2, z2, cmap=cm.Blues, alpha=1, shade=True, vmin=-10, vmax=10, zorder=-1)

ax.plot(x3, y3, z3, color='black', alpha=1, linewidth=2)
ax.plot(x4, y4, z4, color='black', alpha=1, linewidth=2)

u = np.linspace(-np.pi, np.pi, 400)
y5 = np.sin(u)
z5 = np.cos(u)
x5 = np.ones(np.size(u))
xx5 = []
yy5 = []
zz5 = []
y6 = np.sin(u)
z6 = np.cos(u)
x6 = np.ones(np.size(u))
xx6 = []
yy6 = []
zz6 = []

for i in range(np.size(u)):
    p = (x5[i]*x5[i] - 0.5 * z5[i] * z5[i])*z5[i]
    y5[i] = pow(fabs(p), 1/    3)
    if p < 0:
        y5[i] = -y5[i]
    r = pow(x5[i]*x5[i] + y5[i]*y5[i] + z5[i]*z5[i], 1/2)
    x5[i] /= r
    y5[i] /= r
    z5[i] /= r

for i in range(np.size(u)):
    r = pow(x6[i]*x6[i] + y6[i]*y6[i] + z6[i]*z6[i], 1/2)
    x6[i] /= r
    y6[i] /= r
    z6[i] /= r

for i in range(np.size(x5)):
    if z5[i] > 0.02:
        u = y5[i]/z5[i] * a
        v = x5[i] / z5[i] * a
        if fabs(u) <= b * 4 and fabs(v) <= b * 4:
            zz5.append(a)
            yy5.append(u)
            xx5.append(v)

for i in range(np.size(x6)):
    if z6[i] > 0.02:
        u = y6[i]/z6[i] * a
        v = x6[i] / z6[i] * a
        if fabs(u) <= b * 4 and fabs(v) <= b * 4:
            zz6.append(a)
            yy6.append(u)
            xx6.append(v)

#ax.plot(x5, y5, z5, color='blue')
#ax.plot(xx5, yy5, zz5, color='blue')
ax.plot(x6, y6, z6, color='blue')
ax.plot(xx6, yy6, zz6, color='blue')
ax.plot([-u for u in x6], y6, z6, color='blue')
ax.plot([-u for u in xx6], yy6, zz6, color='blue')
ax.view_init(20, 0)
plt.subplots_adjust(left=0.0, right=1, bottom=0.0, top=1, hspace=0, wspace=0)
plt.show()
