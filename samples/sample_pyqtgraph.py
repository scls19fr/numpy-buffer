import sys
import numpy as np
import datetime

from PyQt4.QtCore import QTime, QTimer
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from timestamp import now_timestamp, int2dt
from numpy_buffer import RingBuffer

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        return [int2dt(value).strftime("%H:%M:%S.%f") for value in values]

class MyApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(MyApplication, self).__init__(*args, **kwargs)
        self.t = QTime()
        self.t.start()

        maxlen = 300
        self.data_x = RingBuffer(maxlen)
        self.data_y = RingBuffer(maxlen)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(1000,600)

        self.plot = self.win.addPlot(title='Timed data', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        #self.plot.setYRange(0, 150)
        self.curve = self.plot.plot()

        self.tmr = QTimer()
        self.tmr.timeout.connect(self.update)
        self.tmr.start(100)

        self.y = 100

    def update(self):
        #self.data.append({'x': self.t.elapsed(), 'y': np.random.randint(0, 100)})
        x = now_timestamp()
        self.y = self.y + np.random.uniform(-1, 1)

        self.data_x.append(x)
        self.data_y.append(self.y)
        self.curve.setData(x=self.data_x.partial, y=self.data_y.partial)

def main():
    app = MyApplication(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
