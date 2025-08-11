import numpy as np
import tensorcircuit as tc

def create_circuit_with_prep_0(n):
    """制备所有量子比特为|0⟩态"""
    circuit = tc.Circuit(n)
    return circuit

def create_circuit_with_prep_1(n):
    """制备所有量子比特为|1⟩态"""
    circuit = tc.Circuit(n)
    for i in range(n):
        circuit.x(i)
    return circuit

def execute_and_measure(circuit, shots=10000):
    return circuit.execute(shots=shots)

def measure_readout_error_local(n, shots=10000):
    """
    利用量子比特间不相互干扰的假设，并行测量所有量子比特的readout error
    通过多比特并行测量提高效率
    """
    # 初始化 N×2×2 的张量
    readout_tensor = np.zeros((n, 2, 2))
    
    # 所有量子比特制备为|0⟩态并测量
    circuit_all_0 = create_circuit_with_prep_0(n)
    counts_all_0 = execute_and_measure(circuit_all_0, shots)
    
    # 所有量子比特制备为|1⟩态并测量
    circuit_all_1 = create_circuit_with_prep_1(n)
    counts_all_1 = execute_and_measure(circuit_all_1, shots)
    
    # 从多比特测量结果中提取单比特统计
    for qubit in range(n):
        # 统计|0⟩制备态下第qubit位的测量结果
        count_0_measured_0 = 0
        count_0_measured_1 = 0
        
        for bitstring, count in counts_all_0.items():
            if len(bitstring) == n:
                measured_bit = int(bitstring[n-1-qubit])  # 注意比特顺序
                if measured_bit == 0:
                    count_0_measured_0 += count
                else:
                    count_0_measured_1 += count
        
        # 统计|1⟩制备态下第qubit位的测量结果
        count_1_measured_0 = 0
        count_1_measured_1 = 0
        
        for bitstring, count in counts_all_1.items():
            if len(bitstring) == n:
                measured_bit = int(bitstring[n-1-qubit])  # 注意比特顺序
                if measured_bit == 0:
                    count_1_measured_0 += count
                else:
                    count_1_measured_1 += count
        
        # 计算概率
        p00 = count_0_measured_0 / shots
        p01 = count_0_measured_1 / shots
        p10 = count_1_measured_0 / shots
        p11 = count_1_measured_1 / shots
        
        # 存储到张量中
        readout_tensor[qubit, 0, 0] = p00
        readout_tensor[qubit, 0, 1] = p01
        readout_tensor[qubit, 1, 0] = p10
        readout_tensor[qubit, 1, 1] = p11
    
    return readout_tensor


def analyze_readout_tensor(readout_tensor):
    """分析N×2×2 readout error张量"""
    n_qubits = readout_tensor.shape[0]
    
    print(f"Readout Error Analysis for {n_qubits} qubits:")
    print("=" * 50)
    
    for qubit in range(n_qubits):
        print(f"\nQubit {qubit}:")
        print(f"  P(0|0) = {readout_tensor[qubit, 0, 0]:.4f}")
        print(f"  P(1|0) = {readout_tensor[qubit, 0, 1]:.4f}")
        print(f"  P(0|1) = {readout_tensor[qubit, 1, 0]:.4f}")
        print(f"  P(1|1) = {readout_tensor[qubit, 1, 1]:.4f}")
        
        # 计算保真度
        fidelity_0 = readout_tensor[qubit, 0, 0]
        fidelity_1 = readout_tensor[qubit, 1, 1]
        avg_fidelity = (fidelity_0 + fidelity_1) / 2
        print(f"  Average Readout Fidelity = {avg_fidelity:.4f}")
    
    # 整体统计
    overall_fidelity = np.mean([readout_tensor[:, 0, 0], readout_tensor[:, 1, 1]])
    print(f"\nOverall Average Readout Fidelity: {overall_fidelity:.4f}")
    
    return readout_tensor


def get_readout_matrix_for_qubit(readout_tensor, qubit_idx):
    """获取特定量子比特的2×2 readout error矩阵"""
    return readout_tensor[qubit_idx]


# 使用示例
if __name__ == "__main__":
    # 测量4个量子比特的readout error
    n_qubits = 4
    
    print("多比特并行测量（利用无干扰假设）")
    readout_data = measure_readout_error_local(n_qubits, shots=10000)
    analyze_readout_tensor(readout_data)
    
    # 获取特定量子比特的矩阵
    qubit_0_matrix = get_readout_matrix_for_qubit(readout_data, 0)
    print(f"\nQubit 0 readout matrix:\n{qubit_0_matrix}")