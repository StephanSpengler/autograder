import sys
from exam_grader import init, Task
from test_utilities import uses_HOF_test, run_function_tests, expect_output_param, presetA, presetB

#
# Tests
# 

def test_A5(module):
    tests = [(name, list(zip(names, grades))) for name, names, grades in [
        ("Empty", [], []),
        ("All Low", ["Anna", "Anton", "Liv", "Nils", "Oliver", "Tim"], [3,4,4,4,3,4]),
        ("All High", ["Elise", "Jakob", "Ludwig", "Rafael"], [5,5,5,5]),
        ("Some", ["Anna", "Anton", "Elise", "Liv", "Nils", "Oliver", "Rafael" ,"Tim"], [3,4,5,5,4,3,5,5]),
        ("Large", [f"Student{i}" for i in range(1000)], [i % 6 + 1 for i in range(1000)]),
    ]]
    return run_function_tests(module, "A5", [uses_HOF_test(1)] + [expect_output_param(name + " " + str(values), values, list(map(lambda p: p[0], filter(lambda p: p[1]==5, values)))) for name, values in tests])

import numpy as np
from time import perf_counter as pc
import threading
def test_A6(module):
    def estimate_seq(lst):
        n = len(lst)
        total_min = min(lst)
        total_max = max(lst)
        return n/(n-1)*total_min - 1/(n-1)*total_max, n/(n-1)*total_max - 1/(n-1)*total_min

    tests = [(name, np.array(list(iter)) ) for name, iter in [
        ("Four", range(4, 8)),
        ("Small", range(12)),
        ("Medium", range(1000)),
        ("Large", list(range(10000)) * 4),
        ("Random", np.random.uniform(42, 69, 5000)),
    ]]

    def test_runtime(func):
        def test_func(f, lst):
            start = pc()
            f(lst)
            end = pc()
            return end - start
        def test_batch(size, runs):
            lst = np.random.uniform(0, size**0.5, size)
            count = 0
            p_time_sum = 0
            s_time_sum = 0
            for _ in range(runs):
                p_time = test_func(func, lst)
                p_time_sum += p_time
                s_time = test_func(estimate_seq, lst)
                s_time_sum += s_time
                if p_time * 1.5 < s_time:
                    count += 1
            return count, p_time_sum / runs, s_time_sum / runs

        count, p_time_sum, s_time_sum = test_batch(10**5, 5)
        if count >= 3:
            return None

        def worker():
            print("Running extended performance test for 'Estimation'...")
            count, p_time_sum, s_time_sum = test_batch(10**7, 3)
            print(f"Parallel time avg: {p_time_sum:.4f}s, sequential time avg: {s_time_sum:.4f}s")
            if count >= 2:
                print("Extended test passed.")
            else:
                print("Failed. Retrying with even larger test...")
                count, p_time_sum, s_time_sum = test_batch(10**8, 1)
                print(f"Parallel time avg: {p_time_sum:.4f}s, sequential time avg: {s_time_sum:.4f}s")
                if count >= 1:
                    print("Extended test passed.")
                else:
                    print("Extended test failed.")
        threading.Thread(target=worker).start()
        return f"Test 'runtime' failed: Parallel time (avg: {p_time_sum:.4f}s) not significantly less than sequential time (avg: {s_time_sum:.4f}s). See console for more accurate test."

    return run_function_tests(module, "Estimation", [test_runtime] + [expect_output_param(name + " " + str(values), values, estimate_seq(values)) for name, values in tests])

#
# Main
# 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <script_name> <submissions_folder>")
        sys.exit(1)

    submissions_root = sys.argv[1]
    output_path = "m3.csv"
    submission_file = "m3.py"
    tasks: list[Task] = [
        ("A5", test_A5, presetA),
        ("A6", test_A6, presetA),
    ]

    init(submissions_root, output_path, submission_file, tasks)