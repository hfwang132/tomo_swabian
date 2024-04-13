# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

if __name__ == "__main__":

    ch_1 = 15

    # triggerLevel = 0.1
    triggerLevels = [0.05, 0.1, 0.4, 0.8]

    integration_time = 1 * 1e12

    tagger = createTimeTagger()

    countrate = Countrate(tagger=tagger, channels=[ch_1])

    for triggerLevel in triggerLevels:
        count_lst = []
        tagger.setTriggerLevel(ch_1, triggerLevel)

        for i in range(100):
            countrate.startFor(int(integration_time))
            countrate.waitUntilFinished()
            count = countrate.getData()[0]
            count_lst.append(count)
            # print(count)

        count_lst = np.array(count_lst)

        np.savetxt(f"poisson_{t}_{triggerLevel:.2f}_{integration_time * 1e-9:.1f}.txt", count_lst)

        mean = np.sum(count_lst) / np.size(count_lst)

        standard_deviation = np.sqrt(np.sum((count_lst - mean) ** 2) / (np.size(count_lst) - 1))

        # print(count_lst)
        print(f"Trigger Level = {triggerLevel:.1f} V")
        print(f"Mean = {mean:.2f} Hz")
        print(f"Standard Deviation = {standard_deviation:.2f} Hz")
        print(f"Integration Time = {integration_time * 1e-9:.1f} ms")
        print("===============")
    

    





