import numpy as np
import tensorcircuit as tc
import tensorflow as tf
import matplotlib.pyplot as plt
from noise_cz import expectation_n_noisy_channel_cz
from noise_sim_tc import noise_sim

K = tc.set_backend("tensorflow")

w = 0.9999*np.ones(16)

T = 10


def cnot(circuit, control, target, x):
    circuit.H(target)
    expectation_n_noisy_channel_cz(circuit, control, target, w, x)
    circuit.H(target)




def rzz (c, i, j, theta, x):
    #c.cnot(j, i)
    cnot(c, j, i, x)
    c.rz(i, theta=theta)
    #c.cnot(j, i)
    cnot(c, j, i, x)
    return c

def P (c, n, edges, N, J = -1., h = 1., x = 0.):
    for i in range(n):
        c.rx(i, theta = 2*T*h/N)
    for g0,g1 in edges:
        c = rzz(c, g0, g1, -2*T*J/N, x)
    return c

def test (c, n, edge, N, J = -1., h = 1., x = 0.):
    #c=tc.Circuit(n)
    for i in range(N):
        c = P(c, n, edge, N, J, h, x)
    return c
    # z_exp = c.expectation([tc.gates.z(), [0]])
    # z_exp_float = float(z_exp.numpy())

    # return z_exp_float

# n = 5
# edges = [[1, 2], [3, 4], [0, 1], [2, 3], [1, 2], [3, 4]]

n = 6
edges = [[0, 1], [3, 4], [2, 5], [0, 3], [4, 5], [1, 2], [1, 4]]

# n = 9
# edges = [[0, 1], [3, 4], [7, 8], [2, 5], [0, 3], [4, 5], [6, 7], [1, 2], [4, 7], [5, 8], [3, 6], [1, 4]]



e = 0
f = np.array([0., 3., -3., 1., 0., 0., 0., 0., 0., 0.], dtype=np.complex128)
g = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.int32)

r = np.array([0., 0., 0., 0., 0.], dtype=np.complex128)



for p in range(1):
    t = g[p]
    a = 0
    for i in range(1):
        c = tc.densitymatrix.DMCircuit(n)
        N = 20
        c = test(c, n, edges, N, 1, 1, t)
        #c = noise_sim(c)
        a += c.expectation_ps(z=[0])
        #print(c.expectation_ps(z=[0]))
    a /= 1
    print(g[p], ":", a)
    a *= f[p]
    e += a

print(e)