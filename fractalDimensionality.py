"""
TODO: implement a cluster with a fractal dimensionality of 1.99 and 1.65 and plot logr vs logm of the eden and dla clusters respectively (1.99 for eden and 1.65 for dla).

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

def calculate_radius_vs_mass(grid, cluster_size, num_points, r_stops, grid_center):
    def is_valid_position(position, grid):
        x, y = position
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def get_cluster_mass_within_radius(grid, center, radius):
        mass = 0
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] == 1:
                    distance = np.linalg.norm(np.array([x, y]) - np.array(center))
                    if distance <= radius:
                        mass += 1
        return mass

    radius_vs_mass = []

    for i in range(1, r_stops + 1):
        radius = i * cluster_size / r_stops
        mass_within_radius = get_cluster_mass_within_radius(grid, grid_center, radius)
        radius_vs_mass.append((radius, mass_within_radius))

    return radius_vs_mass

# modify these points to get a bigger/smaller grid
size_of_grid = 20
target_dla_size = 50
dla_resulting_table = dla_cluster_growth(size_of_grid, target_dla_size)
#prepare for the r vs m table
grid_center = (size_of_grid // 2, size_of_grid // 2)
cluster_size = target_dla_size
num_points = target_dla_size
r_stops = 10
# make the table
radius_vs_mass_table = calculate_radius_vs_mass(np.array(dla_resulting_table), cluster_size, num_points, r_stops, grid_center)
radius, mass = zip(*radius_vs_mass_table)

#Find Log of all the arrays
logRadius=np.log(radius)
logMass=np.log(mass)

#Fit a log function using numpy polyfit
fitLog=np.polyfit(logRadius, logMass,1)
fitLogFunc=np.poly1d(fitLog)

#print out the results
print("Parameters for the log fit: slope = ",fitLog[0],"shift: ",fitLog[1])
print("Parameters from the log fit: form is e^",fitLog[1],"*r^",fitLog[0])
num=str(np.round(fitLog[0],3))

#plot the log function
fig=plt.subplot()
plt.scatter(logRadius,logMass, color='tomato', edgecolors='tomato', s=30)
plt.plot(logRadius, fitLogFunc(logRadius),color='dodgerblue', lw=3)
plt.title("Log-log plot, mass vs radius",fontsize=20)
plt.xlabel("Log radius",fontsize=15)
plt.ylabel("Log mass",fontsize=15)
plt.grid(True)
fig.text(2.6,4.3,'fractal dimensionality:'+num)
fig.spines["top"].set_visible(False)  
fig.spines["right"].set_visible(False)  
plt.savefig('logRadiusMass.png')
plt.show()