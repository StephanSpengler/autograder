def base3(x): ##Exercise A1
    if x < 0:
        return '-' + base3(-x)
    elif x <3:
        return str(x)
    else:
        return base3(x//3) + str(x % 3)

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
    if x<0:
        return divisible9(-x)
    elif x==0 or x==9:
        return True
    elif x<10:
        return False
    else:
        return divisible9(digit_sum(x))
    
class TowerHanoi: ##Exercise B1
   def bricklek(self):
       def _bricklek(k, Start=0, Goal=2, Help=1):
           if k== 0:
               return []
           else:
               return  _bricklek(k - 1, Start, Help, Goal) + \
                       [(Start, Goal)] + \
                       _bricklek(k - 1, Help, Goal, Start)

       return _bricklek(self.n)

   def __init__(self, n):
       self.n = n
       self.ListofList = [list(range(n)),[],[]]
       self._time = 0
       self.instructions = self.bricklek()

   def __str__(self):
       Stacks = ["Start", "Help", "Goal"]
       repr = "Step" + str(self._time)+"\n"
       for s,l in zip(Stacks, self.ListofList):
           repr += s + ":"+"\n"
           for n in l:
               repr += "*"*(n+1)+"\n"
       return repr

   def step(self):
       current = self.instructions[self._time]
       Out = current[0]
       In = current[1]
       element = self.ListofList[Out][0]
       self.ListofList[Out] = self.ListofList[Out][1:]
       self.ListofList[In].insert(0,element)
       self._time = self._time+1

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