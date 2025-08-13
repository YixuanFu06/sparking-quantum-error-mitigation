import numpy as np
import tensorcircuit as tc
import tensorflow as tf
import matplotlib.pyplot as plt

K = tc.set_backend("tensorflow")

T = 10
def pauli_gate(c,q,i):
    if i == 1:
        c.x(q)
    elif i == 2:
        c.y(q)
    elif i == 3:
        c.z(q)
    return c
w=0.9999*np.ones(16)

def apply_E_to_cz(c,m,w,q1,q2):
    for k in range(m):
        for i in range(4):
            for j in range(4):
                n = 4*i+j
                rand = np.random.rand()
                if rand > w[n]: 
                    pauli_gate(c, q1, i)
                    pauli_gate(c, q2, j)
    return c


def rzz (c, m, w, i, j, theta):
    c.h(i)
    apply_E_to_cz(c,m,w,j,i)
    c.cz(j, i)
    c.h(i)
    c.rz(i, theta=theta)
    c.h(i)
    apply_E_to_cz(c,m,w,j,i)
    c.cz(j, i)
    c.h(i)
    return c

def P (c, n, edges, m, w, N, J = -1., h = 1.):
    for i in range(n):
        c.rx(i, theta = 2*T*h/N)
    for g0,g1 in edges:
        c = rzz(c, m, w, g0, g1, -2*T*J/N)
    return c

def test (n, edges, m, w, N, J = -1., h = 1.):
    c=tc.Circuit(n)
    for i in range(N):
        c = P(c, n, edges, m, w, N, J, h)
    return c
    # z_exp = c.expectation([tc.gates.z(), [0]])
    # z_exp_float = float(z_exp.numpy())

    # return z_exp_float

n = 5
edges = [[1, 2], [3, 4], [0, 1], [2, 3], [1, 2], [3, 4]]

#n = 6
#edges = [[0, 1], [3, 4], [2, 5], [0, 3], [4, 5], [1, 2], [1, 4]]

# n = 9
# edges = [[0, 1], [3, 4], [7, 8], [2, 5], [0, 3], [4, 5], [6, 7], [1, 2], [4, 7], [5, 8], [3, 6], [1, 4]]


N = 20
for i in range(0,4):
    c = tc.Circuit(n)
    measurements = []
    for j in range(500):
        c = test(n, edges, i, w, N,-1,1)
        measurements.append(c.expectation_ps(z=[0, 1, 2, 3, 4]))
    measurements = np.array(measurements)
    measurements = measurements.sum(axis=0) / 500
    print(measurements)
