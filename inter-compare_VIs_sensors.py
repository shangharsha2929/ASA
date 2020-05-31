"""
Created on Sat Apr 11 17:53:24 2020
This code reads the corresponding VIs(3 day average) from different sensors (phenocamera, 
ground sensor,and UAV) stored as .txt files. The VI values are normalized (0-1), smoothed
using Savitzky-Golay filtering technique and plotted against each other. Users are free to
choose which two sensors they want to compare at once (Plotting all three sensor based VIs
at once might be confusing). For instance: the current script plots Phenocamera based VIs
against UAV based NDVI for the year 2018 and 2019. Lines that plots the ground sensor-based
NDVI are left as comment. 
@author: Shangharsha
"""
#Importing required modules
import matplotlib.pyplot as plt
import sklearn
import numpy as np
from sklearn.preprocessing import minmax_scale
from scipy import signal

###############################################################################################
#2018
###############################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avgGCC3Day.txt','r') as data:
    
    doy = []
    gcc = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        #DOY = int(info[0])
        DOY = int((info[0].split(':'))[1])
        
        #Extract VI information from text file
        #GCC = float(info[1])
        GCC = float((info[1].split(':'))[1].strip())
        
        if GCC != 0.0:
            #Appending the DOY and GCC in respective lists
            doy.append(DOY)
            gcc.append(GCC)

#Converting lists to numpy array
npDOY = np.asarray(doy)
npGCC = np.asarray(gcc, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledGCC= sklearn.preprocessing.minmax_scale(npGCC, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedGCC = np.round(signal.savgol_filter(rescaledGCC, 7, 1), decimals = 3)
###############################################################################################

###############################################################################################
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avgExG3Day.txt','r') as data:
    
    exg = []
    
    for lines in data:
        info = lines.split(',')
            
        #Extract VI information from text file
        ExG = float((info[1].split(':'))[1].strip())
        
        if ExG != 0.0:
            #Appending the ExG values
            exg.append(ExG)

#Converting lists to numpy array
npExG = np.asarray(exg, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledExG= sklearn.preprocessing.minmax_scale(npExG, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedExG = np.round(signal.savgol_filter(rescaledExG, 7, 1), decimals = 3)
###############################################################################################

###############################################################################################
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avgVIg3Day.txt','r') as data:
    
    vig = []
    
    for lines in data:
        info = lines.split(',')
            
        #Extract VI information from text file
        VIg = float((info[1].split(':'))[1].strip())
        
        if VIg != 0.0:
            #Appending the ExG values
            vig.append(VIg)

#Converting lists to numpy array
npVIg = np.asarray(vig, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledVIg= sklearn.preprocessing.minmax_scale(npVIg, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedVIg = np.round(signal.savgol_filter(rescaledVIg, 7, 1), decimals = 3)
###############################################################################################
'''
###############################################################################################
#Fixed sensor NDVI for 2018
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avg3NDVI018AC.txt','r') as data:
    
    doyNDVI_gs = []
    ndvi_gs = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doyNDVI_gs.append(DOY)
            ndvi_gs.append(NDVI)

#Converting lists to numpy array
npDOYNDVI_gs = np.asarray(doyNDVI_gs)
npNDVI_gs = np.asarray(ndvi_gs, dtype=np.float32)

#Filter with a window length of 5 and a degree  polynomial
smoothedNDVI = np.round(signal.savgol_filter(npNDVI_gs, 7, 1), decimals = 5)
'''
###############################################################################################
#UAV 2018
###############################################################################################
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('UAV_NDVI2018.txt', 'r') as udata:
    
    dateNdvi = []
    ndviU = []
    
    for l1 in udata:
        info = l1.split(',')
        
        #Extract DOY information from text file
        DOY1 = int(info[0])
                
        #Extract VI information from text file
        UNDVI1 = float(info[1])
                
        if UNDVI1 != 0.0:
            #Appending the DOY and GCC in respective lists
            dateNdvi.append(DOY1)
            ndviU.append(UNDVI1)

#Converting lists to numpy array
npDOY_ndvi = np.asarray(dateNdvi)
npNDVI_uav = np.asarray(ndviU, dtype=np.float32)

###############################################################################################

###############################################################################################
#2019
###############################################################################################
#Reading .txt file to read the DOY and GCC values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avg19GCC3Day.txt','r') as data:
    
    doy19 = []
    gcc19 = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        #DOY = int(info[0])
        DOY = int((info[0].split(':'))[1])
        
        #Extract VI information from text file
        #GCC = float(info[1])
        GCC = float((info[1].split(':'))[1].strip())
        
        if GCC != 0.0:
            #Appending the DOY and GCC in respective lists
            doy19.append(DOY)
            gcc19.append(GCC)

#Converting lists to numpy array
npDOY19 = np.asarray(doy19)
npGCC19 = np.asarray(gcc19, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledGCC19= sklearn.preprocessing.minmax_scale(npGCC19, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedGCC19 = np.round(signal.savgol_filter(rescaledGCC19, 7, 1), decimals = 3)
###############################################################################################

###############################################################################################
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avg19ExG3Day.txt','r') as data:
    
    exg19 = []
    
    for lines in data:
        info = lines.split(',')
            
        #Extract VI information from text file
        ExG = float((info[1].split(':'))[1].strip())
        
        if ExG != 0.0:
            #Appending the ExG values
            exg19.append(ExG)

#Converting lists to numpy array
npExG19 = np.asarray(exg19, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledExG19 = sklearn.preprocessing.minmax_scale(npExG19, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedExG19 = np.round(signal.savgol_filter(rescaledExG19, 7, 1), decimals = 3)
###############################################################################################

###############################################################################################
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avg19VIg3Day.txt','r') as data:
    
    vig19 = []
    
    for lines in data:
        info = lines.split(',')
            
        #Extract VI information from text file
        VIg = float((info[1].split(':'))[1].strip())
        
        if VIg != 0.0:
            #Appending the ExG values
            vig19.append(VIg)

#Converting lists to numpy array
npVIg19 = np.asarray(vig19, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledVIg19 = sklearn.preprocessing.minmax_scale(npVIg19, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a degree  polynomial
smoothedVIg19 = np.round(signal.savgol_filter(rescaledVIg19, 7, 1), decimals = 3)
###############################################################################################
'''
###############################################################################################
#Fixed Sensor based NDVI for 2019
#Reading .txt file to read the ExG values averaged over 3 days
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('avg3NDVI019AC.txt','r') as data:
    
    doyNDVI19_gs = []
    ndvi19_gs = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int(info[0])
        
        #Extract VI information from text file
        NDVI = float(info[1])
        
        if NDVI != 0.0:
            #Appending the DOY and GCC in respective lists
            doyNDVI19_gs.append(DOY)
            ndvi19_gs.append(NDVI)

#Converting lists to numpy array
npDOY19_gs = np.asarray(doyNDVI19_gs)
npNDVI19_gs = np.asarray(ndvi19_gs, dtype=np.float32)

#Filter with a window length of 5 and a degree  polynomial
smoothedNDVI19 = np.round(signal.savgol_filter(npNDVI19_gs, 7, 1), decimals = 5)
###############################################################################################
'''
###############################################################################################
#UAV 2019
###############################################################################################
#.txt file should be in the same path as the .py file or users shall provide full path for it
with open('UAV_NDVI2019.txt', 'r') as udata:
    
    dateNdvi19 = []
    ndviU19 = []
    
    for l2 in udata:
        info = l2.split(',')
        
        #Extract DOY information from text file
        DOY2 = int(info[0])
                
        #Extract VI information from text file
        UNDVI2 = float(info[1])
                
        if UNDVI2 != 0.0:
            #Appending the DOY and GCC in respective lists
            dateNdvi19.append(DOY2)
            ndviU19.append(UNDVI2)

#Converting lists to numpy array
npDOY_ndvi19 = np.asarray(dateNdvi19)
npNDVI_uav19 = np.asarray(ndviU19, dtype=np.float32)

###############################################################################################
#Plotting the time series of VI
plt.rcParams['figure.figsize'] = (14,14)
plt.figure(0)
plt.subplot(311)
plt.plot(npDOY, smoothedGCC, linewidth=3, color='g', label = 'GCC: 2018') 
plt.plot(npDOY19, smoothedGCC19, linewidth=3, linestyle = '-.', color='g', label = 'GCC: 2019')
plt.plot(npDOY_ndvi, npNDVI_uav, 'ko', markersize = 7, label = 'UAV-NDVI: 2018')
plt.plot(npDOY_ndvi19, npNDVI_uav19, 'ko', markersize = 7, mfc = 'none', label = 'UAV-NDVI: 2019')
plt.ylabel('VI values', fontsize = 18)
#plt.plot(npDOYNDVI_gs, smoothedNDVI, 'ko', markersize = 5, alpha = 0.5, label = 'Sensor NDVI: 2018')
#plt.plot(npDOY19_gs, smoothedNDVI19, 'bo', markersize = 5, mfc = 'none', label = 'Sensor NDVI: 2019')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc = 'upper left', fontsize = 14)

plt.subplot(312)
plt.plot(npDOY, smoothedExG, linewidth=3, color='r', alpha = 0.8, label = 'ExG: 2018')
plt.plot(npDOY19, smoothedExG19, linewidth=3, linestyle = '-.', color='r', alpha = 0.8, label = 'ExG: 2019')
plt.plot(npDOY_ndvi, npNDVI_uav, 'ko', markersize = 7, label = 'UAV-NDVI: 2018')
plt.plot(npDOY_ndvi19, npNDVI_uav19, 'ko', markersize = 7, mfc = 'none', label = 'UAV-NDVI: 2019')
plt.ylabel('VI values', fontsize = 18)
#plt.plot(npDOYNDVI_gs, smoothedNDVI, 'ko', markersize = 5, alpha = 0.5, label = 'Sensor NDVI: 2018')
#plt.plot(npDOY19_gs, smoothedNDVI19, 'bo', markersize = 5, mfc = 'none', label = 'Sensor NDVI: 2019')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc = 'upper left', fontsize = 14)
 
plt.subplot(313)
plt.plot(npDOY, smoothedVIg, linewidth=3, color='m', label = 'VIgreen: 2018')
plt.plot(npDOY19, smoothedVIg19, linewidth=3, linestyle = '-.', color='m', label = 'VIgreen: 2019')
plt.plot(npDOY_ndvi, npNDVI_uav, 'ko', markersize = 7,  label = 'UAV-NDVI: 2018')
plt.plot(npDOY_ndvi19, npNDVI_uav19, 'ko', markersize = 7, mfc = 'none', label = 'UAV-NDVI: 2019')
plt.ylabel('VI values', fontsize = 18)
#plt.plot(npDOYNDVI_gs, smoothedNDVI, 'ko', markersize = 5, alpha = 0.5, label = 'Sensor NDVI: 2018')
#plt.plot(npDOY19_gs, smoothedNDVI19, 'bo', markersize = 5, mfc = 'none', label = 'Sensor NDVI: 2019')

plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (DOY)', fontsize = 18)
#plt.ylabel('Vegetation Indices Values', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)

######################################################################################################