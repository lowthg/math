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

npts = 40
rates1d = -np.log(np.linspace(1/npts, 1, npts)[::-1])
rates1d = np.append(rates1d, np.array([1.35, 2.3, 8]) * rates1d[-1])
rates1dj=np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 3., 4., 6., 10., 40.], 'float')
nptsj = len(rates1dj)
rates1di = rates1d
rates1dk = rates1d
nptsi = len(rates1di)
nptsk = len(rates1dk)
res = [[[None] * nptsk for _ in range(nptsj)] for _ in range(nptsi)]

for i in range(nptsi):
    for j in range(nptsj):
        for k in range(nptsk):
            rates = np.array([rates1di[i], rates1dj[j], rates1dk[k]])
            res[i][j][k] = calc_p1(p0, rates, steps)

fig = mlab.figure(bgcolor=(1,1,1), fgcolor=(0,0,0))
mlab.plot3d([0.0, 1.0], [0.0, 0.0], [0.0, 0.0], color=(0,0,0), tube_radius=0.001)
mlab.plot3d([0., 0.], [0., 1.], [0., 0.], color=(0,0,0), tube_radius=0.001)
mlab.plot3d([0., 0.], [0., 0.], [0., 1.], color=(0,0,0), tube_radius=0.001)
cols = [(0.4, 0.8, 0.4), (0.2, 0.2, 1), Color('orange').rgb, (0.8, 0.2, 0.2), Color('yellow').rgb]

for j in range(nptsj):
    col = cols[j % len(cols)]
    x = np.ndarray([nptsi, nptsk])
    y = x.copy()
    z = x.copy()
    for i in range(nptsi):
        for k in range(nptsk):
            x[i, k] = res[i][j][k][0]
            y[i, k] = res[i][j][k][1]
            z[i, k] = res[i][j][k][2]
    mlab.mesh(x, y, z, color=col, opacity=1.0, representation='mesh', tube_radius=0.001, scale_factor=0.002)


mlab.show()
