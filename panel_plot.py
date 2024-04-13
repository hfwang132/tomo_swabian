from PyQt5 import QtWidgets, uic, QtCore
import sys
from plot_check import Check_Widget
from chart_plot import Plot_Chart
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont
import numpy as np
import pyqtgraph as pg


class Plot_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Plot_Widget, self).__init__(parent=parent)
        self.parent = parent
        uic.loadUi("panel_plot.ui", self)
        self.show()
        self.my_check = []
        for i in range(self.parent.display_volume):
            self.my_check.append(Check_Widget(self))
            exec('self.verticalLayout_check_{}.addWidget(self.my_check[i])'.format(i + 1))
            self.my_check[i].checkBox.setText(str(i+1))
            self.my_check[i].call_ind = i
        self.plot_RGB = [[255, 255, 255] for i in range(self.parent.pattern_volume)]
        self.my_plot = Plot_Chart(self)
        self.verticalLayout_plot.addWidget(self.my_plot)
        self.connect_sig_slot()
        self.Plot_Volume.setRange(100, 5000)
        self.Plot_Volume.setValue(100)
        self.PltVol = 100

    def connect_sig_slot(self):
        self.PltVolSet.clicked.connect(self.PltVolCon)
        self.PltClear.clicked.connect(self.my_plot.plot_reset)

    def PltVolCon(self):
        self.PltVol = self.Plot_Volume.value()
        print(self.PltVol)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Plot_Widget()
    app.exec_()