# This file is created by Haifei

import time
import datetime
import sys
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence
import matplotlib.pyplot as plt
from pylablib.devices import Thorlabs

# 1) init stage

stage = Thorlabs.KinesisMotor("83855348")
stage.home()
stage.wait_for_stop()

# 2) init tagger

tagger = createTimeTagger()
for i in range(1, 17):
    tagger.setTriggerLevel(i, 0.5)

tagger.setInputDelay(8, -1800)
tagger.setInputDelay(3, 6100)
tagger.setInputDelay(5, 2600)
tagger.setInputDelay(7, -6600)

# 3) set channels for tagger

coin_window = 2000

four_fold_idx = [[1, 3, 5, 7], [2, 3, 5, 7], [1, 4, 5, 7], [2, 4, 5, 7], [1, 3, 6, 7], [2, 3, 6, 7], [1, 4, 6, 7], [2, 4, 6, 7], 
             [1, 3, 5, 8], [2, 3, 5, 8], [1, 4, 5, 8], [2, 4, 5, 8], [1, 3, 6, 8], [2, 3, 6, 8], [1, 4, 6, 8], [2, 4, 6, 8]]

four_folds = [Coincidence(
                tagger, four_fold, coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
                ) for four_fold in four_fold_idx]

countrate = Countrate(tagger=tagger, channels=[ch.getChannel() for ch in four_folds])

# dddd = Coincidence(
#             tagger, [1, 3, 5, 7], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
#             )

# ddda = Coincidence(
#             tagger, [1, 3, 5, 8], coincidenceWindow=coin_window, timestamp=CoincidenceTimestamp.ListedFirst
#             )

# countrate = Countrate(tagger=tagger, channels=[dddd.getChannel(), ddda.getChannel()])

# 4) date time

t = datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")
filename = f"data_Haifei/four_photon_vis_{t}.txt"

step = 138
sec = 2*60

if __name__ == "__main__":

    f = open(filename, "w")

    for pos in range(step, 25*34555, step):
        cur_pos = stage.get_position()
        print(f"Current position: {cur_pos/34555:.3f} mm")
        print("Performing four-fold coincidence counting...")
        countrate.startFor(int(sec*1e12))
        for i in range(0, sec):
            sys.stdout.write("\r")
            sys.stdout.write(f"Time remaining: {(sec - i):2d} s")
            sys.stdout.flush()
            time.sleep(1)
        print("\n")
        countrate.waitUntilFinished()
        count = countrate.getCountsTotal()
        print("counts: ", count)
        data = [cur_pos] + [int(num) for num in count]

        f.write(" ".join(map(str, data)))
        f.write("\n")
        f.flush()

        print(f"Moving to position {pos/34555:.3f} mm...")
        stage.move_to(pos)
        stage.wait_for_stop()

    f.close()
