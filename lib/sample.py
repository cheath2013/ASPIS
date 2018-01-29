import matplotlib.pyplot as plt
import numpy as np
import csv
import xlrd
import pyedflib
import matplotlib.animation as animation
import time

# Setup excel sheet for values
workbook = xlrd.open_workbook('Bill1.xls')
worksheet = workbook.sheet_by_name('Bill1')
size = worksheet.ncols-1
channel = str(worksheet.cell(0, 0).value) # row, col
#print(worksheet.row_values(1, 1, worksheet.ncols))


temparray = []
for row in range(worksheet.nrows):
    values = []
    for col in range(worksheet.ncols-1):
        values.append(worksheet.cell(row,col+1).value)
    temparray.append(values)

print(temparray)



# Setup edf sheet for data information
edf = pyedflib.EdfReader('Bill.edf')
duration = edf.file_duration
startMin = edf.starttime_minute
startSec = edf.starttime_second
startTime = (startMin*100) + startSec
#print(duration)
#print(startTime)


#figure = plt.figure()
#ax1 = figure.add_subplot(1,1,1)

## Setup plot 
#plt.xlabel('time (S)')
#plt.ylabel('voltage (uV) for channel' + channel)
#plt.title('EEG DATA')
#worksheet.cell

#plt.axis([0, 126, -600, 600])
#plt.ion()

#for x in range(size):
#    y = worksheet.cell(0, x+1).value
#    plt.scatter(x, y)
#    plt.show()
#    plt.pause(0.05)
   

#while True:
#    plt.pause(0.05)
