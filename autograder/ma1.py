import sys
from exam_grader import init, Task
from test_utilities import run_function_tests, is_recursive_test, expect_output_all

#
# Helper functions
# 

def base3_sol(n):
    return "-" + base3_sol(-n) if n < 0 else str(n) if n < 3 else base3_sol(n // 3) + str(n % 3)

def hanoi_test(TowerHanoi):
    out = [""]

    out.append("TowerHanoi(3)")
    TH = TowerHanoi(3)
    for i in range(5):
        TH.step()
        if i % 2:
            out.append(str(TH))

    out.append("TowerHanoi(6)")
    TH = TowerHanoi(6)
    for i in range(20):
        TH.step()
    out.append(str(TH))

    return "\n".join(out)

#
# Tests
# 

def test_A1(module):
    # Setup tests. Each test is a tuple (name, expected_output, param1, param2, ...)
    tests = [(f"n={n}", base3_sol(n), n) for n in [-100, -10, -1] + list(range(9)) + [10, 100, 1000]]
    # Run tests on function "base3". First test checks for recursion, rest check for expected output.
    return run_function_tests(module, "base3", [is_recursive_test()] + expect_output_all(tests))

def test_A2(module):
    # Setup tests. Each test is a tuple (name, expected_output, param1, param2, ...)
    tests = [(f"n={n}", n % 9 == 0, n) for n in [-45, -25, -5] + list(range(20)) + [81, 1234, 123456789]]
    # Run tests on function "divisible9". First test checks for recursion, rest check for expected output.
    return run_function_tests(module, "divisible9", [is_recursive_test()] + expect_output_all(tests))

def test_B1(module):
    # Run custom test.
    return run_function_tests(module, "TowerHanoi", [hanoi_test])

#
# Main
# 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <script_name> <submissions_folder>")
        sys.exit(1)

    submissions_root = sys.argv[1]
    output_path = "ma1.csv"
    submission_file = "ma1.py"
    tasks: list[Task] = [
        ("A1", test_A1, [0.0, 0.2, 0.5, 0.8, 1.0]),
        ("A2", test_A2, [0.0, 0.2, 0.5, 0.8, 1.0]),
        ("B1", test_B1, [0.0, 0.5, 1.0, 1.5, 2.0]),
    ]

    init(submissions_root, output_path, submission_file, tasks)