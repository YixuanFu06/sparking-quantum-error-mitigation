import numpy as np
import os

from edit_module import add_measure_commands, remove_measure_commands
from pseudoinverse import pseudoinverse, pseudoinverse_locality

TOKEN = 'W6QyiJRRS.DFibko9DVIuZwdqoTa5mGtl8HxoIYy4pfCPMTwhBztGrnXovVzUT0L6c-7nilqVxg1lcWd7Fj0pmLHvmb9RmA8TD8fSndBorSlfdVxPcJRQuKs.R5M9Ecu6G5DyJaAPwULZPs5r6H23G8='

def get_mitigation_matrix(qubits_num: int, shots=8092, token=TOKEN, locality=False) -> np.ndarray:
    """
    获取n比特量子比特的readout error缓解矩阵
    
    Parameters:
    -----------
    n : int
        量子比特数量
    shots : int
        每个态的测量次数
        
    Returns:
    --------
    mitigation_matrix : np.ndarray, shape (2^n, 2^n)
        readout error缓解矩阵
    """

    add_measure_commands(qubits_num)  # 添加测量命令

    from readout_matrix import measure_readout_error_matrix, measure_readout_error_matrix_locality

    if locality:
        readout_matrix = measure_readout_error_matrix_locality(qubits_num, shots=shots, token=token)
    else:
        readout_matrix = measure_readout_error_matrix(qubits_num, shots=shots, token=token)
    print("Measured full readout error matrix:")
    print(readout_matrix)

    if locality:
        readout_matrix_inv = pseudoinverse_locality(readout_matrix)
    else:
        readout_matrix_inv = pseudoinverse(readout_matrix)
    print("Pseudoinverse of the readout error matrix:")
    print(readout_matrix_inv)

    # Save the matrices for later use
    DATA_DIR = "../data"
    if locality:
        MAT_PATH = f"{DATA_DIR}/{qubits_num}qubits_readout_matrix_pseudoinverse_locality.npy"
    else:
        MAT_PATH = f"{DATA_DIR}/{qubits_num}qubits_readout_matrix_pseudoinverse.npy"
    # make sure the directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    np.save(MAT_PATH, readout_matrix_inv)

    print(f"Saved readout matrix and its pseudoinverse to {MAT_PATH}")

    remove_measure_commands()  # 移除测量命令

    return readout_matrix_inv


if __name__ == "__main__":
    qubits_num = 4  # Number of qubits
    get_mitigation_matrix(qubits_num, shots=8092, token=TOKEN, locality=True)
