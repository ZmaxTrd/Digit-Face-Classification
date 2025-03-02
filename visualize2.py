import matplotlib.pyplot as plt
import numpy as np
import time
from ForwardRepeatedAStar import repeatedForwardMain
from BackwardRepeatedAStar import repeatedBackwardMain
from AdaptiveAStar import repeatedAdaptiveMain
import GenerateGridWorlds

def visualize_astar(grid, grid_path, start, goal, larger_g=False):
    """Visualize A* search process separately for each algorithm."""

    rows, cols = len(grid), len(grid[0])

    # Color mapping
    cmap = {
        0: "white",  # Unblocked
        1: "black",  # Blocked
        2: "blue",   # Explored cells
        3: "red"     # Final path
    }

    # Grid to color format
    color_grid = np.array(grid, dtype=int)

    def run_and_visualize(algorithm, algorithm_name):
        """Runs A* search and visualizes it separately."""
        
        fig, ax = plt.subplots()
        ax.set_title(algorithm_name)

        def update_search():
            """Updates the visualization of the grid dynamically."""
            
            ax.clear()
            ax.imshow(color_grid, cmap=plt.cm.binary, interpolation="none")
            plt.pause(0.0001)  # Delay

        def track_explored(cell):
            """Marks explored cells during search."""
            
            if grid[cell.x][cell.y] == 0:  
                color_grid[cell.x, cell.y] = 2  
                update_search()

        print(f"Running {algorithm_name}...")
        color_grid[:] = np.array(grid, dtype=int)  
        path, expanded_cells, runtime = algorithm(grid_path, start, goal, larger_g, track_explored=track_explored)
        
        print(f"Path: {path}")
        print(f"Number of expanded cells: {len(expanded_cells)}")
        print(f"Runtime: {runtime:.5f} seconds")

        if path is None:
            print(f"No path found using {algorithm_name}! The goal is blocked or unreachable.")
            update_search()
            return

        # Final path
        for (x, y) in path:
            color_grid[x, y] = 3  # Mark final path
            update_search()

        plt.show()

    # Run algorithms
    run_and_visualize(repeatedForwardMain, "Repeated Forward A*")
    run_and_visualize(repeatedBackwardMain, "Repeated Backward A*")
    run_and_visualize(repeatedAdaptiveMain, "Repeated Adaptive A*")

# Load from file
grid_path = "grids_txt/gridworld_1.txt"
grid = GenerateGridWorlds.load_grid_from_txt(grid_path)

start = (0, 0)
goal = (100, 100)

visualize_astar(grid, grid_path, start, goal, False)
