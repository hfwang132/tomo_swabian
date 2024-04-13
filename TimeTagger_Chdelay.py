from operator import truediv
import os
import sys
import random
import threading
from xml.etree.ElementTree import TreeBuilder

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QCheckBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from time import sleep


# from functools import partial

# matplotlib for the plots, including its Qt backend
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

# numpy for statistical analysis
import numpy as np

# all required TimeTagger dependencies
from TimeTagger import Coincidences, Counter, Correlation, createTimeTagger, freeTimeTagger, Countrate, CoincidenceTimestamp, Coincidence


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi("TimeTagger_Chdelay.ui", self)
        self.label_connect.setText("OFF")
        self.step_value = 0
        self.connect_value = 0
        self.show()
        self.connect_sig_slot()

        self.ui.set_coin_windows.setRange(0, 10)
        self.ui.set_integ_time.setRange(0, 10000)
        self.ui.delay_time.setDigitCount(12)

        self.list_1 = list()
        self.list_2 = list()

    def connect_sig_slot(self):
        self.ui.push_connect.clicked.connect(self.connectTT)
        self.ui.push_disconnect.clicked.connect(self.disconnectTT)
        self.ui.set_all.clicked.connect(self.set_parameters)
        self.ui.relash.clicked.connect(self.Check_CC_1)
        self.ui.measure.clicked.connect(self.measurement)
        self.ui.CLOSE.clicked.connect(self.close_fun)

    def connectTT(self):
        if self.connect_value == 0:
            self.connect_value = 1
            self.tagger = createTimeTagger()
            self.tagger.setTriggerLevel(1, 0.5)
            self.tagger.setTriggerLevel(2, 0.5)
            self.tagger.setTriggerLevel(3, 0.5)
            self.tagger.setTriggerLevel(4, 0.5)
            self.tagger.setTriggerLevel(5, 0.5)
            self.tagger.setTriggerLevel(6, 0.5)
            self.tagger.setTriggerLevel(7, 0.5)
            self.tagger.setTriggerLevel(8, 0.5)
            self.tagger.setTriggerLevel(9, 0.5)
            self.tagger.setTriggerLevel(10, 0.5)
            self.tagger.setTriggerLevel(11, 0.5)
            self.tagger.setTriggerLevel(12, 0.5)
            self.tagger.setTriggerLevel(13, 0.5)
            self.tagger.setTriggerLevel(14, 0.5)
            self.tagger.setTriggerLevel(15, 0.5)
            self.tagger.setTriggerLevel(16, 0.5)
            self.tagger.setTriggerLevel(17, 0.5)
            self.tagger.setTriggerLevel(18, 0.5)
            print("TimeTagger ultra Connect Sucessfully")
            self.label_connect.setText("ON")

    def disconnectTT(self):
        if self.connect_value == 1:
            self.connect_value = 0
            freeTimeTagger(self.tagger)
            print("TimeTagger ultra Disconnect Sucessfully")
            self.label_connect.setText("OFF")

    def set_parameters(self):
        if self.connect_value == 1:
            self.coin_windows = self.ui.set_coin_windows.value()
            self.integ_time = self.ui.set_integ_time.value()
            print("Set Parameters Successfully.")
            self.Label_parameter.setText("Successfully")
        else:
            print("Please Connect TimeTagger!")
            self.Label_parameter.setText("Please Connect TimeTagger!")

    def Check_CC_1(self):
        self.list_1 = list()
        if self.ui.checkBox_1_1.checkState():
            self.list_1.append(1)
        if self.ui.checkBox_1_2.checkState():
            self.list_1.append(2)
        if self.ui.checkBox_1_3.checkState():
            self.list_1.append(3)
        if self.ui.checkBox_1_4.checkState():
            self.list_1.append(4)
        if self.ui.checkBox_1_5.checkState():
            self.list_1.append(5)
        if self.ui.checkBox_1_6.checkState():
            self.list_1.append(6)
        if self.ui.checkBox_1_7.checkState():
            self.list_1.append(7)
        if self.ui.checkBox_1_8.checkState():
            self.list_1.append(8)
        if self.ui.checkBox_1_9.checkState():
            self.list_1.append(9)
        if self.ui.checkBox_1_10.checkState():
            self.list_1.append(10)
        if self.ui.checkBox_1_11.checkState():
            self.list_1.append(11)
        if self.ui.checkBox_1_12.checkState():
            self.list_1.append(12)
        if self.ui.checkBox_1_13.checkState():
            self.list_1.append(13)
        if self.ui.checkBox_1_14.checkState():
            self.list_1.append(14)
        if self.ui.checkBox_1_15.checkState():
            self.list_1.append(15)
        if self.ui.checkBox_1_16.checkState():
            self.list_1.append(16)
        if self.ui.checkBox_1_17.checkState():
            self.list_1.append(17)
        if self.ui.checkBox_1_18.checkState():
            self.list_1.append(18)
        print(self.list_1)
 
    def measurement(self):
        self.step_value = 0
        self.Coin_list = []
        if len(self.list_1) == 2:
            self.result.setText("The Delay is")
            channel_s = Correlation(
                self.tagger, self.list_1[0], self.list_1[1], binwidth = 50, n_bins = 4000)
            channel_s.clear()
            channel_s.startFor(int(1e9*self.integ_time))
            channel_s.waitUntilFinished()
            channel_data = channel_s.getData()
            x_time = np.linspace(-50*4000/2,50*4000/2,4000)
            delay_2_1 = x_time[np.argmax(channel_data)]
            print(delay_2_1)
            print(int(delay_2_1))
            self.ui.delay_time.display(delay_2_1)
        else:
            self.result.setText("Please choose two channels to calculate the delay time!!!!")



    def close_fun(self):
        if self.connect_value == 1:
            freeTimeTagger(self.tagger)
        self.connect_value = 0
        self.step_value = 1
        self.label_connect.setText("OFF")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    # window.use_config()
    app.exec_()
