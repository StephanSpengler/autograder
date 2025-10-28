class Queue:

    class Node:
        def __init__(self, data, succ=None):
            self.data = data
            self.succ = succ

    def __init__(self):
        self.first = None

    def __iter__(self):
        current = self.first
        while current:
            yield current.data
            current = current.succ
    def __str__(self):
        return '(' + ', '.join([str(x) for x in self]) + ')'

    def Enqueue(self, x):
        if self.first:
            f = self.first
            while f.succ:
                f = f.succ
            f.succ = Queue.Node(x, None)
        else:
            self.first = Queue.Node(x, None)

    def Dequeue(self): ##Exercise A3
        if self.first: self.first = self.first.succ

class BST:
    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right
            self.count = 1  # For use in task B3

        def __str__(self): # For use in task B3 -- to be completed
            return f'({self.key}, {self.count})'

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
        """help function for B3 -- basically, you need to overwrite the stardard insert"""
        pass

    def insert(self, key):
        def _insert(r, key):
            if r is None:
                return self.Node(key)
            elif key < r.key:
                r.left = _insert(r.left, key)
            elif key > r.key:
                r.right = _insert(r.right, key)
            else:
                pass  # Already there
            return r

        self.root = _insert(self.root, key)

    def min(self): ##Exercise A4
        if self.root is None:
            return None
        else:
            r = self.root
            while r.left:
                r = r.left
            return r.key
        
    def insert(self, key):
        """B3: An insert method that maintain the count field in the nodes"""
        def insert(key, r):
            if r == None:
                return BST.Node(key), 1
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
    
class LinkedList:

    class Node:
        def __init__(self, data, succ=None):
            self.data = data
            self.succ = succ

    def __init__(self):
        self.first = None

    def __iter__(self):
        current = self.first
        while current:
            yield current.data
            current = current.succ

    def __str__(self):
        return '(' + ', '.join([str(x) for x in self]) + ')'

    def insert(self, x):
        if self.first is None or x <= self.first.data:
            self.first = LinkedList.Node(x, self.first)
        else:
            f = self.first
            while f.succ and x > f.succ.data:
                f = f.succ
            f.succ = LinkedList.Node(x, f.succ)
    
    def middle(self): ##Exercise B2
        slow = fast = self.first
        if self.first is None:
            return None
        else:
            while fast and fast.succ:
                slow = slow.succ
                fast = fast.succ.succ
            return slow.data


def main():
    print("Test A3:")
    queue = Queue()
    for x in ["A", "B", "C", "D", "E"]:
        queue.Enqueue(x)
    print(queue)
    for _ in range(5):
        queue.Dequeue()
        print(queue)
    print("Test A4:")
    X = [ [5, 8, 3, 7, 2, 6, 9], [4, 1, 3, 6, 7, 5, 8], []]
    for x in X:
        bst = BST()
        for i in x:
            bst.insert(i)
        m = bst.min()
        print(m)
    print("Test B2:")
    X = [[0], [1,2],[1,2,3],[1,2,3,5],[1,2,3,5,8], list(range(100))] #
    for lst in X:
        ll = LinkedList()
        for x in lst:
            ll.insert(x)
        print(ll.middle(), lst[(len(lst))//2])
    print("Test B3:")
    inserts = (10, 5, 1, 7, 20, 30, 15, 17, 12, 2)
    print(f'Inserted keys: {inserts}')
    tree = BST()
    for x in inserts:
        tree.insert(x)
        print(f'After inserting {x}: {repr(tree)}')    
       
if __name__ == '__main__':
    main()
