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
    ax2.set_ylim(0, max(drawdownvals) * 1.01)


    #ax.spines['left'].set_position('zero')
    #ax.spines['right'].set_color('none')
    #ax.spines['bottom'].set_position('zero')
    #ax.spines['top'].set_color('none')

    ax.plot(times, xvals, label='$X$')
    ax.plot(times, xmaxvals, label='$M$')

    ax2.plot(times, drawdownvals, linewidth=0.5, color='green', label='$D$')
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper left')
    #plt.show()

fig2 = plt.figure()
ax3 = plt.axes(projection='3d', frame_on='False')
ax3.set_xticks([])
ax3.set_yticks([])
ax3.set_zticks([])
ax3.set_xlabel('$M$', labelpad=-10)
ax3.set_ylabel('$t$', labelpad=-10)
#ax3.set_zlabel('Drawdown', labelpad=-10)

#ax3 = Axes3D(fig)
for row in pointprocess:
    z = -row[0]
    dtimes = row[1]
    zvals = [z for _ in dtimes]
    dvals = row[2]
    ax3.plot(zvals, dtimes, dvals, color='blue', linewidth=1)
    ax3.plot([z, z], [0, dtimes[-1]], [0, 0], color='black', linewidth=1)
    verts = [list(zip(zvals, dtimes, dvals))]
    art = Poly3DCollection(verts)
    art.set_alpha(0.4)
    art.set_color('grey')
    ax3.add_collection3d(art)

plt.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
plt.show()
