# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt
import sys

tagger = createTimeTagger()

if __name__ == "__main__":


    s_ch = int(sys.argv[1])
    e_ch = int(sys.argv[2])
    sec = sys.argv[3]
    
    # s_ch = 1
    # e_ch = 3
    n_ch = e_ch - s_ch + 1
    n_grid = 4

    fig, axes = plt.subplots(n_ch // n_grid + 1, n_ch if n_ch < n_grid else n_grid, figsize=(15,8))
    axes = axes.flatten() if n_ch > 1 else [axes]

    for ch in range(s_ch, e_ch + 1):
        # ch = 3
        print(f"Testing channel {ch}")

        t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

        thresholdRange = np.arange(0.1,1,0.05)

        count_lst = []

        for triggerLevel in thresholdRange:
            
            tagger.setTriggerLevel(ch, triggerLevel)

            # print("triggerLevel: " + str(triggerLevel))

            countrate = Countrate(tagger=tagger, channels=[ch])
            countrate.startFor(int(1e12))
            countrate.waitUntilFinished()
            count = countrate.getData()[0]
            count = int(count)
            print(triggerLevel, count)
            count_lst.append(count)
            
        count_lst = np.array(count_lst)

        axes[ch - s_ch].plot(thresholdRange, count_lst, "-o")
        axes[ch - s_ch].set_title(f"Ch {ch}")

    plt.xlabel("triggerLevel")
    plt.ylabel("count rate/Hz")
    plt.show()

    freeTimeTagger(tagger)
