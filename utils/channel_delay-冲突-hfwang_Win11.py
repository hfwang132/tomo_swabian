from TimeTagger import Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime
import time

ch_1 = int(sys.argv[1])
ch_2 = int(sys.argv[2])
sec = int(sys.argv[3])

def Tagger_Connect():
    tagger = createTimeTagger()
    for i in range(1, 19):
        tagger.setTriggerLevel(i, 1.0)
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

measure_list = [ch_1, ch_2]
res_value = 5
number_bin = int(sys.argv[4])
data = Get_correlation(tagger,measure_list,res_value,number_bin)
x_time = np.linspace(-res_value*number_bin/2, res_value*(number_bin)/2, number_bin, endpoint=False)

plt.plot(x_time/1000,data)
plt.xlabel("Time (ns)")
plt.ylabel("Correlation Counts")
plt.show()

# print(max(data_1))
max_label = np.argmax(data)
# print(max_label)
delay_2_1 = x_time[max_label]
print(delay_2_1)
Tagger_DisConnect(tagger)


# np.savetxt(data_1)
