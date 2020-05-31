"""
Created on Tue Apr 21 22:55:50 2020
This script reads the .txt file storing the NDVI values from ground sensor and also the 
NDVI values extracted from spline fitted NDVI time series, thus helping to compare the 
two trajectories from different sensors and check if linear offset exists between them.
@author: Shangharsha
"""
#Importing required modules
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from scipy import signal
#####################################################################################################

#####################################################################################################
#Reading .txt file for the year 2018
#Provide either complete path to .txt files or place this .py script to the same path as .txt
with open('UAVVsGround2018.txt','r') as data:
    
    #Skip the header of text file
    next(data)
    
    #Empty list to store the corresponding values from the text file
    doy = []
    ndviUAV = []
    ndviGS = []
    
    #Iterating text file row by row to extract the data in it
    for lines in data:
        
        #Splitting a string based on tab
        info = lines.split('\t')
        
        #Assisgn the values to its corresponding categories
        DOY = int(info[0])
        uavNDVI = float(info[1])
        gsNDVI = float(info[2])
        
        #Appending the values to the empty list declared at the very first
        doy.append(DOY)
        ndviUAV.append(uavNDVI)
        ndviGS.append(gsNDVI)
        
#Converting lists to numpy array
npDOY18 = np.asarray(doy)
npNDVI18GS = np.asarray(ndviGS, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
#Larger window length will make the curves appear more smooth
smoothedNDVI18GS = np.round(signal.savgol_filter(npNDVI18GS, 5, 1), decimals = 5)
#####################################################################################################        
#Reading .txt file for the year 2019
#####################################################################################################
#Provide either complete path to .txt files or place this .py script to the same path as .txt
with open('UAVVsGround2019.txt','r') as data:
    
    #Skip the header of text file
    next(data)
    
    #Empty list to store the corresponding values from the text file
    doy19 = []
    ndviUAV19 = []
    ndviGS19 = []
    
    #Iterating text file row by row to extract the data in it
    for lines in data:
        
        #Splitting a string based on tab
        info = lines.split('\t')
        
        #Assisgn the values to its corresponding categories
        DOY = int(info[0])
        uavNDVI = float(info[1])
        gsNDVI = float(info[2])
        
        #Appending the values to the empty list declared at the very first
        doy19.append(DOY)
        ndviUAV19.append(uavNDVI)
        ndviGS19.append(gsNDVI)

#Converting lists to numpy array
npDOY19 = np.asarray(doy19)
npNDVI19GS = np.asarray(ndviGS19, dtype=np.float32)

#Filter with a window length of 5 and a 1st degree polynomial
#Larger window length will make the curves appear more smooth
smoothedNDVI19GS = np.round(signal.savgol_filter(npNDVI19GS, 5, 1), decimals = 5)

#####################################################################################################
#Plotting both UAV & Ground Sensor derived NDVI values
#####################################################################################################
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
plt.plot(npDOY18, smoothedNDVI18GS, linewidth=4, color='r', alpha = 0.8, label = 'Smoothed Sensor NDVI')
plt.plot(npDOY18, ndviUAV, linewidth=4, color='g', alpha = 0.8, label = 'Spline fitted UAV NDVI')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 14)
plt.ylabel('Normalized Difference Vegetation Index', fontsize = 14)
plt.legend(loc = 'best', fontsize = 14) 

plt.rcParams['figure.figsize'] = (16,8)
plt.figure(1)
plt.plot(npDOY19, smoothedNDVI19GS, linewidth=4, color='r', alpha = 0.8, label = 'Smoothed Sensor NDVI')
plt.plot(npDOY19, ndviUAV19, linewidth=4, color='g', alpha = 0.8, label = 'Spline fitted UAV NDVI')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 14)
plt.ylabel('Normalized Difference Vegetation Index', fontsize = 14)
plt.legend(loc = 'upper left', fontsize = 14) 

#####################################################################################################