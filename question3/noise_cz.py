import tensorcircuit as tc
import numpy as np
from itertools import product
from scipy.optimize import least_squares
from noise_sim_tc import noise_sim

#w = np.array([0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,0.999,])



def expectation_n_noisy_channel_cz(circuit, control, target, w, n_noise: np.int32):
    pauli_gate_funcs = [lambda c, q: None,  # I门不操作
                lambda c, q: c.x(q),
                lambda c, q: c.y(q),
                lambda c, q: c.z(q)]
    if n_noise > 0:
        for i in range(n_noise - 1):
            for i in range(4):
                for j in range(4):
                    n = 4*i+j
                    rand = np.random.rand()
                    if rand < (1-w[n]): #以n_noise_frac*(1-w[n])的概率施加pauli word门，表示噪声
                        pauli_gate_funcs[i](circuit, control)
                        pauli_gate_funcs[j](circuit, target)
    
    # 添加 CZ 门
    circuit.cz(control, target)
    # 添加噪声,虽然看起来对所有门（包括pauli words）都添加了噪声，但实际上噪声只作用于 CZ 门（因为噪声模拟器只作用于2比特门）
    #if n_noise != 0:
        #circuit = noise_sim(circuit) 