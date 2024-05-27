"""
find weights p, q for 2 dice to minimize sum of squares of probs for sum of dice

minimize: sum_k (sum_{i+j=k} p_iq_j)^2
can
"""
import cvxopt.solvers
import numpy
import numpy as np
from cvxopt import matrix
import random


def getPmatrix(p):
    """
    sum_k (sum_{i+j=k} p_iq_j)^2 = sum_{ijkl, i+k=j+l}q_ip_kq_jp_l
    M_{ij}=sum_{i+k=j+l} p_kp_l
    """
    m = matrix(0.0, (6,6))
    v = [0] * 6
    for k in range(6):
        for l in range(k+1):
            v[k-l] += p[k] * p[l]

    for i in range(6):
        for j in range(i+1):
            m[i, j] = m[j,i] = v[i-j]

    return m


e = matrix(1.0, (1, 6))
esum = matrix(1.0, (1,1))
p = numpy.zeros(6)
for i in range(6):
    p[i] = random.uniform(0, 1)
p /= sum(p)
vec0 = matrix(0.0, (6,1))
G = matrix(0.0, (6,6))
for i in range(6):
    G[i,i] = -1

print(p)

for i in range(20):
    m = getPmatrix(p)
    res = cvxopt.solvers.qp(m, vec0, G, vec0, e, esum)
    p = res['x']
    print(p)

