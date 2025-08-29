import time
from operator import truediv
import os
import sys
import random
import threading
import datetime
from xml.etree.ElementTree import TreeBuilder
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QCheckBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import pyqtgraph as pg
from time import sleep
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from Pattern import Pattern_Widget
from panel_plot import Plot_Widget
from panel_display import Display_Widget
from mtimer import Timer_Widget
import numpy as np
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi("TimeTagger_Main.ui", self)
        self.label_connect.setText("OFF")
        self.step_value = 0
        self.connect_value = 0
        self.show()
        self.connect_sig_slot()
        self.pattern_flag = 0
        self.tomo_flag = 0
        self.save_flag = 0
        self.timer_flag = 0
        self.pattern_volume = 24
        self.display_volume = 24
        self.my_plotter = Plot_Widget(self)
        self.verticalLayout_plotter.addWidget(self.my_plotter)
        self.my_display = Display_Widget(self)
        self.verticalLayout_display.addWidget(self.my_display)
        self.my_timer = Timer_Widget(self)
        self.ui.verticalLayout_timer.addWidget(self.my_timer)
        for i in range(1, 19):
            exec('self.ui.delay_value_{}.setRange(-999999, 999999)'.format(i))
        self.ui.set_coin_windows.setRange(1, 100)
        self.coin_windows = 1
        self.ui.set_integ_time.setRange(1, 10000000)
        self.ui.set_integ_time.setValue(100)
        self.integ_time = 100
        self.ui.tomo_number.setRange(2, 6)
        self.ui.tomo_number.setValue(6)
        self.ui.tomo_count.setRange(1, 10000)
        self.ui.tomo_count.setValue(1000)
        self.ui.tomo_loop.setRange(1, 100)
        self.ui.tomo_loop.setValue(1)


    def connect_sig_slot(self):
        self.ui.push_connect.clicked.connect(self.connectTT)
        self.ui.push_disconnect.clicked.connect(self.disconnectTT)
        self.ui.set_all.clicked.connect(self.set_parameters)
        self.ui.set_all_delay.clicked.connect(self.set_delays)
        self.ui.measure.clicked.connect(self.measurement)
        self.ui.acquire.clicked.connect(self.measure_acquire)
        self.ui.but_tomo.clicked.connect(self.set_tomo)
        self.ui.stop.clicked.connect(self.stop_fun)
        self.ui.CLOSE.clicked.connect(self.close_fun)
        self.ui.pattern_reset.clicked.connect(self.pattern_reset_all)

    def pattern_reset_all(self):
        self.my_display.reset_pattern()

    def save_init(self):
        t = datetime.datetime.now()
        t = t.strftime("%y.%m.%d_%H.%M.%S")
        self.filename_data = f"data\{t}_data.txt"
        self.file_data = open(self.filename_data, "w")
        self.filename_info = f"data\{t}_info.txt"
        self.file_info = open(self.filename_info, "w")

    def measure_acquire(self):
        if self.step_value == 0:
            if self.save_flag == 0:
                self.save_flag = 1
                self.save_init()
                #print(self.coin_windows, self.integ_time, file=self.file_info)
                #self.Label_parameter.setText("Data Acquiring...")
                self.measurement()

    def tomo_init(self):
        t = datetime.datetime.now()
        t = t.strftime("%y.%m.%d_%H.%M.%S")
        self.filename_data_s = f"data\{t}_data_s.txt"
        self.file_data_s = open(self.filename_data_s, "w")
        self.filename_data_c = f"data\{t}_data_c.txt"
        self.file_data_c = open(self.filename_data_c, "w")
        self.filename_info = f"data\{t}_info.txt"
        self.file_info = open(self.filename_info, "w")

    def tomo_term(self):
        self.tomo_flag = 0
        self.tomo_info.setText("Tomo Ended")
        print(self.tomo_current_rate_s, file=self.file_data_s)
        self.file_data_c.close()
        self.file_data_s.close()
        self.file_info.close()

    def set_tomo(self):
        if self.step_value == 0:
            self.tomo_flag = 1
            self.tomo_size = self.ui.tomo_number.value()
            self.tomo_counts = self.ui.tomo_count.value()
            self.tomo_current_count_c = 0
            self.tomo_loops = self.ui.tomo_loop.value()
            self.tomo_current_loop = 1
            self.tomo_coupler_size = 2 * self.tomo_size
            self.tomo_pattern_size = np.power(2, self.tomo_size)
            self.tomo_current_list_c = [0 for i in range(self.tomo_pattern_size)]
            self.tomo_current_rate_s = [0 for i in range(self.tomo_coupler_size)]
            self.tomo_timer = 0
            self.my_timer.Measure_Timer.display(self.tomo_timer)
            self.integ_time = 1000
            self.pattern_volume = self.tomo_coupler_size + self.tomo_pattern_size
            self.tomo_info.setText("Tomo Mode...")
            self.tomo_init()
            self.measurement()

    def connectTT(self):
        if self.connect_value == 0:
            self.connect_value = 1
            self.tagger = createTimeTagger()
            for i in range(1, 16):
                self.tagger.setTriggerLevel(i, 0.4)
            # self.tagger.setTriggerLevel(1, 0.5)
            # self.set_delays()
            print("TimeTagger ultra Connect Sucessfully")
            self.Label_parameter.setText("Connected")
            self.label_connect.setText("ON")

    def disconnectTT(self):
        if self.connect_value == 1:
            self.connect_value = 0
            freeTimeTagger(self.tagger)
            print("TimeTagger ultra Disconnect Sucessfully")
            self.Label_parameter.setText("DisConnected")
            self.label_connect.setText("OFF")

    def set_delays(self):
        if self.connect_value == 1:
            for i in range(1, 16):
                exec('self.tagger.setInputDelay(i, int(self.ui.delay_value_{}.value()))'.format(i))
                self.delay_label.setText("Channel Delay Set")
                print("Delay set successfully.")
            delay_hw_1 = self.tagger.getDelayHardware(1)
            delay_hw_2 = self.tagger.getDelayHardware(2)
            print(f"Hardware delay: {delay_hw_1}, {delay_hw_2}")
            delay_sw_1 = self.tagger.getDelaySoftware(1)
            delay_sw_2 = self.tagger.getDelaySoftware(2)
            print(f"Software delay: {delay_sw_1}, {delay_sw_2}")
        else:
            self.Label_parameter.setText("Please Connect TimeTagger!")

    def set_parameters(self):
        if self.connect_value == 1:
            self.coin_windows = self.ui.set_coin_windows.value()
            if self.tomo_flag == 0:
                self.integ_time = self.ui.set_integ_time.value()
                self.Label_parameter.setText("Set Parameters Successfully.")
            else:
                self.Label_parameter.setText("Tomo mode on, integ_time locked")
            #print("Set Parameters Successfully.")
        else:
            #print("Please Connect TimeTagger!")
            self.Label_parameter.setText("Please Connect TimeTagger!")

    def testplot(self):
        self.my_display.display_list = [(i+1.0) for i in range(self.pattern_volume)]
        self.time_lag = 100
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.my_display.request_update.emit)
        timer.start(self.time_lag)

    def measurement(self):
        #for i in range(1, 19):
        #    print(self.tagger.getTriggerLevel(i))
        if self.step_value == 0:
            if self.connect_value == 1:
                if self.save_flag == 1:
                    self.save_init()
                    self.Label_parameter.setText("Data Acquiring...")
                thread = threading.Thread(target=self.measure_start)
                thread.setDaemon(True)  # 设置守护线程，主线程退出，采集结束
                thread.start()

    def measure_start(self):
        if self.step_value == 0:
            self.step_value = 1
            print('Start measurement!')
            self.my_display.measure_process()


    def stop_fun(self):
        if self.connect_value == 1:
            self.step_value = 0
            if self.save_flag == 1:
                self.save_flag = 0
                self.file_data.close()
                self.file_info.close()
            if self.tomo_flag == 1:
                self.tomo_term()
            self.pattern_volume = 24
            print("Stop measurement!")

    def close_fun(self):
        if self.connect_value == 1:
            freeTimeTagger(self.tagger)
        self.connect_value = 0
        self.step_value = 0
        self.label_connect.setText("OFF")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    # window.use_config()
    app.exec_()
    
