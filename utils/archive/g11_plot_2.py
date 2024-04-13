# This file is created by Haifei

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    filename_1 = "data_Haifei/g11_self_20000_100_20_15.txt"
    filename_2 = "data_Haifei/g11_self_20000_100_20_16.txt"
    # count_lst = []
    with open(filename_1, 'r') as f:
        lines_1 = f.readlines()
    with open(filename_2, 'r') as f:
        lines_2 = f.readlines()
    count_lst_1 = [[int(x) for x in line.strip().split()] for line in lines_1]
    count_lst_1 = np.array(count_lst_1, dtype=np.int)
    count_lst_2 = [[int(x) for x in line.strip().split()] for line in lines_2]
    count_lst_2 = np.array(count_lst_2, dtype=np.int)
    plt.plot(count_lst_1[:,0], count_lst_1[:,3])
    plt.plot(count_lst_2[:,0], count_lst_2[:,3])
    plt.xlabel("delay/ps")
    plt.ylabel("coincidence count rate/Hz")
    plt.show()
