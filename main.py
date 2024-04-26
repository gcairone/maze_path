import pygame
import sys
import maze_gen
import path_planning
from parameters import *
from simulate_sensors import *
import preprocessing


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

CELL_SIZE = 7
MARGIN = 1

color_map = {
    0: WHITE, # EMPTY
    1: BLACK, # WALL
    2: GREY, # UNKNOWN
    3: GREEN, # ENTRY
    4: YELLOW, # EXIT
    5: BLUE, # POSITION
    6: RED # PATH TAKEN
}



def draw_matrix(screen, matrix):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            color = color_map.get(cell, YELLOW)  # Giallo per valori non mappati
            pygame.draw.rect(screen, color, (x * (CELL_SIZE + MARGIN), y * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE))



def scan_choose_move(real_map, grid_r):

    
    update_grid_by_sensors(grid_r, real_map)
    
    
    # choose target cell
    ex = find_exit(grid_r)
    if ex is None:
        target_pos = grid_r.get_target_position(policy="furthest")
    else:
        target_pos = ex
        print("Exit found")
    print(f"Pos chosen:{target_pos}")

    if(target_pos==None):
        raise ValueError("TARGET POS NOT FOUNDED")

    path = grid_r.find_optimal_path(target_pos)
        
    grid_r.traverse(path, real_map)
    print(f"Map updated")



def main():
    pygame.init()
    
    matrix_generated = maze_gen.gen_maze_2()

    grid_r = path_planning.MapReconstruction(position=(50, 2))

    matrix = grid_r.gridmap
    rows = len(matrix)
    cols = len(matrix[0])
    WINDOW_SIZE = (cols * (CELL_SIZE + MARGIN), rows * (CELL_SIZE + MARGIN))

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Matrix Color")

    screen.fill(WHITE)
    draw_matrix(screen, matrix)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scan_choose_move(matrix_generated, grid_r)
                    draw_matrix(screen, matrix)
                    print("Screen updated")
                    print()

        pygame.display.flip()

if __name__ == "__main__":
    main()
