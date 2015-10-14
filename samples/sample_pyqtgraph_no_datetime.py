#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example demonstrates a random walk with pyqtgraph.
"""

import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from numpy_buffer import RingBuffer #  https://github.com/scls19fr/numpy-buffer

class RandomWalkPlot:
    def __init__(self, win):
        #self.plot = pg.plot()
        self.plot = win.addPlot(title="Updating plot")
        
        self.ptr = 0
        
        #pen = 'r'
        pen = pg.mkPen('b', style=QtCore.Qt.SolidLine)
        self.curve = self.plot.plot(pen=pen, symbol='+')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        self.value = 1000 # initial value
        N = 100 # number of elements into circular buffer
        
        self.data_y = RingBuffer(N, self.value)
        

    def update(self):
        self.value += np.random.uniform(-1, 1)

        self.data_y.append(self.value)
        
        self.curve.setData(y=self.data_y) #  size is increasing up to N
        #self.curve.setData(y=self.data_y.all[::-1]) #  size is always N
        
        #if self.ptr == 0:
        #    self.plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        #self.ptr += 1

def main():
    #QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication(sys.argv)

    #mw = QtGui.QMainWindow()
    #mw.resize(800,800)

    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    win = pg.GraphicsWindow(title="Basic plotting examples")
    win.resize(1000, 600)
    win.setWindowTitle('plot')

    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)
    
    upl = RandomWalkPlot(win)
    
    ## Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
	main()
