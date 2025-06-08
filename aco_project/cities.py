import numpy as np

cities = np.array([
    [0, 0],
    [1, 5],
    [5, 2],
    [6, 6]
])

num_points = len(cities)

distance = np.zeros((num_points, num_points))
for i in range(num_points):
    for j in range(num_points):
        distance[i][j] = np.linalg.norm(cities[i] - cities[j])

def get_distance():
    return distance

def get_cities():
    return cities

def get_num_points():
    return num_points
