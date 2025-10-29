from functools import reduce
import concurrent.futures as future
import numpy as np

def A5(zip_exam): ##Exercise A5
    out = []
    for name, grade in zip_exam:
        if grade == 5:
            out.append(name)
    return out
def generate_list(n):
    a = np.random.randint(0,9)
    b = np.random.randint(10, 19)
    return np.random.uniform(a,b,n)
def Estimation(lst): ##Exercise A6
    n = len(lst)
    n_p = 4
    with future.ProcessPoolExecutor() as executor:
        futures = [executor.submit(EstimationSeq, lst[i::n_p]) for i in range(n_p)]
    results = [f.result() for f in future.as_completed(futures)]
    import statistics
    minmin = statistics.mean(r[0] for r in results)
    maxmax = statistics.mean(r[1] for r in results)
    l = n / (n-1)
    u = 1 / (n-1)
    a = l * minmin - u * maxmax
    b = l * maxmax - u * minmin
    return (a, b)
def EstimationSeq(l):
    return (min(l), max(l))
def main():

    print("Test A5:")
    names = ["Anna", "Anton", "Jakob",
    "Ludwig", "Nils", "Oliver",
    "Rafael", "Tim"]
    grades = [3,4,5,5,4,3,5,5]
    #for l, f in zip(names, grades):
       # print(f'{l} receives {f}')
    print(A5(zip(names, grades)))
    print("Test A6:")
    n = 10**6
    lst = generate_list(n)
    print(Estimation(lst))
if __name__ == '__main__':
    main()