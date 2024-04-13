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

    coin_12 = Coincidence(
            tagger, [ch_1, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )

    count_lst = []
    ran = int(sys.argv[3])
    step = int(sys.argv[4])
    # for delay in range(-20000,-16000,100):
    for delay in range(-ran,ran,step):#range(-25000,-15000,step):
        tagger.setInputDelay(ch_2, delay)
        countrate = Countrate(tagger=tagger, channels=[ch_1, ch_2, coin_12.getChannel()])
        countrate.startFor(int(50e12))
        countrate.waitUntilFinished()
        count = countrate.getData()
        
        s_1 = count[0]
        s_2 = count[1]
        c_12 = count[2]

        unheralded_g2 = c_12 * 80_000_000 / (s_1 * s_2 + 1e-7)
        
        count = [int(num) for num in count]

        print(delay, count)
        count_lst.append([delay/1000] + count + [unheralded_g2])

    freeTimeTagger(tagger)

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
    filename = f"data_Haifei/g111_normalized_{t}_{ran}_{step}_{coin_window}_{ch_1}_{ch_2}_{triggerLevel}.txt"

    count_lst = np.array(count_lst)

    fig, axs = plt.subplots(2, figsize=(8, 15))
    # plt.figure(figsize=(12,8))
    axs[0].plot(count_lst[:,0], count_lst[:,3], 'o', label="coin_12")
    # axs[0].set_xlabel("(t2 - t1)/ns")
    axs[0].set_ylabel("coin. count rate/Hz")
    axs[0].legend()
    axs[1].plot(count_lst[:,0], count_lst[:,4], 'o', label="unheralded_g2")
    axs[1].set_xlabel("(t2 - t1)/ns")
    axs[1].set_ylabel("g2")
    axs[1].legend()

    try:
        plt.savefig(filename[:-4]+".jpg")
        # np.savetxt(count_lst, filename)
        with open(filename, "w") as f:
            for count in count_lst:
                f.write(" ".join(map(str, count)))
                f.write("\n")
    except:
        print("not working in the directory, cannot save pictures and data!")

    plt.show()
    
    
    


