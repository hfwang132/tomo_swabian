# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 15

    tagger = createTimeTagger()
    
    coin_window = 500
    
    ran = 10000
    step = 200

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")

    plt.figure(figsize=(10,6))

    thresholdRange = np.arange(0.05,0.9,0.1)

    for triggerLevel in thresholdRange:
        count_lst = []
        tagger.setTriggerLevel(ch_1, triggerLevel)

        print("triggerLevel: " + str(triggerLevel))

        for delay in range(-ran,ran,step):
            ch_1_delayed = DelayedChannel(tagger, ch_1, delay)

            coin = Coincidence(
                    tagger, [ch_1, ch_1_delayed.getChannel()], coincidenceWindow=20, timestamp=CoincidenceTimestamp.ListedFirst
                )
            
            countrate = Countrate(tagger=tagger, channels=[ch_1, ch_1_delayed.getChannel(), coin.getChannel()])
            countrate.startFor(int(1e10))
            countrate.waitUntilFinished()
            count = countrate.getData()
            count = [int(num) for num in count]
            print(delay, count)
            count_lst.append([delay] + count)

        filename = f"data_Haifei/g11_self_{t}_{ran}_{step}_{coin_window}_{ch_1}_{triggerLevel:.3f}.txt"

        with open(filename, "w") as f:
            for count in count_lst:
                f.write(" ".join(map(str, count)))
                f.write("\n")

        count_lst = np.array(count_lst)
        plt.plot(count_lst[:,0], count_lst[:,3])

    freeTimeTagger(tagger)

    plt.xlabel("delay/ps")
    plt.ylabel("coin. count rate/Hz")
    plt.legend([f"{threshold:.2f} V" for threshold in thresholdRange])
    plt.savefig(filename[:-4]+".jpg")
    plt.show()
    
    
    
    
    
    
