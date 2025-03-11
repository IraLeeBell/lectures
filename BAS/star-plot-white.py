import numpy as np
import matplotlib.pyplot as plt

def create_star_grid(dim=10, fill_value=0.0, transit_value=1.0):
    """Create a grid representing a star with a roughly circular illuminated region."""
    grid = np.ones((dim, dim)) * fill_value  # Background is black
    
    # Define the approximate circular region to dim/2 radius
    center = dim // 2
    radius = dim // 3  # Adjust to cover ~60% of squares
    
    for i in range(dim):
        for j in range(dim):
            if (i - center)**2 + (j - center)**2 <= radius**2:
                grid[i, j] = transit_value  # Bright star region
    
    return grid

def plot_grids():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    # Create grids
    grid_white = create_star_grid(transit_value=1.0)  # Fully white star
    grid_95_white = create_star_grid(transit_value=0.50)  # 95% white transit
    
    for ax, grid, title in zip(axes, [grid_white, grid_95_white],
                               ["Purely White Star (Left)", "50% White Star (Right)"]):
        ax.imshow(grid, cmap='gray', vmin=0, vmax=1)
        ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
        ax.grid(which="minor", color='gray', linestyle='-', linewidth=1)
        ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
        ax.set_title(title)
    
    plt.suptitle("Simulating Exoplanet Transit Depth Visibility")
    plt.show()

if __name__ == "__main__":
    plot_grids()
