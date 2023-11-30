"""
Label and create an eden cluster similar to FIgure 7.17
"""
import numpy as np
import matplotlib.pyplot as plt

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
                        print("appended pt: ",ni," ",nj) #quick little print to show it hasnt hung up.

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

# set params
size_of_lattice = 200
target_cluster_size = 4000
resulting_cluster = grow_cluster(size_of_lattice, target_cluster_size)

# Display the result using matplotlib
plt.imshow(resulting_cluster, cmap='gray')
plt.title('Eden Cluster Growth Simulation')
plt.savefig("edenClusterSim.png")
plt.show()
