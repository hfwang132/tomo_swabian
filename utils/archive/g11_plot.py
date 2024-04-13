# This file is created by Haifei

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    filename = "g11_40000_50_100.txt"
    # count_lst = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    count_lst = [[int(x) for x in line.strip().split()] for line in lines]
    count_lst = np.array(count_lst, dtype=np.int)
    print(count_lst)
    plt.plot(count_lst[:,0], count_lst[:,3])
    plt.xlabel("delay/ps")
    plt.ylabel("coincidence count rate/Hz")
    plt.show()
