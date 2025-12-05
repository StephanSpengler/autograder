# Autograder for 1TD722 exam

This small autograder provides a lightweight, semi-automatic grading workflow for programming exams (or assignments).
It runs automated tests on student submission files, opens the submission in the default editor, and presents a simple GUI to record numeric grades for each task. Results are saved to a CSV file.

## Contents

- `exam_grader.py` - Main interactive grader UI and orchestration.
- `test_utilities.py` - Helper test functions used by assignment runners (simple test harness, comparators, recursion checks, HOF checks).
- `example/` - Example assignment runners for the 2025 1TD722 exam. Defines tasks, test functions and grading schema.

## Requirements

- Python 3.8+
- `tkinter` (for the grading GUI). On Debian/Ubuntu: `sudo apt install python3-tk`

## Quick start

1. Prepare a submissions directory where each student has a subdirectory named by their student id or username. Each student's folder should contain the expected submission file. Example layout:

```
submissions/
	alice/
		m1.py
		m2.py
		m3.py
		m4.py
	bob/
		m1.py
		m2.py
		m3.py
		m4.py
```

2. Run the assignment runner from this `autograder` directory.

```bash
python3 -m example.m1 example/submissions	# run grader for assignment 1 -> m1.csv
python3 -m example.m2 example/submissions	# run grader for assignment 2 -> m2.csv
...
```

3. Each runner writes a CSV (`m1.csv`, `m2.csv`, ...) containing `student` plus one column per task defined in the runner. While grading the GUI will:

- open the student's submission file in your default editor (untested on Windows and MacOS - feel free to delete this comment if you think it works),
- run the automated tests and display the textual test results for each task,
- allow you to set a numeric score per task using quick buttons or typing a value,
- save grades to the CSV file.

Use the Prev/Next/Skip buttons to move between students. If you navigate while there are unsaved changes you'll be prompted to save. The Reload button will reload the submission file and rerun all tests. This is useful in case you changed the file, for example if there was a syntax error preventing the file to load.

## Output CSV format

The CSV created by the grader has a header row with `student` followed by the task ids defined in the runner (for MA1: `A1,A2,B1`). Each student row contains saved numeric scores or blank entries for missing scores.

Example `m1.csv`:

```
student,A1,A2,B1
alice,1.0,0.8,2.0
bob,0.5,0.0,
```

## How the grader works (developer notes)

- Assignment runners (like `m1.py`..`m4.py`) define a `tasks` list with tuples: (`task_id`, `test_function`, `grading_scheme`).
	- `task_id` — short string shown in GUI (e.g. `A1`).
	- `test_function` — callable(module) -> str: accepts the imported student module and returns a human-readable string summarizing tests for that task. This string is displayed in the GUI.
	- `grading_scheme` — list of numeric values used to populate quick-score buttons.
- Callers start the interactive grader with `exam_grader.init(submissions_root, output_path, submission_file, tasks)`.

### Test utilities provided

`test_utilities.py` contains helpers used by the provided runners and recommended when writing new tests. Notable helpers:

- `presetA`, `presetB` — common grading presets used by the runners.
- `load_func(module, func_name)` — get a function object from a module or raise an AttributeError.
- `truncate100(text)` — helper to shorten long messages for display.
- `collect_failed(failed, tests)` — helper that turns a list of failure messages into a single text block (or "All tests passed.").
- `run_function_tests(module, func_name, tests)` — wrapper for testing functions inside a student module:
	- looks up `func_name` in `module` (raises/explains if missing),
	- calls each test in `tests`, passing the extracted function as the single argument,
	- each test callable should accept the function and return `None` on success or an error string on failure,
	- `run_function_tests` collects failures and returns a single string ("All tests passed." or a concatenated failure summary).
- `expect_output_param(name, param, expected)` / `expect_output_func(name, tester, expected)` — helpers to build simple tests that call the student's function (or a custom tester) and compare results to `expected`. They return callables suitable for `run_function_tests`.
- `uses_HOF_test(count=1)` — returns a test that inspects source code and ensures higher-order constructs (map/filter/lambda/comprehensions/generator expressions) are used at least `count` times.
- `is_recursive_test(expected=True)` — checks whether a function uses direct recursion (inspect & AST).

The provided runners (`m1`..`m4`) demonstrate these helpers in action. Each runner defines tasks for its assignment and writes `mX.csv` where `X` is the assignment number.

## Adding a new assignment runner

Follow these steps to add a new grader for an assignment:

1. Copy an existing runner (e.g. `m1.py`) to `mN.py` and edit the bottom of the file.
2. Update the runner configuration:
	 - `submission_file` — the filename expected in each student folder (e.g. `m5.py`).
	 - `output_path` — the CSV file to write (e.g. `m5.csv`).
	 - `tasks` — a list of (`task_id`, `test_fn`, `grading_scheme`) tuples. `test_fn` must follow the contract below.

3. Implement `test_fn` functions.

Test contract (important)

- Each `test_fn` passed to `init()` must accept the imported student module as its single parameter and return a one-line or multi-line string describing the test results for that task. For example, return "All tests passed." on success or a multi-line report explaining failures.
- If you want to test a specific function inside the module, use `run_function_tests(module, func_name, tests)`:
	- `run_function_tests` will extract `func_name` from the module and call each item in `tests` with that function as argument.
	- Each test in `tests` should accept the function (not the module) and return `None` on success or a failure string on error.
	- `run_function_tests` formats a single summary string from the tests which you then return from your `test_fn`.

Helper patterns

- Use `expect_output_param` / `expect_output_func` to build small test callables quickly. Example:

```python
from test_utilities import run_function_tests, expect_output_param

def test_A(module):
		# Tests are (name, param, expected)
		cases = [("small", 1, 2), ("zero", 0, 0)]
		# Build callables and run
		return run_function_tests(module, "foo", [expect_output_param(name, param, expected) for name, param, expected in cases])
```

- Use `expect_output_func(name, tester, expected)` when you need a custom tester wrapper (tester receives the student's function and should return the value to compare).
- Use `uses_HOF_test(count=...)` or `is_recursive_test()` when you need structural checks that inspect source code.

Example task registration (bottom of runner):

```python
tasks = [
		("A1", test_A1, presetA),
		("A2", test_A2, presetA),
		("B1", test_B1, presetB),
]
init(submissions_root, output_path, submission_file, tasks)
```

## Notes on the supplied runners

- The repo currently includes `m1.py`..`m4.py` covering the course exercises. Each runner demonstrates a mix of functional tests, performance checks, structural (AST) checks and I/O interaction tests.

## Troubleshooting

- If submissions are not opening: `exam_grader` uses a platform-aware `_open_file` helper. Adjust or replace `_open_file` in `exam_grader.py` to suit your environment (for headless grading you can make `_open_file` a no-op).
- If the GUI doesn't appear: ensure `tkinter` is installed (`python3 -m tkinter` is a quick smoke-test).
- If a student's file fails to import: the GUI will show the import error. Inspect the file in your editor and fix syntax/runtime issues in the student's code before grading.
- If a CSV is not updated: ensure the grader process has write permission to the `autograder/` directory.

## License

This software is licensed under the GNU General Public License version 3.

## Contact

If you need help modifying the grader, open an issue on GitHub or [contact me](https://www.uu.se/en/contact-and-organisation/staff?query=N22-489) directly.