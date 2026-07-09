from ortools.linear_solver import pywraplp

def solve_production_problem():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Không thể khởi tạo solver GLOP")
        return

    # Biến quyết định: Số lượng sản phẩm I và II
    x1 = solver.NumVar(0, solver.infinity(), 'x1')
    x2 = solver.NumVar(0, solver.infinity(), 'x2')

    # Ràng buộc nguyên liệu
    solver.Add(4 * x1 + 2 * x2 <= 60, "Nguyen_Lieu_A")
    solver.Add(2 * x1 + 4 * x2 <= 48, "Nguyen_Lieu_B")

    # Hàm mục tiêu: Lợi nhuận -> Max
    solver.Maximize(8 * x1 + 6 * x2)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("=== KẾT QUẢ BÀI TOÁN SẢN XUẤT ===")
        print(f"Số lượng sản phẩm I (x1): {x1.solution_value():.2f}")
        print(f"Số lượng sản phẩm II (x2): {x2.solution_value():.2f}")
        print(f"Lợi nhuận tối đa: {solver.Objective().Value():.2f}")
    else:
        print("Không tìm thấy lời giải tối ưu.")

if __name__ == '__main__':
    solve_production_problem()