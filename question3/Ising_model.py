from operator import index
import tensorcircuit as tc
import numpy as np
import random
from noise_cz import expectation_n_noisy_channel_cz

c2 = tc.Circuit(5)
for i in range(5):
    c2.rx(i, theta=-0.5)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.rz(2, theta=-0.25)
c2.rz(4, theta=-0.25)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.cnot(0, 1)
c2.cnot(2, 3)
c2.rz(1, theta=-0.5)
c2.rz(3, theta=-0.5)
c2.cnot(0, 1)
c2.cnot(2, 3)
c2.rx(0, theta=-1)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.rz(2, theta=-0.25)
c2.rz(4, theta=-0.25)
c2.cnot(1, 2)
c2.cnot(3, 4)
for i in range(1, 5):
    c2.rx(i, theta=-1)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.rz(2, theta=-0.25)
c2.rz(4, theta=-0.25)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.cnot(0, 1)
c2.cnot(2, 3)
c2.rz(1, theta=-0.5)
c2.rz(3, theta=-0.5)
c2.cnot(0, 1)
c2.cnot(2, 3)
c2.rx(0, theta=-0.5)
c2.cnot(1, 2)
c2.cnot(3, 4)
c2.rz(2, theta=-0.25)
c2.rz(4, theta=-0.25)
c2.cnot(1, 2)
c2.cnot(3, 4)
for i in range(1, 5):
    c2.rx(i, theta=-0.5)

# print("c2.state():", c2.state())
print(c2.expectation_ps(z=[0, 1, 2, 3, 4]))
s = c2.state()

def rx(circuit, index, theta, x):
    circuit.rx(index, theta=theta)
def cnot(circuit, control, target, x):
    circuit.H(target)
    expectation_n_noisy_channel_cz(circuit, control, target, x)
    circuit.H(target)
def rz(circuit, index, theta, x):
    circuit.rz(index, theta=theta)



# e = np.zeros(2**5, dtype=np.complex128)
e = 0
f = np.array([0., 3., 0., -2.], dtype=np.complex128)
g = np.array([0., 1., 1.2, 1.5], dtype=np.complex128)

r = np.array([0., 0., 0., 0., 0.], dtype=np.complex128)

for p in range(4):
    t = g[p]
    #a = np.zeros(2**5, dtype=np.complex128)
    a = 0
    for _ in range(10):
        c = tc.Circuit(5)
        for i in range(5):
            rx(c, i, -0.5, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        rz(c, 2, -0.25, t)
        rz(c, 4, -0.25, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        cnot(c, 0, 1, t)
        cnot(c, 2, 3, t)
        rz(c, 1, -0.5, t)
        rz(c, 3, -0.5, t)
        cnot(c, 0, 1, t)
        cnot(c, 2, 3, t)
        rx(c, 0, -1, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        rz(c, 2, -0.25, t)
        rz(c, 4, -0.25, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        for i in range(1, 5):
            rx(c, i, -1, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        rz(c, 2, -0.25, t)
        rz(c, 4, -0.25, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        cnot(c, 0, 1, t)
        cnot(c, 2, 3, t)
        rz(c, 1, -0.5, t)
        rz(c, 3, -0.5, t)
        cnot(c, 0, 1, t)
        cnot(c, 2, 3, t)
        rx(c, 0, -0.5, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        rz(c, 2, -0.25, t)
        rz(c, 4, -0.25, t)
        cnot(c, 1, 2, t)
        cnot(c, 3, 4, t)
        for i in range(1, 5):
            rx(c, i, -0.5, t)
        #a += c.state()
        a += c.expectation_ps(z=[0, 1, 2, 3, 4])
    a /= 10
    print(g[p], ":", a)
    a *= f[p]
    e += a
print(e)
# print(e - s)