import numpy as np

# Define the size and labels for two-qubit Pauli operators (4x4=16)
pauli_labels = ['II', 'IX', 'IY', 'IZ', 'XI', 'XX', 'XY', 'XZ', 'YI', 'YX', 'YY', 'YZ', 'ZI', 'ZX', 'ZY', 'ZZ']

# Initialize the 16x16 matrix M with zeros
M = np.zeros((16, 16), dtype=int)

# Fill the matrix M based on Pauli commutation relations
for i in range(16):
    for j in range(16):
        # Decompose indices into qubit components (q1, q2)
        q1_i, q2_i = divmod(i, 4)
        q1_j, q2_j = divmod(j, 4)
        
        # Check commutation on each qubit
        comm_q1 = 0 if (q1_i == 0 or q1_j == 0 or q1_i == q1_j) else 1
        comm_q2 = 0 if (q2_i == 0 or q2_j == 0 or q2_i == q2_j) else 1
        
        # Operators anti-commute if odd number of anti-commuting qubits
        M[i, j] = (comm_q1 + comm_q2) % 2

# Compute the pseudoinverse M_plus = (1/8) * M
M_plus = M / 8.0

# Print M_plus with row and column labels
print("Pseudoinverse matrix M_plus:")
print("       " + " ".join(f"{label:>6}" for label in pauli_labels))
for i, label in enumerate(pauli_labels):
    row_str = " ".join(f"{val:6.3f}" for val in M_plus[i])
    print(f"{label}: {row_str}")
