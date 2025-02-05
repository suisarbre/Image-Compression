import numpy as np

def compute_svd(matrix):
    try:
        U, sigma, Vt = np.linalg.svd(matrix, full_matrices=False)
        
    except Exception as e:
        print("An error occured: ", e)
        return None
    
    return U, sigma, Vt

def compress(U, sigma, Vt, k=50):
    """
    Compress the image by keeping the top `k` singular values.
    Returns the reconstructed (compressed) matrix.
    """
    # Truncate matrices
    U_k = U[:, :k]          # First k columns of U
    sigma_k = sigma[:k]     # First k singular values
    Vt_k = Vt[:k, :]       # First k rows of Vt
    
    # Reconstruct the compressed matrix
    reconstructed = U_k @ np.diag(sigma_k) @ Vt_k
    
    # Clip values to 0-255 and convert back to uint8
    reconstructed = np.clip(reconstructed, 0, 255)
    return reconstructed.astype(np.uint8)

def calculate_metrics(original, compressed, k):
    # Compression ratio
    original_size = original.shape[0] * original.shape[1]
    compressed_size = k * (original.shape[0] + original.shape[1] + 1)
    ratio = original_size / compressed_size
    
    # Mean Squared Error (MSE)
    mse = np.mean((original - compressed) ** 2)
    
    return ratio, mse