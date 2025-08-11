import os
import numpy as np

from edit_module import add_measure_commands, remove_measure_commands
from get_readout_pseudoinverse import get_mitigation_matrix
from mitigation import apply_mitigation, apply_mitigation_locality

TOKEN = 'W6QyiJRRS.DFibko9DVIuZwdqoTa5mGtl8HxoIYy4pfCPMTwhBztGrnXovVzUT0L6c-7nilqVxg1lcWd7Fj0pmLHvmb9RmA8TD8fSndBorSlfdVxPcJRQuKs.R5M9Ecu6G5DyJaAPwULZPs5r6H23G8='

def apply_mitigation_matrix(qubits_num: int, shots: int, measure_results: dict, token=TOKEN) -> np.ndarray:
    '''
    应用readout error缓解矩阵到测量结果
    Parameters:
    -----------
    qubits_num : int
        量子比特数量
    shots : int
        每个态的测量次数
    measure_results : dict
        测量结果字典，格式为 {bitstring: count}
    Returns:
    --------
    mitigated_distribution : np.ndarray
        缓解后的分布，形状为 (2^qubits_num,)
    '''

    MAT_PATH = f"../data/{qubits_num}qubits_readout_matrix_pseudoinverse.npy"
    if not os.path.exists(MAT_PATH):
        print(f"Mitigation matrix not found at {MAT_PATH}. Generating it...")
        A_inv = get_mitigation_matrix(qubits_num, shots=shots, token=token, locality=False)
    else:
        print(f"Loading mitigation matrix from {MAT_PATH}...")
        A_inv = np.load(MAT_PATH)

    measured_distribution = np.zeros(2**qubits_num)

    for measured_bitstring, count in measure_results.items():
        if len(measured_bitstring) == qubits_num:
            measured_state = int(measured_bitstring, 2)
            probability = count / shots
            measured_distribution[measured_state] = probability

    print("Measured distribution (with readout error):")
    print(measured_distribution)

    mitigated_distribution = apply_mitigation(A_inv, measured_distribution)

    print("Mitigated distribution:")
    print(mitigated_distribution)

    return mitigated_distribution

def apply_mitigation_matrix_locality(qubits_num: int, shots: int, measure_results: np.ndarray, qubit_index: int, token=TOKEN) -> np.ndarray:
    '''
    应用readout error缓解矩阵到单个量子比特的测量结果（基于locality假设）
    Parameters:
    -----------
    qubits_num : int
        量子比特数量
    shots : int
        每个态的测量次数
    measure_results : np.ndarray
        形状为 (2,)
    qubit_index : int
        需要缓解的量子比特索引（0-based）
    Returns:
    --------
    mitigated_distribution : np.ndarray
        缓解后的单个量子比特分布，形状为 (2,)
    '''

    MAT_PATH = f"../data/{qubits_num}qubits_readout_matrix_pseudoinverse.npy"
    if not os.path.exists(MAT_PATH):
        print(f"Mitigation matrix not found at {MAT_PATH}. Generating it...")
        A_inv = get_mitigation_matrix(qubits_num, shots=shots, token=token, locality=True)
    else:
        print(f"Loading mitigation matrix from {MAT_PATH}...")
        A_inv = np.load(MAT_PATH)

    print(f"Measured marginal distribution for qubit {qubit_index} (with readout error):")
    print(measure_results)

    mitigated_distribution = apply_mitigation_locality(A_inv, measure_results, qubit_index)

    print(f"Mitigated marginal distribution for qubit {qubit_index}:")
    print(mitigated_distribution)

    return mitigated_distribution


if __name__ == "__main__":
    n = 2
    shots = 8092

    add_measure_commands(n)
    import tensorcircuit as tc
    from tensorcircuit.cloud import apis

    def construct_circuit(n) -> tc.Circuit:
        c = tc.Circuit(n)

        c.x(1)
        if n > 1:
            c.cx(1, 0)

        return c

    c = construct_circuit(n)
    ts = apis.submit_task(provider="tencent", device='tianji_s2', circuit=c, shots=shots)
    print(ts.results())
    mitigated_distribution = apply_mitigation_matrix(n, shots, ts.results(), token=TOKEN)
    # mitigated_distribution = apply_mitigation_matrix_locality(n, shots, ts.results(), token=TOKEN)

    remove_measure_commands()
