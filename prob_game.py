"""
Probability game for math.stackexchange
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


npts = 4001
xvals = np.linspace(1.0, 2.0, npts)
y = np.zeros([npts])
y[0] = 1.0
y[-1] = 0.75
eps = 0.00001

method = 1
solve = False

max_iters = 0
if method == 0:
    for i in range(1, npts-1):
        x = xvals[i]
        # p = 0.5 + q
        # p(x) = a + b q(x')
        a = 0.5
        b = 1.0

        for j in range(1000):
            # p(x) = 0.5 + 0.5 * p(x/(2-x))
            # q(x) = 0.25 + 0.5 * q(x/(2-x))
            x = x / (2.0 - x)
            a += b * 0.25
            b *= 0.5
            while x >= 2:
                # q(x) = 0.5 * q(x-1)
                x -= 1.0
                b *= 0.5
                if b < eps:
                    break
            if b < eps:
                break
            max_iters = max(max_iters, j)
        y[i] = a
else:
    for i in range(1, npts-1):
        x = xvals[i]
        a = 0.5
        b = 1.0
        for j in range(1000):
            # x < 1/(1 - 2^{-n})
            # 1 - 1/x < 2^{-n}
            # x/(1-dx)=1/(1-2^{-n})
            # x-dx = 2*x(1-2^{-n-1})-1

            u = 1.0 - 1.0/x
            if u <= eps:
                a += b * 0.5
                break
            v = math.pow(2.0, math.floor(math.log2(u)))
            x = x * (1.0 - v)*2 - 1.0
            b *= 0.5
            a += b * (0.5 - v)
            if b < eps:
                break
            max_iters = max(max_iters, j)
        y[i] = a


print('max iters:', max_iters)

# f = interpolate.interp1d(xvals, y)
# x0 = 1.5
# a = 0.5
# b = 1
# x = x0
# while x >= 2:
#     x -= 1
#     b *= 0.5
# p0 = a + b*(f(x) - 0.5)
#
# maxp = 0.5
#
# for dx in np.linspace(0.249, 0.251, 100):
#     x = x0 - dx
#     a = 0.5
#     if x <= 1:
#         a = 0.75
#     else:
#         for j in range(1000):
#             if x <= 2.0:
#                 a *= f(x) - 0.5
#                 break
#             x -= 1
#             a *= 0.5
#
#         a += 0.5
#
#     b = 0.5
#     x = x0 / (1.0 - dx)
#     for j in range(1000):
#         if x <= 2.0:
#             b *= f(x) - 0.5
#             break
#         x -= 1
#         b *= 0.5
#
#     p = a + b
#     maxp = max(p, maxp)
#
#     print(dx, p)
#
# print('p:', p0)
# print('max:', maxp)

x1vals = y1vals = None
if solve:
    n = 20
    n1 = (npts - 1) * n + 1
    x1vals = np.linspace(1.0, 1.0 + n, n1)
    y1vals = np.zeros(n1)

    for i in range(n):
        y1vals[i*(npts-1):(i+1)*(npts-1)+1] = (y-0.5)/(2**i)

    x2 = [min(x - 1, 1.0) for x in x1vals]

    for iter in range(4):
        dp = 0.0
        for i in range(1, n1 - 1):
            a = x1vals[i]
            p = y1vals[i]
            if i - npts + 1 >= 0:
                p = max(p, y1vals[i - npts + 1] * 0.5)
            for j in range(max(i-npts+2, 0), i):
                p0 = y1vals[j]
                x = a / (1.0 - (a-x1vals[j]))
                b = 0.5
                if x > n + 1:
                    m = math.ceil(x) - n - 1
                    # print(i, j, a, x)
                    x -= m
                    # print(m)
                    b *= 0.5**m
                m = math.ceil((x-1.0) * (npts-1))
                while m >= 0:
                    p1 = p0 * 0.5 + y1vals[m] * b
                    if p1 > p:
                        p = p1
                        x2[i] = a - x1vals[j]
                    m -= npts - 1
                    b *= 0.5
            dp = max(dp, p-y1vals[i])
            y1vals[i] = p
        print(dp)

plt.plot(xvals, y, label='p0(a)')
if solve:
    plt.plot(x1vals[:npts], y1vals[:npts] + 0.5, label='p(a)')
plt.plot(xvals, 0.5/xvals+0.5, label='1/2+1/(2a)')
# ax = plt.twinx()
# npts2 = math.ceil((npts-1)*1) + 1
# ax.plot(x1vals[:npts2], x2[:npts2], color='r')

plt.legend(loc='best')
plt.margins(0, tight=True)
plt.show()


# p(a) >= 0.5(p(a-x)+p(a/(1-x))
# q(a) >= 0.5(q(a-x)+q(a/(1-x))
# 1 >= 2^{x-1}+2^{-ax/(1-x)-1}
# a = 1:
# 1 >= 2^{x-1}+2^{-1/(1-x)}
# 2^{x-1} - (1/(1-x)^2)2^{-1/(1-x)}
