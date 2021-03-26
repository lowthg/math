"""
Plots a Brownian motion B(t), using covariances E[B(s)B(t)]=s(1-t) over s <= t
and,
- sine series B(t) = sum_{n >= 1} s(n) sin(pi n t)
- cos-sin series B(t) = sum_{n >=1}( c(2n) cos(2 pi n t) + s(2n) sin(2 pi n t) )
where
- Var(s(n)) = Var(c(n)) = 2/(pi n)^2
- Cov(s(m),s(n)) = Cov(c(m),c(n)) = 0 for m != n
- Cov(s(n),B(t)) = sin(pi n t) * 2/(pi n)^2
- Cov(c(n),B(t)) = cos(pi n t) * 2/(pi n)^2 for n even
- Cov(s(m),c(n)) = 0 for m+n even
- Cov(s(m),c(n)) = ( (1/(m-n)-1/(m+n)) * 4 / (pi^3 * m * n) for m+n odd
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def bbcovs(cov, times):
    ntimes = len(times)
    for i in range(0, ntimes):
        t = 1 - times[i]
        cov[i] = t * times[i]
        for j in range(0, i):
            cov[i, j] = cov[j, i] = times[j] * t


def main():
    seed = 6
    ntimes = 400
    nsines = 100

    pi = math.pi
    sin = math.sin

    np.random.seed(seed)
    times = np.linspace(0.0, 1.0, ntimes)

    nrands = ntimes + nsines
    cov = np.ndarray(shape=(nrands, nrands))

    bbcovs(cov, times)

    # compute c-values
    c0 = ntimes - 1
    for n in range(1, nsines + 1):
        c = pi * n
        c = 2 / (c*c)
        cov[c0 + n, c0 + n] = c
        for m in range(1, n):
            cov[c0 + m, c0 + n] = cov[c0+n, c0+m] = 0
        for i in range(0, ntimes):
            cov[c0+n, i] = cov[i, c0+n] = c * sin(pi * n * times[i])

    rands = np.random.multivariate_normal(np.zeros(shape=(nrands,)), cov)

    # compute Brownian bridge
    bpath = rands[0:ntimes]

    # compute sign series
    sineseries = []
    sinepath = np.zeros(ntimes)
    for n in range(1, nsines + 1):
        c = rands[c0 + n]
        for i in range(0, ntimes):
            sinepath[i] += c * sin(pi * n * times[i])
        sineseries.append(sinepath.copy())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times, bpath, label='Brownian bridge', linewidth=1, color='black')
    for n in range(1, 10):
        color = 'blue'
        label = 'sine approximations' if n == 1 else None
        ax.plot(times, sineseries[n-1], label=label, linewidth=1, color=color, alpha=0.8)
    n = nsines
    ax.plot(times, sineseries[n-1], label='sine approx., {} terms'.format(n), linewidth=1, color='red', alpha=1)
    ax.plot([0, 1], [0, 0], linewidth=0.5, color='black')
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
    ax.legend(loc='lower right')
    plt.show()


main()
