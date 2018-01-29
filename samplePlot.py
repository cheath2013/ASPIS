# -*- coding: utf-8 -*-
"""
This is an example of how data coming into ASPIS will be plotted on a scrolling graph,
replicating an eeg monitor. 

"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import xlrd

# Setup excel sheet for values
workbook = xlrd.open_workbook('files/Jimbo.xlsx')
worksheet = workbook.sheet_by_index(0)
channel = 'EEG Data for ' + str(worksheet.cell(0,0).value)

# Values from excel sheet into 1D array to be read into data plot
data = []
for row in range(0,1): # Only take the first Channel
    values = []
    for col in range(1, worksheet.ncols-1): # Only take the first 1000 values
        #values.append(float(worksheet.cell(row,col+1).value))  # creates 2D array
        if worksheet.cell(row,col+1).value != '':
            data.append(float(worksheet.cell(row,col+1).value))


app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,1000)
win.setWindowTitle('ASPIS')
p = win.addPlot(title=channel)
p.setYRange(-600, 600, padding=0)
p.setXRange(0, 2560, padding=0)
curve = p.plot(data, pen='y')
    




def update():
    global curve, data, ptr, p
    data[:-1] = data[1:]  # shift data in the array one sample left
    curve.setData(data)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)   




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()