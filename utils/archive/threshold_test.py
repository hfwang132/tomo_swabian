# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 15
    ch_2 = 16
    

    tagger = createTimeTagger()
    
    coin_window = 500

    coin = Coincidence(
            tagger, [ch_1, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    
    
    ran = 25000
    step = 250

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

    plt.figure(figsize=(6,8))

    thresholdRange = np.arange(0.67,0.8,0.02)

    for triggerLevel in thresholdRange:
        count_lst = []
        tagger.setTriggerLevel(ch_1, triggerLevel)
        tagger.setTriggerLevel(ch_2, triggerLevel)

        print("triggerLevel: " + str(triggerLevel))

        for delay in range(-ran,ran,step):
            tagger.setInputDelay(ch_2, delay)
            countrate = Countrate(tagger=tagger, channels=[ch_1, ch_2, coin.getChannel()])
            countrate.startFor(int(1e10))
            countrate.waitUntilFinished()
            count = countrate.getData()
            count = [int(num) for num in count]
            print(delay, count)
            count_lst.append([delay] + count)

        filename = f"data_Haifei/g11_{t}_{ran}_{step}_{coin_window}_{ch_1}_{ch_2}_{triggerLevel:.3f}.txt"

        with open(filename, "w") as f:
            for count in count_lst:
                f.write(" ".join(map(str, count)))
                f.write("\n")

        count_lst = np.array(count_lst)
        plt.plot(count_lst[:,0], count_lst[:,3])

    freeTimeTagger(tagger)

    plt.xlabel("delay/ps")
    plt.ylabel("coin. count rate/Hz")
    plt.legend(list(map(str, thresholdRange)))
    plt.savefig(filename[:-4]+".jpg")
    plt.show()
    
    
    
    
    
    
