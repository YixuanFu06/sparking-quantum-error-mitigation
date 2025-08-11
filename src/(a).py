import numpy as np
import tensorcircuit as tc
import warnings
from itertools import product

warnings.filterwarnings('ignore')

def create_circuit_with_prep_state(n, target_state):
    """
    制备指定的n比特经典态
    
    Parameters:
    -----------
    n : int
        量子比特数量
    target_state : str or int
        目标态，可以是二进制字符串'101'或整数5
        
    Returns:
    --------
    circuit : tc.Circuit
        制备指定态的量子线路
    """
    circuit = tc.Circuit(n)
    
    # 转换为二进制字符串
    if isinstance(target_state, int):
        target_state = format(target_state, f'0{n}b')
    
    # 对每个应该为|1⟩的量子比特应用X门
    for i, bit in enumerate(target_state):
        if bit == '1':
            circuit.x(i)
    
    return circuit


def execute_and_measure(circuit, shots=10000):
    """执行量子线路并测量"""
    return circuit.execute(shots=shots)


def measure_full_readout_error_matrix(n, shots=10000):
    """
    不基于locality假设，测量完整的readout error矩阵
    
    对于n个量子比特，readout error矩阵A是2^n × 2^n的矩阵
    A[i,j] = P(测量到态i | 制备态j)
    
    Parameters:
    -----------
    n : int
        量子比特数量
    shots : int
        每个态的测量次数
        
    Returns:
    --------
    readout_matrix : np.ndarray, shape (2^n, 2^n)
        完整的readout error矩阵
    """
    n_states = 2**n
    readout_matrix = np.zeros((n_states, n_states))
    
    
    for prepared_state in range(n_states):
        prepared_bitstring = format(prepared_state, f'0{n}b')
        print(f"制备态 |{prepared_bitstring}⟩ ({prepared_state+1}/{n_states})...")
        
        # 制备目标态
        circuit = create_circuit_with_prep_state(n, prepared_state)
        
        # 重复测量
        counts = execute_and_measure(circuit, shots)
        
        # 统计每个测量结果的概率
        for measured_bitstring, count in counts.items():
            if len(measured_bitstring) == n:
                measured_state = int(measured_bitstring, 2)
                probability = count / shots
                
                # A[measured_state, prepared_state] = P(测量到measured | 制备prepared)
                readout_matrix[measured_state, prepared_state] = probability
        
        # 显示该制备态的主要测量结果
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        top_results = sorted_counts[:min(3, len(sorted_counts))]
        print(f"  主要测量结果: {[(bs, f'{c/shots:.3f}') for bs, c in top_results]}")
        print()
    
    return readout_matrix