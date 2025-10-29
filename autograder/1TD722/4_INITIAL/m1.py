def base3(x): ##Exercise A1
    pass

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
    pass
class TowerHanoi: ##Exercise B1
   pass

def main():
    print("Test A1:")
    for x in [3,6,20,27,28,52]:
        print(base3(x), end=" ")
    print("")
    print("Test A2:")
    for x in [9,18,9000, 25689, 24606]:
        print(divisible9(x), end=" ")
    print("")
    print("Test B1:")
    TH = TowerHanoi(3)
    for _ in range(5):
        TH.step()
        print(TH)
if __name__ == '__main__':
    main()