# -*- coding: utf-8 -*-
"""
Verification library for seizure prediction and detection algorithm. Takes in brain wave data and
detects and predicts when seizures will happen. Uses a modified version of pacpy.pac named "pacpyC" due to 
an issue with numpy 1.13 not accepting floats as an index.
Modification in firfC.py @ line 48 'int(Ntaps)'

"""

import pyedflib
import pprint
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from scipy.signal import hilbert, chirp
from pacpyC import plv
from firfC import firf
import math
import collections
import matplotlib.pyplot as plt
import sys
import time


def getSignals(fileName):

    """
    Purpose: Take in edf EEG file and put signals in a 2D array and return  that array                                                             
                                                                       
    Dependencies: pyedflib, np                                             
                                                                        
    Parameters: fileName: Edf file path                                    
                                                                        
    Sample Call: data, file = getSignals("John.edf")  

    Returns: 2D array with eeg data
             edf reader object
    """

    print("Collecting EEG signals from", fileName)
    f = pyedflib.EdfReader(fileName)
    n = f.signals_in_file
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
    return sigbufs, f




def getParams(f):

    """
    Purpose: Allow for the selection of electrode working and reference    
    channels. Returns reference and working indicies.                      
                                                                        
    Dependencies: pyedflib, pprint                                         
                                                                        
    Parameters: f: pyedflib file object                                    
                                                                        
    Sample Call: working, reference = getParams(f)   

    """
    # Setup channel selection
    sigLabs = f.getSignalLabels()
    channels = {}
    for i in range(len(sigLabs)):
        channels[str(i)] = str(sigLabs[i])
    
    #print("Please select the working channel from the list")
    channelPrint = pprint.pformat(channels)
    print(channelPrint)
    working = input("Please select a working channel from the list by entering its #: ")
    print("You have selected the working channel: " + sigLabs[int(working)])
    reference = input("Please select a reference channel from the list by entering its #: ")
    print("You have selected the reference channel " + sigLabs[int(reference)])
    return working, reference




def getSTDdev(data, f):

    """
    Purpose: Calculate the standard deviation of all channels to locate
    the area of the highest seizure occurence. The channel with the highest 
    standard deviation is selected as the working electrode and the channel
    with the lowest is selected as the reference electrode. Returns working 
    and reference indicies.                                
                                                                        
    Dependencies: pprint, pyedflib                                         
                                                                        
    Parameters  

    ----------

    data: 2D array with eeg data                               
       f: pyedflib file object                                 
                                                                        
    Sample Call: working, reference = getSTDdev(data) 

    """

    print("Finding the Standard Deviation of each channel")

    stdDev = {}
    siglabs = f.getSignalLabels()

    largestval = 0
    largestIndex = 0

    smallestVal = 200
    smallestIndex = 0

    print("Computing the Standard Deviation of all the channels")
    for i in range(len(data)):
        dev = np.std(data[i])
        stdDev[i] = dev
    
    
    items = [(v, k) for k, v in stdDev.items()]
    items.sort()
    smallIndex = items[0][1]
    largeIndex = items[len(items) - 1][1]

    stdPrint = pprint.pformat(items)
    print(stdPrint)

    print("The Largest std dev is at channel", siglabs[largeIndex])
    print(siglabs[largeIndex], " is the working channel")
    print("The Smallest std dev is at channel", siglabs[smallIndex])
    print(siglabs[smallIndex], " is the reference channel")
    
    return largeIndex, smallIndex
        

def getPlvthresh(f, data, sampleFreq, calcRate, startPoint, endPoint, wrkIndex, refIndex, plot = True):

    """

    Purpose: Compute the Phase lock value over a specified amount of time for 
    the 2 given electrodes.                                                   
                                                                           
    Dependencies: np, pacpy, math, collections, matplotlib                    
                                                                           
    Parameters
    
    ----------
    
    f: pyedflib file object                                       
    data: 2D array of eeg data                                    
    sampleFreq: rate at which data was sampled                    
    calcRate: rate at which plv needs to be calculated in seconds 
    startPoint: point in data to start calculating in seconds     
    endPoint: point in data to stop calculating in secconds       
    wrkIndex: index of selected working electrode                 
    refIndex: index of selected reference electrode               
    plot: boolean, false if no plot is neccesary  


    """

    start_time = time.time()
    pvalDict = {}
    avalDict = {}
    ptr = 0
    captureRate = int(calcRate) * int(sampleFreq)
    wkSensor = np.zeros(captureRate)
    refSensor = np.zeros(captureRate)
    siglabs = f.getSignalLabels()
    start = int(startPoint) * int(sampleFreq)
    end = int(endPoint) * int(sampleFreq)
    windowSize = 1000

    print(" ")
    print("Calculating PLV over two selected channels every %s data points" %captureRate)
    print("working channel:", siglabs[wrkIndex])
    print("reference channel:", siglabs[refIndex])
    print("Testing duration: %s data points" % (int(end) - int(start)))

    # Read the EEG data as instructed
    for i in range(start, end): 
      
        # wrkIndex and refIndex signifies which channel to read the data from
        wkSensor[ptr] = data[wrkIndex][i]
        refSensor[ptr] = data[refIndex][i]

        # when the capture rate is reached, compute the PLV
        if ptr != 0 and ptr%(captureRate-1) == 0:

            """
            In order to avoid spurious detection of locking due to noise
            and small oscillation coupling, we initially bandpass filter the
            time series in order to focus on the frequency areas that produce
            pre-ictal and ictal behavior.

            """
            wkFiltered = firf(wkSensor, (6,12), 256, 2)
            refFiltered = firf(refSensor, (6,12), 256, 2)


            """
            Seizure prediction analysis begins with the decomposition of
            EEG via Hilbert transformation. The signal is split into two parts,
            the analytic amplitude(AA) and the analytic phase(AP).

            """
            wk_signal = hilbert(wkFiltered)
            ref_signal = hilbert(refFiltered)

            wk_AP = np.unwrap(np.angle(wk_signal))
            ref_AP = np.unwrap(np.angle(ref_signal))


            pVal = np.abs(np.mean(np.exp(1j * (wk_AP - ref_AP))))
            pVal = math.ceil(pVal*100)/100 # round number to the hundreths decimal

            pkey = pVal
            if pVal > .6 and pVal < .99: 
                #print(pVal)
                if pkey in pvalDict:
                    value = pvalDict[pkey]
                    pvalDict[pkey] = value + 1
                else:
                    pvalDict[pkey] = 1
            ptr = 0 # reset the array, fill up with new values, and recompute PLV
        ptr += 1
        
   
    pod = collections.OrderedDict(sorted(pvalDict.items())) 
    print(pod)

    print("--- %s seconds ---" % (time.time() - start_time))

    if plot:
        plt.plot(range(len(pod)), pod.values())
        plt.xticks(range(len(pod)), pod.keys())
        plt.show()






def main():
    
    fileName = input("Please enter path to EEG file: ")

    data, f = getSignals(fileName)

    sampleFreq = f.getSampleFrequency(0)
    numSamps = f.getNSamples()[0]
    print("Samples detected in file: ", numSamps)
    print("Sampling rate detected: ", sampleFreq)

    print("Please choose method of Electrode selection")
    print("STD Deviation - Y")
    print("Manual Selection - N")
    selection = input("Enter Selection (Y/N): ")

    if selection == "Y":
        wrkIndex, refIndex = getSTDdev(data,f)
    elif selection == "N":
        wrkIndex, refIndex = getParams(f)
    else:
        print("Invalid Input, exiting")
        SystemExit()

    calcRate = input("How often (in seconds) should the PLV be calculated?: ")
    periodReq = input("If there is a specific period to measure, enter Y. Otherwise, enter N.: ")

    if periodReq == "Y":
        print("The duration of the file is %s seconds" % str(f.getFileDuration()))
        startPoint = input("What is the start point in seconds?: ")
        endPoint = input("What is the end point in seconds?: ")
        getPlvthresh(f, data, sampleFreq, calcRate, startPoint, endPoint, int(wrkIndex), int(refIndex))
    elif periodReq == "N":
        startPoint = 0
        endPoint = f.getFileDuration()
        getPlvthresh(f, data, sampleFreq, calcRate, startPoint, endPoint, int(wrkIndex), int(refIndex))
    else:
        print("Invalid Input, exiting")
        SystemExit()




if __name__== "__main__":
  main()





