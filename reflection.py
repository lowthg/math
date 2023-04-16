"""
Plots Brownian motion, and associated brownian bridges on subintervals
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

K = 0.1
#(K, seed )= 1.2, 18
#(K, seed) = 1.5, 28
(K, seed) = (0.6, 43)
npts = 1000
tmax = 1.0


random.seed(seed)
times = np.linspace(0, tmax, npts)
Xvals = np.zeros(npts)
reflected = False

for i in range(1, npts):
    t0 = times[i-1]
    t1 = times[i]
    dt = t1 - t0
    X0 = Xvals[i-1]
    X1 = X0 + random.gauss(0, np.sqrt(dt))
    Xvals[i] = X1
    if not reflected and X1 > K:
        reflected = True
        Xrtimes = np.linspace(t0, tmax, npts - i + 1)
        Xrvals = np.zeros(npts - i + 1)
        tau = ((X1 - K) * t0 + (K - X0) * t1) / (X1 - X0)
        Xrtimes[0] = tau
        Xrvals[0] = K
        j = 0
    if reflected:
        j += 1
        Xrvals[j] = 2 * K - X1

assert reflected

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Xrtimes, Xrvals, linewidth=1, color="green")
ax.plot(times, Xvals, linewidth=1, color="blue")
ax.plot([0, times[-1]], [0, 0], linewidth=0.5, color="black")
ax.plot([0, times[-1]], [K, K], linewidth=1, color="grey", alpha=0.5)
ax.plot([tau, tau], [0, Xrvals[0]], linewidth=1, color="grey", linestyle="dashed")


plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.rcParams.update({"text.usetex": True})

ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 1)
#ax.set_ylim(0)
ax.set_xticks([])
ax.set_yticks([])
ax.text(tau-0.008, -0.04, '$\\tau$')
ax.text(tau/2, K + 0.01, '$a$')
ax.text(0.75, 0.28, '$X$')
ax.text(0.75, 0.92, '$X^r$')

plt.show()
