import random

# Tham số thuật toán có thể đặt bên ngoài hoặc trong hàm
alpha = 1
beta = 5
rho = 0.5
Q = 100

pheromone = None  # sẽ được khởi tạo bên ngoài

distance = None
num_points = None

def heuristic(i, j):
    if distance[i][j] == 0:
        return 0
    return 1.0 / distance[i][j]

def select_next_city(current_city, visited):
    probabilities = []
    for j in range(num_points):
        if j not in visited:
            tau = pheromone[current_city][j] ** alpha #pheromone laf mảng hai chiều, current_city là số kiến đang đứng, j là thành phố muốn đến
            eta = heuristic(current_city, j) ** beta  #heuristic là hamf, current_city là số kiến đang đứng, j là thành phố muốn đến
            probabilities.append(tau * eta)
        else:
            probabilities.append(0)
    total = sum(probabilities)
    if total == 0:
        return None
    probabilities = [p / total for p in probabilities]
    return random.choices(range(num_points), weights=probabilities)[0]

def total_distance(path):
    dist = 0
    for i in range(len(path) - 1):
        dist += distance[path[i]][path[i + 1]]
    dist += distance[path[-1]][path[0]]
    return dist

def run_aco(num_ants, num_iterations, dist_matrix):
    global pheromone, distance, num_points
    distance = dist_matrix
    num_points = len(distance)
    pheromone = [[1 for _ in range(num_points)] for _ in range(num_points)]

    best_path = None
    best_distance = float('inf')
    paths_per_iteration = []

    for iteration in range(num_iterations):
        all_paths = []
        for ant in range(num_ants):
            path = [0]  # bắt đầu cố định từ thành phố 0
            while len(path) < num_points:
                next_city = select_next_city(path[-1], path)
                if next_city is None:
                    break
                path.append(next_city)
            dist = total_distance(path)
            all_paths.append((path, dist))
            if dist < best_distance:
                best_distance = dist
                best_path = path
        paths_per_iteration.append(all_paths)

        # Cập nhật pheromone
        for i in range(num_points):
            for j in range(num_points):
                pheromone[i][j] *= (1 - rho)
        for path, dist in all_paths:
            for i in range(len(path) - 1):
                pheromone[path[i]][path[i + 1]] += Q / dist
            pheromone[path[-1]][path[0]] += Q / dist

    return best_path, best_distance, paths_per_iteration
