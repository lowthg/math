import matplotlib.pyplot as plt
import numpy as np
import math

plotnum = 4
a = 3
if plotnum == 4:
    ymax = 6
else:
    ymax = 8
ymin = -ymax

def getx(y):
    x3 = y*y - a
    x = math.pow(math.fabs(x3), 1/3)
    if x3 < 0:
        x = -x
    return x

def combine(p, q):
    gamma = (q[1] - p[1]) / (q[0] - p[0])
    x = gamma * gamma - p[0] - q[0]
    y = p[1] + gamma * (x - p[0])
    return x, y

def plotline(p, q, xmin, xmax, ax):
    gamma = (q[1] - p[1]) / (q[0] - p[0])
    y0 = p[1] + gamma * (xmin - p[0])
    y1 = p[1] + gamma * (xmax - p[0])
    ax.plot([xmin, xmax], [y0, y1], color='orange', zorder=-1)

yvals = np.linspace(-ymax, ymax, 200)
xvals = np.zeros(np.size(yvals))
for i in range(np.size(yvals)):
    xvals[i] = getx(yvals[i])
xmax = max(xvals)
xmin = min(xvals) - 0.2

if plotnum == 1:
    yP = 0.4
    yQ = 1.8
    yR = -1.2
elif plotnum == 2:
    yP = 0.7
    yQ = 1.65
    yR = -4
elif plotnum == 3:
    yP = 0.2
    yQ = 1.75
    yR = -1.0
elif plotnum == 4:
    yP = -1
    yQ = 1.8
    yR = -1.0
else:
    yP = yQ = yR = 0

P = (getx(yP), yP)
Q = (getx(yQ), yQ)
R = (getx(yR), yR)
PQ = combine(P, Q)
PaQ = (PQ[0], -PQ[1])
QR = combine(Q, R)
QaR = (QR[0], -QR[1])
PQR = combine(PaQ, R)
mPQR = (PQR[0], -PQR[1])
PQRa = (PQR[0], -PQR[1])
mP = (P[0], -P[1])
mR = (R[0], -R[1])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(xvals, yvals)

ax.text(P[0] + 0.02, P[1] + 0.2, '$P$', ha='right')
ax.text(Q[0], Q[1] + 0.24, '$Q$', ha='center')
ax.scatter([P[0], Q[0], PQ[0]], [P[1], Q[1], PQ[1]], color='tab:blue')
plotline(P, Q, xmin, xmax, ax)
ax.text(PQ[0] - 0.02, PQ[1] + 0.1, '$P\circ Q$', ha='right')

if plotnum < 4:
    ax.text(R[0], R[1]+0.2, '$R$', ha='center')
    ax.text(QR[0]-0.03, QR[1]+0.15, '$Q\circ R$', ha='right')
    ax.scatter([R[0], QR[0]], [R[1], QR[1]], color='tab:blue')
    plotline(Q, R, xmin, xmax, ax)

if plotnum == 1:
    ax.scatter([PaQ[0], QaR[0], PQRa[0]], [PaQ[1], QaR[1], PQRa[1]], color='tab:blue')
    ax.scatter([PQR[0]], [PQR[1]], color='tab:green')
    ax.text(PaQ[0], PaQ[1], '$P+Q$')
    ax.text(QaR[0], QaR[1], '$Q+R$')
    ax.text(PQRa[0], PQRa[1], '$P+Q+R$', ha='right')
    plotline(P, QaR, xmin, xmax, ax)
    plotline(R, PaQ, xmin, xmax, ax)
    ax.plot([PQ[0], PQ[0]], [ymin, ymax], color='orange', zorder=-1)
    ax.plot([QR[0], QR[0]], [ymin, ymax], color='orange', zorder=-1)
    ax.plot([PQR[0], PQR[0]], [ymin, ymax], color='orange', zorder=-1)
if plotnum == 2:
    ax.scatter([mP[0], mR[0]], [mP[1], mR[1]], color='tab:blue')
    ax.scatter([mPQR[0]], [mPQR[1]], color='tab:green')
    ax.plot([P[0], P[0]], [ymin, ymax], color='orange', zorder=-1)
    ax.plot([R[0], R[0]], [ymin, ymax], color='orange', zorder=-1)
    plotline(PQ, mR, xmin, xmax, ax)
    plotline(QR, mP, xmin, xmax, ax)
    ax.text(mP[0]-0.04, mP[1]-0.4, '$-P$', ha='right')
    ax.text(mR[0]-0.04, mR[1], '$-R$', ha='right')
if plotnum == 3:
    ax.scatter([PaQ[0], QaR[0]], [PaQ[1], QaR[1]], color='tab:blue')
    ax.scatter([PQR[0]], [PQR[1]], color='tab:green')
    ax.plot([PQ[0], PQ[0]], [ymin, ymax], color='orange', zorder=-1)
    ax.plot([QR[0], QR[0]], [ymin, ymax], color='orange', zorder=-1)
    plotline(PaQ, R, xmin, xmax, ax)
    plotline(QaR, P, xmin, xmax, ax)
    ax.text(PaQ[0]+0.03, PaQ[1]+0.2, '$P+Q$', ha='left')
    ax.text(QaR[0]-0.04, QaR[1]-0.4, '$Q+R$', ha='right')
if plotnum == 4:
    ax.scatter([PaQ[0]], [PaQ[1]], color='tab:blue')
    ax.plot([PQ[0], PQ[0]], [ymin, ymax], color='orange', zorder=-1)
    ax.text(PaQ[0]+0.03, PaQ[1]+0.2, '$P+Q$', ha='left')


ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.axis('off')
plt.subplots_adjust(left=0.0, right=1, bottom=0.0, top=1, hspace=0, wspace=0)
plt.show()

