# from cities import get_cities, get_distance
# from aco import run_aco
# from visualize import visualize_aco
#
# def main():
#     cities = get_cities()
#     distance = get_distance()
#
#     num_ants = 5
#     num_iterations = 10
#
#     best_path, best_distance, paths_per_iteration = run_aco(num_ants, num_iterations, distance)
#
#     print("Best path:", best_path)
#     print("Best distance:", best_distance)
#
#     visualize_aco(cities, best_path, best_distance, paths_per_iteration, num_iterations)
#
# if __name__ == "__main__":
#     main()
from cities import get_cities, get_distance
from aco import run_aco
from visualize import visualize_aco

def main():
    cities = get_cities()
    distance = get_distance()

    num_ants = 5
    num_iterations = 10

    best_path, best_distance, paths_per_iteration = run_aco(num_ants, num_iterations, distance)

    print("\n🟢 Best path (by ant colony optimization):")
    path_str = " → ".join(f"C{city}" for city in best_path + [best_path[0]])  # thêm quay lại điểm đầu
    print(path_str)

    print(f"🔵 Total distance: {best_distance:.2f} units")

    visualize_aco(cities, best_path, best_distance, paths_per_iteration, num_iterations)

if __name__ == "__main__":
    main()
