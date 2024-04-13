from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont
import numpy as np
import pyqtgraph as pg


class Check_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Check_Widget, self).__init__(parent=parent)
        self.parent = parent
        uic.loadUi("plot_check.ui", self)
        self.show()
        self.connect_sig_slot()
        self.CR.setValidator(QIntValidator(0, 255))
        self.CG.setValidator(QIntValidator(0, 255))
        self.CB.setValidator(QIntValidator(0, 255))
        self.CR.setText("255")
        self.CG.setText("255")
        self.CB.setText("255")
        self.Set_Flag.setText("OFF")
        self.Set_Flag.setStyleSheet("background-color:transparent")
        self.plot_flag = 0
        self.call_ind = 0
        self.plot_rgb = [255, 255, 255]

    def connect_sig_slot(self):
        self.Set_Button.clicked.connect(self.Plot_Check)

    def Plot_Check(self):
        if self.checkBox.checkState():
            self.plot_flag = 1
            self.parent.plot_RGB[self.call_ind][0] = int(self.CR.text())
            self.parent.plot_RGB[self.call_ind][1] = int(self.CG.text())
            self.parent.plot_RGB[self.call_ind][2] = int(self.CB.text())
            self.Set_Flag.setText("ON")
            exec('self.Set_Flag.setStyleSheet("background-color:rgb({}, {}, {})")'.format(self.parent.plot_RGB[self.call_ind][0], self.parent.plot_RGB[self.call_ind][1], self.parent.plot_RGB[self.call_ind][2]))
            self.parent.my_plot.plot_set(self.call_ind)
        else:
            self.Set_Flag.setText("OFF")
            self.Set_Flag.setStyleSheet("background-color:transparent")
            self.plot_flag = 0
            self.parent.plot_RGB[self.call_ind] = [255, 255, 255]
            self.parent.my_plot.curve[self.call_ind].clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Check_Widget()
    app.exec_()