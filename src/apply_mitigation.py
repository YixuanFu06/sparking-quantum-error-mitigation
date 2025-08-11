import numpy as np

def project_to_simplex(v: np.ndarray) -> np.ndarray:
    """
    Project vector v onto the probability simplex using the efficient algorithm.
    
    Parameters:
    v (np.ndarray): Input vector (quasi-probability distribution)
    
    Returns:
    np.ndarray: Projected vector on probability simplex
    """
    n = len(v)
    # Sort in descending order
    u = np.sort(v)[::-1]
    
    # Find the threshold
    cumsum = np.cumsum(u)
    j = np.arange(1, n + 1)
    cond = u - (cumsum - 1) / j > 0
    
    if np.any(cond):
        rho = np.max(np.where(cond)[0])
        theta = (cumsum[rho] - 1) / (rho + 1)
    else:
        theta = (cumsum[-1] - 1) / n
    
    # Project
    return np.maximum(v - theta, 0)

def apply_mitigation(A_inv: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Apply the mitigation matrix to the input state vector.
    
    Parameters:
    A_inv (np.ndarray): The pseudoinverse of the matrix A.
    x (np.ndarray): The state vector to be mitigated.
    
    Returns:
    np.ndarray: The mitigated state vector.
    """
    # Ensure the dimensions match
    if A_inv.shape[0] != A_inv.shape[1]:
        raise ValueError("A_inv must be a square matrix.")
    if A_inv.shape[0] != x.shape[0]:
        raise ValueError("Dimensions of A and mitigation_matrix must match.")
    
    quasi_x = A_inv @ x

    # Project the quasi-probability distribution onto the simplex
    mitigated_x = project_to_simplex(quasi_x)  

    return mitigated_x

if __name__ == "__main__":
    # Example usage
    v = np.array([-0.1, 0.2, -0.2, 0.7, 0.4])
    
    u = project_to_simplex(v)
    print("Projected vector:", u)
