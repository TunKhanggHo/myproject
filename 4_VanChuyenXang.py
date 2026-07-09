from ortools.linear_solver import pywraplp

def solve_transportation_problem():
    # Sử dụng solver GLOP cho bài toán vận tải tuyến tính
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Không thể khởi tạo solver GLOP")
        return

    # Số liệu chính xác từ bảng Slide 12:
    # Ma trận chi phí vận chuyển từ kho i đến trạm j
    cost_matrix = [
        [30, 27, 26, 9,  23],  # kho 1
        [13, 4,  22, 3,  1 ],  # kho 2
        [3,  1,  5,  4,  24],  # kho 3
        [16, 30, 17, 10, 16]   # kho 4
    ]
    
    supply = [4, 6, 10, 10]       # Lượng xăng dự trữ tại 4 kho
    demand = [7, 7, 7, 7, 2]       # Nhu cầu tiêu thụ tại 5 trạm

    num_sources = len(supply)
    num_destinations = len(demand)

    # 1. Khai báo biến quyết định x[i][j]: lượng xăng chuyển từ kho i đến trạm j
    x = {}
    for i in range(num_sources):
        for j in range(num_destinations):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')

    # 2. Ràng buộc cung: Tổng lượng xăng xuất đi từ mỗi kho không vượt quá lượng dự trữ
    for i in range(num_sources):
        solver.Add(solver.Sum([x[i, j] for j in range(num_destinations)]) <= supply[i], f'Supply_{i}')

    # 3. Ràng buộc cầu: Mỗi trạm phải nhận đủ nhu cầu tiêu thụ
    for j in range(num_destinations):
        solver.Add(solver.Sum([x[i, j] for i in range(num_sources)]) == demand[j], f'Demand_{j}')

    # 4. Hàm mục tiêu: Tổng chi phí vận chuyển thấp nhất -> Min
    objective_terms = []
    for i in range(num_sources):
        for j in range(num_destinations):
            objective_terms.append(cost_matrix[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("=== KẾT QUẢ BÀI TOÁN VẬN CHUYỂN XĂNG ===")
        print(f"Tổng chi phí vận chuyển tối ưu: {solver.Objective().Value():.2f}\n")
        print("Phương án vận chuyển chi tiết:")
        for i in range(num_sources):
            for j in range(num_destinations):
                val = x[i, j].solution_value()
                if val > 0:
                    print(f"-> Từ Kho {i+1} đến Trạm {j+1}: Vận chuyển {val:.1f} đơn vị (Chi phí gốc: {cost_matrix[i][j]})")
    else:
        print("Không tìm thấy phương án vận chuyển khả thi.")

if __name__ == '__main__':
    solve_transportation_problem()