lass Queue:

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
        self.first = self.first.succ if self.first else None

class BST:
    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right
            self.count = 1  # For use in task B3

        def __str__(self): # For use in task B3 -- to be completed to print a pair (key, count)
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

    def insert(self, key): ## Exercise B3 -- basically, you need to overwrite the stardard insert (just comment the one below)
        def _insert(r, key):
            if r is None:
                return self.Node(key)
            if r.key == key:
                pass
            r.count += 1
            if key < r.key:
                r.left = _insert(r.left, key)
            else:
                r.right = _insert(r.right, key)
            return r

        self.root = _insert(self.root, key)
        
    # def insert(self, key):
    #     """ Standard binary search tree insertion, not a part of B3 """
    #     def _insert(r, key):
    #         if r is None:
    #             return self.Node(key)
    #         elif key < r.key:
    #             r.left = _insert(r.left, key)
    #         elif key > r.key:
    #             r.right = _insert(r.right, key)
    #         else:
    #             pass
    #         return r

    #     self.root = _insert(self.root, key)
    
    def min(self): ##Exercise A4
        m = self.root
        while m and m.left:
            m = m.left
        return m.key if m else None

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

    # Complexity: Theta(n)
    def middle(self): ##Exercise B2
        if self.first is None:
            return None
        l = m = self.first
        while l and l.succ:
            l = l.succ.succ
            m = m.succ
        return m.data

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