# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence, DelayedChannel
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ch_1 = 1
    # ch_2 = 16

    tagger = createTimeTagger()
    tagger.setTriggerLevel(ch_1, 0.05)
    # tagger.setTriggerLevel(ch_2, 0.5)
    
    count_lst = []

    ran = 40000

    for delay in range(-ran, ran, 100):
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

    freeTimeTagger(tagger)

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
    filename = f"data_Haifei/g11_self_{t}.txt"

    with open(filename, "w") as f:
        for count in count_lst:
            f.write(" ".join(map(str, count)))
            f.write("\n")
    
    count_lst = np.array(count_lst)
    plt.plot(count_lst[:,0], count_lst[:,3])
    plt.show()


