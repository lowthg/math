import random
import numpy as np
import math
from scipy import linalg
from colour import Color
from mayavi import mlab

def calc_p1(p0, rates, steps):
    M = np.diag(-rates * (steps[:-1] + steps[1:])) + np.diag(rates[1:] * steps[1:-1], 1) + np.diag(rates[:-1] * steps[1:-1], -1)
    return np.matmul(linalg.expm(M), p0)


p0 = np.array([1, 0, 1], 'float')
p0 /= sum(p0)
steps = np.array([1, 0.5, 1, 1], 'float')
n = 3

npts = 40
rates1d = -np.log(np.linspace(1/npts, 1, npts)[::-1])
rates1d = np.append(rates1d, np.array([1.35, 2.3, 8]) * rates1d[-1])
rates1di = rates1d
rates1dj = rates1d
rates1dk = rates1d
nptsi = len(rates1di)
nptsj = len(rates1dj)
nptsk = len(rates1dk)
res = [[[None] * nptsk for _ in range(nptsj)] for _ in range(nptsi)]

for i in range(nptsi):
    for j in range(nptsj):
        for k in range(nptsk):
            rates = np.array([rates1di[i], rates1dj[j], rates1dk[k]])
            res[i][j][k] = calc_p1(p0, rates, steps)

dets = [[[None] * (nptsk-1) for _ in range(nptsj-1)] for _ in range(nptsi-1)]
x = [[[None] * (nptsk-1) for _ in range(nptsj-1)] for _ in range(nptsi-1)]
y = [[[None] * (nptsk-1) for _ in range(nptsj-1)] for _ in range(nptsi-1)]
z = [[[None] * (nptsk-1) for _ in range(nptsj-1)] for _ in range(nptsi-1)]

J = np.matrix(np.ndarray([n, n], 'float'))
for i in range(nptsi-1):
    for j in range(nptsj-1):
        for k in range(nptsk-1):
            for l in range(3):
                J[0,l] = res[i][j][k][l] - res[i+1][j][k][l]
                J[1,l] = res[i][j][k][l] - res[i][j+1][k][l]
                J[2,l] = res[i][j][k][l] - res[i][j][k+1][l]
            dets[i][j][k] = linalg.det(J)
            x[i][j][k] = 0.5 * (rates1di[i] + rates1di[i+1])
            y[i][j][k] = 0.5 * (rates1dj[j] + rates1dj[j+1])
            z[i][j][k] = 0.5 * (rates1dk[k] + rates1dk[k+1])





fig = mlab.figure(bgcolor=(1,1,1), fgcolor=(0,0,0))
mlab.plot3d([0.0, 1.0], [0.0, 0.0], [0.0, 0.0], color=(0,0,0), tube_radius=0.001)
mlab.plot3d([0., 0.], [0., 1.], [0., 0.], color=(0,0,0), tube_radius=0.001)
mlab.plot3d([0., 0.], [0., 0.], [0., 1.], color=(0,0,0), tube_radius=0.001)

mlab.contour3d(x, y, z, dets, contours=[0.1e-6])


mlab.show()
