import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
import numpy as np

class QtPanningPlot:

    def __init__(self,title):
        self.win = pg.GraphicsLayoutWidget()
        self.title = title
        self.win.setWindowTitle(f"{title}")
        self.plt = self.win.addPlot()
        self.plt.setYRange(0,1)
        self.plt.setXRange(0,2000)
        self.curve = self.plt.plot()
        self.data = []
        # any additional initalisation code goes here (filters etc)
        self.timestamps = []
        self.sr_text = pg.LabelItem('0Hz', **{"size": "15"})
        self.win.addItem(self.sr_text)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
        self.win.show()
        
    def update(self):
        self.data=self.data[-2000:]
        if self.data:
            self.curve.setData(np.hstack(self.data))

        # calculate sampling rate and update to plot
        if len(self.timestamps) > 1:
            sr = (len(self.timestamps) - 1) / (self.timestamps[-1] - self.timestamps[0])
            self.sr_text.setText(f"{int(sr)}Hz")

    def addData(self, d, now):
        self.data.append(d)

        # add timestamps
        self.timestamps.append(now)