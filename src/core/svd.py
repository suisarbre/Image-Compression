import numpy as np

def compute_svd(matrix):
    try:
        U_r, sigma_r, Vt_r = np.linalg.svd(matrix[:,:,0], full_matrices=False)
        U_g, sigma_g, Vt_g = np.linalg.svd(matrix[:,:,1], full_matrices=False)
        U_b, sigma_b, Vt_b = np.linalg.svd(matrix[:,:,2], full_matrices=False)
        
    except Exception as e:
        print("An error occured: ", e)
        return None
    
    return (U_r, sigma_r, Vt_r), (U_g, sigma_g, Vt_g), (U_b, sigma_b, Vt_b)

def compress(U_r, sigma_r, Vt_r, U_g, sigma_g, Vt_g, U_b,sigma_b, Vt_b, k=50):
    """Compress each channel and merge them."""
    # Compress Red channel
    compressed_r = U_r[:, :k] @ np.diag(sigma_r[:k]) @ Vt_r[:k, :]
    
    # Compress Green channel
    compressed_g = U_g[:, :k] @ np.diag(sigma_g[:k]) @ Vt_g[:k, :]
    
    # Compress Blue channel
    compressed_b = U_b[:, :k] @ np.diag(sigma_b[:k]) @ Vt_b[:k, :]
    
    # Merge channels and clip to 0-255
    compressed = np.stack([compressed_r, compressed_g, compressed_b], axis=2)
    compressed = np.clip(compressed, 0, 255).astype(np.uint8)
    
    return compressed

def calculate_metrics(original, compressed, k):
    # Compression ratio
    original_size = original.shape[0] * original.shape[1]
    compressed_size = k * (original.shape[0] + original.shape[1] + 1)
    ratio = original_size / compressed_size
    
    # Mean Squared Error (MSE)
    mse = np.mean((original - compressed) ** 2)
    
    return ratio, mse