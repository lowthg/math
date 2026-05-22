import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import math

class Point(tuple):
    def __new__(cls, *x):
        res = (x[0]**3 + x[1]**3 - Point.a * x[2]**3)
        assert res == 0
        return tuple.__new__(cls, x)

    a = 7
    verbose = False

    def display(self):
        print('x,y,z =', tuple(self))

    def tangent(self):
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
        x = self
        a = self.a
        v = (x[0] * x[0], x[1] * x[1], -a * x[2] * x[2])
        y = (v[1]*x[2]-v[2]*x[1], v[2]*x[0]-v[0]*x[2], v[0]*x[1]-v[1]*x[0])

        p = 3 * (x[0] * y[0] * y[0] + x[1] * y[1] * y[1] - a * x[2] * y[2] * y[2])
        q = y[0]**3 + y[1]**3 - a * y[2]**3

        return Point(x[0]*q - y[0]*p, x[1]*q - y[1]*p, x[2]*q - y[2]*p)

    def __mul__(self, y):
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
        x = self
        if x[0] * y[1] == x[1] * y[0] and x[0] * y[2] == x[2] * y[0] and x[1] * y[2] == x[2] * y[1]:
            # if x, y proportional, use doubling formula instead
            z = x.tangent()
        else:
            s = x[0] * x[0] * y[0] + x[1] * x[1] * y[1] - self.a * x[2] * x[2] * y[2]
            t = y[0] * y[0] * x[0] + y[1] * y[1] * x[1] - self.a * y[2] * y[2] * x[2]
            z = x[0] * t - y[0] * s, x[1] * t - y[1] * s, x[2] * t - y[2] * s

        g = math.gcd(*z)
        if z[0] < 0 or (z[0] == 0 and z[1] < 0) or (z[0] == z[1] == 0 and z[2] < 0):
            g = -g
        z = Point(z[0] // g, z[1] // g, z[2] // g)

        if Point.verbose: z.display()

        return z

    def __neg__(self):
        z = self
        return Point(-z[1], -z[0], -z[2]) if z[1] < 0 else Point(z[1], z[0], z[2])

    def __add__(self, y):
        return -(self * y)


"""
we want to solve x/(y+z)+y/(x+z)+z/(x+y)=4
set (u,v,w)=(y+z,x+z,x+y), so 2x=-u+v+w etc
solve: (-u+v+w)/u+...=8
solve: (v+w)/u+(u+w)/v+(u+v)/w=11
write multiplicatively: vw(v+w)+uw(u+w)+uv(u+v)=11uvw
trivial solns: (0,0,1), (0,1,0), (1,0,0), (0,1,-1), (1,0,-1),(1,-1,0)
found soln: (x,y,z)=(11,4,-1) or (u,v,w)=(3, 10, 15) but x,y,z not positive
"""

O = Point(1, -1, 0)
P = Point(2, -1, 1)

Point.verbose = True

P2 = P*P
P2_ = -P2

P3 = P2_ * P
P6 = P3*P3

P4=P2_ * P2_
P6_ = P4 * P2
