# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 15

    tagger = createTimeTagger()

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

    plt.figure(figsize=(10,6))

    triggerLevel_lower = 0.01
    triggerLevel_upper = 0.89
    triggerLevel_step = 0.01

    thresholdRange = np.arange(triggerLevel_lower,triggerLevel_upper,triggerLevel_step)

    lst = []
    for triggerLevel in thresholdRange:
        
        tagger.setTriggerLevel(ch_1, triggerLevel)
        
        countrate = Countrate(tagger=tagger, channels=[ch_1])
        countrate.startFor(int(1e11))
        countrate.waitUntilFinished()
        count = countrate.getData()[0]
        count = int(count)
        print(f"{triggerLevel:.3f}", count)
        lst.append([triggerLevel, count])

    lst = np.array(lst)
    filename = f"data_Haifei/threshold_{t}_{ch_1}_{triggerLevel_lower:.3f}_{triggerLevel_upper:.3f}_{triggerLevel_step:.3f}.txt"
    plt.plot(lst[:,0], lst[:,1])

    with open(filename, "w") as f:
        for it in lst:
            f.write(" ".join(map(str, it)))
            f.write("\n")

    freeTimeTagger(tagger)

    plt.ylim([0, None])
    plt.xlabel("threshold voltage/V")
    plt.ylabel("count rate/Hz")
    plt.savefig(filename[:-4]+".jpg")
    plt.show()
    
    
    
    
    
    
