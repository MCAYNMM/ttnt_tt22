import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----- Dữ liệu thành phố (tọa độ 2D) -----
cities = np.array([
    [0, 0],
    [1, 5],
    [5, 2],
    [6, 6]
])

num_points = len(cities)
num_ants = 5
num_iterations = 10

# Tính khoảng cách giữa các điểm
distance = np.zeros((num_points, num_points)) # tạo mảng hai chiều toàn số 0 với kính thước num_points * num_points
for i in range(num_points):
    for j in range(num_points):
        distance[i][j] = np.linalg.norm(cities[i] - cities[j]) # tính khoảng cách giữa các thành phố với nhau

alpha = 1
beta = 5
rho = 0.5
Q = 100

pheromone = np.ones((num_points, num_points)) # tạo mảng hai chiều toàn số 1 với kính thước num_points * num_points


def heuristic(i, j):
    if distance[i][j] == 0:
        return 0
    return 1.0 / distance[i][j]


def select_next_city(current_city, visited):
    probabilities = []
    for j in range(num_points):
        if j not in visited:
            tau = pheromone[current_city][j] ** alpha
            eta = heuristic(current_city, j) ** beta
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


best_path = None
best_distance = float('inf')

# Lưu kết quả mỗi vòng lặp để vẽ animation
paths_per_iteration = []

# for iteration in range(num_iterations):
#     all_paths = []
#     for ant in range(num_ants):
#         path = [random.randint(0, num_points - 1)]
#         while len(path) < num_points:
#             next_city = select_next_city(path[-1], path)
#             if next_city is None:
#                 break
#             path.append(next_city)
#         dist = total_distance(path)
#         all_paths.append((path, dist))
#         if dist < best_distance:
#             best_distance = dist
#             best_path = path
#     paths_per_iteration.append(all_paths)
#
#     # Cập nhật pheromone
#     pheromone = (1 - rho) * pheromone
#     for path, dist in all_paths:
#         for i in range(len(path) - 1):
#             pheromone[path[i]][path[i + 1]] += Q / dist # cập nhập pheromone
#         pheromone[path[-1]][path[0]] += Q / dist # câập nhập pheromone cho điểm đầu điểm cuối

for iteration in range(num_iterations):
    all_paths = []
    for ant in range(num_ants):
        path = [0]  # Bắt đầu cố định từ thành phố 0
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


print("Best path:", best_path)
print("Best distance:", best_distance)

# ------ Phần vẽ animation với matplotlib ------

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)
ax.set_title("Ant Colony Optimization - TSP")

# Vẽ các thành phố (điểm)
ax.scatter(cities[:, 0], cities[:, 1], c='red')
for i, (x, y) in enumerate(cities):
    ax.text(x + 0.1, y + 0.1, f"C{i}", fontsize=12)

best_line = None  # Đường đi tốt nhất (màu xanh lá)
paths_lines = []  # Các đường đi vòng hiện tại (màu đỏ)


def update(frame):
    global best_line, paths_lines

    # Xóa các đường đỏ vòng trước (nếu có)
    for line in paths_lines:
        line.remove()
    paths_lines = []

    ax.set_xlabel(f"Iteration {frame + 1} / {num_iterations} - Best Distance: {best_distance:.2f}")

    if frame < num_iterations - 1:
        # Vẽ đường đỏ vòng hiện tại
        all_paths = paths_per_iteration[frame]
        for path, dist in all_paths:
            x = [cities[p][0] for p in path] + [cities[path[0]][0]]
            y = [cities[p][1] for p in path] + [cities[path[0]][1]]
            line, = ax.plot(x, y, color='red', alpha=0.5)
            paths_lines.append(line)

        # Vẽ đường xanh tốt nhất (chỉ vẽ 1 lần)
        if best_path is not None and best_line is None:
            x_best = [cities[p][0] for p in best_path] + [cities[best_path[0]][0]]
            y_best = [cities[p][1] for p in best_path] + [cities[best_path[0]][1]]
            best_line, = ax.plot(x_best, y_best, color='green', linewidth=3, label='Best Path')
            ax.legend()

    else:
        # Vòng cuối: chỉ vẽ đường tốt nhất, không vẽ đường đỏ
        if best_line is not None:
            # Đường xanh có rồi thì thôi
            pass
        else:
            # Nếu chưa có đường xanh, vẽ nó
            x_best = [cities[p][0] for p in best_path] + [cities[best_path[0]][0]]
            y_best = [cities[p][1] for p in best_path] + [cities[best_path[0]][1]]
            best_line, = ax.plot(x_best, y_best, color='green', linewidth=3, label='Best Path')
            ax.legend()



ani = FuncAnimation(fig, update, frames=num_iterations, repeat=False, interval=500)

plt.show()
