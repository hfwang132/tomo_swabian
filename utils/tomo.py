# author: Haifei (haifei_wang@u.nus.edu)
# date: 12 Apr 2024
# function: 6-channel tomography data collection using Swabian Time Tagger

import traceback
import time
import datetime
import sys
import numpy as np
from TimeTagger import Coincidences, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp

# 0. coincidence combinations for 6 channels
# I admit this is chunky, but it's good for readability

coin_lst = [
    [1, 3, 5, 7, 9, 11], [2, 3, 5, 7, 9, 11], [1, 4, 5, 7, 9, 11], [2, 4, 5, 7, 9, 11], 
    [1, 3, 6, 7, 9, 11], [2, 3, 6, 7, 9, 11], [1, 4, 6, 7, 9, 11], [2, 4, 6, 7, 9, 11], 
    [1, 3, 5, 8, 9, 11], [2, 3, 5, 8, 9, 11], [1, 4, 5, 8, 9, 11], [2, 4, 5, 8, 9, 11], 
    [1, 3, 6, 8, 9, 11], [2, 3, 6, 8, 9, 11], [1, 4, 6, 8, 9, 11], [2, 4, 6, 8, 9, 11], 
    [1, 3, 5, 7, 10, 11], [2, 3, 5, 7, 10, 11], [1, 4, 5, 7, 10, 11], [2, 4, 5, 7, 10, 11], 
    [1, 3, 6, 7, 10, 11], [2, 3, 6, 7, 10, 11], [1, 4, 6, 7, 10, 11], [2, 4, 6, 7, 10, 11], 
    [1, 3, 5, 8, 10, 11], [2, 3, 5, 8, 10, 11], [1, 4, 5, 8, 10, 11], [2, 4, 5, 8, 10, 11], 
    [1, 3, 6, 8, 10, 11], [2, 3, 6, 8, 10, 11], [1, 4, 6, 8, 10, 11], [2, 4, 6, 8, 10, 11], 
    [1, 3, 5, 7, 9, 12], [2, 3, 5, 7, 9, 12], [1, 4, 5, 7, 9, 12], [2, 4, 5, 7, 9, 12], 
    [1, 3, 6, 7, 9, 12], [2, 3, 6, 7, 9, 12], [1, 4, 6, 7, 9, 12], [2, 4, 6, 7, 9, 12], 
    [1, 3, 5, 8, 9, 12], [2, 3, 5, 8, 9, 12], [1, 4, 5, 8, 9, 12], [2, 4, 5, 8, 9, 12], 
    [1, 3, 6, 8, 9, 12], [2, 3, 6, 8, 9, 12], [1, 4, 6, 8, 9, 12], [2, 4, 6, 8, 9, 12], 
    [1, 3, 5, 7, 10, 12], [2, 3, 5, 7, 10, 12], [1, 4, 5, 7, 10, 12], [2, 4, 5, 7, 10, 12], 
    [1, 3, 6, 7, 10, 12], [2, 3, 6, 7, 10, 12], [1, 4, 6, 7, 10, 12], [2, 4, 6, 7, 10, 12], 
    [1, 3, 5, 8, 10, 12], [2, 3, 5, 8, 10, 12], [1, 4, 5, 8, 10, 12], [2, 4, 5, 8, 10, 12], 
    [1, 3, 6, 8, 10, 12], [2, 3, 6, 8, 10, 12], [1, 4, 6, 8, 10, 12], [2, 4, 6, 8, 10, 12]
]

# 1. init tagger

tagger = createTimeTagger()
for i in range(1, 17):
    tagger.setTriggerLevel(i, 0.4)

# 2. set delay
# you can retrieve these delays from `all_channel_delay.py`

delays = [-2652, -6350, -9632, -4300, -9227, -4585, -9050, -8720, -7812, -3165, -12087]

for i in range(11):
    tagger.setInputDelay(i + 2, delays[i])

# 3. init coincidence channels

coin = Coincidences(
                tagger, coin_lst, coincidenceWindow=5000, timestamp=CoincidenceTimestamp.Average
                )

countrate = Countrate(tagger=tagger, channels=coin.getChannels())



# 4. seconds and loops input via command line
sec = int(sys.argv[1])
loop = int(sys.argv[2])

# 5. metadata - time and filename
start_time = datetime.datetime.now()
start_time_filename = start_time.strftime("%y.%m.%d_%H.%M.%S")
start_time_str = start_time.strftime("20%y-%m-%d %H:%M:%S")
filename = f"data_tomo/tomo_{start_time_filename}.txt"
finish_time = (start_time + datetime.timedelta(seconds=sec*loop))
finish_time_str = finish_time.strftime("20%y-%m-%d %H:%M:%S")
print(f"Start time : {start_time_str}")
print(f"Estimated finish time : {finish_time_str}")

# 6. open file for writing
f = open(filename, "w")



# 7. measurement with interruption handles
# you can interrupt this measurement anytime you like
# the existing measured data will be saved

try:
    for l in range(loop): # loop is necessary since quality of states may degrade over time
        countrate.startFor(int(sec * 1e12)) # start counting for `sec` seconds
        for i in range(0, sec):
            time.sleep(1) # counting is an asynchronous process
            count = countrate.getCountsTotal() # get counts every second for display
            ### display ###
            # some metadata
            sys.stdout.write(f"Loop {l + 1}/{loop}, Time remaining: {(sec - i - 1):4d} s, Total counts: {sum(count)}, "
                              f"Counts/min: {sum(count)*60/(i+1):.2f}, "
                              f"Sec/count: {(i + 1) / (sum(count) if sum(count) else sum(count)+1):.2f} \n")
            
            # display the counts
            n_lines = 4
            for j in range(0, len(count), int(len(count) / n_lines)):
                sys.stdout.write(np.array2string(count[j: int(j + len(count) / n_lines)], separator=' ', 
                                                 max_line_width=np.inf, formatter={'int': '{:3d}'.format})[1:-1] + "\n")

            # refresh everything
            if i < sec - 1: 
                sys.stdout.write("\x1b[1A\x1b[2K" * (n_lines + 1)) 
            ### end display ###
        
        countrate.waitUntilFinished() # make sure to synchronize
        count = countrate.getCountsTotal() # get counts
        f.write(f"{count}\n") # and write to your file
except Exception:
    traceback.print_exc()
finally:
    # interruption handle which makes sure the existing measured data are properly saved
    if countrate.isRunning():
        print("========================================================================================")
        print(f"Measurement interrupted! Do not worry, the existing measured data will be saved in {filename}.")
        print("========================================================================================")
        countrate.stop()
        count = countrate.getCountsTotal()
        f.write(f"{count}\n")
    # make sure to close your file and disconnect your TT
    f.close()
    freeTimeTagger(tagger=tagger)