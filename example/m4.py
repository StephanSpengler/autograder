import sys
from library.exam_grader import init, Task
from library.test_utilities import collect_failed, presetA, presetB

#
# Tests
# 

import io
from contextlib import redirect_stdout
from unittest.mock import patch

def test_calculator(module, tests):
    tests.append(("quit", "Bye"))
    buf = io.StringIO()
    user_inputs = iter([input for (input, _) in tests])
    outputs = []
    def fake_input(prompt=""):
        outputs.append(buf.getvalue().rstrip())
        buf.truncate(0)
        buf.seek(0)
        return next(user_inputs)

    # Capture printed output
    error = None
    with patch("builtins.input", fake_input), redirect_stdout(buf):
        try:
            module.main()
        except SystemExit:
            # expected when 'quit' is entered
            pass
        except Exception as e:
            error = e

    outputs.append(buf.getvalue().rstrip())
    failed = []
    for ((input, expected), output) in zip([("start", "Numerical calculator")] + tests, outputs):
        if expected.startswith("***"):
            if output.startswith(expected):
                continue
        if not output == expected:
            failed.append(f"Test '{input}' failed: expected:\n{expected}\nbut got:\n{output}")
    if error is not None:
        failed.append(f"Test raised an unexpected exception: {error}")
    
    return collect_failed(failed)

def test_A7(module):
    return test_calculator(module, [
        ("sqrt(9)", "3.0"),
        ("sqrt(16)", "4.0"),
        ("sqrt(2)", str(2**0.5)),
        ("sqrt(0)", "0.0"),
        ("sqrt(25)", "5.0"),
        ("sqrt(-1)", "*** Evaluation error:"), # messsage may vary
        ("sqrt(9", "*** Syntax error:"), # messsage may vary
    ])

def test_A8(module):
    mem = "\n".join([
        "   0     : 0",
        "   1     : 1",
        "   2.0   : 1",
        "   3.0   : 2",
        "   4.0   : 3",
        "   5.0   : 5",
    ])
    tests = [
        ("fib(5)", "5"),
        ("mem", mem),
        ("fib(100)", "354224848179261915075"),
        ("fib(99)", "218922995834555169026"),
        ("fib(101)", "573147844013817084101"),
        ("fib(-2)", "*** Evaluation error:  Illegal argument to fib: -2.0"),
    ]
    return test_calculator(module, tests)

import re
def test_B4(module):
    buf = io.StringIO()
    age = 42
    inputs = [""]
    outputs = []
    expecteds = ["Numerical calculator"]
    pattern = re.compile(r"Is your age less than (\d+)\?:")
    def fake_input(prompt=""):
        if len(outputs) > 1000:
            raise RuntimeError("Too many inputs/outputs, possible infinite loop")
        prompt = prompt.strip()
        outputs.append(buf.getvalue().rstrip())
        buf.truncate(0)
        buf.seek(0)
        if prompt == "Input:":
            if len(expecteds) < 2:
                # no append here, wait for question
                inputs.append("age()")
                return "age()"
            else:
                expecteds.append(str(age)) # this is the expected output for the age input
                expecteds.append("Bye")
                inputs.append("quit")
                return "quit"
        match = pattern.match(prompt)
        if match:
            expecteds.append("") # this is the expected output for the question
            try:
                q = int(match.group(1))
                if age < q:
                    inputs.append("yes")
                    return "yes"
                else:
                    inputs.append("no")
                    return "no"
            except:
                pass
        raise RuntimeError(f"Test failed: unexpected prompt: '{prompt}'")

    # Capture printed output
    error = None
    with patch("builtins.input", fake_input), redirect_stdout(buf):
        try:
            module.main()
        except SystemExit:
            # expected when 'quit' is entered
            pass
        except Exception as e:
            error = e

    outputs.append(buf.getvalue().rstrip())
    failed = []
    for (input, expected, output) in zip(inputs, expecteds, outputs):
        if expected.startswith("***"):
            if output.startswith(expected):
                continue
        if not output == expected:
            failed.append(f"Test '{input}' failed: expected:\n{expected}\nbut got:\n{output}")
    if error is not None:
        failed.append(f"Test raised an unexpected exception: {error}")
        
    return collect_failed(failed) + "\n" + test_calculator(module, [
        ("age", "*** Syntax error:"), # messsage may vary
        ("age(", "*** Syntax error:"), # messsage may vary
        ("age(5)", "*** Syntax error:"), # messsage may vary
        ("age()", ""),
        ("y", "*** Syntax error:"), # message may vary
    ])

#
# Main
# 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <script_name> <submissions_folder>")
        sys.exit(1)

    submissions_root = sys.argv[1]
    output_path = "m4.csv"
    submission_file = "m4.py"
    tasks: list[Task] = [
        ("A7", test_A7, presetA),
        ("A8", test_A8, presetA),
        ("B4", test_B4, presetB),
    ]

    init(submissions_root, output_path, submission_file, tasks)