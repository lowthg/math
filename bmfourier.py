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
import matplotlib.pyplot as plt

# compute Brownian bridge and sine series
nt = 400
nsines = 100
np.random.seed(6)
times = np.linspace(0.0, 1.0, nt)
nrands = nt + nsines
cov = np.zeros(shape=(nrands, nrands))

for i, t in enumerate(times):
    cov[i, :i+1] = cov[:i+1, i] = times[:i+1] * (1-t)

for i in range(nsines):
    cov[nt + i, nt + i] = c = 2 / (np.pi * (i+1))**2
    cov[nt + i, :nt] = cov[:nt, nt+i] = np.sin(times * np.pi * (i+1)) * c

rands = np.random.multivariate_normal(np.zeros(shape=(nrands,)), cov)
series = np.cumsum([np.sin(times * np.pi * (i+1)) * rands[nt + i] for i in range(nsines)], axis=0)

# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(times, rands[0:nt], label='Brownian bridge', linewidth=1, color='black')  # plot bbridge
for i in range(39):
    alpha = 0.8 * np.exp(-i * 0.1)
    label = 'sine approximations' if i == 0 else None
    ax.plot(times, series[i], label=label, linewidth=1, color='blue', alpha=alpha)
ax.plot(times, series[-1], label='sine approx., {} terms'.format(nsines), linewidth=1, color='red')
ax.plot([0, 1], [0, 0], linewidth=0.5, color='black')
ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
ax.set_frame_on(False)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
ax.legend(loc='lower right')
plt.show()
