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


# 构建含噪声的电路和噪声电路的输出


def noise_sim(c_mat):
    """
    对于输入的电路中, 2 qubit gate 后面插入 noise. 
    c_mat: OpenQASM 字符串或者 tensorcircuit.densitymatrix.DMCircuit 对象

    """
    if isinstance(c_mat, str):
        # print("c_mat 是字符串")
        c_mat = tc.densitymatrix.DMCircuit.from_openqasm(c_mat)


    c_mat_qir = c_mat.to_qir()


    c_mat_noise = tc.densitymatrix.DMCircuit(c_mat._nqubits)
    for index in c_mat_qir:


        if len(index['index']) >= 2:


            for jndex in index['index']:

                # 注意 noise 需要在 gate 前面加入才可以. # 这里加入 single qubit_noise
                c_mat_noise.depolarizing(jndex,px = 0.001, py = 0, pz = 0.001)

            # 这个地方可以加入任何我们想要加入的 noise, 下面试试能不能加入 2 qubit 的 noise 进去. 
            # cs = tc.channels.generaldepolarizingchannel(0.002,2)
            cs = tc.channels.generaldepolarizingchannel([0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],2)
            c_mat_noise.apply_general_kraus(cs, [[index['index'][0], index['index'][1]]])


                


            c_mat_noise.append_from_qir([index])

        else:
            c_mat_noise.append_from_qir([index])

    return c_mat_noise

c_mat_noise = noise_sim(c_mat)
print("noiseless circuit expectation:", c_mat.expectation_ps(z=[windex for windex in range(qubit_num)]))
print("noisy circuit expectation:", c_mat_noise.expectation_ps(z=[windex for windex in range(qubit_num)]))


