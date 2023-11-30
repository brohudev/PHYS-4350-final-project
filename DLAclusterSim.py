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

def get_perimeter_points(cluster):
    perimeter_points = []
    for x in range(cluster.shape[0]):
        for y in range(cluster.shape[1]):
            if cluster[x, y] == 1:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i != 0 or j != 0) and is_valid_position((x+i, y+j), cluster):
                            if cluster[x+i, y+j] == 0:
                                perimeter_points.append((x+i, y+j))
    return perimeter_points

def add_particle(grid):
    perimeter_points = get_perimeter_points(grid)

    if perimeter_points:
        # Select a random particle outside the perimeter_points
        random_particle = tuple(np.random.choice(grid.shape[0], size=2))
        
        while random_particle not in perimeter_points:
            # Until the particle touches a point in the perimeter_points, have it perform a random walk.
            random_particle = random_walk(random_particle, grid)
        
        # Take this perimeter point and make grid[point] = 1
        grid[random_particle] = 1
        print("added another point: ",random_particle) # small progress tracker    

def dla_cluster_growth(size, target_size):
    grid = initialize_grid(size)
    center = size // 2
    grid[center, center] = 1  # Seed at the origin
    r_vs_m = []
    current_size = 1

    while current_size < target_size:
       add_particle(grid)
       current_size = np.sum(grid)
       print("grid size is now: ", current_size)  # small progress tracker

    return grid

# modify these points to get a bigger/smaller grid
size_of_grid = 20
target_dla_size = 50
dla_resulting_table = dla_cluster_growth(size_of_grid, target_dla_size)

print(dla_resulting_table)
plt.imshow(dla_resulting_table, cmap='gray')
plt.title('DLA Cluster Growth Simulation')
plt.show()