"""
Created on Tue Apr 21 01:22:19 2020
Reads the .txt file storing the ground sensor NDVI, raw UAV-NDVI and also the smoothed 
UAV-NDVI values all in one plot for the year 2018 and 2019.
@author: Shangharsha
"""
###################################################################################
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.preprocessing import minmax_scale
from scipy import signal

###################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#Please provide full path to the .txt file
with open('UAV_GSclipped18.txt','r') as data:
    
    doy = []
    ndvi = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doy.append(DOY)
            ndvi.append(NDVI)

#Converting lists to numpy array
npDOY18 = np.asarray(doy)
npNDVI18 = np.asarray(ndvi, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedNDVI18 = np.round(signal.savgol_filter(npNDVI18, 5, 1), decimals = 5)
###################################################################################

###################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#Please provide full path to the .txt file
with open('UAV_NDVI2018.txt','r') as data:
    
    doy = []
    ndvi = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doy.append(DOY)
            ndvi.append(NDVI)

#Converting lists to numpy array
npDOY18U = np.asarray(doy)
npNDVI18U = np.asarray(ndvi, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedNDVI18U = np.round(signal.savgol_filter(npNDVI18U, 5, 1), decimals = 5)
###################################################################################

#Plotting the time series of VI
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
plt.plot(npDOY18, smoothedNDVI18, 'go', markersize= '8', label = 'Sensor derived NDVI')
plt.plot(npDOY18U, npNDVI18U, 'bs', markersize= '10', label = 'UAV derived NDVI')
plt.plot(npDOY18U, smoothedNDVI18U, 'r^', markersize= '8', label = 'Smoothed UAV NDVI')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'best', fontsize = 14) 

###################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#Please provide full path to the .txt file
with open('UAV_GSclipped19.txt','r') as data:
    
    doy = []
    ndvi = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doy.append(DOY)
            ndvi.append(NDVI)

#Converting lists to numpy array
npDOY19 = np.asarray(doy)
npNDVI19 = np.asarray(ndvi, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedNDVI19 = np.round(signal.savgol_filter(npNDVI19, 5, 1), decimals = 5)
###################################################################################

###################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#Please provide full path to the .txt file
with open('UAV_NDVI2019.txt','r') as data:
    
    doy = []
    ndvi = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doy.append(DOY)
            ndvi.append(NDVI)

#Converting lists to numpy array
npDOY19U = np.asarray(doy)
npNDVI19U = np.asarray(ndvi, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedNDVI19U = np.round(signal.savgol_filter(npNDVI19U, 5, 1), decimals = 5)
###################################################################################

#Plotting the time series of VI
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(1)
plt.plot(npDOY19, smoothedNDVI19, 'go', markersize= '8', label = 'Sensor derived NDVI')
plt.plot(npDOY19U, npNDVI19U, 'bs', markersize= '10', label = 'UAV derived NDVI')
plt.plot(npDOY19U, smoothedNDVI19U, 'r^', markersize= '8', label = 'Smoothed UAV NDVI')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'best', fontsize = 14) 