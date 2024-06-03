"""
geometric continued fraction
"""

"""
"""

import matplotlib.pyplot as plt
import matplotlib.patches
from scipy.stats import norm
import math

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.axis('off')
height = 1
width = math.pi

ax.set_xlim(0, width)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
plt.subplots_adjust(left=0.0, right=1, bottom=0.0, top=1, hspace=0, wspace=0)


x0, x1, y0, y1 = 0, width, 0, 1

colors = [_ for _ in matplotlib.colors.TABLEAU_COLORS.keys()]
i = 0

while True:
    color = colors[i]
    i = (i + 1) % len(colors)
    width = x1 - x0
    height = y1 - y0
    if min(width, height) < 0.001:
        break
    if width > height:
        w = height
        x, y = x0, y0
        x0 += w
    else:
        w = width
        x, y = x0, y1 - w
        y1 -= w
    r = matplotlib.patches.Rectangle((x, y), w, w, fill=True, lw=1, color='black', fc=color)
    ax.add_patch(r)

plt.show()
