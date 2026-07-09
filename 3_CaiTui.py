from ortools.algorithms.python import knapsack_solver

def solve_knapsack_problem():
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        'KnapsackExample'
    )

    # Giả lập dữ liệu đồ vật
    values = [60, 100, 120]
    weights = [[10, 20, 30]]
    capacities = [50]  # Sức chứa của túi W

    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    print("=== KẾT QUẢ BÀI TOÁN CÁI TÚI ===")
    print(f"Tổng giá trị lớn nhất: {computed_value}")
    
    total_weight = 0
    print("Các đồ vật được chọn:")
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            print(f"-> Vật {i+1}: Giá trị = {values[i]}, Trọng lượng = {weights[0][i]}")
            total_weight += weights[0][i]
    print(f"Tổng trọng lượng trong túi: {total_weight}")

if __name__ == '__main__':
    solve_knapsack_problem()