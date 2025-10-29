import sys
from exam_grader import init, Task
from test_utilities import run_function_tests, expect_output_func, presetA, presetB

# 
# BST implementation
# 
class BST_Sol:
    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right
            self.count = 1

        def __str__(self):
            return str((self.key, self.count))

        def __iter__(self):
            if self.left:
                yield from self.left
            yield self
            if self.right:
                yield from self.right

    def __init__(self, init=None):
        self.root = None
        if init:
            for x in init:
                self.insert(x)

    def __iter__(self):
        if self.root:
            yield from self.root

    def __str__(self):
        return '<' + ', '.join([str(x.key) for x in self]) + '>'

    def __repr__(self):
        return '<' + ', '.join([str(x) for x in self]) + '>'

    def insert(self, key):
        def insert(key, r):
            if r == None:
                return self.Node(key), 1
            elif key == r.key:
                return r, 0
            elif key < r.key:
                r.left, increased = insert(key, r.left)
                r.count += increased
                return r, increased
            else:
                r.right, increased = insert(key, r.right)
                r.count += increased
                return r, increased

        self.root, _ = insert(key, self.root)
        return self

#
# Tests
# 

def test_A3(module):
    def queue_tester(Queue, values):
        q = Queue()
        for x in values:
            q.Enqueue(x)

        out = ""
        for _ in range(len(values)):
            q.Dequeue()
            out += str(q) + "\n"
        return out.strip()

    tests = [
        ("Empty", []),
        ("Single", ["X"]),
        ("Multiple", ["A", "B", "C", "D", "E"]),
        ("Duplicates", ["H", "e", "l", "l", "o"]),
    ]
    def dequeue_all(a):
        return "\n".join("(" + ", ".join(str(x) for x in a[start+1:]) + ")" for start in range(len(a)))
    return run_function_tests(module, "Queue", [expect_output_func(name + " " + str(values), lambda func, values=values: queue_tester(func, values), dequeue_all(values)) for name, values in tests])

import random
def test_A4(module):
    def BST_tester(BST, values):
        bst = BST()
        for x in values:
            bst.insert(x)
        return bst.min()
    
    sorted100 = list(range(100))
    shuffled = sorted100[:]
    random.shuffle(shuffled)
    tests = [
        ("Empty", []),
        ("Single", [42]),
        ("Multiple1", [5, 8, 3, 7, 2, 6, 9]),
        ("Multiple2", [4, 1, 3, 6, 7, 5, 8]),
        ("Sorted", sorted100),
        ("Shuffled", shuffled),
    ]
    return run_function_tests(module, "BST", [expect_output_func(name + " " + str(values), lambda func, values=values: BST_tester(func, values), None if len(values) == 0 else min(values)) for name, values in tests])

def test_B2(module):
    def LL_tester(LinkedList, values):
        ll = LinkedList()
        for x in values:
            ll.insert(x)
        return ll.middle()

    sorted100 = list(range(100))
    shuffled = sorted100[:]
    random.shuffle(shuffled)

    tests = [
        ("Empty", []),
        ("Single", [10]),
        ("Two", [10, 20]),
        ("Three", [10, 20, 30]),
        ("Four", [10, 20, 30, 40]),
        ("Five", [10, 20, 30, 40, 50]),
        ("Six", [10, 20, 30, 40, 50, 60]),
        ("Seven", [10, 20, 30, 40, 50, 60, 70]),
        ("RandomOdd", [7, 1, 3, 9, 5]),
        ("RandomEven", [8, 2, 0, 4]),
        ("Sorted", sorted100),
        ("Shuffled", shuffled),
    ]
    return run_function_tests(module, "LinkedList", [expect_output_func(name + " " + str(values), lambda func, values=values: LL_tester(func, values), None if len(values) == 0 else sorted(values)[len(values)//2]) for name, values in tests])

def test_B3(module):
    def BST_tester(BST, values):
        out = ""
        bst = BST()
        for x in values:
            bst.insert(x)
            out += repr(bst) + "\n"
        return out.strip()

    sorted100 = list(range(100))
    shuffled = sorted100[:]
    random.shuffle(shuffled)
    tests = [
        ("Empty", []),
        ("Single", [42]),
        ("Multiple1", [5, 8, 3, 7, 2, 6, 9]),
        ("Multiple2", [4, 1, 3, 6, 7, 5, 8]),
        ("Duplicates", [10, 20, 10, 30, 20, 40]),
        ("Sorted", sorted100),
        ("Shuffled", shuffled),
    ]
    return run_function_tests(module, "BST", [expect_output_func(name, lambda func, values=values: BST_tester(func, values), BST_tester(BST_Sol, values)) for name, values in tests])

#
# Main
# 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <script_name> <submissions_folder>")
        sys.exit(1)

    submissions_root = sys.argv[1]
    output_path = "m2.csv"
    submission_file = "m2.py"
    tasks: list[Task] = [
        ("A3", test_A3, presetA),
        ("A4", test_A4, presetA),
        ("B2", test_B2, presetB),
        ("B3", test_B3, presetB),
    ]

    init(submissions_root, output_path, submission_file, tasks)