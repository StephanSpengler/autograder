from functools import reduce
import concurrent.futures as future
import numpy as np

def A5(zip_exam): ##Exercise A5
    return list(map(lambda p: p[0], filter(lambda p: p[1]==5, zip_exam)))
    #return [names[i] for i in range(len(names)) if grades[i]==5]
def generate_list(n):
    a = np.random.randint(0,9)
    b = np.random.randint(10, 19)
    return np.random.uniform(a,b,n)
def Estimation(lst): ##Exercise A6
    n = len(lst)
    n_p = 4
    reshaped = lst.reshape(n_p, -1)
    with future.ProcessPoolExecutor() as ex:
        minimals = ex.map(min, reshaped)
        maximals = ex.map(max, reshaped)
        minimals = list(minimals)
        maximals = list(maximals)
    total_min = min(minimals)
    total_max = max(maximals)
    return n/(n-1)*total_min - 1/(n-1)*(total_max), n/(n-1)*total_max - 1/(n-1)*(total_min)
def main():

    print("Test A5:")
    names = ["Anna", "Anton", "Jakob",
    "Ludwig", "Nils", "Oliver",
    "Rafael", "Tim"]
    grades = [3,4,5,5,4,3,5,5]
    #for l, f in zip(names, grades):
    #   print(f'{l} receives {f}')
    print(A5(zip(names, grades)))
    print("Test A6:")
    n = 10**6
    lst = generate_list(n)
    print(Estimation(lst))
if __name__ == '__main__':
    main()