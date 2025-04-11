import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import math


def findSoln1():
    for x in range(1, 1000):
        for y in range(-x, x+1):
            if y == 0 or y == -x:
                continue
            c = x + y
            k = abs(y)
            for z in range(-k, k+1):
                if z == 0 or z == -y or z == -x:
                    continue
                a = y+z
                b = x+z
                if x*b*c + y*a*c + z*a*b == 4*a*b*c:
                    print('Found:', x, y, z)
                    return


def double(x, a):
    """
    x should satisfy (x1+x2)/x0+(x0+x2)/x1+(x0+x1)/x2=a
    returns z satisfying same

    write as: (x1)^2 x2 + perms = a x0 x1 x2

    deriv of x1^2 x2 + perms - a x0 x1 x2 is:
    (2 x0 x1 + 2 x0 x2 + x1^2 + x2^2 - a x1 x2, ...)
    let y be orthogonal to this and x

    z = sx + ty satisfies eqn in s^3 and s^2t terms, giving t^2(ps+qt)
    take (s,t) = (q, -p)
    """
    v = (2 * x[0] * (x[1]+x[2]) + x[1]*x[1] + x[2]*x[2] - a*x[1]*x[2],
         2 * x[1] * (x[0]+x[2]) + x[0]*x[0] + x[2]*x[2] - a*x[0]*x[2],
         2 * x[2] * (x[0]+x[1]) + x[0]*x[0] + x[1]*x[1] - a*x[0]*x[1])
    y = (v[1]*x[2]-v[2]*x[1], v[2]*x[0]-v[0]*x[2], v[0]*x[1]-v[1]*x[0])

    p = q = 0
    for i, j in [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]:
        # expand zi^2z_j term
        p += y[i]*y[i]*x[j] + 2*y[i]*x[i]*y[j]
        q += y[i]*y[i]*y[j]
    p -= a*(y[0]*y[1]*x[2] + y[0]*x[1]*y[2] + x[0]*y[1]*y[2])
    q -= a*y[0]*y[1]*y[2]

    return x[0]*q - y[0]*p, x[1]*q - y[1]*p, x[2]*q - y[2]*p


def add1(x, y, a):
    """
    x and y should satisfy (x1+x2)/x0+(x0+x2)/x1+(x0+x1)/x2=a
    returns z = sx + ty satisfying the same

    write as (x1+x2)x1x2 + cyclic = a x0 x1 x2
    equiv: (x1)^2 x2 + perms = a x0 x1 x2

    z = sx+ty
    expand both sides of eqn using z. s^3 and t^3 automatically vanish. Only s^2t and st^2
    terms remain. Cancel st to get ps + qt = 0.
    can take (s, t) = (q, -p), so z = qx - py
    """
    if x[0] * y[1] == x[1]*y[0] and x[0]*y[2] == x[2]*y[0] and x[1]*y[2] == x[2]*y[1]:
        # if x, y proportional, use doubling formula instead
        return double(x, a)

    s_lhs = t_lhs = 0
    for i, j in [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]:
        # expand zi^2z_j term
        s_lhs += x[i]*x[i]*y[j] + 2*x[i]*y[i]*x[j]
        t_lhs += y[i]*y[i]*x[j] + 2*y[i]*x[i]*y[j]
    s_rhs = a*(x[0]*x[1]*y[2] + x[0]*y[1]*x[2] + y[0]*x[1]*x[2])
    t_rhs = a*(y[0]*y[1]*x[2] + y[0]*x[1]*y[2] + x[0]*y[1]*y[2])
    s = t_lhs - t_rhs
    t = s_rhs - s_lhs

    return x[0]*s + y[0]*t, x[1]*s + y[1]*t, x[2]*s + y[2]*t


def add(x, y, a):
    z = add1(x, y, a)
    g = math.gcd(*z)
    if z[0] < 0 or (z[0] == 0 and z[1] < 0) or (z[0] == z[1] == 0 and z[2] < 0):
        g = -g

    return z[0]//g, z[1]//g, z[2]//g

"""
we want to solve x/(y+z)+y/(x+z)+z/(x+y)=4
set (u,v,w)=(y+z,x+z,x+y), so 2x=-u+v+w etc
solve: (-u+v+w)/u+...=8
solve: (v+w)/u+(u+w)/v+(u+v)/w=11
write multiplicatively: vw(v+w)+uw(u+w)+uv(u+v)=11uvw
trivial solns: (0,0,1), (0,1,0), (1,0,0), (0,1,-1), (1,0,-1),(1,-1,0)
found soln: (x,y,z)=(11,4,-1) or (u,v,w)=(3, 10, 15) but x,y,z not positive
"""


def findSoln(n):
    x = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (3, 10, 15)]
    for z in x:
        assert (z[0]+z[1])*z[0]*z[1] + (z[0]+z[2])*z[0]*z[2] + (z[1]+z[2])*z[1]*z[2] == 11 * z[0] * z[1] * z[2]

    for _ in range(n):
        y = x.copy()

        for i in range(len(x)):
            for j in range(i+1):
                z = add(x[i], x[j], 11)
                if z not in y:
                    y.append(z)
                    u = (-z[0]+z[1]+z[2], z[0]-z[1]+z[2], z[0]+z[1]-z[2])
                    if u[0] > 0 and u[1] > 0 and u[2] > 0:
                        return u
        x = y
    return None


x = findSoln(4)

if x is not None:
    g = math.gcd(*x)
    x = (x[0] // g, x[1] // g, x[2] // g)
    print('Solution found!')
    print('x =', x[0], 'num digits =', math.floor(math.log10(x[0]))+1)
    print('y =', x[1], 'num digits =', math.floor(math.log10(x[1]))+1)
    print('z =', x[2], 'num digits =', math.floor(math.log10(x[2]))+1)
    print(x[0]/(x[1]+x[2])+x[1]/(x[0]+x[2])+x[2]/(x[0]+x[1]))

