from PyQt5 import QtWidgets, uic, QtCore
import sys
from Pattern import Pattern_Widget
import time
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont
import numpy as np
import pyqtgraph as pg
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence

class Display_Widget(QtWidgets.QWidget):

    request_update = QtCore.pyqtSignal()
    request_data = QtCore.pyqtSignal()
    request_display = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Display_Widget, self).__init__(parent=parent)
        self.parent = parent
        uic.loadUi("panel_display.ui", self)
        self.show()
        self.my_pattern = []
        for i in range(self.parent.pattern_volume):
            self.my_pattern.append(Pattern_Widget(self))
            exec('self.verticalLayout_pattern_{}.addWidget(self.my_pattern[i])'.format(i))
            #self.my_pattern[i].call_ind = i
        self.request_update.connect(self.parent.my_plotter.my_plot.update)
        self.request_display.connect(self.measure_display)
        self.request_data.connect(self.data_acquire)

    def get_bin(self, bin_num, bin_size):
        bin_ans = []
        temp_num = bin_num
        for i in range(bin_size):
            bin_ans.append(temp_num % 2)
            temp_num = temp_num // 2
        return bin_ans

    def tomo_getlist(self):
        self.Single_list = [i for i in range(1, self.parent.tomo_coupler_size+1)]
        self.Coin_list = []
        self.pattern_listt = [[] for i in range(self.parent.pattern_volume)]
        for i in range(self.parent.tomo_coupler_size):
            self.pattern_listt[i].append(i+1)
        for i in range(self.parent.tomo_pattern_size):
            temp_bin = self.get_bin(i, self.parent.tomo_size)
            temp_list = []
            for j in range(self.parent.tomo_size):
                temp_list.append(2 * j + temp_bin[j] + 1)
            self.Coin_list.append(temp_list)
            self.pattern_listt[i + self.parent.tomo_coupler_size] = temp_list
        print(self.pattern_listt, file=self.parent.file_info)
        CC_list = []
        multi_channel_S = self.multi_channel_get(self.Coin_list)
        for i in range(len(multi_channel_S)):
            CC_list.append(multi_channel_S[i])
        self.measure_list = []
        self.measure_list = self.Single_list + CC_list


    def reset_pattern(self):
        self.Single_list = []
        self.Single_label = []
        self.Coin_list = []
        self.Coin_label = []
        self.pattern_listt = [[] for i in range(self.parent.pattern_volume)]
        for i in range(self.parent.display_volume):
            self.my_pattern[i].Pattern_Reset()
        print("Pattern Reset!")

    def get_display_list(self):
        self.Single_list = []
        self.Single_label = []
        self.Coin_list = []
        self.Coin_label = []
        self.pattern_listt = [[] for i in range(self.parent.pattern_volume)]
        for i in range(self.parent.display_volume):
            if len(self.my_pattern[i].pattern_list) != 0:
                if len(self.my_pattern[i].pattern_list) == 1:
                    self.Single_list.append(self.my_pattern[i].pattern_list[0])
                    self.Single_label.append(i)
                else:
                    self.Coin_list.append(self.my_pattern[i].pattern_list)
                    self.Coin_label.append(i)
            if self.parent.save_flag == 1:
                self.pattern_listt[i] = self.my_pattern[i].pattern_list
        if self.parent.save_flag == 1:
            print(self.pattern_listt[i], file=self.parent.file_info)

    def measure_getlist(self):
        CC_list = []
        if len(self.Coin_label) != 0:
            multi_channel_S = self.multi_channel_get(self.Coin_list)
            for i in range(len(multi_channel_S)):
                CC_list.append(multi_channel_S[i])
        self.measure_list = []
        self.measure_list = self.Single_list + CC_list

    def data_acquire(self):
        if self.parent.tomo_flag == 0:
            if self.parent.timer_flag == 1:
                self.parent.my_timer.timer_reset()
        self.current_data = self.Measure_getValue(self.measure_list)
        if self.parent.save_flag == 1:
            print(self.current_data, file=self.parent.file_data)
        if self.parent.tomo_flag == 1:
            self.current_data_s = self.current_data[:self.parent.tomo_coupler_size]
            self.current_data_c = self.current_data[self.parent.tomo_coupler_size:]

    def measure_display(self):
        display_data_s = []
        display_data_c = []
        if len(self.Single_label) == 0:
            display_data_c = self.current_data
        else:
            display_data_s = self.current_data[0:len(self.Single_label)]
            display_data_c = self.current_data[len(self.Single_label):len(self.current_data)]
        for i in range(self.parent.display_volume):
            if i in self.Single_label:
                position = self.Single_label.index(i)
                self.display_list[i] = display_data_s[position]
            if i in self.Coin_label:
                position = self.Coin_label.index(i)
                self.display_list[i] = display_data_c[position]
        self.Number_display(self.display_list)


    def measure_process(self):
        self.get_display_list()
        if self.parent.tomo_flag == 0:
            self.measure_getlist()
        else:
            self.tomo_getlist()
        self.display_list = [0 for i in range(self.parent.display_volume)]
        if self.parent.integ_time > 5000:
            self.parent.my_timer.timer_start()
            self.parent.timer_flag = 1
        while self.parent.step_value == 1:
            if self.parent.step_value == 0:
                if self.parent.save_flag == 1:
                    self.file_info.close()
                    self.file_data.close()
                    self.save_flag = 0
                if self.parent.tomo_flag == 1:
                    self.parent.tomo_term()
                break
            if self.parent.pattern_flag == 1:
                if self.parent.save_flag == 0:
                    self.get_display_list()
                    if self.parent.tomo_flag == 0:
                        self.measure_getlist()
                    self.parent.pattern_flag = 0
                else:
                    self.Label_parameter.setText("Data Acquiring... Coincidence pattern not changed")
                    self.parent.pattern_flag = 0
            #if self.parent.tomo_flag == 1:
                #self.parent.step_value = 0
                #break
            self.data_acquire()
            if self.parent.tomo_flag == 0:
                self.request_display.emit()
                self.request_update.emit()
            if self.parent.tomo_flag == 1:
                self.parent.tomo_timer += 1
                self.parent.my_timer.Measure_Timer.display(self.parent.tomo_timer)
                print(self.current_data_s)
                print(self.current_data_c)
                self.temp_list = np.sum([self.parent.tomo_current_list_c, self.current_data_c], axis=0).tolist()
                self.parent.tomo_current_list_c = self.temp_list
                self.parent.tomo_current_count_c = sum(self.parent.tomo_current_list_c)
                for i in range(self.parent.tomo_coupler_size):
                    self.parent.tomo_current_rate_s[i] = (self.parent.tomo_current_rate_s[i] * (self.parent.tomo_timer - 1) + self.current_data_s[i]) / self.parent.tomo_timer
                if self.parent.tomo_current_count_c > self.parent.tomo_counts:
                    print(self.parent.tomo_current_list_c, file=self.parent.file_data_c)
                    print(self.parent.tomo_current_list_c)
                    self.parent.tomo_current_count_c = 0
                    self.parent.tomo_current_list_c = [0 for i in range(self.parent.tomo_pattern_size)]
                    self.parent.tomo_current_loop += 1
                    if self.parent.tomo_current_loop > self.parent.tomo_loops:
                        self.parent.step_value = 0
                        self.parent.tomo_term()
                self.parent.ui.Event_Counter.display(self.parent.tomo_current_count_c)
                self.parent.ui.Loop_Counter.display(self.parent.tomo_current_loop)
        self.parent.timer_flag = 0


    def Measure_getValue(self, measure_list):
        self.channel_s = Countrate(self.parent.tagger, measure_list)
        self.channel_s.clear()
        self.channel_s.startFor(int(1e9 * self.parent.integ_time))
        self.channel_s.waitUntilFinished()
        channel_data = self.channel_s.getData()
        return channel_data

    def multi_channel_get(self, Coin_list):
        self.channel_c = Coincidences(
            self.parent.tagger, Coin_list, coincidenceWindow=int(1e3 * self.parent.coin_windows), timestamp=CoincidenceTimestamp.ListedFirst
        )
        multi_channel_S = self.channel_c.getChannels()
        return multi_channel_S

    def Number_display(self, display_data):
        for i in range(self.parent.pattern_volume):
                self.my_pattern[i].Pattern_display.display(display_data[i])



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Display_Widget()
    app.exec_()