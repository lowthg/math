"""
accuracy of discrete approximation to continuous barrier
f(x)=xexp(-x)
f'(x)=(1-x)exp(-x)
f''(x)=(x-2)exp(-x)
f(1)=exp(-1)
f''(1)=-exp(-1)
"""

import math
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import matplotlib.animation as animation


def f2(x):
    if x <= -1:
        return 0.
    else:
        return (x+1) * math.exp(-x)

def g2(x):
    return math.exp(-x*x/2)

def scalef2(n):
    return math.sqrt(n)

def f4(x):
    return max(1+x*(1+x/2*(1+x/3)), 0) * math.exp(-x)

def scalef4(n):
    return math.sqrt(math.sqrt(np.longdouble(n)))

def g4(x):
    return math.exp(-x**4/24)

def update(frame):
    plt.clf()

    yvals = [g(x) for x in xvals]
    plt.xlim(xrange[0], xrange[1])
    plt.ylim(0, 1.1)
    plt.yticks([0, 1])
    plt.xticks([xrange[0], 0, xrange[1]])
    plt.plot(xvals, yvals, linewidth=1, color='black', label=gstr)

    n = frame
    a = 1/scalef(n)
    yvals = [f(x) for x in xvals]
    plt.plot(xvals, yvals, linewidth=1, color='blue', label=fstr, alpha=0.5)
    yvals = [math.pow(f(x*a), n) for x in xvals]
    plt.plot(xvals, yvals, linewidth=1, color='blue', label=scalestr, alpha=1)
    plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.99, hspace=0, wspace=0)
    plt.legend(loc='upper left', prop=lprop)
    plt.text(0, 1.05, 'n = {}'.format(n), ha='center', va='center')


style = 0

if style == 2:
    f = f2
    g = g2
    scalef = scalef2
    fstr = '$f(x)=(x+1)^+e^{-x}$'
    scalestr = '$f(x/\\sqrt{n})^n$'
    gstr = '$\\exp(-x^2/2)$'
    xrange = [-3, 3]
    lprop = {}
    frames = list(range(1, 20))
    frames += list(range(20, 40, 2))
    frames += list(range(40, 60, 4))
    frames += list(range(60, 100, 8))
    frames += list(range(100, 150, 10))
    frames += list(range(150, 1000, 20))
elif style == 4:
    f = f4
    g = g4
    scalef = scalef4
    fstr = '$f(x)=(1+x+x^2/2+x^3/6)^+e^{-x}$'
    scalestr = '$f(x/\\,\\sqrt[4]{n})^n$'
    gstr = '$\\exp(-x^4/4!)$'
    xrange = [-5, 5]
    lprop = {'size': 8}
    frames = list(range(1, 20))
    frames += list(range(20, 40, 4))
    frames += list(range(40, 80, 10))
    frames += list(range(80, 150, 15))
    frames += list(range(150, 400, 50))
    frames += list(range(400, 5000, 200))
elif style == 0:
    def f(x):
        y = math.fabs(x)
        if y < 1e-10:
            return 1.0
        else:
            return 1 - math.exp(-1/y*(1+math.sin(2/y)/2))

    def g(x):
        y = math.fabs(x)
        if y <= 1:
            return 1.0
        else:
            return 0.0

    def scalef(n):
        """
        exp(-n*exp(-1/x * (1+sin(1/x)/2)))
        exp(-exp(log(n)-log(n)/x * (2+sin(log(n)/x))))
        """
        return math.log(n)

    fstr = '$f(x)=1-e^{-(1+\\sin(2/|x|)/2)/|x|}$'
    scalestr = '$f(x/\\log(n))^n$'
    gstr = '$I(|x| < 1)$'
    xrange = [-2, 2]
    lprop = {'size': 8}
    frames = list(range(2, 20))
    frames += list(range(20, 70, 5))
    frames += list(range(70, 100, 10))
    frames += list(range(100, 200, 20))
    frames += list(range(200, 1000, 50))
    frames += list(range(1000, 2000, 200))

var = 1  # -f(0)/f''(0)

fig = plt.figure()
ax = fig.add_subplot(111)
npts=401
xvals = np.linspace(xrange[0], xrange[1], npts)


print(len(frames))

ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)

if True:
    animation_file = 'functionpowers.gif'
    ani.save(animation_file, writer='pillow')
else:
    plt.show()