from PIL import Image
from parameters import *

def image_to_matrix(image_path):
    WALL_THRESHOLD = 128  

    image = Image.open(image_path)
    image = image.resize((COLUMNS, ROWS))

    image = image.convert("L")  

    width, height = image.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            if pixel_value < WALL_THRESHOLD:
                row.append(WALL)
            else:
                row.append(EMPTY)
        matrix.append(row)

    return matrix
"""
maze_matrix = image_to_matrix("maze_img.PNG")

# Print the matrix (for demonstration)
for row in maze_matrix:
    print(row)
"""