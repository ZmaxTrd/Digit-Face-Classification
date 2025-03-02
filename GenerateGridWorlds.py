import random
import numpy as np
import matplotlib.pyplot as plt
import os  

GRID_SIZE = 101  # size of the grid (101x101)
NUM_ENVIRONMENTS = 50  # number of grid environments to generate
BLOCK_PROBABILITY = 0.3  # probability of a cell being blocked
UNBLOCKED = 0
BLOCKED = 1

def generate_gridworld():
    
    # initialize the grid with all cells as unvisited & unblocked
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    visited = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    
    # start from a random cell
    start_x, start_y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    stack = [(start_x, start_y)]
    visited[start_x, start_y] = True
    
    # depth-first search to generate the gridworld
    while stack:
        x, y = stack[-1]
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not visited[nx, ny]]
        
        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            visited[nx, ny] = True
            if random.random() < BLOCK_PROBABILITY:
                grid[nx, ny] = BLOCKED  # block the cell with 30% probability
            else:
                grid[nx, ny] = UNBLOCKED  # unblock the cell with 70% probability
                stack.append((nx, ny))  # add to stack to continue DFS
        else:
            stack.pop()  # backtrack if no unvisited neighbors
    
    return grid

def generate_multiple_gridworlds(num_environments):
    gridworlds = []
    for _ in range(num_environments):
        gridworld = generate_gridworld()
        gridworlds.append(gridworld)
    return gridworlds

def save_gridworlds(gridworlds, filename="gridworlds.npy", txt_directory="grids_txt"):
    """Saves gridworlds as .npy and properly formatted text files with spaces."""
    
    np.save(filename, gridworlds)

    if not os.path.exists(txt_directory):
        os.makedirs(txt_directory)

    for i, grid in enumerate(gridworlds):
        txt_filename = f"{txt_directory}/gridworld_{i + 1}.txt"

        #save with spaces between numbers
        with open(txt_filename, "w") as f:
            for row in grid:
                f.write(" ".join(map(str, row)) + "\n")  #join numbers with spaces

def load_gridworlds(filename="gridworlds.npy"):
    return np.load(filename, allow_pickle=True)

def save_gridworld_images(gridworlds, directory="grids"):
    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # save each gridworld as an image
    for i, grid in enumerate(gridworlds):
        plt.imshow(grid, cmap='binary', interpolation='none')
        plt.colorbar(label="Blocked (1) / Unblocked (0)")
        plt.title(f"Grid World {i + 1}")
        plt.savefig(f"{directory}/gridworld_{i + 1}.png")  # save as PNG
        plt.close()  # close the figure to free memory

def load_grid_from_txt(filename):
    """Loads a gridworld from a text file."""
    return np.loadtxt(filename, dtype=int)  # convert file into numpy array