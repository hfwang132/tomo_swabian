from PyQt5 import QtWidgets, uic, QtCore
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont

class Plot_Chart(pg.GraphicsWindow):

    def __init__(self, parent=None):
        #pg.GraphicsWindow.__init__(self)
        super(Plot_Chart, self).__init__(parent=parent)
        self.parent = parent
        #self.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.p1 = self.addPlot()
        self.p1.setLimits(yMin=0)
        #self.plot_max_volume = 100
        self.plot_flag = [1 for i in range(self.parent.parent.display_volume)]
        self.plot_reset()

    def plot_reset(self):
        self.ptr1 = 0
        self.p1.clear()
        self.plot_data = [[] for i in range(self.parent.parent.display_volume)]
        self.curve = []
        for i in range(self.parent.parent.display_volume):
            self.curve.append(self.p1.plot(self.plot_data[i], pen=QColor(self.parent.plot_RGB[i][0], self.parent.plot_RGB[i][1], self.parent.plot_RGB[i][2])))

    def plot_set(self, ind):
        self.curve[ind].clear()
        self.curve[ind] = self.p1.plot(self.plot_data[ind], pen=QColor(self.parent.plot_RGB[ind][0], self.parent.plot_RGB[ind][1], self.parent.plot_RGB[ind][2]))

    def update(self):
        self.ptr1 += 1
        for i in range(self.parent.parent.display_volume):
            self.plot_data[i].append(0)
            if self.ptr1 >= self.parent.PltVol:
                self.plot_data[i][:-1] = self.plot_data[i][1:]
                self.plot_data[i].pop()
            if self.parent.my_check[i].plot_flag:
                    self.plot_data[i][-1] = self.parent.parent.my_display.display_list[i]
                    self.curve[i].setData(self.plot_data[i])
                    if self.ptr1 >= self.parent.PltVol:
                        self.curve[i].setPos(self.ptr1, 0)

if __name__ == '__main__':
    w = Plot_Chart()
    w.show()
    QtGui.QApplication.instance().exec_()