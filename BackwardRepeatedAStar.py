from MinBinaryHeap import MinBinaryHeap
import time
from ComplementaryFunctions import generateStates, manhattanDistance, determineActions, successorState, checkAdjacent, find_nearest_unblocked, reconstruct_path
from State import State
import numpy as np

# move from target to agent current state (start)
def computePath(open_list, closed_list, start, expanded, counter, states, track_explored):
    while start.g > open_list.peek().f:
        current = open_list.pop() # pop the min f valued state from the heap
        closed_list.add(current) # add the current state to the closed state since it is going to be expanded
        expanded.append((current.x, current.y)) 
        # if track_explored:
        #     track_explored(current)
            
        for action in determineActions(current, states, closed_list):
            successor = successorState(current, action, states)
            # if successor.isBlocked:
            #     continue
            
            if successor.search < counter:
                successor.g = float('inf')
                successor.search = counter
                
            if successor.g > current.g + 1:
                successor.g = current.g + 1
                successor.pointer = current
                
                if open_list.contains(successor): # if successor in open list, remove it 
                    open_list.remove(successor)
                
                successor.update() # update f value
                open_list.insert(successor)
                
        if open_list.isEmpty():
            break

def repeatedBackwardMain(grid_path, start, goal, larger_g = True, track_explored = None):
    states = generateStates(grid_path)
    
    start_state = states[start[0]][start[1]]
    goal_state = states[goal[0]][goal[1]]

    #if start is blocked
    if start_state.isBlocked:
        print(f"Start state {start} is blocked. Searching for nearest unblocked state...")
        start_state = find_nearest_unblocked(start, states)
        if not start_state:
            print("No unblocked state found near start. Terminating.")
            return None, None, None
    
    #if goal is blocked
    if goal_state.isBlocked:
        print(f"Goal state {goal} is blocked. Searching for nearest unblocked state...")
        goal_state = find_nearest_unblocked(goal, states)
        if not goal_state:
            print("No unblocked state found near goal. Terminating.")
            return None, None, None
        
    if start_state is None or goal_state is None:
        print("No valid path exists in this grid. Terminating.")
        return None, None, None
    
    counter = 0
    path = []
    expanded = []
    
    checkAdjacent(goal_state, states) # check goal to start
    path.append(np.array((goal_state.x, goal_state.y)))
    
    for rows in states:
        for state in rows:
            state.h = manhattanDistance(state, start_state) # distance to start
        
    start_time = time.time()
    while goal_state != start_state: # continue until goal reaches start
        counter += 1
        
        goal_state.g = 0 # goal is the "start" of search
        goal_state.search = counter
        start_state.g = float('inf') # start is the "goal" of search
        start_state.search = counter
        
        open_list = MinBinaryHeap(larger_g)
        closed_list = set()
        
        goal_state.update() # update f(s) of goal state
        open_list.insert(goal_state) # insert goal state into open list
        
        computePath(open_list, closed_list, start_state, expanded, counter, states, track_explored) # search from goal to start
        
        if open_list.isEmpty():
            return None, expanded, time.time() - start_time
                
        while goal_state != start_state:
            current = start_state # current is agents position
            
            while (current.pointer is not None) and (current != goal_state):
                if current.pointer == goal_state:
                    break
                current = current.pointer
                
            if current.isObserved is False:
                goal_state = current # add current state to path
                path.append(np.array((current.x, current.y)))
                if track_explored:
                    track_explored(current)
                checkAdjacent(current, states)
            else: 
                break
            
    expanded.append(np.array((start_state.x, start_state.y))) # add start state to expanded list
    shortest_path = reconstruct_path(path)
    end_time = time.time()
        
    return shortest_path, expanded, end_time - start_time
