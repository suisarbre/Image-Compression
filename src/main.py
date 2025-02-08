from core.imageloader import load_image
from core.svd import *
import matplotlib.pyplot as plt
from gui.toASCII import rgb_to_ascii

# Load the image
matrix = load_image("data/input/nature-7398357_1920.jpg")

if matrix is not None:
    print(rgb_to_ascii(matrix,100))