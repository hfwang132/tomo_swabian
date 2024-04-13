import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    filename = "data_Haifei/g11_40000_50_100.txt"
    # count_lst = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    count_lst = [[int(x) for x in line.strip().split()] for line in lines]
    count_lst = np.array(count_lst, dtype=np.int)
    print(count_lst)
    plt.plot(count_lst[:,0], count_lst[:,3])
    plt.plot(count_lst[:,0], count_lst[:,3] + 10000)
    plt.xlabel("delay/ps")
    plt.ylabel("coincidence count rate/Hz")
    lst = [0.1, 0.2]
    print(list(map(str, lst)))
    plt.legend(list(map(str, lst)))
    plt.show()
