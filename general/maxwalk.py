"""
generate random walk, maximum, and equivalent max distributed RV from spitzer's theorem
"""
import numpy as np
import random
import matplotlib.pyplot as plt


def get_samples(n_steps, random_sample, n_samples):
    s_n = np.zeros(n_samples)
    s_max = np.zeros(n_samples)
    s_alt = np.zeros(n_samples)
    s_vals = np.zeros(n_steps + 1)
    for isample in range(n_samples):
        for i in range(1, n_steps + 1):
            s_vals[i] = s_vals[i - 1] + random_sample()
        s_n[isample] = s_vals[-1]
        s_max[isample] = max(s_vals)
        r_alt = 0.0
        t1 = n_steps
        while t1 > 0:
            t0 = random.randint(0, t1 - 1)
            r_alt += max(s_vals[t1] - s_vals[t0], 0)
            t1 = t0
        s_alt[isample] = r_alt

    return s_n, s_max, s_alt

random.seed(1)
random_sample = lambda: random.gauss(0, 1)  # step distribution
random_sample = lambda: random.randint(0, 1)*2 - 1
random_sample = lambda: random.uniform(-1, 1)+0.1


s_n, s_max, s_alt = get_samples(20, random_sample, 100000)

n_bins = 50

fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)

axs[0].hist(s_n, bins=n_bins)
axs[1].hist(s_max, bins=n_bins)
axs[2].hist(s_alt, bins=n_bins)

plt.show()
