# Autograder for 1TD722 exam

This small autograder provides a lightweight, semi-automatic grading workflow for programming exams (or assignments).
It runs automated tests on student submission files, opens the submission in the default editor, and presents a simple GUI to record numeric grades for each task. Results are saved to a CSV file.

## Contents

- `exam_grader.py` - Main interactive grader UI and orchestration.
- `ma1.py` - Example grader runner for assignment MA1. Defines tasks, test functions and grading schema.
- `test_utilities.py` - Helper test functions used by assignment runners (simple test harness, comparators, recursion checks, HOF checks).

## Requirements

- Python 3.8+
- `tkinter` (for the grading GUI). On Debian/Ubuntu: `sudo apt install python3-tk`

## Quick start

1. Prepare a submissions directory where each student has a subdirectory named by their student id or username. Each student's folder should contain the expected submission file (for MA1 the file name is `ma1.py`). Example layout:

```
submissions/
	alice/
		ma1.py
	bob/
		ma1.py
```

2. Run the assignment runner from this `autograder` directory. Example for MA1:

```bash
python3 ma1.py /path/to/submissions
```

3. The grader will create/update `ma1.csv` in the `autograder/` directory. Each row contains a `student` value and one column per task (A1, A2, B1 for MA1). While grading the GUI will:

- open the student's submission file in your default editor (untested on Windows and MacOS - feel free to delete this comment if you think it works),
- run the automated tests and display the textual test results for each task,
- allow you to set a numeric score per task using quick buttons or typing a value,
- save grades to the CSV file.

Use the Prev/Next/Skip buttons to move between students. If you navigate while there are unsaved changes you'll be prompted to save.

## Output CSV format

The CSV created by the grader has a header row with `student` followed by the task ids defined in the runner (for MA1: `A1,A2,B1`). Each student row contains saved numeric scores or blank entries for missing scores.

Example `ma1.csv`:

```
student,A1,A2,B1
alice,1.0,0.8,2.0
bob,0.5,0.0,
```

## How the grader works (developer notes)

- Assignment runners (like `ma1.py`) define a list of tasks with the shape: (`task_id`, `test_function`, `grading_scheme`).
	- `task_id` is a short string shown in the GUI, e.g. `A1`.
	- `test_function` is a callable that accepts the imported student module and returns a human-readable string describing test results.
	- `grading_scheme` is a list of numeric values used to populate quick-score buttons in the GUI.
- The runner calls `exam_grader.init(submissions_root, output_path, submission_file, tasks)` to start the interactive grading.
- Tests are written using the helpers in `test_utilities.py`. Typical helpers include:
	- `run_function_tests(module, func_name, tests)` — runs a set of callable checks on a named function and returns a string summarizing failures or success.
	- `expect_output(name, expected, *params)` — returns a test callable that asserts function output equals `expected` for the given parameters.
	- `is_recursive_test(func)` — checks whether a function uses direct recursion by inspecting source code.

## Adding a new assignment runner

1. Copy `ma1.py` to a new file (e.g. `ma2.py`).
2. Edit the `submission_file`, `output_path` and `tasks` definitions at the bottom to match the new assignment:

- `submission_file` — the filename to look for inside each student's folder (e.g. `ma2.py`).
- `output_path` — the CSV file to write (e.g. `ma2.csv`).
- `tasks` — list of tuples (`id`, `test_fn`, `[score buttons]`).

3. Implement test functions that accept an imported module and return a one-line or multi-line string describing test results.

4. Run the new runner with the submissions directory:

```bash
python3 ma2.py /path/to/submissions
```

### Test contract and helpers

Each `test_fn` you pass to `init()` must accept a single argument: the imported student module. The function should return a human-readable string describing the result of the automated tests for that task; for example, return "All tests passed." on success or one-or-more lines explaining failures. These strings are displayed in the GUI when grading.

To simplify writing tests for functions inside the student module the project provides a few helpers in `test_utilities.py`:

- `run_function_tests(module, func_name, tests)`
	- This wrapper looks up the function named `func_name` inside the imported `module` and calls each test in the `tests` list, passing the extracted function as the single argument. Each test in `tests` must therefore accept the function (not the module) and return `None` for success or a string describing the failure. `run_function_tests` collects these results and returns a single string summary (either "All tests passed." or a concatenation of failure messages).

- `expect_output(name, expected, *params)`
	- Returns a test callable that, when given a function `f`, will call `f(*params)` and compare the result to `expected`. If the result differs, the callable returns an explanatory failure string; otherwise it returns `None`.

- `expect_output_all(tests)`
	- Accepts a list of test descriptions of the form `(name, expected, param1, param2, ...)` and maps them to a list of `expect_output(...)` callables. This list is ready to pass into `run_function_tests`.

Example pattern for a task testing a function named `foo` inside student submissions:

```python
from test_utilities import run_function_tests, expect_output_all

def test_task_1(module):
		# Create descriptions: (name, expected, param1, param2, ...)
		cases = [
				("small", 3, 1, 2),
				("zero", 0, 0),
		]
		# run_function_tests will look up `foo` in the module and run each expect_output test
		return run_function_tests(module, "foo", expect_output_all(cases))

# tasks = [("T1", test_task_1, [0.0, 0.5, 1.0]), ...]
```

This pattern keeps your per-task test functions focused: they accept the imported student module, assemble the per-function tests (using `expect_output` / `expect_output_all`) and return the `run_function_tests(...)` result string.

## Troubleshooting

- If submissions are not opening: adjust the code in the function `_open_file` of the file `exam_grader.py` to your operating system.
- If the GUI doesn't appear: ensure `tkinter` is installed (`python3 -m tkinter` is a quick smoke-test).
- If a student's file fails to import: the GUI will show the import error. Inspect the file in your editor and fix syntax/runtime issues in the student's code before grading.
- If `ma1.csv` is not updated: ensure the grader process has write permission to the `autograder/` directory.

## License & contact

This software is intended for teaching and internal use. If you need help modifying the grader, open an issue or contact the course staff.