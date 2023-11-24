"""
Label and create a DLA cluster with a random walk demonstration in the same picture (?) per Figure 7.18
"""
import numpy as np
import matplotlib.pyplot as plt

def initialize_grid(size):
    return np.zeros((size, size), dtype=int)

def is_valid_position(position, grid):
    x, y = position
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

def random_walk(position, grid):
    while True:
        move = np.random.choice(['up', 'down', 'left', 'right'])
        
        if move == 'up':
            new_position = (position[0] - 1, position[1])
        elif move == 'down':
            new_position = (position[0] + 1, position[1])
        elif move == 'left':
            new_position = (position[0], position[1] - 1)
        elif move == 'right':
            new_position = (position[0], position[1] + 1)

        if is_valid_position(new_position, grid):
            return new_position

def dla_cluster_growth(size, target_size):
    grid = initialize_grid(size)
    center = size // 2
    grid[center, center] = 1  # Seed at the origin
    current_size = 1

    while current_size < target_size:
        # Randomly release a particle some distance away from the seed
        distance = np.random.randint(5, size // 2)
        angle = np.random.uniform(0, 2 * np.pi)
        particle_position = (
            center + int(distance * np.cos(angle)),
            center + int(distance * np.sin(angle))
        )
        print("released a new point onto canvas: ",particle_position)

        while not np.any(grid[particle_position]):
            particle_position = random_walk(particle_position, grid)
        # Stick the particle to the seed, increasing the cluster size
        grid[particle_position] = 1
        current_size += 1
        print("the current size is now: ",current_size)

    return grid

# Example usage
size_of_grid = 10
target_dla_size = 50
dla_resulting_cluster = dla_cluster_growth(size_of_grid, target_dla_size)

# Display the result using matplotlib
plt.imshow(dla_resulting_cluster, cmap='gray')
plt.title('DLA Cluster Growth Simulation')
plt.show()
