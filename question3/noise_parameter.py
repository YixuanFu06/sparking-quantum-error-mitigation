import tensorcircuit as tc
import numpy as np
from scipy.linalg import lstsq
from tensorcircuit.channels import amplitudedampingchannel

tc.set_backend("numpy")

I = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = [I, X, Y, Z]
PAULI_LABELS = ['I', 'X', 'Y', 'Z']

PAULIS_2Q = [np.kron(p1, p2) for p1 in PAULIS for p2 in PAULIS]
PAULI_LABELS_2Q = [l1 + l2 for l1 in PAULI_LABELS for l2 in PAULI_LABELS]

def do_commute(A, B):
    return np.allclose(A @ B, B @ A)

def apply_pauli_gate(circuit, pauli_index, qubits=[0, 1]):
    
    qubit0_pauli = pauli_index // 4  
    qubit1_pauli = pauli_index % 4  
    
    if qubit0_pauli == 1:  
        circuit.x(qubits[0])
    elif qubit0_pauli == 2: 
        circuit.y(qubits[0])
    elif qubit0_pauli == 3: 
        circuit.z(qubits[0])

    if qubit1_pauli == 1:   
        circuit.x(qubits[1])
    elif qubit1_pauli == 2:
        circuit.y(qubits[1])
    elif qubit1_pauli == 3:
        circuit.z(qubits[1])
    
    return circuit

def measure_pauli_expectation(circuit, pauli_k_index):
    
    dm = circuit.state()
    
    if len(dm.shape) == 1:
        dm = np.outer(dm, dm.conj())
    
    P_k = PAULIS_2Q[pauli_k_index]
    
    expectation = np.real(np.trace(dm @ P_k))
    return expectation

def pauli_twirling_experiment(pauli_k_index):

    twirled_sum = 0.0
    
    for g_index in range(16):

        exp_circuit = tc.Circuit(2)
        
        exp_circuit = apply_pauli_gate(exp_circuit, g_index)
        
        exp_circuit = apply_pauli_gate(exp_circuit, pauli_k_index)
        
        exp_circuit = apply_pauli_gate(exp_circuit, g_index)
        
        exp_circuit.cz(0, 1)
        exp_circuit.apply_channel(secret_noise_channel)
        
        exp_circuit = apply_pauli_gate(exp_circuit, g_index)
        
        expectation = measure_pauli_expectation(exp_circuit, pauli_k_index)
        
        twirled_sum += expectation
    
    twirled_expectation = twirled_sum / 16.0
  
    f_k = (twirled_expectation + 1.0) / 2.0

    return f_k


gamma = 0.1
secret_noise_channel = amplitudedampingchannel(gamma, q=[0], nq=2)

c = tc.Circuit(2)  
c.cz(0, 1)         
c.apply_channel(secret_noise_channel) 
fidelities = []

for k in range(1, 16):  
    f_k = pauli_twirling_experiment(k)
    fidelities.append(f_k)
    
M = np.zeros((15, 15))
for k in range(15):
    for j in range(15):
        P_k = PAULIS_2Q[k+1]
        P_j = PAULIS_2Q[j+1]
        if not do_commute(P_k, P_j):
            M[k, j] = 1

f_vector = np.array(fidelities)
y_vector = -np.log(f_vector) / 2

lambda_solved, residuals, rank, s = lstsq(M, y_vector)

for k in range(15):
    label = PAULI_LABELS_2Q[k+1]
    print(f"λ_{label} = {lambda_solved[k]:.4f}")