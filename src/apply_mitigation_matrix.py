import os
import numpy as np

from edit_module import add_measure_commands, remove_measure_commands
from get_readout_pseudoinverse import get_mitigation_matrix
from mitigation import apply_mitigation, apply_mitigation_locality

TOKEN = 'W6QyiJRRS.DFibko9DVIuZwdqoTa5mGtl8HxoIYy4pfCPMTwhBztGrnXovVzUT0L6c-7nilqVxg1lcWd7Fj0pmLHvmb9RmA8TD8fSndBorSlfdVxPcJRQuKs.R5M9Ecu6G5DyJaAPwULZPs5r6H23G8='

def apply_mitigation_matrix(qubits_num: int, shots: int, measure_results: dict, token=TOKEN, locality=False) -> np.ndarray:
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

    DATA_DIR = "../data"
    if locality:
        MAT_PATH = f"{DATA_DIR}/{qubits_num}qubits_readout_matrix_pseudoinverse_locality.npy"
    else:
        MAT_PATH = f"{DATA_DIR}/{qubits_num}qubits_readout_matrix_pseudoinverse.npy"

    if not os.path.exists(MAT_PATH):
        print(f"Mitigation matrix not found at {MAT_PATH}. Generating it...")
        A_inv = get_mitigation_matrix(qubits_num, shots=shots, token=token, locality=locality)
    else:
        print(f"Loading mitigation matrix from {MAT_PATH}...")
        A_inv = np.load(MAT_PATH)

    if locality:
        if A_inv.shape[0] != qubits_num or A_inv.shape[1] != 2 or A_inv.shape[2] != 2:
            raise ValueError("A_inv must be a 3D tensor of shape (qubits_num, 2, 2) for locality.")
        # convert the n * 2 * 2 matrix [A_inv0, A_inv1, ..., A_inv{n-1}] to a single 2^n * 2^n matrix
        A_inv_tensor_product = A_inv[0]
        for i in range(1, qubits_num):
            A_inv_tensor_product = np.kron(A_inv_tensor_product, A_inv[i])
        A_inv = A_inv_tensor_product
    else:
        if A_inv.shape[0] != 2**qubits_num or A_inv.shape[1] != 2**qubits_num:
            raise ValueError("A_inv must be a square matrix of shape (2^n, 2^n).")

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


if __name__ == "__main__":
    n = 9
    shots = 8092

    add_measure_commands(n)
    import tensorcircuit as tc
    from tensorcircuit.cloud import apis

    def construct_circuit(n) -> tc.Circuit:
        c = tc.Circuit(n)

        for i in range(n):
            c.h(i)

        return c

    c = construct_circuit(n)
    ts = apis.submit_task(provider="tencent", device='tianji_s2', circuit=c, shots=shots)
    print(ts.results())
    mitigated_distribution = apply_mitigation_matrix(n, shots, ts.results(), token=TOKEN, locality=True)

    remove_measure_commands()
