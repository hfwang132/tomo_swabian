# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 2

    tagger = createTimeTagger()

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

    plt.figure(figsize=(10,6))

    thresholdRange = np.arange(0.01,0.2,0.005)

    count_lst = []

    for triggerLevel in thresholdRange:
        
        tagger.setTriggerLevel(ch_1, triggerLevel)

        print("triggerLevel: " + str(triggerLevel))


        countrate = Countrate(tagger=tagger, channels=[ch_1])
        countrate.startFor(int(1e12))
        countrate.waitUntilFinished()
        count = countrate.getData()[0]
        count = int(count)
        print(triggerLevel, count)
        count_lst.append(count)
        
    count_lst = np.array(count_lst)

    freeTimeTagger(tagger)

    plt.plot(thresholdRange, count_lst, "-o")
    plt.xlabel("triggerLevel")
    plt.ylabel("count rate/Hz")
    plt.show()
