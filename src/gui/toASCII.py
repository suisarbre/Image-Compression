from PIL import Image

def rgb_to_ascii(matrix, width = 100):
    '''Converts a greyscale matrix to ASCII art.'''
    image = Image.fromarray(matrix)
    ratio = image.width / image.height
    height = int(width * ratio)
    image = image.resize((width, height))
    
    ascii_chars = 'Ñ@#W$9876543210?!abc;:+=-,._ '
    ascii_art = []
    
    for y in range(height):
        row = []
        for x in range(width):
            r,g,b = image.getpixel((x,y))
            brightness = r * 0.299 + g * 0.587 + b * 0.114
            
            char = ascii_chars[min(int(brightness // 30), len(ascii_chars) - 1)]
            
            color_code = f"\033[38;2;{r};{g};{b}m"
            row.append(f"{color_code}{char}")

        ascii_art.append(''.join(row))
    ascii_art.append("\033[0m")
    return "\n".join(ascii_art)
    