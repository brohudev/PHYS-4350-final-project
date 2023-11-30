import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def initialize_lattice(size):
    return np.zeros((size, size), dtype=int)

def get_perimeter_points(cluster):
    perimeter_points = []
    rows, cols = cluster.shape

    for i in range(rows):
        for j in range(cols):
            if cluster[i, j] == 1:
                neighbors = [
                    (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)
                ]
                for neighbor in neighbors:
                    ni, nj = neighbor
                    if 0 <= ni < rows and 0 <= nj < cols and cluster[ni, nj] == 0:
                        perimeter_points.append((ni, nj))

    return list(set(perimeter_points))

def add_particle(cluster):
    perimeter_points = get_perimeter_points(cluster)

    if perimeter_points:
        chosen_point = np.random.choice(len(perimeter_points))
        i, j = perimeter_points[chosen_point]
        cluster[i, j] = 1

def grow_cluster(size, target_size):
    cluster = initialize_lattice(size)
    cluster[size // 2, size // 2] = 1  # Place seed at the center
    current_size = 1

    while current_size < target_size:
        add_particle(cluster)
        current_size = np.sum(cluster)

    return cluster
def calculate_radius_vs_mass(grid, size_of_grid, r_stops, grid_center):
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
        radius = i *  size_of_grid / r_stops
        mass_within_radius = get_cluster_mass_within_radius(grid, grid_center, radius)
        radius_vs_mass.append((radius, mass_within_radius))

    return radius_vs_mass

# set params
size_of_lattice = 100
target_cluster_size = 4000
resulting_cluster = grow_cluster(size_of_lattice, target_cluster_size)

# # Display the result using matplotlib
# plt.imshow(resulting_cluster, cmap='gray')
# plt.title('Eden Cluster Growth Simulation')
# plt.show()

np.save("resulting_cluster.npz", resulting_cluster) 
#prepare for the r vs m table
grid_center = ( size_of_lattice // 2, size_of_lattice // 2)
r_stops = 50
# make the table
radius_vs_mass_table = calculate_radius_vs_mass(np.array(resulting_cluster),size_of_lattice, r_stops, grid_center)
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

def fit_log_func(x, a, b):
    return a * x + b

# Perform the least squares fit
params, covariance = curve_fit(fit_log_func, logRadius, logMass)

# Get the fitted parameters
a_fit, b_fit = params

# Plot the log function and the fit
fig = plt.subplot()
plt.scatter(logRadius, logMass, color='tomato', edgecolors='tomato', s=30, label='Data')
plt.plot(logRadius, fit_log_func(logRadius, a_fit, b_fit), color='dodgerblue', lw=3, label='Least Squares Fit')
plt.title("Log-log plot, mass vs radius", fontsize=20)
plt.xlabel("Log radius", fontsize=15)
plt.ylabel("Log mass", fontsize=15)
plt.grid(True)
fig.text(2.6, 4.3, 'fractal dimensionality: {:.2f}'.format(a_fit))
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)

plt.legend()  # Show legend with labels for clarity
plt.savefig('fractalDimensionalityEden.png')
plt.show()