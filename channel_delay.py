from TimeTagger import Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate
import matplotlib.pyplot as plt
import numpy as np

def Tagger_Connect():
    tagger = createTimeTagger()
    tagger.setTriggerLevel(1, 0.5)
    tagger.setTriggerLevel(2, 0.5)
    tagger.setTriggerLevel(3, 0.5)
    tagger.setTriggerLevel(4, 0.5)
    tagger.setTriggerLevel(5, 0.5)
    tagger.setTriggerLevel(6, 0.5)
    tagger.setTriggerLevel(7, 0.5)
    tagger.setTriggerLevel(8, 0.5)
    tagger.setTriggerLevel(9, 0.5)
    tagger.setTriggerLevel(10, 0.5)
    tagger.setTriggerLevel(11, 0.5)
    tagger.setTriggerLevel(12, 0.5)
    tagger.setTriggerLevel(13, 0.5)
    tagger.setTriggerLevel(14, 0.5)
    tagger.setTriggerLevel(15, 0.5)
    tagger.setTriggerLevel(16, 0.5)
    tagger.setTriggerLevel(17, 0.5)
    tagger.setTriggerLevel(18, 0.5)
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
    channel_s.startFor(int(1e12))
    channel_s.waitUntilFinished()
    channel_data = channel_s.getData()
    return channel_data

tagger = Tagger_Connect()
tagger.setInputDelay(1, 0)
tagger.setInputDelay(2, 0)
tagger.setInputDelay(3, 0)

measure_list = [1 ,5]
res_value = 50
number_bin = 400
data_1 = Get_correlation(tagger,measure_list,res_value,number_bin)
x_time = np.linspace(-res_value*number_bin/2,res_value*number_bin/2,number_bin)

plt.plot(x_time/1000,data_1)
plt.xlabel("Time (ns)")
plt.ylabel("Correlation Counts")
plt.show()

# print(max(data_1))
max_label = np.argmax(data_1)
# print(max_label)
delay_2_1 = x_time[max_label]
print(delay_2_1)
Tagger_DisConnect(tagger)