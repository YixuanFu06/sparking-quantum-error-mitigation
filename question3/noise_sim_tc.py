import tensorcircuit as tc
from tensorcircuit.channels import amplitudedampingchannel
import numpy as np


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


            # for jndex in index['index']:

            #     # 注意 noise 需要在 gate 前面加入才可以. # 这里加入 single qubit_noise
            #     c_mat_noise.depolarizing(jndex,px = 0.001, py = 0, pz = 0.001)

            # 这个地方可以加入任何我们想要加入的 noise, 下面试试能不能加入 2 qubit 的 noise 进去. 
            # cs = tc.channels.generaldepolarizingchannel(0.002,2)
            cs = tc.channels.generaldepolarizingchannel([1.68e-3,1.65e-3,1.2e-3,8.28e-4,3.53e-4,0,9.94e-4,1.06e-3,6.87e-5,0,8.53e-4,1.08e-3,1.26e-3,1.47e-3,0],2)
            c_mat_noise.apply_general_kraus(cs, [[index['index'][0], index['index'][1]]])


                


            c_mat_noise.append_from_qir([index])

        else:
            c_mat_noise.append_from_qir([index])

    return c_mat_noise
