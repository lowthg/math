import math

class Point(tuple):
    def __new__(cls, *u):
        res = (sum([u[i] * u[j] * u[j] for i, j in [(0, 1), (0, 2), (1, 0),
                                                    (1, 2), (2, 0), (2, 1)]])
               - 11 * u[0] * u[1] * u[2])
        assert res == 0, "{} is not on the curve!".format(u)
        if u[0] < 0 or (0 == u[0] > u[1]) or (0 == u[0] == u[1] > u[2]):
            return tuple.__new__(cls, tuple(-_ for _ in u))
        return tuple.__new__(cls, u)

    verbose = False

    def xyz(self):
        x = tuple(sum(self) - 2*u for u in self)
        return x if any(_ % 2 for _ in x) else tuple(_ // 2 for _ in x)

    def display(self):
        x = self.xyz()
        print('x,y,z =', x)
        if all(_ > 0 for _ in x):
            print('****** solution found!!! ******')

    def __mul__(self, v):
        """
        u and v should satisfy
            u1u2(u1+u2) + u0u2(u0+u2) + u0u1(u0+u1) = 11u0u1u2
        returns w = su + tv satisfying the same
        using chord construction
        """
        u = self
        if (u[0] * v[1] == u[1] * v[0] and u[0] * v[2] == u[2] * v[0]
                and u[1] * v[2] == u[2] * v[1]):
            w = u.tangent() # if x, y proportional, use tangent instead
        else:
            p = q = 0
            for i, j in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]:
                p += u[i]*u[i]*v[j] + 2 * u[i]*v[i]*u[j]
                q += v[i]*v[i]*u[j] + 2 * v[i]*u[i]*v[j]
            p -= 11 * (u[0]*u[1]*v[2] + u[0]*v[1]*u[2] + v[0]*u[1]*u[2])
            q -= 11 * (v[0]*v[1]*u[2] + v[0]*u[1]*v[2] + u[0]*v[1]*v[2])
            w = u[0]*q - v[0]*p, u[1]*q - v[1]*p, u[2]*q - v[2]*p

        g = math.gcd(*w)
        w = Point(*(_//g for _ in w))

        if Point.verbose: w.display()

        return w

    def tangent(self):
        """
        u should satisfy
            u1u2(u1+u2) + u0u2(u0+u2) + u0u1(u0+u1) = 11u0u1u2
        returns new point satisfying the same
        using tangent construction
        """
        u = self
        g = (2 * u[0] * (u[1]+u[2]) + u[1]*u[1] + u[2]*u[2] - 11*u[1]*u[2],
             2 * u[1] * (u[0]+u[2]) + u[0]*u[0] + u[2]*u[2] - 11*u[0]*u[2],
             2 * u[2] * (u[0]+u[1]) + u[0]*u[0] + u[1]*u[1] - 11*u[0]*u[1])
        v = (g[1]*u[2]-g[2]*u[1], g[2]*u[0]-g[0]*u[2], g[0]*u[1]-g[1]*u[0])

        p = q = 0
        for i, j in [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]:
            # expand zi^2z_j term
            p += v[i]*v[i]*u[j] + 2*v[i]*u[i]*v[j]
            q += v[i]*v[i]*v[j]
        p -= 11*(v[0]*v[1]*u[2] + v[0]*u[1]*v[2] + u[0]*v[1]*v[2])
        q -= 11*v[0]*v[1]*v[2]

        return Point(u[0]*q - v[0]*p, u[1]*q - v[1]*p, u[2]*q - v[2]*p)

    def __neg__(self):
        z = self
        return Point(z[0], z[2], z[1])

    def __add__(self, y):
        return -(self * y)

"""
we want to solve x/(y+z)+y/(x+z)+z/(x+y)=4
set (u,v,w)=(y+z,x+z,x+y)
solve: vw(v+w)+uw(u+w)+uv(u+v)=11uvw
trivial solutions: (1,0,0), (0,1,0), (0,0,1), (0,1,-1), (1,0,-1),(1,-1,0)
"""

def find_positive(*point, n=10):
    pts = list(point)
    count = len(pts)

    for step in range(n):
        print('\nstep', step)
        for i in range(len(pts)):
            for j in range(i+1):
                z = pts[i] * pts[j]
                if z not in pts:
                    pts.append(z)
                    print('Q{}=Q{}xQ{}: {}'.format(count, i, j, z))
                    count += 1
                    u = z.xyz()
                    if all(_ > 0 for _ in u):
                        print('solution found on step {}!!'
                              '\nx={}\ny={}\nz={}'.format(step, *u))
                        return u
    return None

P1 = Point(1, 0, 0)
P2 = Point(0, 1, 0)
P3 = Point(0, 0, 1)
O1 = Point(0, 1, -1)
O2 = Point(1, 0, -1)
O3 = Point(1, -1, 0)
