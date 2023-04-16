"""
Shows drawdown point process for time series
reads the series from a csv file, containing the columns time,low,high,open,close,volume
Only time (unix time) and close e actually used, and must be in increasing time order
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
import random

ntimes = 10000
random.seed(3)

rows = []
times = [0.0]
xvals = [0.0]
xmaxvals = [0.0]
drawdownvals = [0.0]
xmax = 0.0

# array of [a,times,vals]

pointprocess = []

dtimes = []
dvals = []
t0 = 0

for itime in range(1, ntimes):
    t = itime
    x = xvals[itime - 1] + random.gauss(0, 1)
    times.append(t)
    xvals.append(x)
    if t0 == 0:
        t0 = t
    dt = t - t0
    if x < xmax:
        drawdown = xmax - x
        dvals.append(drawdown)
        dtimes.append(dt)
    else:
        if len(dtimes) > 1:
            dvals.append(0.0)
            dtimes.append(dt)
            pointprocess.append([xmax, dtimes, dvals])
        dtimes = [0]
        dvals = [0.0]
        t0 = t
        drawdown=0.0
        xmax = x
    xmaxvals.append(xmax)
    drawdownvals.append(drawdown)

print(len(xvals))
maxt = times[-1]

plt.rcParams.update({"text.usetex": True})

if True:
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xticks([])
    ax.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax.set_xlim(0, maxt)
    ax2.set_xlim(0, maxt)
    ax2.set_ylim(0, max(drawdownvals) * 1.1)


    #ax.spines['left'].set_position('zero')
    #ax.spines['right'].set_color('none')
    #ax.spines['bottom'].set_position('zero')
    #ax.spines['top'].set_color('none')

    ax.plot(times, xvals, label='$X$')
    ax.plot(times, xmaxvals, label='$X^*$')

    ax2.plot(times, [abs(x) for x in xvals], linewidth=0.8, color='blue', label='$\\vert X\\vert$', alpha=0.7)
    ax2.plot(times, drawdownvals, linewidth=1, color='green', label='$X^*-X$')
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper left')
    plt.show()
