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
width = math.exp(1)

ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_xticks([])
ax.set_yticks([])


x0, x1, y0, y1 = 0, width, 0, 1

colors = [_ for _ in matplotlib.colors.TABLEAU_COLORS.keys()]
i = 0
j = 0
dir = None

lw = [1, 1, 1, 1, 0.5, 0.5, 0.1, 0.1, 0.05, 0.02, 0.02, 0.05, 0.01]
while True:
    color = colors[i % len(colors)]
    width = x1 - x0
    height = y1 - y0
    if min(width, height) < 0.00001:
        break
    if width > height:
        w = height
        x, y = x0, y0
        x0 += w
        if dir == 1:
            j += 1
        dir = 0
    else:
        w = width
        x, y = x0, y1 - w
        y1 -= w
        if dir == 0:
            j += 1
        dir = 1
    r = matplotlib.patches.Rectangle((x, y), w, w, fill=True, lw=lw[min(i, len(lw)-1)], color='black', fc=color)
    ax.add_patch(r)
    i += 1

print(j)

plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.subplots_adjust(left=0.0, right=1, bottom=0.0, top=1, hspace=0, wspace=0)
print('saving...')
plt.savefig('plot.png', dpi=3000, bbox_inches=0, pad_inches=0)
print('saved')

plt.show()
