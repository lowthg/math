import matplotlib.pyplot as plt
from sympy import symbols, plot_implicit, Eq, plot_parametric
import sympy

x, y, t = symbols('x y t')
if False:
    p = plot_implicit(Eq(y*y + 3 * x * y - x * x * x + 4 * x, 1), (x, -4.6, 7.8), (y, -6.4, 9.4), adaptive=False,
                      depth=1, points=2000, line_color='grey', show=False, xlabel='$x$', ylabel='$y$')
    p.show()
if False:
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

if False:
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

