# vera mappa
from parameters import *
import preprocessing
import pygame

def gen_maze():
    rows = ROWS
    columns = COLUMNS
    gridmap = [[EMPTY for _ in range(columns)] for _ in range(rows)]


    # disegna muri
    for i in range(rows):
        gridmap[i][0] = WALL
        gridmap[i][columns - 1] = WALL
    for i in range(columns):
        gridmap[0][i] = WALL
        gridmap[rows - 1][i] = WALL
        
    for i in range(1, rows - 5):
        if i % 10 == 0:
            if i % 20 == 0:
                for j in range(1, columns - 8):
                    gridmap[i][j] = WALL
            else:
                for j in range(8, columns - 1):
                    gridmap[i][j] = WALL
        # else:
            # gridmap[i][1] = WALL
            # gridmap[i][columns - 2] = WALL
    for i in range(10, 150):
        for j in range(10, 20):
            gridmap[i][j] = EMPTY
    for i in range(150, 250):
        for j in range(25, 35):
            gridmap[i][j] = EMPTY
    for i in range(100, 110):
        gridmap[0][i] = ENTRY
    for i in range(100, 110):
        gridmap[rows - 1][i] = EXIT

    return gridmap

def gen_maze_2():
    gridmap = preprocessing.image_to_matrix("maze2.PNG")
    for i in range(47, 53):
        gridmap[i][0] = ENTRY
    for i in range(47, 53):
        gridmap[i][ROWS - 1] = EXIT
    return gridmap




if __name__ == "__main__":
    print(gen_maze_2())
