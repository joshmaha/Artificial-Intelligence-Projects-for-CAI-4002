# Joshua Maharaj U24183946
# CAI 4002 Intro to AI, Project 1

from typing import List, Tuple
import json, heapq

def get_neighbors(state: Tuple[int], size: int) -> List[Tuple[Tuple[int], int]]:

    neighbors = []
    zero_index = state.index(0)  # Find empty space
    row, col = divmod(zero_index, size)

    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    for _, (dr, dc) in moves.items():
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size:
            swap_index = nr * size + nc
            new_state = list(state)
            new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
            neighbors.append((tuple(new_state), state[swap_index]))  # Store the tile moved
    
    return neighbors

def manhattan_distance(state: Tuple[int], size: int) -> int:

    distance = 0  # variable for total distance so far 

    for i, tile in enumerate(state):  # Loop through each tile in the grid
        if tile == 0:  # Skip the empty space (0) since it doesn't need to move
            continue  

        # Find the correct position of the tile
        correct_pos = tile  # The correct position is simply the tile's value

        # Get the current row and column of this tile
        current_row, current_col = divmod(i, size)

        # Get the correct row and column where this tile should be
        correct_row, correct_col = divmod(correct_pos, size)

        # Calculate how many moves (steps) the tile needs to reach its correct place
        distance += abs(correct_row - current_row) + abs(correct_col - current_col)

    return distance  # Return the total Manhattan Distance for the puzzle


# f(n) = g(n) + h(n)
# where g(n) is cost so far to reach n, h(n) is estimated cost from n to goal state and 
# f(n) is the estimated total cost through n to goal state
def a_star_search(size: int, grid: List[int]) -> List[int]:

    start_state = tuple(grid)  # convert input list into a tuple  
    goal_state = tuple(range(size * size))  

    
    frontier = [(manhattan_distance(start_state, size), 0, start_state, [])] # priority queue format:(f(n), g(n), current state, path_taken)
    visited = set()  # previous board states stored in set 

    while frontier:  # iterate to get all possible options
        f_value, g, current_state, path = heapq.heappop(frontier)  
        if current_state in visited:  # skip past visited states
            continue
        visited.add(current_state)  # Mark this state as visited

        if current_state == goal_state:  # return path if goal state obtained
            return path  

        # Expand neighbors (possible tile moves)
        for next_state, moved_tile in get_neighbors(current_state, size):
            if next_state not in visited:
                # Calculate f(n) = g(n) + h(n)
                heapq.heappush(frontier, (g + 1 + manhattan_distance(next_state, size), 
                                          g + 1, 
                                          next_state, 
                                          path + [moved_tile]))

    return []  # If no solution is found, return an empty list


def solveSlider(size: int, grid: List[int]) -> List[int]:
    
    return a_star_search(size, grid)

