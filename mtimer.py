from PyQt5 import QtWidgets, uic, QtCore
import sys
import time
import threading
import numpy as np
import pyqtgraph as pg


class Timer_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Timer_Widget, self).__init__(parent=parent)
        self.parent = parent
        uic.loadUi("mtimer.ui", self)
        self.show()
        self.timer_reset()

    def timer_reset(self):
        self.current_timer = 0
        self.Measure_Timer.display(self.current_timer)

    def timer_start(self):
        thread_timer = threading.Thread(target=self.timer_run)
        thread_timer.setDaemon(True)  # 设置守护线程，主线程退出，采集结束
        thread_timer.start()

    def timer_run(self):
        while True:
            time.sleep(1)
            self.current_timer += 1
            self.Measure_Timer.display(self.current_timer)
            if self.parent.timer_flag == 0:
                self.timer_reset()
                break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Timer_Widget()
    app.exec_()
