# Joshua Maharaj U24183946, CAI 4002 Intro to AI, Project 1 
# 8 puzzle project based on A* search using f(n) = g(n) + h(n)
# g(n) is cost so far to reach n, initialise to 0 at start
# h(n) is estimated cost from n to goal state (Manhattan distance) 
# f(n) is the estimated total cost through n to goal state

from typing import List, Tuple
import json, heapq

# returns list of tuples for all valid moves blank tile can make
def adj_tiles(state: Tuple[int], size: int) -> List[Tuple[Tuple[int], int]]:
    
    adj_list = []  
    empty_tile = state.index(0)  # find blank tile in tuple
    empty_row = empty_tile // size
    empty_column = empty_tile % size # get position values of tile 0
    
    # moves of tile 0 by changing its row or column(1st and 2nd entries) and its resulting positions (3rd entry)
    moves = [
        (-1, 0, empty_tile - size), (1, 0, empty_tile + size), (0, -1, empty_tile - 1), (0, 1, empty_tile + 1)   
        #move up                        move down               move left                   move right 
    ]
    
    # loop through all possible moves
    for row, column, res_pos in moves:
        new_row = empty_row + row # update row and column
        new_column = empty_column + column
        # ensure move is within grid dimensions
        if new_row in range(0,size) and new_column in range(0,size):
            # create new state, then swap tile 0 with other tile being moved
            new_state = list(state)
            new_state[empty_tile], new_state[res_pos] = new_state[res_pos], new_state[empty_tile]
            adj_list.append((tuple(new_state), state[res_pos])) # update list with new state and resulting position of tile 0 after move
    
    return adj_list

# hueristic function based on Manhattan distance which estimates path cost from n to goal state 
def man_dist(state: Tuple[int], size: int) -> int:
    
    dist = 0
    for i in range(len(state)):
        if state[i] != 0:  # skip empty tile
            cur_row = i // size    # calculate current and goal positions of each tile 
            cur_column = i % size
            tile_num = state[i] # actual tile #
            goal_row = tile_num // size 
            goal_column = tile_num % size
            dist += abs(cur_row - goal_row) + abs(cur_column - goal_column) # distance to goal position for this 1 tile
    return dist # total distance for all tiles to get in right place

# A* search to find the shortest possible path
def a_star(size: int, grid: List[int]) -> List[int]:

    initial_state = tuple(grid) # store grid as tuple 
    goal_state = tuple(range(size * size)) # store goal grid format eg (0,1,2,3) for 2x2 grid; use range to get 0 tile
    gn = 0 # initialise g(n) to 0
    path = [] # empty so far
    frontier = [(man_dist(initial_state, size), gn, initial_state, path)]  # initialise priority queue to hold (f(n), g(n), current state, path)
    heapq.heapify(frontier)
    visited = set() # keep track of visited states
    
    while frontier:    # loop through all possible moves
    
        fn, gn, cur_state, path = heapq.heappop(frontier)   # extract all info on lowest f(n) value in priority queue
        if cur_state == goal_state:
            return path # return if solution found
        else:
            visited.add(cur_state)  # track visited
            for next_state, moved_tile in adj_tiles(cur_state, size): # loop through all possible next states
                if next_state not in visited:   # check all unvisited states
                    gn += 1 # increment because we have made 1 move
                    fn = gn + man_dist(next_state, size) # f(n) = g(n) + h(n)
                    heapq.heappush(frontier, (fn, gn, next_state, path + [moved_tile]))  # add this state to priority queue with updated values 
    return path # no solution found

# main function
def solveSlider(size: int, grid: List[int]) -> List[int]:
    
    return a_star(size, grid)


