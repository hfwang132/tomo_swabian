# This file is created by Haifei

import datetime
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence
import matplotlib.pyplot as plt
import sys
import time
 
print("Arguments passed:")

for arg in sys.argv:
    print(arg, end = " ")

print("\n")

def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.1,0.8), **kw)

def annot_min(x,y, ax=None):
    xmin = x[np.argmin(y)]
    ymin = y.min()
    text= "x={:.3f}, y={:.3f}".format(xmin, ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=120")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="bottom")
    ax.annotate(text, xy=(xmin, ymin), xytext=(0.1,0.1), **kw)

if __name__ == "__main__":

    ch_h = int(sys.argv[1])
    ch_1 = int(sys.argv[2])
    ch_2 = int(sys.argv[3])
    triggerLevel = 0.8

    tagger = createTimeTagger()
    tagger.setTriggerLevel(ch_h, triggerLevel) # heralding
    tagger.setTriggerLevel(ch_1, triggerLevel)
    tagger.setTriggerLevel(ch_2, triggerLevel)

    coin_window = int(sys.argv[6])

    coin_1h = Coincidence(
            tagger, [ch_h, ch_1], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    coin_2h = Coincidence(
            tagger, [ch_h, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    coin_12 = Coincidence(
            tagger, [ch_1, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    coin_12h = Coincidence(
            tagger, [ch_h, ch_1, ch_2], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
        )
    
    tagger.setInputDelay(ch_h, -2200)

    count_lst = []
    ran = int(sys.argv[4])
    step = int(sys.argv[5])
    for delay in range(-ran,ran,step):
        tagger.setInputDelay(ch_2, delay)
        countrate = Countrate(tagger=tagger, channels=[ch_h, ch_1, ch_2, coin_12h.getChannel(), coin_1h.getChannel(), coin_2h.getChannel(), coin_12.getChannel()])
        sec = int(sys.argv[7])
        countrate.startFor(int(sec * 1e12))
        for i in range(0, sec - 1):
            sys.stdout.write("\r")
            sys.stdout.write(f"Time remaining: {(sec - i - 1):4d} s")
            sys.stdout.flush()
            time.sleep(1)
        print("")
        countrate.waitUntilFinished()
        count = countrate.getData()
        
        s_h = count[0]
        s_1 = count[1]
        s_2 = count[2]
        c_12h = count[3]
        c_1h = count[4]
        c_2h = count[5]
        c_12 = count[6]

        unheralded_g2 = c_12 * 80_000_000 / (s_1 * s_2 + 1e-7)
        heralded_g2 = c_12h * s_h / (c_1h * c_2h + 1e-7)
        
        count = [int(num) for num in count]

        print(delay, count)
        count_lst.append([delay/1000] + count + [heralded_g2, unheralded_g2])

    freeTimeTagger(tagger)

    t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
    filename = f"data_Haifei/g111_normalized_{t}_{ran}_{step}_{coin_window}_{ch_h}_{ch_1}_{ch_2}_{triggerLevel}.txt"

    count_lst = np.array(count_lst)

    fig, axs = plt.subplots(2, figsize=(8, 15))
    # plt.figure(figsize=(12,8))
    axs[0].plot(count_lst[:,0], count_lst[:,4], 'o', label="coin_12h")
    axs[0].plot(count_lst[:,0], count_lst[:,5], 'o', label="coin_1h")
    axs[0].plot(count_lst[:,0], count_lst[:,6], 'o', label="coin_2h")
    axs[0].plot(count_lst[:,0], count_lst[:,7], 'o', label="coin_12")
    # axs[0].set_xlabel("(t2 - t1)/ns")
    axs[0].set_ylabel("coin. count rate/Hz")
    axs[0].legend()
    axs[1].plot(count_lst[:,0], count_lst[:,8], 'o', label="heralded_g2")
    # axs[1].plot(count_lst[:,0], count_lst[:,9], 'o', label="unheralded_g2")
    axs[1].set_xlabel("(t2 - t1)/ns")
    axs[1].set_ylabel("g2")
    axs[1].legend()
    annot_min(count_lst[:,0], count_lst[:,8])
    # annot_max(count_lst[:,0], count_lst[:,9])

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
    
    
    


