import numpy as np
from matplotlib.pyplot import viridis
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from scipy.interpolate import interp1d
import matplotlib.colors as mcolors

def convex_envelope(x, f):
    """
    Lower convex envelope of a function sampled on increasing x values.

    Parameters
    ----------
    x : 1D numpy array
        Strictly increasing x values.
    f : 1D numpy array
        Function values.

    Returns
    -------
    g : 1D numpy array
        Convex envelope evaluated on the original x grid.
    """

    x = np.asarray(x)
    f = np.asarray(f)
    n = len(x)

    # indices of vertices of lower convex hull
    hull = []

    for i in range(n):
        while len(hull) >= 2:
            j = hull[-2]
            k = hull[-1]

            # slopes jk and ki
            s1 = (f[k] - f[j]) / (x[k] - x[j])
            s2 = (f[i] - f[k]) / (x[i] - x[k])

            if s1 >= s2:
                hull.pop()
            else:
                break
        hull.append(i)

    # interpolate on original grid
    g = np.empty_like(f)

    for a, b in zip(hull[:-1], hull[1:]):
        t = (x[a:b+1] - x[a]) / (x[b] - x[a])
        g[a:b+1] = (1 - t) * f[a] + t * f[b]

    return g

magic1 = (3-math.sqrt(5))/2
magic2 = 1 - magic1
scale1 = magic1/magic2
scale2 = 1 - scale1*scale1

def iterate_f(f):
    x, y, = (f['x'], f['y'])
    n = len(x)
    x1 = []
    y1 = []
    for i in range(n):
        x1.append([(1-a, -b) for a,b in x[i][::-1]])  # x -> 1-x, and reversed order to keep increasing
        y1.append(y[i][::-1] * scale1)
    for i in range(n):
        x1.append([(0,0)] + [(1 - b, b - a) for a, b in x[i][::-1]])  # x -> 1 - magic2*x, and reversed order to keep increasing
        y1.append(np.concatenate(([0], y[i][::-1] * scale2 - np.array([a+b*magic2 for a,b in x[i][::-1]]) * scale1)))
    return {'level': f['level'] + 1, 'x': x1, 'y': y1}

xvals1 = [(0,0), (0,1), (1,0)]  # x value (a,b) represents a+b*magic2
yvals1 = np.array([0., -1., 0.])
f = {'level': 0, 'x': [xvals1], 'y': [yvals1]}

for _ in range(8):
    f = iterate_f(f)

x_map = {}
for x in f['x']:
    for a, b in x:
        x_map[(a, b)] = a + magic2 * b

print('num x points:', len(x_map.keys()))
print('num t points:', len(f['x']))


# check min grid separation
# n = len(f['x'])
# min_sep = 1.
# for i in range(n):
#     min_sep = min(min_sep, np.min(f['x'][i][1:]-f['x'][i][:-1]))
# print('min separation:', min_sep)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
ax.set_frame_on(False)

ax.plot([0,1], [0,0], linewidth=1, color="black")
for xvals, yvals in zip(f['x'], f['y']):
    ax.plot([a + b * magic2 for a, b in xvals], yvals, linewidth=1, color="black")
ax.set_xlim(0, 1)
ax.set_ylim(-1, 0)

ax.set_xticks([])
ax.set_yticks([])

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
plt.show()

x, x_val = zip(*sorted(x_map.items(), key=lambda x: x[1]))
print(x)
print(x_val)
nt = len(f['x'])+1
t_val = np.linspace(0, 1, nt)[::-1]

X, T = np.meshgrid(x_val, t_val)
Y = X * 0

for i in range(nt-1):
    interp = interp1d([x_map[x0] for x0 in f['x'][i]],
                      f['y'][i],
                      kind='linear',
                      bounds_error=False,
                      fill_value=np.nan)
    Y[i+1] = interp(x_val)

H = X * 0
for i in range(nt-1, 0, -1):
    print('i', i)
    H[i-1] = convex_envelope(x_val, H[i] - Y[i-1] + Y[i])

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(projection='3d')

base = plt.get_cmap("plasma")
cmap = mcolors.LinearSegmentedColormap.from_list(
    "viridis_light",
    base(np.linspace(0.5, 1.0, 256))
)
ax.plot_surface(X, T, Y, cmap=cmap, lw=0.2, rstride=1, cstride=1, edgecolors='black')
# ax.plot_wireframe(X, T, Y, rstride=1, cstride=1,linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("t")
ax.set_zlabel("y")

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
ax.view_init(elev=30, azim=-60)
plt.show()

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(projection='3d')

ax.plot_surface(X, T, H, cmap=cmap, lw=0.2, rstride=1, cstride=1, edgecolors='black')
# ax.plot_wireframe(X, T, H, rstride=1, cstride=1, linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("t")
ax.set_zlabel("y")

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0, wspace=0)
ax.view_init(elev=30, azim=120)
plt.show()