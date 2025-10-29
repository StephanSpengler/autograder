def base3(x): ##Exercise A1
    return str(x) if x < 3 else base3(x // 3) + str(x % 3)

def divisible9(x): ##Exercise A2
    def digit_sum(x):
        """ Computes and returns the sum of the digits
        """
        if x < 10:
            return x
        else:
            result  = 0
            y = str(x)
            for i in y:
                result += int(i)
            return result
    while x > 9:
        x = digit_sum(x)
    return x == 9 or x == 0

class TowerHanoi: ##Exercise B1
    def __init__(self, n):
        self.towers = [list(reversed(range(1, n+1))), [], []]
        self.n = n
        self.steps = 0
        self.gen = self.move(n, 0, 2, 1)

    def step(self):
        self.steps += 1
        src, dst = next(self.gen)
        self.towers[dst].append(self.towers[src].pop())

    def move(self, n, src, dst, help):
        if n == 1:
            yield (src, dst)
        else:
            yield from self.move(n-1, src, help, dst)
            yield (src, dst)
            yield from self.move(n-1, help, dst, src)
    
    def __str__(self):
        out = f"Step{self.steps}\n"
        for l in reversed(range(self.n)):
            for tower in self.towers:
                size = tower[l] if len(tower) > l else 0
                out += "*" * size + " " * (self.n - size + 1)
            out += "\n"
        return out

def main():
    print("Test A1:")
    for x in [3,6,20,27,28,52]:
        print(base3(x), end=" ")
    print("")
    print("Test A2:")
    for x in [9,18,9000, 25689, 24606]:
        print(divisible9(x), end=" ")
    for x in range(-100,1000):
        assert divisible9(x) == (x % 9 == 0)
    print("")
    print("all good")
    print("Test B1:")
    TH = TowerHanoi(3)
    for _ in range(5):
        TH.step()
        print(TH)
if __name__ == '__main__':
    main()