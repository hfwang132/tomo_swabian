from PyQt5 import QtWidgets, uic, QtCore
import sys
import numpy as np
import pyqtgraph as pg


class Pattern_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Pattern_Widget, self).__init__(parent=parent)
        self.parent = parent
        uic.loadUi("Pattern.ui", self)
        self.show()
        self.connect_sig_slot()

        self.pattern_list = []
        self.pattern_list_cur = []


    def connect_sig_slot(self):
        self.Pattern_set.clicked.connect(self.Check_CC)

    def Check_CC(self):
        self.pattern_list = []
        if self.checkBox_1.checkState():
            self.pattern_list.append(1)
        if self.checkBox_2.checkState():
            self.pattern_list.append(2)
        if self.checkBox_3.checkState():
            self.pattern_list.append(3)
        if self.checkBox_4.checkState():
            self.pattern_list.append(4)
        if self.checkBox_5.checkState():
            self.pattern_list.append(5)
        if self.checkBox_6.checkState():
            self.pattern_list.append(6)
        if self.checkBox_7.checkState():
            self.pattern_list.append(7)
        if self.checkBox_8.checkState():
            self.pattern_list.append(8)
        if self.checkBox_9.checkState():
            self.pattern_list.append(9)
        if self.checkBox_10.checkState():
            self.pattern_list.append(10)
        if self.checkBox_11.checkState():
            self.pattern_list.append(11)
        if self.checkBox_12.checkState():
            self.pattern_list.append(12)
        if self.checkBox_13.checkState():
            self.pattern_list.append(13)
        if self.checkBox_14.checkState():
            self.pattern_list.append(14)
        if self.checkBox_15.checkState():
            self.pattern_list.append(15)
        if self.checkBox_16.checkState():
            self.pattern_list.append(16)
        if self.checkBox_17.checkState():
            self.pattern_list.append(17)
        if self.checkBox_18.checkState():
            self.pattern_list.append(18)
        if self.pattern_list_cur != self.pattern_list:
            self.parent.parent.pattern_flag = 1
            self.pattern_list_cur = self.pattern_list
        print(self.pattern_list)

    def Pattern_Reset(self):
        self.pattern_list = []
        for i in range(1, 19):
            exec("self.checkBox_{}.setChecked(False)".format(i))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Pattern_Widget()
    app.exec_()
