from TimeTagger import Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime
import time

tagger = createTimeTagger()
for i in range(1, 19):
    tagger.setTriggerLevel(i, 1)
print("TimeTagger ultra Connect Sucessfully")

bin_width = 5
number_bin = 20000
sec = 30

# Define Correlation

corr_1_2 = Correlation(tagger, 1, 2, binwidth=bin_width, n_bins=number_bin)

corr_1_4 = Correlation(tagger, 1, 4, binwidth=bin_width, n_bins=number_bin)
corr_1_6 = Correlation(tagger, 1, 6, binwidth=bin_width, n_bins=number_bin)
corr_1_8 = Correlation(tagger, 1, 8, binwidth=bin_width, n_bins=number_bin)
corr_1_10 = Correlation(tagger, 1, 10, binwidth=bin_width, n_bins=number_bin)
corr_1_12 = Correlation(tagger, 1, 12, binwidth=bin_width, n_bins=number_bin)

corr_2_3 = Correlation(tagger, 2, 3, binwidth=bin_width, n_bins=number_bin)
corr_2_5 = Correlation(tagger, 2, 5, binwidth=bin_width, n_bins=number_bin)
corr_2_7 = Correlation(tagger, 2, 7, binwidth=bin_width, n_bins=number_bin)
corr_2_9 = Correlation(tagger, 2, 9, binwidth=bin_width, n_bins=number_bin)
corr_2_11 = Correlation(tagger, 2, 11, binwidth=bin_width, n_bins=number_bin)

corr_lst = [corr_1_2, 
            corr_1_4, 
            corr_1_6, 
            corr_1_8, 
            corr_1_10,
            corr_1_12,
            corr_2_3, 
            corr_2_5, 
            corr_2_7, 
            corr_2_9, 
            corr_2_11]

# Start Measurements

for corr in corr_lst:
    corr.startFor(int(sec * 1e12))

for i in range(0, sec - 1):
    sys.stdout.write("\r")
    sys.stdout.write(f"Time remaining: {(sec - i - 1):4d} s")
    sys.stdout.flush()
    time.sleep(1)
print("\n")

time.sleep(1) # Make sure the measurements are completed

# Retrieve Data

corr_1_2_data = corr_1_2.getData()

corr_1_4_data = corr_1_4.getData()
corr_1_6_data = corr_1_6.getData()
corr_1_8_data = corr_1_8.getData()
corr_1_10_data = corr_1_10.getData()
corr_1_12_data = corr_1_12.getData()

corr_2_3_data = corr_2_3.getData()
corr_2_5_data = corr_2_5.getData()
corr_2_7_data = corr_2_7.getData()
corr_2_9_data = corr_2_9.getData()
corr_2_11_data = corr_2_11.getData()

corr_data_lst = [
    corr_1_2_data ,
    corr_2_3_data ,
    corr_1_4_data ,
    corr_2_5_data ,
    corr_1_6_data ,
    corr_2_7_data ,
    corr_1_8_data ,
    corr_2_9_data ,
    corr_1_10_data,
    corr_2_11_data,
    corr_1_12_data
]

# Plot

x_time = np.linspace(-bin_width*number_bin/2, bin_width*(number_bin)/2, number_bin, endpoint=False) + bin_width/2

fig, ax = plt.subplots(6, 2)
ax[0, 0].plot(x_time, corr_1_2_data)
ax[1, 0].plot(x_time, corr_1_4_data)
ax[2, 0].plot(x_time, corr_1_6_data)
ax[3, 0].plot(x_time, corr_1_8_data)
ax[4, 0].plot(x_time, corr_1_10_data)
ax[5, 0].plot(x_time, corr_1_12_data)
ax[0, 1].plot(x_time, corr_2_3_data)
ax[1, 1].plot(x_time, corr_2_5_data)
ax[2, 1].plot(x_time, corr_2_7_data)
ax[3, 1].plot(x_time, corr_2_9_data)
ax[4, 1].plot(x_time, corr_2_11_data)

ax[0, 0].title.set_text("1/2")
ax[1, 0].title.set_text("1/4")
ax[2, 0].title.set_text("1/6")
ax[3, 0].title.set_text("1/8")
ax[4, 0].title.set_text("1/10")
ax[5, 0].title.set_text("1/12")
ax[0, 1].title.set_text("2/3")
ax[1, 1].title.set_text("2/5")
ax[2, 1].title.set_text("2/7")
ax[3, 1].title.set_text("2/9")
ax[4, 1].title.set_text("2/11")

fig.suptitle('Time differences between all channels')

# for a in ax:
#     a.set_xlabel('time difference/ps')
#     a.set_ylabel('counts')

# mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()
fig.set_size_inches(18, 14)
plt.show()

# Compute delays

delays = []

for data in corr_data_lst:
    max_label = np.argmax(data)
    delay = x_time[max_label]
    delays.append(delay)

for i in range(11):
    if i % 2 == 1:
        delays[i] = delays[i] + delays[0]

# print("")
print(delays)


