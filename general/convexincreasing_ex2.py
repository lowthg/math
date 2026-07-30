import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from scipy.interpolate import interp1d

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

for _ in range(9):
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

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(projection='3d')

# ax.plot_surface(X, T, Y, cmap='viridis')
ax.plot_wireframe(
    X, T, Y,
    rstride=1,
    cstride=1,
    linewidth=0.5,
)
ax.set_xlabel("x")
ax.set_ylabel("t")
ax.set_zlabel("y")

plt.show()