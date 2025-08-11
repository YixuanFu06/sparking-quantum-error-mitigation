from noise_sim_tc import noise_sim
import tensorcircuit as tc
from tensorcircuit.channels import amplitudedampingchannel
import numpy as np

# 从 txt 文件读取电路

qubit_num = 6 # 我们读取一个 6 qubit 的 Ising model 的演化电路. 

with open("openqasm_str.txt", "r", encoding="utf-8") as f:
    openqasm_str = f.read()

print("电路: ", openqasm_str)

# 转换为 tc 格式的电路并且输出
c_mat = tc.densitymatrix.DMCircuit.from_openqasm(openqasm_str)
print("noise-free circuit expectation:", c_mat.expectation_ps(z=[windex for windex in range(qubit_num)]))
c_mat.draw()

c_mat_noise = noise_sim(c_mat)
print("noiseless circuit expectation:", c_mat.expectation_ps(z=[windex for windex in range(qubit_num)]))
print("noisy circuit expectation:", c_mat_noise.expectation_ps(z=[windex for windex in range(qubit_num)]))