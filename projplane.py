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
z = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
x = np.outer(np.ones(np.size(u)), np.cos(v))

a = -1.5
b = 2
u = np.linspace(-b * 2, b * 2, 20)
v = np.linspace(-b * 2, b * 2, 20)
x2 = np.outer(np.ones(np.size(u)), np.ones(np.size(u))) * a
y2 = np.outer(u, np.ones(np.size(v)))
z2 = np.outer(np.ones(np.size(u)), v)
u = np.linspace(0, np.pi, 50)
x3 = np.zeros(np.size(u))
z3 = np.sin(u)
y3 = np.cos(u)
x4 = np.zeros(np.size(u))
z4 = -np.sin(u)
y4 = np.cos(u)

#    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))  # aspect ratio is 1:1:1 in data space
ax.set_box_aspect((np.ptp([-1,1]), np.ptp([-1,1]), np.ptp([-1,1])))  # aspect ratio is 1:1:1 in data space
ax.set_xlim(-2, 2)
ax.set_ylim(-b, b)
ax.set_zlim(-b, b)
ax.axis('off')
# Plot the surface
ax.plot_wireframe(x2, y2, z2, alpha=0.6, color='grey', zorder=-1)
#ax.plot_wireframe(x, y, z, alpha=1, color='blue', zorder=0, linewidth=0.3)
ax.plot_surface(x, y, z, cmap=cm.Blues, alpha=0.5, shade=True, vmin=-3, vmax=1.5, zorder=0, linewidth=1, color='grey')
#ax.plot_surface(x2, y2, z2, cmap=cm.Blues, alpha=1, shade=True, vmin=-10, vmax=10, zorder=-1)

u1 = (1, 2, 1)
u2 = (1, -2, 1.5)
u3 = (1, 0, 0)
u4 = (1, 1, -1)
p1 = [a/u1[0] * x for x in u1]
r1 = [x / sqrt(u1[0]*u1[0]+u1[1]*u1[1]+u1[2]*u1[2]) for x in u1]
s1 = [-x for x in r1]
q1 = [10 * x for x in u1]
p2 = [a/u2[0] * x for x in u2]
r2 = [-x / sqrt(u2[0]*u2[0]+u2[1]*u2[1]+u2[2]*u2[2]) for x in u2]
s2 = [-x for x in r2]
q2 = [10 * x for x in u2]
p3 = [a/u3[0] * x for x in u3]
r3 = [x / sqrt(u3[0]*u3[0]+u3[1]*u3[1]+u3[2]*u3[2]) for x in u3]
s3 = [-x for x in r3]
q3 = [10 * x for x in u3]
p4 = [a/u4[0] * x for x in u4]
r4 = [-x / sqrt(u4[0]*u4[0]+u4[1]*u4[1]+u4[2]*u4[2]) for x in u4]
s4 = [-x for x in r4]
q4 = [10 * x for x in u4]
ax.plot([p1[0],q1[0]], [p1[1], q1[1]], [p1[2], q1[2]], color='green')
ax.plot([p2[0],q2[0]], [p2[1], q2[1]], [p2[2], q2[2]], color='green')
ax.plot([p3[0],q3[0]], [p3[1], q3[1]], [p3[2], q3[2]], color='green')
ax.plot([p4[0],q4[0]], [p4[1], q4[1]], [p4[2], q4[2]], color='green')
ax.plot(x3, y3, z3, color='black', alpha=1, linewidth=2)
ax.plot(x4, y4, z4, color='black', alpha=0.6, linewidth=2)
ax.scatter([p1[0], p2[0], p3[0], p4[0], r1[0], s2[0], r3[0], r4[0]], [p1[1], p2[1], p3[1], p4[1], r1[1], s2[1], r3[1], r4[1]], [p1[2], p2[2], p3[2], p4[2], r1[2], s2[2], r3[2], r4[2]], alpha=1, color='black')
ax.scatter([s1[0], r2[0], s3[0], s4[0]], [s1[1], r2[1], s3[1], s4[1]], [s1[2], r2[2], s3[2], s4[2]], alpha=0.4, color='black')



u = np.linspace(-np.pi, np.pi, 100)
y5 = np.sin(u)
x5 = np.cos(u)
z5 = np.ones(np.size(u))
for i in range(np.size(u)):
    z5[i] = pow(fabs((y5[i]*y5[i] - 3)*x5[i]), 1/3)
    if (y5[i]*y5[i] - 3)*x5[i] < 0:
        z5[i] = -z5[i]
    r = pow(x5[i]*x5[i] + y5[i]*y5[i] + z5[i]*z5[i], 1/2)
    x5[i] /= r
    y5[i] /= r
    z5[i] /= r
ax.plot(x5, y5, z5, color='green')

plt.show()
