"""
Shows drawdown point process for time series
reads the series from a csv file, containing the columns time,low,high,open,close,volume
Only time (unix time) and close e actually used, and must be in increasing time order
"""
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import math

filename = 'C:\\Users\\FiercePC\\Documents\\Workspace\\Temp\\btc.csv'

rows = []

times = []
xvals = []
xmaxvals = []
drawdownvals = []
xmax = 0.0

# array of [a,times,vals]

pointprocess = []

with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dtimes = []
    dvals = []
    t0 = 0
    for row in reader:
        t, x = (int(row[0]), float(row[4]))
        times.append(t)
        xvals.append(x)
        if t0 == 0:
            t0 = t
        dt = t - t0
        if x < xmax:
            drawdown = 1.0 - x / xmax
            dvals.append(drawdown)
            dtimes.append(dt)
        else:
            if len(dtimes) > 1:
                dvals.append(0.0)
                dtimes.append(dt)
                pointprocess.append([xmax,dtimes,dvals])
            dtimes = [0]
            dvals = [0.0]
            t0 = t
            drawdown=0.0
            xmax = x
        xmaxvals.append(xmax)
        drawdownvals.append(drawdown)

print(len(xvals))


if False:
    fig = plt.figure()
    ax = fig.add_subplot(121)

    #ax.spines['left'].set_position('zero')
    #ax.spines['right'].set_color('none')
    #ax.spines['bottom'].set_position('zero')
    #ax.spines['top'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([])

    ax.plot(times, xvals)
    ax.plot(times, xmaxvals)

    ax2 = fig.add_subplot(122)
    ax2.plot(times, drawdownvals)

    #plt.show()

plt.rcParams.update({"text.usetex": True})
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
    z = -math.log(row[0])
    dtimes = [t / 60.0 / 60.0 / 24.0 for t in row[1]]
    zvals = [z for _ in dtimes]
    dvals = [x*100 for x in row[2]]
    ax3.plot(zvals, dtimes, dvals, color='blue', linewidth=1)
    ax3.plot([z, z], [0, dtimes[-1]], [0, 0], color='black', linewidth=1)
    verts = [list(zip(zvals, dtimes, dvals))]
    art = Poly3DCollection(verts)
    art.set_alpha(0.4)
    art.set_color('grey')
    ax3.add_collection3d(art)


plt.show()
