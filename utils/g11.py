# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence
import matplotlib.pyplot as plt
import sys
 
print("Arguments passed:")

for arg in sys.argv:
    print(arg, end = " ")

print("\n")

if __name__ == "__main__":

    ch_1 = int(sys.argv[1])
    ch_2 = int(sys.argv[2])
    triggerLevel = 0.8

    tagger = createTimeTagger()
    tagger.setTriggerLevel(ch_1, triggerLevel)
    tagger.setTriggerLevel(ch_2, triggerLevel)

    coin_window = int(sys.argv[5])

    coin = Coincidence(
            tagger, [ch_1, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    
    count_lst = []
    ran = int(sys.argv[3])
    step = int(sys.argv[4])
    # for delay in range(-2000,-500,50):
    for delay in range(-ran,ran,step):#range(-25000,-15000,step):
        tagger.setInputDelay(ch_2, delay)
        countrate = Countrate(tagger=tagger, channels=[ch_1, ch_2, coin.getChannel()])
        countrate.startFor(int(1e12))
        countrate.waitUntilFinished()
        count = countrate.getData()
        count = [int(num) for num in count]
        print(delay, count)
        count_lst.append([delay] + count)

    freeTimeTagger(tagger)

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
    filename = f"data_Haifei/g11_{t}_{ran}_{step}_{coin_window}_{ch_1}_{ch_2}_{triggerLevel}.txt"

    count_lst = np.array(count_lst)

    plt.figure(figsize=(12,8))
    plt.plot(count_lst[:,0], count_lst[:,3])
    plt.xlabel("delay/ps")
    plt.ylabel("coin. count rate/Hz")
    
    try:
        plt.savefig(filename[:-4]+".jpg")
        with open(filename, "w") as f:
            for count in count_lst:
                f.write(" ".join(map(str, count)))
                f.write("\n")
    except:
        print("not working in the directory, cannot save pictures and data!")
        pass
    
    plt.show()
    
    


