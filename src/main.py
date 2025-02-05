from core.imageloader import load_image
from core.svd import *
import matplotlib.pyplot as plt
# Load the image
matrix = load_image("data/input/nature-7398357_1920.jpg")

if matrix is not None:
    U, sigma, Vt = compute_svd(matrix)
    print(f"U shape: {U.shape}")
    print(f"Sigma length: {len(sigma)}")
    print(f"Vt shape: {Vt.shape}")
    
    k = 50
    compressed = compress(U, sigma, Vt, k)

    # Plot original vs compressed
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(matrix, cmap='gray')
    plt.title(f"Original (Rank {min(matrix.shape)})")

    plt.subplot(1, 2, 2)
    plt.imshow(compressed, cmap='gray')
    plt.title(f"Compressed (k={k}, Rank {k})")
    plt.show()
    
    print(calculate_metrics(matrix, compressed, k))