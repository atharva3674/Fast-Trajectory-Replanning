import numpy
import time
import random
from statistics import mean, stdev
import sys
import math
import heapq
from heapq import heappop, heappush, heapify
import buildGrid
from buildGrid import Grid
from minHeap import MinHeap

class Cell: 
    def __init__(self, coordinate, parent=None, f_val=0, g_val=0, h_val=0):
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.parent = parent
        self.f_value = f_val
        self.g_value = g_val
        self.h_value = h_val
    
# 0 is obstacle, 1 good

cells_expanded = 0

def repeated_adaptive_AStar(initial, goal, grid):

    start = Cell(initial)
    end = Cell(goal)
    cells = {} # dictionary
    cells[initial] = start # initial and goal are tuples of the coordinates
    cells[goal] = end
    master_path = [initial] # entire path that agent follows from initial to goal

    number_rows = len(grid)
    number_columns = len(grid[0])

    current = start

    # add the blocked states in our initial field of view to our dictionary, make sure coordinates in line 
    # neighbors of current cell
    neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

    for neighbor in neighbors:
        # if coordinate is in bounds then continue to next neighboring position
        if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
            # it is an obstacle, take note of it
            if grid[neighbor[1]][neighbor[0]] == 0:
                temp_cell = Cell(initial, current)
                temp_cell.g_value = float('inf')
                temp_cell.h_value = computeManhattan(temp_cell, end)
                temp_cell.f_value = temp_cell.g_value
                cells[neighbor] = temp_cell

    
    while not(current.x == end.x and current.y == end.y):
        
        # PLANNING
        start_A_Star = current        
        cell = forward_adaptive_AStar(start_A_Star, end, cells, grid)
        
        path = []
        
        # build path and update h-values
        goal_g_value = end.g_value

        while not(cell.x == current.x and cell.y == current.y):
            path.append((cell.x, cell.y))
            cell.h_value = goal_g_value - cell.g_value

            cell = cell.parent

        cell.h_value = goal_g_value - cell.g_value

        #print(path)

        # EXECUTION 
        
        for i in range(len(path)-1, -1, -1):
            
            # check if next coordinate is an obstacle
            next_x_coordinate = path[i][0]
            next_y_coordinate = path[i][1]
            
            if grid[next_y_coordinate][next_x_coordinate] == 0:
                # don't move there
                cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
                cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
                break

            else:
                # move current to next cell
                current = cells[(next_x_coordinate, next_y_coordinate)]
                # add the coordinate to the master path - because the coordinate is not an obstacle
                master_path.append((next_x_coordinate, next_y_coordinate))

                # after moving cell, observe directly adjacent cells in vision to see if they are obstacles
                neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

                for neighbor in neighbors:
                    # if coordinate is in bounds then continue to next neighboring position
                    if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                        # it is an obstacle, take note of it
                        if grid[neighbor[1]][neighbor[0]] == 0:
                            temp_cell = Cell(initial, current)
                            temp_cell.g_value = float('inf')
                            temp_cell.h_value = computeManhattan(temp_cell, end)
                            temp_cell.f_value = temp_cell.g_value
                            cells[neighbor] = temp_cell
                
    #print(master_path)

    return master_path


def repeated_forward_AStar(initial, goal, grid):

    start = Cell(initial)
    end = Cell(goal)
    cells = {} # dictionary
    cells[initial] = start # initial and goal are tuples of the coordinates
    cells[goal] = end
    master_path = [initial] # entire path that agent follows from initial to goal

    number_rows = len(grid)
    number_columns = len(grid[0])

    current = start

    # add the blocked states in our initial field of view to our dictionary, make sure coordinates in line 
    # neighbors of current cell
    neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

    for neighbor in neighbors:
        # if coordinate is in bounds then continue to next neighboring position
        if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
            # it is an obstacle, take note of it
            if grid[neighbor[1]][neighbor[0]] == 0:
                temp_cell = Cell(initial, current)
                temp_cell.g_value = float('inf')
                temp_cell.h_value = computeManhattan(temp_cell, end)
                temp_cell.f_value = temp_cell.g_value
                cells[neighbor] = temp_cell

    # while agent is not at end cell
    while not(current.x == end.x and current.y == end.y):

        # PLANNING     
        cell = forward_AStar(current, end, cells, grid)
        path = []
        
        # build path
        while not(cell.x == current.x and cell.y == current.y):
            path.append((cell.x, cell.y))
            cell = cell.parent

        # Note: current cell isn't ever appended to the path list

        print(path)
   
        # EXECUTION 
        
        for i in range(len(path)-1, -1, -1):
            
            # check if next coordinate is an obstacle  (x,y)
            next_x_coordinate = path[i][0]
            next_y_coordinate = path[i][1]
            
            if grid[next_y_coordinate][next_x_coordinate] == 0:
                # don't move there
                cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
                cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
                break

            else:
                # move current to next cell
                current = cells[(next_x_coordinate, next_y_coordinate)]
                # add the coordinate to the master path - because the coordinate is not an obstacle
                master_path.append((next_x_coordinate, next_y_coordinate))

                # after moving cell, observe directly adjacent cells in vision to see if they are obstacles
                neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

                for neighbor in neighbors:
                    # if coordinate is in bounds then continue to next neighboring position
                    if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                        # it is an obstacle, take note of it
                        if grid[neighbor[1]][neighbor[0]] == 0:
                            # cell already exists
                            if (neighbor[0], neighbor[1]) in cells:
                                cells[neighbor].g_value = float('inf')
                                cells[neighbor].f_value = float('inf')
                            # creating new cell
                            else:
                                temp_cell = Cell(initial, current)
                                temp_cell.g_value = float('inf')
                                temp_cell.h_value = computeManhattan(temp_cell, end)
                                temp_cell.f_value = temp_cell.g_value
                                cells[neighbor] = temp_cell
            
    #print(master_path)
    
    return master_path

    
# pass in initial and goal as references to Cell objects
def forward_AStar(initial, goal, cells, grid):
    
    global cells_expanded
    
    #open_list = []
    
    # reset g-value of starting cell during each call of A*
    initial.g_value = 0
    initial.f_value = initial.h_value

    number_rows = len(grid)
    number_columns = len(grid[0])
    
    #heappush(open_list, (initial.f_value, initial.g_value, random.random(), initial))
    open_list = MinHeap()
    open_list.heappush((initial.f_value, initial.g_value, random.random(), initial))
    closed_list = set()

    # set pointer to initial cell
    current = initial

    while open_list.length() > 0:
        # pop smallest f-value in open list (if multiple cells with same f-value, use one with larger g-value)
        #current_f_value, current_g_value, current_tiebreaker, current = heappop(open_list)
        current_f_value, current_g_value, current_tiebreaker, current = open_list.heappop()
        
        if (current.x, current.y) in closed_list:
            continue

        cells_expanded += 1
        # add cell to closed list
        closed_list.add((current.x, current.y))

        if current.x == goal.x and current.y == goal.y:
            return current

        # neighbors of current cell
        neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

        for neighbor in neighbors:
            # if coordinates are not in bounds then continue to next neighboring position
            if not (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                continue
            # if neighbor is in closed list, ignore it
            if (neighbor[0], neighbor[1]) in closed_list:
                continue
            else:
                # cell needs to be created
                if neighbor not in cells:
                    temp_cell = Cell(neighbor, current)
                    cells[neighbor] = temp_cell # add cell to dictionary so it can be referenced later
                    temp_g = current.g_value + 1
                    temp_h = computeManhattan(temp_cell, goal)
                    temp_f = temp_g + temp_h
                    temp_cell.f_value = temp_f
                    temp_cell.g_value = temp_g
                    temp_cell.h_value = temp_h
                
                    # push to heap
                    #heappush(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                    open_list.heappush((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                    
                else:
                    # make sure it's not an obstacle
                    if cells[neighbor].g_value != float('inf'):
                        temp_cell = cells[neighbor]
                        temp_cell.parent = current
                        temp_g = current.g_value + 1
                        #temp_h = cells[neighbor].h_value
                        temp_h = computeManhattan(temp_cell, goal)
                        temp_f = temp_g + temp_h
                        temp_cell.f_value = temp_f
                        temp_cell.g_value = temp_g
                        temp_cell.h_value = temp_h

                        # push to heap
                        #heappush(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                        open_list.heappush((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))

    return current


# pass in initial and goal as references to Cell objects
def forward_adaptive_AStar(initial, goal, cells, grid):
    
    global cells_expanded
    
    # code for repeated forward A*
    #open_list = [] # structure of each element should be as follows: (f-value, Cell object), heap
    
    # reset g-value of starting cell during each call of A*
    initial.g_value = 0
    initial.f_value = initial.h_value

    number_rows = len(grid)
    number_columns = len(grid[0])
    
    #heappush(open_list, (initial.f_value, initial.g_value, random.random(), initial))
    open_list = MinHeap()
    open_list.heappush((initial.f_value, initial.g_value, random.random(), initial))
    closed_list = set()

    # set pointer to initial cell
    current = initial

    while open_list.length() > 0:
        # pop smallest f-value in open list (if multiple cells with same f-value, use one with larger g-value)
        #current_f_value, current_g_value, current_tiebreaker, current = heappop(open_list)
        current_f_value, current_g_value, current_tiebreaker, current = open_list.heappop()

        
        if (current.x, current.y) in closed_list:
            continue

        cells_expanded += 1
        # add cell to closed list
        closed_list.add((current.x, current.y))

        if current.x == goal.x and current.y == goal.y:
            return current

        # neighbors of current cell
        neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

        for neighbor in neighbors:
            # if coordinates are not in bounds then continue to next neighboring position
            if not (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                continue
            # if neighbor is in closed list, ignore it
            if (neighbor[0], neighbor[1]) in closed_list:
                continue
            else:
                # cell needs to be created
                if neighbor not in cells:
                    temp_cell = Cell(neighbor, current)
                    cells[neighbor] = temp_cell # add cell to dictionary so it can be referenced later
                    temp_g = current.g_value + 1
                    temp_h = computeManhattan(temp_cell, goal)
                    temp_f = temp_g + temp_h
                    temp_cell.f_value = temp_f
                    temp_cell.g_value = temp_g
                    temp_cell.h_value = temp_h
                
                    # push to heap
                    #heappush(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                    open_list.heappush((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                    
                else:
                    # make sure it's not an obstacle
                    if cells[neighbor].g_value != float('inf'):
                        temp_cell = cells[neighbor]
                        temp_cell.parent = current
                        temp_g = current.g_value + 1
                        temp_h = cells[neighbor].h_value
                        #temp_h = computeManhattan(temp_cell, goal)
                        temp_f = temp_g + temp_h
                        temp_cell.f_value = temp_f
                        temp_cell.g_value = temp_g
                        temp_cell.h_value = temp_h

                        # push to heap
                        #heappush(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                        open_list.heappush((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
    return current


def repeated_backward_AStar(initial, goal, grid):
    start = Cell(initial)
    end = Cell(goal)
    cells = {} # dictionary
    cells[initial] = start # initial and goal are tuples of the coordinates
    cells[goal] = end
    master_path = [initial] # entire path that agent follows from initial to goal

    number_rows = len(grid)
    number_columns = len(grid[0])

    current = start
    
    # add the blocked states in our initial field of view to our dictionary, make sure coordinates in line 
    # neighbors of current cell
    neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

    
    for neighbor in neighbors:
        # if coordinate is in bounds then continue to next neighboring position
        if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
            # it is an obstacle, take note of it
            if grid[neighbor[1]][neighbor[0]] == 0:
                temp_cell = Cell(initial, current)
                temp_cell.g_value = float('inf')
                temp_cell.h_value = computeManhattan(temp_cell, start)
                temp_cell.f_value = temp_cell.g_value
                cells[neighbor] = temp_cell
    
    while not(current.x == end.x and current.y == end.y):

        # PLANNING
        start_A_Star = current        
        cell = forward_AStar(end, start_A_Star, cells, grid)
        
        path = []
        # build path
        while not(cell.x == end.x and cell.y == end.y):
            path.append((cell.x, cell.y))
            cell = cell.parent
        
        path.append((end.x, end.y))
        
        #print(path)

        # EXECUTION 
        steps = 0
        for i in range(1, len(path)):
            
            # check if next coordinate is an obstacle
            next_x_coordinate = path[i][0]
            next_y_coordinate = path[i][1]
            
            if grid[next_y_coordinate][next_x_coordinate] == 0:
                # don't move there
                cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
                cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
                break

            else:
                steps += 1
                # move current to next cell
                current = cells[(next_x_coordinate, next_y_coordinate)]
                # add the coordinate to the master path - because the coordinate is not an obstacle
                master_path.append((next_x_coordinate, next_y_coordinate))

                # after moving cell, observe directly adjacent cells in vision to see if they are obstacles
                neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

                for neighbor in neighbors:
                    # if coordinate is in bounds then continue to next neighboring position
                    if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                        # it is an obstacle, take note of it
                        if grid[neighbor[1]][neighbor[0]] == 0:
                            if neighbor in cells:
                                cells[neighbor].g_value = float('inf')
                                cells[neighbor].f_value = float('inf')
                            else:
                                temp_cell = Cell(initial, current)
                                temp_cell.g_value = float('inf')
                                #temp_cell.h_value = computeManhattan(temp_cell, start)
                                temp_cell.f_value = temp_cell.g_value
                                cells[neighbor] = temp_cell

    #print(master_path)

    return master_path


def computeManhattan(current, end):
    return abs(end.x - current.x) + abs(end.y - current.y)

if __name__ == "__main__":
    
    gridObject = Grid()
    start = (0, 0)
    end = (100, 100)

    gridObject.build_new_maze()
    gridObject.generate_figure()

    path_to_color = repeated_forward_AStar(start, end, gridObject.grid)
    gridObject.color_path(path_to_color)

    #path_to_color = repeated_backward_AStar(start, end, gridObject.grid)
    #gridObject.color_path(path_to_color)
    
    #path_to_color = repeated_adaptive_AStar(start, end, gridObject.grid)
    #gridObject.color_path(path_to_color)
    
    '''
    forwardCellsExpanded = []
    forwardTime = []
    backwardCellsExpanded = []
    backwardTime = []
    adaptiveCellsExpanded = []
    adaptiveTime = []
    
    for i in range(50):
        gridObject.build_new_maze()    

        # forward
        cells_expanded = 0
        startTime = time.time()
        repeated_forward_AStar(start, end, gridObject.grid)
        endTime = time.time()

        forwardCellsExpanded.append(cells_expanded)
        forwardTime.append(endTime - startTime)
        
        # backward
        cells_expanded = 0
        startTime = time.time()
        repeated_backward_AStar(start, end, gridObject.grid)
        endTime = time.time()

        backwardCellsExpanded.append(cells_expanded)
        backwardTime.append(endTime - startTime)

        # adaptive
        cells_expanded = 0
        startTime = time.time()
        repeated_adaptive_AStar(start, end, gridObject.grid)
        endTime = time.time()
        
        adaptiveCellsExpanded.append(cells_expanded)
        adaptiveTime.append(endTime - startTime)
           

    
    print("")
    print("FORWARD A* STATISTICS (Prioritize Smaller G-Values):")
    print("Cells Expanded Mean: " + str(round(mean(forwardCellsExpanded), 4)))
    print("Cells Expanded Std Dev: " + str(round(stdev(forwardCellsExpanded), 4)))
    print("Runtime Mean: " + str(round(mean(forwardTime), 4)) + " s")
    print("Runtime Std Dev: " + str(round(stdev(forwardTime), 4)) + "s")
    
    print("")
    print("BACKWARD A* STATISTICS:")
    print("Cells Expanded Mean: " + str(round(mean(backwardCellsExpanded), 4)))
    print("Cells Expanded Std Dev: " + str(round(stdev(backwardCellsExpanded), 4)))
    print("Runtime Mean: " + str(round(mean(backwardTime), 4)) + " s")
    print("Runtime Std Dev: " + str(round(stdev(backwardTime), 4)) + " s")

    print("")
    print("ADAPTIVE A* STATISTICS:")
    print("Cells Expanded Mean: " + str(round(mean(adaptiveCellsExpanded), 4)))
    print("Cells Expanded Std Dev: " + str(round(stdev(adaptiveCellsExpanded), 4)))
    print("Runtime Mean: " + str(round(mean(adaptiveTime), 4)) + " s")
    print("Runtime Std Dev: " + str(round(stdev(adaptiveTime), 4)) + " s")
    
    '''
   
        
        