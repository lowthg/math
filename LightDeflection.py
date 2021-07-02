"""
Shows the paths of light travelling through medium of variable refractive index
"""

import numpy as np
import math
import matplotlib.pyplot as plt


def rho(x):
    """
    The refractive index as a function of x
    """
    r = math.sqrt(x[0] * x[0] + x[1] * x[1])
    u = max(1.0 - 1.0 / r, 1e-5)
    return math.pow(2.0 - u, 3) / u


def rho1d(r):
    u = max(1.0 - 1.0 / r, 1e-5)
    return math.pow(2.0 - u, 3) / u



def inrange_func(xmin, xmax, ymin, ymax):
    """
    0 => still in range of plot
    1 => outside of plot range
    2 => absorbed by event horizon
    """
    def f(x):
        if not (xmin <= x[0] <= xmax and ymin <= x[1] <= ymax):
            return 1
        if x[0] * x[0] + x[1] * x[1] <= 1.0:
            return 2
        return 0
    return f


def eulerstep(x, v, dt, rho):
    """
    x = position, v = xdot / |xdot|
    Lagrangian is r | xdot |
    Invariance under time changes, we normalize so that xdot = v, giving
    dv/dt = a - a.v v, where a = grad(rho)/rho
    or, v(t+dt) = R_{w.a dt} v, where R is rotation matrix and w is orthogonal unit vector to v
    """
    v /= math.sqrt(v[0] * v[0] + v[1] * v[1])
    x0 = x + v * dt * 0.5
    w = np.array([v[1], -v[0]])  # orthogonal basis v,w
    a = (rho(x0 + w * 0.5 * dt) - rho(x0 - w * 0.5 * dt)) / rho(x0)  # w.grad(rho)/rho dt
    c = math.cos(a)
    s = math.sin(a)
    v1 = v * c + w * s
    return x + (v + v1) * dt * 0.5, v1


def computepath(x, v, dt, r, inrange, maxlength):
    pathx = []
    pathy = []
    t = 0.0
    end = -1
    while t < maxlength:
        pathx.append(x[0])
        pathy.append(x[1])
        x, v = eulerstep(x, v, dt, r)
        t += dt
        assert t < maxlength
        end = inrange(x)
        if end != 0:
            break
        pathx.append(x[0])
        pathy.append(x[1])
    return pathx, pathy, end


xmax = 45
xmin = -600.0
ymin = -30
ymax = 30
plotrangey = 30
plotrangex = 45
inrange = inrange_func(xmin, xmax, ymin, ymax)

starts = [0, -2.5, -5, -7.5, -10, -10.4, -12.5, -15, -17.5, -20, -22.5, -25, -27.5, -30]

maxlength = (xmax - xmin) * 10
dt = 0.02
paths = []

r1 = 1 / (2 - math.sqrt(3))

maxr = rho([r1, 0])
print('Max refractive index: ', maxr)
print('Apparent radius: ', maxr * r1)
print('Photon sphere: ', r1)

print("Show light paths? [y/n]")
if input().lower()[0] == 'y':
    for start in starts:
        x = np.array([xmin, start])
        v = np.array([1.0, 0])
        paths.append(computepath(x, v, dt, rho, inrange, maxlength))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    circle1 = plt.Circle((0, 0), 1, color='black', fill=True)  # event horizon
    circle2 = plt.Circle((0, 0), r1, color='black', fill=False, linewidth=2)  # photon sphere
    circle3 = plt.Circle((0, 0), maxr * r1, color='black', fill=False, linewidth=1)  # apparent size
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)
    for (pathx, pathy, end) in paths:
        if end == 1:
            color = 'blue'  # not absorbed
        else:
            color = 'red'
        ax.plot(pathx, pathy, linewidth=1, color=color)
        if math.fabs(pathy[0]) > 0.01:
            ax.plot(pathx, [-y for y in pathy], linewidth=1, color=color)
    ax.set_xlim(-plotrangex, plotrangex)
    ax.set_ylim(-plotrangey, plotrangey)
    ax.set_aspect(1)
    #plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    plt.show()
else:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel('$n(r)$')
    plt.xlabel('$r$')
    xvals = np.linspace(r1, 60.0, 100)
    yvals = [rho1d(r) for r in xvals]
    ax.plot(xvals, yvals)
    ax.set_xlim(xvals[0], xvals[-1])
    ax.set_ylim(1, yvals[0])
#    ax2 = fig.add_subplot(212)
#    xvals2 = np.linspace(1.001, 20.0, 100)
#    yvals2 = [rho1d(r) * r for r in xvals2]
#    ax2.plot(xvals2, yvals2)
#    ax2.set_xlim(1, xvals2[-1])
#    ax2.set_ylim(10, yvals2[-1])
#    plt.ylabel('$n(r)r$')
#    plt.xlabel('$r$')
    plt.rcParams.update({"text.usetex": True})

    plt.grid()
    plt.show()
