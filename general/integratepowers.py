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


def f(x):
    if x <= -1:
        return 0.
    else:
        return (x+1) * math.exp(-x)


def update(frame):
    plt.clf()

    yvals = [math.exp(-x * x / 2 / var) for x in xvals]
    plt.xlim(-xrange, xrange)
    plt.ylim(0, 1.1)
    plt.yticks([0, 1])
    plt.xticks([-xrange, 0, xrange])
    plt.plot(xvals, yvals, linewidth=1, color='black', label='$\\exp(-x^2/2)$')

    n = frame
    a = 1/math.sqrt(n)
    yvals = [f(x)/c for x in xvals]
    plt.plot(xvals, yvals, linewidth=1, color='blue', label='$f(x)=(x+1)^+e^{-x}$', alpha=0.5)
    yvals = [math.pow(f(x*a)/c, n) for x in xvals]
    plt.plot(xvals, yvals, linewidth=1, color='blue', label='$f(x/\\sqrt{n})^n$', alpha=1)
    plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.99, hspace=0, wspace=0)
    plt.legend(loc='upper right')
    plt.text(0, 1.05, 'n = {}'.format(n), ha='center', va='center')


c = f(0)
var = 1  # -f(0)/f''(0)

fig = plt.figure()
ax = fig.add_subplot(111)
xrange=3
npts=401
xvals = np.linspace(-xrange, xrange, npts)

frames = list(range(1, 20))
frames += list(range(20, 40, 2))
frames += list(range(40, 60, 4))
frames += list(range(60, 100, 8))
frames += list(range(100, 150, 10))
frames += list(range(150, 1000, 20))

print(len(frames))

ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)

if False:
    animation_file = 'functionpowers.gif'
    ani.save(animation_file, writer='pillow')
else:
    plt.show()