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
    ch_3 = int(sys.argv[3])
    triggerLevel = 0.8

    tagger = createTimeTagger()
    tagger.setTriggerLevel(ch_1, triggerLevel) # heralding
    tagger.setTriggerLevel(ch_2, triggerLevel)
    tagger.setTriggerLevel(ch_3, triggerLevel)

    coin_window = 1000

    coin = Coincidence(
            tagger, [ch_1, ch_2, ch_3], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    
    

    count_lst = []
    ran = 80000
    step = 500
    delayRange = np.arange(-ran, ran, step)
    # for delay in range(-20000,-16000,100):
    for delay_herald in delayRange:#range(-25000,-15000,step):
        count_lst_herald = []
        for delay in delayRange:#range(-25000,-15000,step):
            tagger.setInputDelay(ch_1, delay_herald)
            tagger.setInputDelay(ch_3, delay)
            countrate = Countrate(tagger=tagger, channels=[coin.getChannel()])
            countrate.startFor(int(5e10))
            countrate.waitUntilFinished()
            count = countrate.getData()[0]
            print(delay_herald, delay, count)
            count_lst_herald.append(count)
        count_lst.append(count_lst_herald)

    freeTimeTagger(tagger)

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
    filename = f"data_Haifei/g111_{t}_{ran}_{step}_{coin_window}_{ch_1}_{ch_2}_{ch_3}_{triggerLevel}.txt"

    count_lst = np.array(count_lst)

    plt.figure(figsize=(12,8))
    
    delay_herald, delay = np.meshgrid(delayRange, delayRange)

    im = True

    if im:
        plt.imshow(count_lst, extent=[delay_herald.min(), delay_herald.max(), delay.min(), delay.max()], origin='lower', cmap='viridis')
        plt.colorbar()
        plt.xlabel("delay herald")
        plt.ylabel("delay")
    else:
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(delay_herald, delay, count_lst, linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)

    try:
        np.savetxt(filename, count_lst)
        plt.savefig(filename[:-4]+".jpg")
    except:
        print("not working in the directory, cannot save pictures and data!")
        
    plt.show()
    
    
    


