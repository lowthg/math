from sympy import symbols, plot_implicit, Eq, plot_parametric
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


x, y, t = symbols('x y t')
if True:
    p = plot_implicit(Eq(y*y + 3 * x * y - x * x * x + 4 * x, 1), (x, -4.6, 7.8), (y, -6.4, 9.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='$x$', ylabel='$y$')
    p.show()
if False:  # circle
    p = plot_implicit(Eq(x*x + y*y, 1), (x, -1.4, 1.4), (y, -1.4, 1.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='', aspect_ratio=(1,1))
    p1 = plot_parametric((1-9*t, 3*t), show=False)
    p.append(p1[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(1.04, 0.04, '$P$', fontsize='large')
    ax.text(-4/5 - 0.06, 3/5 + 0.06, '$Q$', fontsize='large')
    ax.scatter([1, -4/5], [0, 3/5])
    backend.plt.show()

if False:  # hyperbola
    p = plot_implicit(Eq(x*x - y*y, 1), (x, -3, 3), (y, -3, 3), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='', aspect_ratio=(1,1))

    a, b = (-5/4, -3/4)
    u, v = (2, 1)
    t1 = 2 * (a * u - b * v) / (v * v - u * u)
    a1 = a + u * t1
    b1 = b + v * t1
    p1 = plot_parametric((a+u*t, b+v*t), show=False)
    p.append(p1[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(a - 0.14, b + 0.08, '$P$', fontsize='large')
    ax.text(a1 - 0.18, b1 + 0.1, '$Q$', fontsize='large')
    ax.scatter([a, a1], [b, b1])
    ax.plot([-4, 4], [-4, 4], color='grey', linewidth=1, linestyle='dotted')
    ax.plot([-4, 4], [4, -4], color='grey', linewidth=1, linestyle='dotted')
    backend.plt.show()

if False:  # degenerate
    p1 = plot_implicit(Eq(y*y -x * x * (x + 1), 0), (x, -1.2, 1.2), (y, -1.6, 1.6), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p2 = plot_implicit(Eq(y*y -x * x * x, 0), (x, -0.2, 1.5), (y, -1.6, 1.6), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p1.show()
    p2.show()

if False:  # elliptic point from two previous
    p = plot_implicit(Eq(y*y + 3 * x * y - x * x * x + 4 * x, 1), (x, -4.6, 7.8), (y, -6.4, 9.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p1 = plot_parametric((3*t, 3-2*t), show=False)

    def f(t):
        return 3*t, 3-2*t

    p.append(p1[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    p1 = f(-1.158)
    p2 = f(-0.28)
    p3 = f(0.917)
    ax.scatter([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]])
    ax.text(p1[0]-0.4, p1[1]-0.5, '$P$', fontsize='large')
    ax.text(p2[0]+0.1, p2[1]+0.1, '$Q$', fontsize='large')
    ax.text(p3[0]-0.15, p3[1]+0.28, '$R$', fontsize='large')
    backend.plt.show()

if False:  # elliptic point from one previous
    p = plot_implicit(Eq(y*y + 3 * x * y - x * x * x + 4 * x, 1), (x, -4.6, 7.8), (y, -6.4, 9.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p1 = plot_parametric((2*t, 3.745-2.5*t), show=False)

    def f(t):
        return 2*t, 3.745-2.5*t

    p.append(p1[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    p1 = f(-1.158)
    p2 = f(1.22)
    ax.scatter([p1[0], p2[0]], [p1[1], p2[1]])
    ax.text(p1[0]-0.0, p1[1]+0.2, '$P$', fontsize='large')
    ax.text(p2[0]-0.15, p2[1]+0.28, '$Q$', fontsize='large')
    backend.plt.show()

if False:  # constructing points
    p = plot_implicit(Eq(y*y - x * x * x, 3), (x, -1.8, 2), (y, -3.3, 3.3), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p1 = plot_parametric((1 + t, 2 + 3/4 * t), show=False)
    p2 = plot_parametric((1 + t, -2 -139/156 * t), show=False)
    p.append(p1[0])
    p.append(p2[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    p1 = (1, 2)
    p2 = (-23/16, 11/64)
    p3 = (1, -2)
    p4 = (1873/1521, -130870/59319)
    ax.scatter([p1[0], p2[0], p3[0], p4[0]], [p1[1], p2[1], p3[1], p4[1]])
    ax.text(p1[0]-0.05, p1[1]+0.1, '$P$', fontsize='large')
    ax.text(p2[0]-0.10, p2[1]+0.16, '$Q$', fontsize='large')
    ax.text(p3[0]-0.02, p3[1]+0.1, '$P^\prime$', fontsize='large')
    ax.text(p4[0]-0.02, p4[1]+0.1, '$R$', fontsize='large')
    backend.plt.show()

if False:  # hyperbola intersections
    p = plot_implicit(Eq(x*x - y*y, 1), (x, -3, 3), (y, -3, 3), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='', aspect_ratio=(1,1))

    a, b = (-5/4, -3/4)
    u, v = (2, 1)
    t1 = 2 * (a * u - b * v) / (v * v - u * u)
    a1 = a + u * t1
    b1 = b + v * t1
    c1 = 1.3
    yc = (c1 * c1 - 1) / (2 * c1)
    xc = yc - c1
    p1 = plot_parametric((a+u*t, b+v*t), show=False)
    p2 = plot_parametric((t, t + c1), show=False)
    p.append(p1[0])
    p.append(p2[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    ax.scatter([a, a1, xc], [b, b1, yc])
    ax.plot([-4, 4], [-4, 4], color='grey', linewidth=1, linestyle='dotted')
    ax.plot([-4, 4], [4, -4], color='grey', linewidth=1, linestyle='dotted')
    backend.plt.show()

if False:  # elliptic intersections
    p = plot_implicit(Eq(y*y - x * x * x, 3), (x, -1.8, 2.5), (y, -4.4, 4.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='')
    p1 = plot_parametric((t, 1.5 + 3/4 * t), show=False)
    x4 = 0.9
    p2 = plot_parametric((x4, t), show=False)
    p.append(p1[0])
    p.append(p2[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    x1 = -1.415
    x2 = 0.34
    x3 = 1.65
    y1 = 3/4 * x1 + 1.5
    y2 = 3/4 * x2 + 1.5
    y3 = 3/4 * x3 + 1.5
    y4 = sqrt(x4*x4*x4 + 3)
    ax.scatter([x1, x2, x3, x4, x4], [y1, y2, y3, y4, -y4])
    backend.plt.show()

if False:  # circle
    p = plot_implicit(Eq(x*x + y*y, 1), (x, -3, 5), (y, -1.4, 1.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='', ylabel='', aspect_ratio=(1,1))
    u1 = 2
    u2 = 0.5
    u3 = -0.8
    u4 = -0.3
    a = -1
    p0 = plot_parametric((t, a), line_color='grey', show=False)
    p1 = plot_parametric((u1*t, 1-t), show=False)
    p2 = plot_parametric((u2*t, 1-t), show=False)
    p3 = plot_parametric((u3*t, 1-t), show=False)
    p4 = plot_parametric((u4*t, 1-t), show=False)
    p5 = plot_parametric((t, 1), show=False)
    p.append(p0[0])
    p.append(p1[0])
    p.append(p2[0])
    p.append(p3[0])
    p.append(p4[0])
    p.append(p5[0])
    backend = p.backend(p)
    backend.process_series()
    backend.fig.tight_layout()
    ax = backend.ax[0]
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.text(4.75, 1.02, '$\infty$', fontsize=15)
    ax.text(2.3, a + 0.03, '$F$', fontsize=13)
    ax.text(-0.2, 1.02, '$P$', fontsize=13)
#    ax.text(-4/5 - 0.06, 3/5 + 0.06, '$Q$', fontsize=40)
    x1 = 2 * u1 / (u1*u1 + 1)
    y1 = (u1*u1 - 1) / (u1*u1 + 1)
    z1 = (1-a) * u1
    x2 = 2 * u2 / (u2*u2 + 1)
    y2 = (u2*u2 - 1) / (u2*u2 + 1)
    z2 = (1-a) * u2
    x3 = 2 * u3 / (u3*u3 + 1)
    y3 = (u3*u3 - 1) / (u3*u3 + 1)
    z3 = (1-a) * u3
    x4 = 2 * u4 / (u4*u4 + 1)
    y4 = (u4*u4 - 1) / (u4*u4 + 1)
    z4 = (1-a) * u4
    ax.scatter([0, x1, z1, x2, z2, x3, z3, x4, z4], [1, y1, a, y2, a, y3, a, y4, a])
    backend.plt.show()

if False:  # sphere projection
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
    u = np.linspace(-b * 2, b * 2, 20)
    v = np.linspace(-b * 2, b * 2, 20)
    x2 = np.outer(np.ones(np.size(u)), np.ones(np.size(u))) * a
    y2 = np.outer(u, np.ones(np.size(v)))
    z2 = np.outer(np.ones(np.size(u)), v)


#    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))  # aspect ratio is 1:1:1 in data space
    ax.set_box_aspect((np.ptp([-1,1]), np.ptp([-1,1]), np.ptp([-1,1])))  # aspect ratio is 1:1:1 in data space
    # Plot the surface
    ax.plot_surface(x, y, z, cmap=cm.Greys, alpha=0.8, shade=True, vmin=-3, vmax=1.5, zorder=2)
    ax.plot_surface(x2, y2, z2, cmap=cm.Blues, alpha=1, shade=True, vmin=-10, vmax=10, zorder=1)
#    ax.plot_wireframe(x, y, z, alpha=0.6, color='black')
    p1 = [x*10 for x in (1, 2, 1)]
    ax.plot([-p1[0],p1[0]], [-p1[1], p1[1]], [-p1[2], p1[2]], color='blue')
    ax.scatter([0], [0], [0], alpha=1, color='black')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-b, b)
    ax.set_zlim(-b, b)
    ax.axis('off')
    plt.show()

#p2 = plot(x+1, line_color='blue', show=False)
#p.append(p2[0])
#print(p)
#backend = p.backend(p)
#backend.process_series()
#backend.fig.tight_layout()
#ax = backend.ax[0]
#backend.plt.show()
#plot_implicit(Eq(y*y -x*x*x - x*x, 0), (x, -2, 5), adaptive=False, depth=1, points=1000, line_color='grey')
#backend.show()

