from collections import deque
from parameters import *
from simulate_sensors import update_grid_by_sensors

class MapReconstruction:
    def __init__(self, position) -> None:
        self.gridmap = [[UNKNOWN for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.change_position(position)
    
    def update(self, new_map):
        if len(new_map) != ROWS or len(new_map[0]) != COLUMNS:
            print("Error: New map has a different shape.")
            return
        for i in range(ROWS):
            for j in range(COLUMNS):
                if new_map[i][j] != UNKNOWN and self.gridmap[i][j] != PATH_TAKEN:
                    self.gridmap[i][j] = new_map[i][j]
                    

        self.gridmap[self.position[0]][self.position[1]] = CURRENT_POSITION

    def change_position(self, position):
        self.position = position
        self.gridmap[self.position[0]][self.position[1]] = CURRENT_POSITION


    def find_optimal_path(self, target_position):
        def is_valid_position(x, y):
            return 0 <= x < ROWS and 0 <= y < COLUMNS and self.gridmap[x][y] != WALL and self.gridmap[x][y] != UNKNOWN

        def get_valid_neighbors(x, y):
            neighbors = []
            deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dx, dy in deltas:
                nx, ny = x + dx, y + dy
                if is_valid_position(nx, ny):
                    neighbors.append((nx, ny))

            return neighbors

        if not self.position or not is_valid_position(*target_position):
            return None

        visited = set()
        queue = deque([(self.position, [])])

        while queue:
            current_position, path = queue.popleft()
            if current_position == target_position:
                return path + [current_position]

            if current_position in visited:
                continue
            visited.add(current_position)

            for neighbor in get_valid_neighbors(*current_position):
                queue.append((neighbor, path + [current_position]))

        return None


    def traverse(self, path, real_map):
        """
        Takes a valid path, update the map traversing through the path
        """
        for pos in path[::4]:
            update_grid_by_sensors(self, real_map)
            self.change_position(pos)
        for pos in path[:-1]:
            self.gridmap[pos[0]][pos[1]] = PATH_TAKEN
        self.change_position(path[-1])

    def get_target_position(self, policy="furthest"):
        if policy == "random":
            return self.get_target_position_random()
        if policy == "furthest":
            return self.get_target_position_furthest()
        if policy == "nearest":
            return self.get_target_position_nearest()


    def get_target_position_random(self):
        margin = 5
        for row in range(margin, ROWS-margin):
            for col in range(margin, COLUMNS-margin):
                if self.gridmap[row][col] != EMPTY:
                    continue 
                if UNKNOWN not in [self.gridmap[row+1][col], self.gridmap[row-1][col], self.gridmap[row][col+1], self.gridmap[row][col-1]]:
                    continue
                too_near_to_wall = False
                for i in range(row-margin, row+margin+1):
                    for j in range(col-margin,col-margin+1):
                        if i < 0 or i >= ROWS or j < 0 or j >= COLUMNS:
                            continue
                        if self.gridmap[i][j]==WALL:
                            too_near_to_wall = True
                if too_near_to_wall:
                    continue
                if self.find_optimal_path((row, col)) == None:
                    continue
                if (row, col) == self.position:
                    continue
                return (row, col)
            
    def get_target_position_furthest(self):
        result = None
        now_lenght = 0
        margin = 5
        for row in range(margin, ROWS-margin):
            for col in range(margin, COLUMNS-margin):
                if self.gridmap[row][col] != EMPTY:
                    continue 
                if UNKNOWN not in [
                    self.gridmap[row+1][col], 
                    self.gridmap[row-1][col], 
                    self.gridmap[row][col+1],
                    self.gridmap[row][col-1]
                ]:
                    continue
                #if WALL in [self.gridmap[row+1][col+1], self.gridmap[row+1][col], self.gridmap[row+1][col-1], self.gridmap[row][col+1], self.gridmap[row][col-1], self.gridmap[row-1][col+1], self.gridmap[row-1][col], self.gridmap[row-1][col-1]]:
                #    continue
                too_near_to_wall = False
                for i in range(row-margin, row+margin+1):
                    for j in range(col-margin,col-margin+1):
                        if i < 0 or i >= ROWS or j < 0 or j >= COLUMNS:
                            continue
                        if self.gridmap[i][j]==WALL:
                            too_near_to_wall = True
                if too_near_to_wall:
                    continue
                if (row, col) == self.position:
                    continue
                path = self.find_optimal_path((row, col))
                if path is not None and len(path) > now_lenght:
                    result = (row, col)
                    now_lenght = len(path)

        return result
    def get_target_position_nearest(self):
        result = None
        now_lenght = 1000000
        margin = 2
        for row in range(margin, ROWS-margin):
            for col in range(margin, COLUMNS-margin):
                if self.gridmap[row][col] != EMPTY:
                    continue 
                if UNKNOWN not in [
                    self.gridmap[row+1][col], 
                    self.gridmap[row-1][col], 
                    self.gridmap[row][col+1],
                    self.gridmap[row][col-1]
                ]:
                    continue
                too_near_to_wall = False
                for i in range(row-margin, row+margin+1):
                    for j in range(col-margin,col-margin+1):
                        if i < 0 or i >= ROWS or j < 0 or j >= COLUMNS:
                            continue
                        if self.gridmap[i][j]==WALL:
                            too_near_to_wall = True
                if too_near_to_wall:
                    continue
                if (row, col) == self.position:
                    continue
                path = self.find_optimal_path((row, col))
                if path is not None and len(path) < now_lenght:
                    result = (row, col)
                    now_lenght = len(path)

        return result





    

    

