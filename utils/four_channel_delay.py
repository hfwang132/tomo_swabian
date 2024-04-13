from TimeTagger import Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, Coincidence, CoincidenceTimestamp
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime
import time

ch_H = int(sys.argv[1])
ch_V = int(sys.argv[2])
ch_1h = int(sys.argv[3])
ch_2h = int(sys.argv[4])
sec = int(sys.argv[5])
number_bin = int(sys.argv[6])

def Tagger_Connect():
    tagger = createTimeTagger()
    for i in range(1, 19):
        tagger.setTriggerLevel(i, 1.5)
    print("TimeTagger ultra Connect Sucessfully")
    return tagger

def Tagger_DisConnect(tagger):
    freeTimeTagger(tagger)
    print("TimeTagger ultra Disconnect Sucessfully")

def Measure_getValue(tagger, measure_list):
    channel_s = Countrate(tagger, measure_list)
    channel_s.clear()
    channel_s.startFor(int(1e9 * 500))
    channel_s.waitUntilFinished()
    channel_data = channel_s.getData()
    return channel_data
        
def Get_correlation(tagger,list,res_value,number_bin):
    channel_s = Correlation(tagger, list[0], list[1], binwidth=res_value, n_bins=number_bin)
    channel_s.clear()
    # sec = 60
    channel_s.startFor(int(sec * 1e12))
    for i in range(0, sec - 1):
        sys.stdout.write("\r")
        sys.stdout.write(f"Time remaining: {(sec - i - 1):4d} s")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")
    channel_s.waitUntilFinished()
    channel_data = channel_s.getData()
    return channel_data

tagger = Tagger_Connect()
# tagger.setInputDelay(ch_H, 0)
# tagger.setInputDelay(ch_V, 0)

# 45 degree
ch_1h_H = Coincidence(
            tagger, [ch_H, ch_1h], coincidenceWindow=5000, timestamp=CoincidenceTimestamp.Average
            )

ch_2h_V = Coincidence(
            tagger, [ch_V, ch_2h], coincidenceWindow=5000, timestamp=CoincidenceTimestamp.Average
            )

# 0 degree
ch_1h_V = Coincidence(
            tagger, [ch_V, ch_1h], coincidenceWindow=5000, timestamp=CoincidenceTimestamp.Average
            )

ch_2h_H = Coincidence(
            tagger, [ch_H, ch_2h], coincidenceWindow=5000, timestamp=CoincidenceTimestamp.Average
            )

degree_0 = False

measure_list_45 = [ch_1h_H.getChannel(), ch_2h_V.getChannel()]
measure_list_0 = [ch_2h_H.getChannel(), ch_1h_V.getChannel()]
res_value = 5

if degree_0:
    data_0 = Get_correlation(tagger,measure_list_0,res_value,number_bin)
else:
    data_45 = Get_correlation(tagger,measure_list_45,res_value,number_bin)

x_time = np.linspace(-res_value*number_bin/2,res_value*(number_bin)/2,number_bin)

if degree_0:
    plt.plot(x_time/1000, data_0)
else:
    plt.plot(x_time/1000, data_45)
plt.xlabel("Time (ns)")
plt.ylabel("Correlation Counts")
plt.show()

# print(max(data_1))
if degree_0:
    max_label = np.argmax(data_0)
else:
    max_label = np.argmax(data_45)
# print(max_label)
delay = x_time[max_label]
print(delay)
Tagger_DisConnect(tagger)


# np.savetxt(data_1)