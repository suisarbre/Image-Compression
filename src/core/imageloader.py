from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def load_image(path):
    try:
        img = Image.open(path)
        img = img.convert('L')
        img = np.array(img)
        # plt.imshow(img, cmap='gray')
        # plt.title("Original Grayscale Image")
        # plt.axis('off')
        # plt.show()
        
    except FileNotFoundError:
        print("File not found")
        return None
    
    except Exception as e:
        print("An error occured: ", e)
        return None
    
    return img

    
if __name__ == "__main__":
    image_path = "data/input/nature-7398357_1920.jpg"  # Replace with your image path
    matrix = load_image(image_path)
    
    if matrix is not None:
        print("Image loaded successfully!")
        print(f"Image shape (height, width): {matrix.shape}")
        print(f"Pixel range: {matrix.min()} to {matrix.max()} (0=black, 255=white)")