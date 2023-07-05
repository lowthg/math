"""
Computes c = c(p) chosen such that discrete barrier condition
pX(t)+(1-p)X(s) + x |X(t) - X(s)| >= K
has zero expected overshoot
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.interpolate as interp


pdf = stats.norm.pdf
cdf = stats.norm.cdf


def discrete_adj( npts, dx, p, c):
    """
    (X_{t-1},X_t) = (x,y)
    p * y + (1-p) * x + c |y-x|
    for y > x, assume p + c > 1
        p*y + (1-p)*x + c*(y-x) > 0
        (p+c) * (y-x) + x > 0
        y > -(p+c-1)*x/(p+c)
    for y < x, for p < c
        p*y + (1-p)*x - c*(y-x) > 0
        (p-c)*y + (1-p+c)*x > 0
        y < (1 + 1/(c-p))*x
    """
    v = np.zeros(npts + 1)
    m = np.matrix(np.zeros(shape=[npts + 1, npts + 1]))
    cdfvec = np.zeros(npts*2 + 2)
    for i in range(len(cdfvec)):
        cdfvec[i] = cdf((i - npts - 0.5)*dx)

    assert p + c >= 1
    a = 1 - 1/(p+c)
    if c > p + 0.0001:
        b = 1 + 1/(c-p)
    else:
        b = 0

    for i in range(npts + 1):
        low = a * i * dx
        i0 = int(math.ceil(low/dx))
        assert i0 <= i
        k = i*dx - low
        v[i] = pdf(k) - i*dx*cdf(-k)
        m[i, i0] = cdf(k) - cdf((i-i0-0.5)*dx)
        if b > 0:
            high = b*i*dx
            i1 = min(int(math.floor(high/dx)), npts)
            assert i1 >= i
            k1 = high - i*dx
            v[i] += -(pdf(k1) + i*dx*cdf(-k1))
            if i1 > i0:
                m[i, i1] = cdf((i - i1 + 0.5)*dx) - cdf(i*dx - high)
            else:
                m[i, i1] = cdf(k) - cdf(-k1)
        else:
            i1 = npts
            assert i1 > i0
            m[i, i1] = cdf((i - i1 + 0.5)*dx)

        for j in range(i0 + 1, i1):
            m[i, j] = cdfvec[i - j + 1 + npts] - cdfvec[i - j + npts]

    return m, v


width = 8
npts = 1000
dx = width/npts

p0 = 0.7311253

vals = [
    0.5,    0.87290,
    0.51,   0.87261,
    0.52,   0.87173,
    0.53,   0.87027,
    0.54,   0.86823,
    0.55,   0.86560,
    0.56,   0.86239,
    0.57,   0.85861,
    0.58,   0.854251,
    0.59,   0.84932,

    0.6,    0.84383,
    0.61,   0.83779,
    0.62,   0.83120,
    0.63,   0.82407,
    0.64,   0.81646,
    0.65,   0.808351,
    0.66,   0.79980,
    0.67,   0.790845,
    0.68,   0.781548,
    0.69,   0.77196,

    0.7,    0.76216,
    0.71,   0.75224,
    0.72,   0.742255,
    0.73,   0.73226,

    p0, p0
]


parr = []
carr = []
v = []
for i in range(0, len(vals), 2):
    v.append([vals[i], vals[i+1]])

v.sort(key=lambda a: a[0])

for i in range(len(v) - 1, 0, -1):
    parr.append(1-v[i][0])
    carr.append(v[i][1])
for i in range(len(v)):
    parr.append(v[i][0])
    carr.append(v[i][1])

fig = plt.figure()

xvals = np.linspace(0, npts * dx, npts + 1)
spline = interp.CubicSpline(parr, carr, bc_type=((1, 1), (1, -1)))
ax = fig.add_subplot(111)

if True:
    for p, s in [(0.3, '0.3'), (0.4, '0.4'), (0.5, '0.5'), (0.6, '0.6'), (0.7, '0.7'), (p0, '0.73')]:
        c = spline(p)
        m, v = discrete_adj(npts, dx, p, c)
        betas = np.linalg.solve(np.identity(npts + 1) - m, v)
        print(betas[-1])
        print(p, c)
        ax.plot(xvals, betas, linewidth=2, label='p={}'.format(s))
    m, v = discrete_adj(npts, dx, 1, 0)
    betas = np.linalg.solve(np.identity(npts + 1) - m, v)
#    ax.plot((xvals + 0.5826), (betas - 0.5826), linewidth=1, label='shift'.format(p))
    ax.plot((xvals+0.5826), (betas-0.5826), linewidth=2, label='shift'.format(p))
    print(betas[-1])

    ax.legend(loc='upper right')
    ax.plot([0, 4], [0, 0], linewidth=0.5, color='grey', linestyle='dashed')
    ax.set_xlim(0, 3)

fig = plt.figure()
ax = fig.add_subplot(111)
p1 = 1
ax.set_xlim(1-p1, p1)
ax.set_ylim(2*p0-p1, 0.875)
#ax.set_xticks([])
#ax.set_yticks([])

#sigma = 0.7
#ax.text(0.5, 0.3, "$X$", fontsize=13)
#ax.text(0.12, k - 0.035, "$K$", fontsize=13)

ax.plot(parr, carr, linewidth=1, color='blue')
ax.plot([p0, p1], [p0, 2*p0-p1], linewidth=1, color='grey', linestyle='dashed')
ax.plot([1-p0, 1-p1], [p0, 2*p0-p1], linewidth=1, color='grey', linestyle='dashed')
#plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()