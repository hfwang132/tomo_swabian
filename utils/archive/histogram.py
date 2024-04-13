# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

if __name__ == "__main__":

    t = "23.11.17_17.23.37"

    count_lst_1 = np.loadtxt(f"poisson_{t}_0.05_1000.0.txt")
    count_lst_2 = np.loadtxt(f"poisson_{t}_0.10_1000.0.txt")
    count_lst_3 = np.loadtxt(f"poisson_{t}_0.40_1000.0.txt")
    count_lst_4 = np.loadtxt(f"poisson_{t}_0.80_1000.0.txt")

    plt.hist(count_lst_1, bins=np.size(count_lst_1))
    plt.show()

