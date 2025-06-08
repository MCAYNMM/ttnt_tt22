import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Tham số ---
num_agents = 30 # số lượng chim
num_iterations = 20 # số vòng chim bay
dim = 2 # không gian hai chiều
lower_bound = -10
upper_bound = 10

# Hàm mục tiêu
def objective(x): # Hàm tính mục tiêu
    return np.sum(x**2)

# Khởi tạo vị trí
agents = np.random.uniform(lower_bound, upper_bound, (num_agents, dim)) # là mảng hai chiều
fitness = np.array([objective(agent) for agent in agents]) # chữa giá trị của mỗi chim
best_agent = agents[np.argmin(fitness)] # tìm tọa độ chim tốt nhất
best_score = np.min(fitness) # tìm chim tốt nhất

positions_per_iteration = [agents.copy()] #lưu tất cả vị trí của con chim tại mỗi vòng lặp
convergence = [best_score] # danh sách lưu lại giá trị tốt nhất sau mỗi vòng lặp

# --- Tối ưu + Ghi lại vị trí ---
for iteration in range(num_iterations):
    r1 = np.random.rand()

    for i in range(num_agents):
        A = 2 * r1 - 1 # random từ -1 đến 1
        C = 2 * np.random.rand(dim) # random từ 0 đến 2
        D = np.abs(C * best_agent - agents[i])
        new_position = best_agent - A * D

        new_position = np.clip(new_position, lower_bound, upper_bound)
        new_fitness = objective(new_position)

        if new_fitness < fitness[i]: #cập nhập nếu giá trị mới tốt hơn giá trị hiện tại của mồng biển
            agents[i] = new_position
            fitness[i] = new_fitness

        if new_fitness < best_score: # cập nhập nếu tốt hơn giá trị tốt nhất
            best_agent = new_position
            best_score = new_fitness

    positions_per_iteration.append(agents.copy())
    convergence.append(best_score)

# --- Animation ---
fig, ax = plt.subplots(figsize=(6, 6))
sc = ax.scatter([], [], c='blue', label='Seagulls')
best_pt = ax.scatter([], [], c='red', marker='*', s=200, label='Best')

ax.set_xlim(lower_bound, upper_bound)
ax.set_ylim(lower_bound, upper_bound)
ax.set_title("Seagull Optimization Algorithm (SOA)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()

def animate(frame):
    positions = positions_per_iteration[frame]
    sc.set_offsets(positions)
    best_pt.set_offsets([best_agent])
    ax.set_title(f"Iteration {frame}/{num_iterations} | Best Score: {convergence[frame]:.5f}")
    return sc, best_pt

ani = FuncAnimation(fig, animate, frames=num_iterations, interval=200, repeat=False)

plt.show()
