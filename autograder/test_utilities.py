import ast
import inspect

#
# Main test runner
# 

def run_function_tests(module, func_name, tests):
    """
    Run a list of test callables on a given function.

    Parameters:
        module: module or namespace containing the function
        func_name: name of the function to test
        tests: list of callables, each taking the function as argument
               and returning None (success) or an error message (failure)
    """
    if not hasattr(module, func_name):
        return f"Function '{func_name}' is not defined."
    
    func = getattr(module, func_name)
    failed = []

    for test_fn in tests:
        msg = test_fn(func)
        if msg is not None:
            failed.append(msg)

    if not failed:
        return "All tests passed."
    
    messages = []
    for i, msg in enumerate(failed):
        if i > 10:
            messages.append(f"... and {len(failed) - 10} more failures.")
            break
        messages.append(msg)
    return "\n".join(messages)

#
# Test utility functions
# 

def expect_output_param(name, param, expected):
    """
    Create a test callable that calls the function with `param`
    and compares the result to expected.

    Returns a callable(func) -> None | error_message
    """
    return expect_output_func(name, lambda f: f(param), expected)

def expect_output_func(name, tester, expected):
    """
    Create a test callable that calls the tester function
    and compares the result to expected.

    Returns a callable(func) -> None | error_message
    """
    if len(name) > 100:
        name = name[:100] + '..'
    def run_test(func):
        try:
            result = tester(func)
        except Exception as e:
            return f"Test '{name}' raised an exception: {e}"

        if result != expected:
            return f"Test '{name}' failed: expected {expected}, got {result}"
        return None
    return run_test

def is_recursive_test(expected=True):
    """
    Checks if the function is directly recursive.
    """
    def test(func):
        try:
            source = inspect.getsource(func)
        except OSError:
            return f"Test 'recursion_check' failed: cannot get source code."

        tree = ast.parse(source)
        func_name = func.__name__

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_name:
                    if expected:
                        return None  # success: recursion detected
                    else:
                        return f"Test 'recursion_check' failed: function is recursive"
        if expected:
            return f"Test 'recursion_check' failed: function is not recursive"
        return None  # success: no recursion detected
    return test

def uses_HOF_test(count=1):
    """
    Checks if the function uses higher-order functions, lambdas, comprehensions, or generator expressions.
    """
    HOF_names = {'map', 'filter', 'reduce', 'any', 'all', 'sorted'}

    def test(func):
        try:
            source = inspect.getsource(func)
        except OSError:
            return f"Test 'HOF_check' failed: cannot get source code."

        tree = ast.parse(source)
        hof_count = 0

        class HOFVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                nonlocal hof_count
                # Direct HOF calls
                if isinstance(node.func, ast.Name) and node.func.id in HOF_names:
                    hof_count += 1
                # Qualified calls like functools.reduce
                if isinstance(node.func, ast.Attribute) and node.func.attr in HOF_names:
                    hof_count += 1
                # Lambda as argument
                for arg in node.args:
                    if isinstance(arg, ast.Lambda):
                        hof_count += 1
                self.generic_visit(node)

            def visit_Lambda(self, node):
                nonlocal hof_count
                hof_count += 1
                self.generic_visit(node)

            def visit_ListComp(self, node):
                nonlocal hof_count
                hof_count += 1
                self.generic_visit(node)

            def visit_SetComp(self, node):
                nonlocal hof_count
                hof_count += 1
                self.generic_visit(node)

            def visit_DictComp(self, node):
                nonlocal hof_count
                hof_count += 1
                self.generic_visit(node)

            def visit_GeneratorExp(self, node):
                nonlocal hof_count
                hof_count += 1
                self.generic_visit(node)

        HOFVisitor().visit(tree)

        if hof_count >= count:
            return None  # success
        else:
            return f"Test 'HOF_check' failed: expected at least {count} higher-order usage(s), found {hof_count}"

    return test
