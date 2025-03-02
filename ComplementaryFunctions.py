from State import State
import numpy as np
from GenerateGridWorlds  import load_grid_from_txt
from collections import deque
import numpy as np

def generateStates(path):
    """function to load grid from text and initialize all states"""
    
    grid = load_grid_from_txt(path)
    return [[State(x, y, True if int(grid[x][y]) == 1 else False) for y in range(len(grid[0]))] for x in range(len(grid))]

def manhattanDistance(a, b):
    """function to calculate the manhattan distance from state a to state b (heuristic function for this a* implementation)"""
    
    return abs(a.x - b.x) + abs(a.y - b.y)

def determineActions(state, states, closed_list):
    """function to determine all possible actions after a state expansion
    checks to see if the adjacent states exist, have not and not in closed list
    """
    
    actions = []
    r = state.x
    c = state.y
    
    if c - 1 >= 0: # state to the left of the current
        if (states[r][c - 1].isObserved is False) and (states[r][c - 1] not in closed_list):
            actions.append('l')
            
    if r - 1 >= 0: # state above the curent    
        if (states[r - 1][c].isObserved is False) and (states[r - 1][c] not in closed_list):
            actions.append('u')
            
    if c + 1 <= len(states[0]) - 1: # state to the right of current
        if (states[r][c + 1].isObserved is False) and (states[r][c + 1] not in closed_list):
            actions.append('r')
            
    if r + 1 <= len(states) - 1: # state below the current 
        if (states[r + 1][c].isObserved is False) and (states[r + 1][c] not in closed_list):
            actions.append('d')
            
    return actions

def successorState(state, action, states):
    """function which returns a state depending on actions for each current state"""
    
    r = state.x
    c = state.y
    
    if action == 'l':
        return states[r][c - 1]
    
    elif action == 'u':
        return states[r - 1][c]
    
    elif action == 'r':
        return states[r][c + 1]
    
    elif action == 'd':
        return states[r + 1][c]
    
    else: 
        return None
    
def checkAdjacent(state, states):
    r = state.x
    c = state.y

    if r + 1 <= len(states) - 1:
        states[r + 1][c].isObserved = states[r + 1][c].isBlocked

    if r - 1 >= 0:
        states[r - 1][c].isObserved = states[r - 1][c].isBlocked

    if c + 1 <= len(states[0]) - 1:
        states[r][c + 1].isObserved = states[r][c + 1].isBlocked

    if c - 1 >= 0:
        states[r][c - 1].isObserved = states[r][c - 1].isBlocked
        
def find_nearest_unblocked(coord, states):
    r, c = len(states), len(states[0])
    queue = deque([coord])  # BFS queue
    visited = set()
    visited.add(coord)

    while queue:
        x, y = queue.popleft()
        
        if not states[x][y].isBlocked:
            return states[x][y]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < r and 0 <= ny < c and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
    return None

def reconstruct_path(path):
    i = 0
    while i < len(path) - 1:
        location = path[i]
        hasDuplicate = False
        for j in range(i + 1, len(path)):
            if all(location == path[j]):
                hasDuplicate = True
                del path[i + 1 : j + 1]
                break
        if not hasDuplicate:
            i += 1

    return path
