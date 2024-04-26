from parameters import *
import random

def simulate_scan(real_map, position):
    lidar_map = [[UNKNOWN for _ in range(COLUMNS)] for _ in range(ROWS)]

    for row in range(ROWS):
        for col in range(COLUMNS):
            if (row, col) == position:
                continue
            
            
            if is_visible(real_map, position, (row, col)):
                lidar_map[row][col] = real_map[row][col]

    return lidar_map

def is_visible(real_map, start, end):
    # Bresenham's line algorithm 
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        if real_map[x0][y0] == WALL:
            return False
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return True




def simulate_gaussian_sensors(real_map, position, probability_decay_factor=5, num_cells=200):
    info_map = [[UNKNOWN for _ in range(COLUMNS)] for _ in range(ROWS)]
    
    for _ in range(num_cells):
        row_offset = int(random.gauss(0, probability_decay_factor))
        col_offset = int(random.gauss(0, probability_decay_factor))
        row = max(0, min(position[0] + row_offset, ROWS - 1))
        col = max(0, min(position[1] + col_offset, COLUMNS - 1))
        
        info_map[row][col] = real_map[row][col]
    
    return info_map

def simulate_circle_sensors(real_map, position, radius=10):
    info_map = [[UNKNOWN for _ in range(COLUMNS)] for _ in range(ROWS)]
    
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (position[0]-row)**2 + (position[1]-col)**2 < radius**2:
                info_map[row][col] = real_map[row][col]
    
    return info_map





def update_grid_by_sensors(grid_r, real_map):

    
    matrix_sensors = simulate_circle_sensors(real_map, grid_r.position, 15)
    grid_r.update(matrix_sensors)




def find_exit(grid_r):
    # return exit 
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid_r.gridmap[row][col] == EXIT:
                return (row, col)
    return None