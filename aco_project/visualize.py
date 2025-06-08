import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def visualize_aco(cities, best_path, best_distance, paths_per_iteration, num_iterations):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(min(cities[:, 0]) - 1, max(cities[:, 0]) + 1)
    ax.set_ylim(min(cities[:, 1]) - 1, max(cities[:, 1]) + 1)
    ax.set_title("Ant Colony Optimization - TSP")

    ax.scatter(cities[:, 0], cities[:, 1], c='red')
    for i, (x, y) in enumerate(cities):
        ax.text(x + 0.1, y + 0.1, f"C{i}", fontsize=12)

    current_line = None  # Đường đỏ của vòng lặp hiện tại
    best_line = None     # Đường xanh tốt nhất

    def update(frame):
        nonlocal current_line, best_line

        # Xóa đường vòng lặp trước nếu có
        if current_line is not None:
            current_line.remove()
            current_line = None

        # Nếu chưa đến vòng cuối, vẽ đường vòng lặp hiện tại màu đỏ
        if frame < num_iterations:
            # Lấy tất cả đường đi của vòng này, lấy 1 con kiến ví dụ (hoặc trung bình?)
            # Ở đây mình vẽ con kiến đầu tiên của vòng, bạn có thể thay đổi nếu muốn
            if len(paths_per_iteration[frame]) > 0:
                path, dist = paths_per_iteration[frame][0]
                x = [cities[p][0] for p in path] + [cities[path[0]][0]]
                y = [cities[p][1] for p in path] + [cities[path[0]][1]]
                current_line, = ax.plot(x, y, color='red', alpha=0.7, linewidth=2)
            ax.set_xlabel(f"Iteration {frame + 1} / {num_iterations} - Best Distance: {best_distance:.2f}")

            # Ẩn đường tốt nhất trong lúc chạy (nếu muốn)
            if best_line is not None:
                best_line.set_visible(False)

        else:
            # Đến vòng cuối, xóa đường vòng lặp nếu có
            if current_line is not None:
                current_line.remove()
                current_line = None
            # Hiện đường tốt nhất màu xanh
            if best_line is None:
                x_best = [cities[p][0] for p in best_path] + [cities[best_path[0]][0]]
                y_best = [cities[p][1] for p in best_path] + [cities[best_path[0]][1]]
                best_line, = ax.plot(x_best, y_best, color='green', linewidth=3, label='Best Path')
                ax.legend()
            else:
                best_line.set_visible(True)
            path_str = " → ".join(f"C{city}" for city in best_path + [best_path[0]])
            ax.set_xlabel(f"Best Path: {path_str} | Distance: {best_distance:.2f}")

    ani = FuncAnimation(fig, update, frames=num_iterations + 1, repeat=False, interval=700)
    plt.show()
