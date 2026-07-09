from ortools.linear_solver import pywraplp

def solve_assignment_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Không thể khởi tạo solver SCIP")
        return

    # Giả sử ma trận chi phí của 3 kỹ sư làm 3 việc
    costs = [
        [5, 9, 1],
        [10, 3, 2],
        [8, 7, 4]
    ]
    num_engineers = len(costs)
    num_jobs = len(costs[0])

    # Biến nhị phân x[i][j]
    x = {}
    for i in range(num_engineers):
        for j in range(num_jobs):
            x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # Ràng buộc: Mỗi kỹ sư làm đúng 1 việc
    for i in range(num_engineers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_jobs)]) == 1)

    # Ràng buộc: Mỗi việc chỉ giao cho 1 kỹ sư
    for j in range(num_jobs):
        solver.Add(solver.Sum([x[i, j] for i in range(num_engineers)]) == 1)

    # Hàm mục tiêu: Tổng chi phí -> Min
    objective_terms = []
    for i in range(num_engineers):
        for j in range(num_jobs):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("=== KẾT QUẢ BÀI TOÁN PHÂN CÔNG ===")
        print(f"Tổng chi phí tối thiểu: {solver.Objective().Value()}")
        for i in range(num_engineers):
            for j in range(num_jobs):
                if x[i, j].solution_value() > 0.5:
                    print(f"-> Kỹ sư {i+1} làm việc {j+1} (Chi phí: {costs[i][j]})")
    else:
        print("Không tìm thấy phương án phân công tối ưu.")

if __name__ == '__main__':
    solve_assignment_problem()