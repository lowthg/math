import numpy as np
import numpy.random
import scipy.special
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import pylab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def putPrice(mu, s, x):
    if s < 1-1e-9:
        if s > 1e-9:
            t = max(1/s - 1, 0)
            a = mu * t
            b = (1-mu) * t
            return x * scipy.special.betainc(a, b, x) - mu * scipy.special.betainc(a+1, b, x)
        else:
            return max(x-mu, 0)
    else:
        return x * (1-mu)


def varCond(mu, s, t, x):
    """
    variance of process at time t conditional on equalling x at time s
    """
    dP = putPrice(mu, t, x) - putPrice(mu, s, x)
    u = 0.5 * (s + t)
    v = 1/u - 1
    pdf = scipy.stats.beta(mu*v, (1-mu)*v).pdf(x)
    res = 2 * dP / pdf
#    res = max(min(res, 10), 0)

    return res


def sampleBeta(mu, s, t, x):
    """
    sample beta process at t conditional on being x at s
    """
    var = varCond(mu, s, t, x)
    if var < 1e-9:
        return x
    u = x * (1-x) / var - 1
    return scipy.stats.beta.rvs(x*u, (1-x)*u)


def betaProcess(mu, tVals):
    n = len(tVals)
    xVals = np.zeros(n)
    xVals[0] = mu
    for i in range(1, n):
        xVals[i] = sampleBeta(mu, tVals[i-1], tVals[i], xVals[i-1])

    return xVals

np.random.seed(5)
nt = 100
ns = 200
tVals = np.linspace(0.05, 1, nt)
sVals = np.linspace(1/(ns+1), 1-1/(ns+1), ns)
sValsAll = np.zeros(ns + 2)
sValsAll[1:-1] = sVals
sValsAll[-1] = 1

xVals0 = np.zeros(nt) + 1

if True:
    xVals = np.zeros(ns+2)
    a = 40
    for i in range(1, ns+2):
        xVals[i] = xVals[i-1] + scipy.stats.gamma((sValsAll[i] - sValsAll[i-1])*a).rvs()
    xVals /= xVals[-1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r'$\mu$')
    ax.plot(sValsAll, xVals, linewidth=1, color='black')  # plot bbridge
    plt.show()

if False:
    """vol smile"""
    mu = 0.4
    Z3 = np.ndarray(shape=(ns+2, nt))
    X3, Y3 = np.meshgrid(tVals, sValsAll)
    for i in range(1, nt):
        Z3[0,i] = Z3[ns+1,i] = 0
        for j in range(ns):
            dt = tVals[i] - tVals[i-1]
            var = varCond(mu, tVals[i-1], tVals[i], sVals[j])
            vol = math.sqrt(var/dt)

            Z3[j+1, i] = vol

    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')#, frame_on='True')
    surf = ax2.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5, rstride=2, cstride=2)#, rstride=1, cstride=1) # coolwarm, Reds, summer
    ax2.set_box_aspect((2, 1, 1))
    ax2.set_xlim3d(0, 1)
    ax2.set_ylim3d(0, 1)
    ax2.set_zlim3d(0, 1)
    ax2.set_xlabel(r'$t$')
    ax2.set_ylabel(r'$x$')
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    plt.show()

if False:
    Z3 = np.ndarray(shape=(ns+2, nt))
    X3, Y3 = np.meshgrid(tVals, sValsAll)
    Z3[ns+1] = xVals0

    mu0 = 1.

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r'$t$')
    ax.set_ylabel(r'$\mu$', rotation=0)


    for i in range(ns-1, -1, -1):
        mu = sVals[i]
        tVals1 = tVals / (tVals * (1-mu0) + mu0)
        xVals = betaProcess(mu/mu0, tVals1) * xVals0
        ax.plot(tVals, xVals, linewidth=1, color='black')  # plot bbridge
        Z3[i+1] = xVals
        xVals0 = xVals
        mu0 = mu

    Z3[0] = np.zeros(nt)


    plt.show()

    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')#, frame_on='True')
    surf = ax2.plot_surface(X3, Y3, Z3, cmap=cm.coolwarm, edgecolor='black', linewidth=0.5, rstride=1, cstride=2)#, rstride=1, cstride=1) # coolwarm, Reds, summer
    ax2.set_box_aspect((2, 1, 1))
    ax2.set_xlim3d(0, 1)
    ax2.set_ylim3d(0, 1)
    ax2.set_ylim3d(0, 1)
    ax2.set_xlabel(r'$t$')
    ax2.set_ylabel(r'$\mu$')
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    plt.show()

    print(sampleBeta(0.4, 0.5, 0.51, 0.3))

