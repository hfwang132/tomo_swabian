# This file is created by Haifei

import datetime
import time
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 15
    ch_2 = 16
    
    tagger = createTimeTagger()

    coin = Coincidence(
                    tagger, [ch_1, ch_2], coincidenceWindow=2000, timestamp=CoincidenceTimestamp.ListedFirst
                )

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

    plt.figure(figsize=(12,12))

    triggerLevel_lower = 0.01
    triggerLevel_upper = 1.1
    triggerLevel_step = 0.01

    thresholdRange = np.arange(triggerLevel_lower,triggerLevel_upper,triggerLevel_step)

    count_lst = []
    for y in thresholdRange:
        lst = []
        st = time.time()
        print(f"y = {y:.3f}")
        for x in thresholdRange:
            tagger.setTriggerLevel(ch_1, x)
            tagger.setTriggerLevel(ch_2, y)
            
            countrate = Countrate(tagger=tagger, channels=[coin.getChannel()])
            countrate.startFor(int(1e10))
            countrate.waitUntilFinished()
            count = countrate.getData()[0]
            lst.append(count)
        et = time.time()
        print(f"time elapsed = {(et - st):.2f} s")
        count_lst.append(lst)

    count_lst = np.array(count_lst)
    filename = f"data_Haifei/threshold_coin_{t}_{ch_1}_{ch_2}_{triggerLevel_lower:.3f}_{triggerLevel_upper:.3f}_{triggerLevel_step:.3f}.txt"

    np.savetxt(filename, count_lst)

    freeTimeTagger(tagger)

    x, y = np.meshgrid(thresholdRange, thresholdRange)

    # ax = plt.axes(projection='3d')
    # ax.plot_surface(x, y, count_lst, cmap='viridis')
    plt.imshow(count_lst, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis')
    plt.colorbar()
    plt.xlabel("threshold for 15")
    plt.ylabel("threshold for 16")

    plt.savefig(filename[:-4]+".jpg")
    plt.show()
    
    
    
    
    
    
