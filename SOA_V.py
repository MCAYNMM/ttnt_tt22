import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Tham số ---
num_agents = 30  # số lượng chim
num_iterations = 10  # số vòng lặp (tăng lên để rõ hiệu quả)
dim = 2  # không gian 2 chiều
lower_bound = -10
upper_bound = 10


# Hàm mục tiêu: tổng bình phương tọa độ (bài toán tối ưu min)
def objective(x):
    return np.sum(x ** 2)


# Khởi tạo vị trí chim ngẫu nhiên
agents = np.random.uniform(lower_bound, upper_bound, (num_agents, dim))
fitness = np.array([objective(agent) for agent in agents])
best_agent = agents[np.argmin(fitness)].copy()
best_score = np.min(fitness)

positions_per_iteration = [agents.copy()]
convergence = [best_score]

# --- Thuật toán SOA mở rộng ---
for iteration in range(num_iterations):
    r1 = np.random.rand()  # số ngẫu nhiên dùng cho A
    for i in range(num_agents):
        A = 2 * r1 - 1  # trong [-1,1]
        C = 2 * np.random.rand(dim)  # trong [0,2]
        D = np.abs(C * best_agent - agents[i])

        # Xác định tỷ lệ giữa di cư và tấn công xoáy tròn theo iteration
        # Lúc đầu ưu tiên di cư, về sau ưu tiên tấn công xoáy tròn
        spiral_prob = iteration / num_iterations

        if np.random.rand() > spiral_prob:
            # --- Giai đoạn di cư ---
            new_position = best_agent - A * D
        else:
            # --- Giai đoạn tấn công xoáy tròn ---
            # Công thức xoắn ốc (spiral):
            # new_position = D * exp(b * t) * cos(2*pi*t) + best_agent
            # b và t là tham số kiểm soát hình xoắn
            b = 1  # tham số kiểm soát xoắn
            t = np.random.rand() * 2  # ngẫu nhiên trong [0,2]
            spiral = D * np.exp(b * t) * np.cos(2 * np.pi * t)
            new_position = spiral + best_agent

        # Giới hạn vị trí trong phạm vi
        new_position = np.clip(new_position, lower_bound, upper_bound)

        new_fitness = objective(new_position)

        # Cập nhật nếu tốt hơn
        if new_fitness < fitness[i]:
            agents[i] = new_position
            fitness[i] = new_fitness

        if new_fitness < best_score:
            best_agent = new_position.copy()
            best_score = new_fitness

    positions_per_iteration.append(agents.copy())
    convergence.append(best_score)

# --- Vẽ animation ---
fig, ax = plt.subplots(figsize=(6, 6))
sc = ax.scatter([], [], c='blue', label='Seagulls')
best_pt = ax.scatter([], [], c='red', marker='*', s=200, label='Best')

ax.set_xlim(lower_bound, upper_bound)
ax.set_ylim(lower_bound, upper_bound)
ax.set_title("Seagull Optimization Algorithm (SOA) with Spiral Attack")
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
