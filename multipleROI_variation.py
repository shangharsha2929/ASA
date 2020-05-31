"""
Created on Sat Apr 11 20:47:44 2020
Code to check the variation in VI trajectories within multiple ROIs chosen within individual images.
This code uses the .txt file of average VIs from 1dayaverage/3dayaverage code for ROIs located
close to Phenocamera and far away from it to see if there is effect of overestimation and 
underestimation of signals altering the quality of time series.
@author: Shangharsha
"""
#Importing required modules
import matplotlib.pyplot as plt
import sklearn
import numpy as np
from sklearn.preprocessing import minmax_scale
from scipy import signal

##################################################################################################
#Region of Interest (ROI1) representing canopy level and near to Phenocam
##################################################################################################
#Read all text files storing standardized VI values.
with open('avg1GCC3Day.txt','r') as data:
    
    doy = []
    gcc = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY = int((info[0].split(':'))[1])
        
        #Extract VI information from text file
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

#Filter with a window length of 5 and a 1st degree polynomial
smoothedGCC = np.round(signal.savgol_filter(rescaledGCC, 5, 1), decimals = 3)
##################################################################################################

##################################################################################################
#Region of Interest (ROI4) representing canopy level and far from Phenocam (horizon)
##################################################################################################
#Read all text files storing standardized VI values.
with open('avgGCC3Day.txt','r') as data:
    
    doy2 = []
    gcc2 = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract DOY information from text file
        DOY2 = int((info[0].split(':'))[1])
        
        #Extract VI information from text file
        GCC2 = float((info[1].split(':'))[1].strip())
        
        if GCC2 != 0.0:
            #Appending the DOY and GCC in respective lists
            doy2.append(DOY2)
            gcc2.append(GCC2)

#Converting lists to numpy array
npDOY2 = np.asarray(doy2)
npGCC2 = np.asarray(gcc2, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledGCC2 = sklearn.preprocessing.minmax_scale(npGCC2, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedGCC2 = np.round(signal.savgol_filter(rescaledGCC2, 5, 1), decimals = 3)
##################################################################################################

#Plotting the time series of VI
plt.rcParams['figure.figsize'] = (14,12)
plt.figure(0)
plt.subplot(311)
plt.plot(npDOY, smoothedGCC, linewidth=3, color='g', label = 'ROI1')
plt.plot(npDOY2, smoothedGCC2, linewidth=2, linestyle = '--', color='g', label = 'ROI4')  
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('GCC', fontsize = 18)
plt.legend(loc = 'upper right', fontsize = 14)   

##################################################################################################
#Checking shift in 2nd VI i.e. ExG
##################################################################################################
#Read all text files storing standardized VI values.
with open('avg1ExG3Day.txt','r') as data:
    
    exg = []
    
    for lines in data:
        info = lines.split(',')
             
        #Extract VI information from text file
        ExG = float((info[1].split(':'))[1].strip())
        
        if ExG != 0.0:
            #Appending the ExG values
            exg.append(ExG)

#Converting list to numpy array
npExG = np.asarray(exg, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledExG= sklearn.preprocessing.minmax_scale(npExG, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedExG = np.round(signal.savgol_filter(rescaledExG, 5, 1), decimals = 3)
##################################################################################################

##################################################################################################
#Region of Interest (ROI4) representing canopy level and far from Phenocam (horizon)
##################################################################################################
#Read all text files storing standardized VI values.
with open('avgExG3Day.txt','r') as data:
    
    exg2 = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract VI information from text file
        ExG2 = float((info[1].split(':'))[1].strip())
        
        if ExG2 != 0.0:
            #Appending the ExG values
            exg2.append(ExG2)

#Converting lists to numpy array
npExG2 = np.asarray(exg2, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledExG2 = sklearn.preprocessing.minmax_scale(npExG2, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedExG2 = np.round(signal.savgol_filter(rescaledExG2, 5, 1), decimals = 3)
##################################################################################################

#Plotting the time series of VI
plt.subplot(312)
plt.plot(npDOY, smoothedExG, linewidth=3, color='r', label = 'ROI1')
plt.plot(npDOY2, smoothedExG2, linewidth=2, linestyle = '--', color='r', label = 'ROI4')  
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('ExG', fontsize = 18)
plt.legend(loc = 'upper right', fontsize = 14)   

##################################################################################################
#Checking shift in 3rd VI i.e. VIg
##################################################################################################
#Read all text files storing standardized VI values.
with open('avg1VIg3Day.txt','r') as data:
    
    vig = []
    
    for lines in data:
        info = lines.split(',')
             
        #Extract VI information from text file
        VIg = float((info[1].split(':'))[1].strip())
        
        if VIg != 0.0:
            #Appending the ExG values
            vig.append(VIg)

#Converting list to numpy array
npVIg = np.asarray(vig, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledVIg= sklearn.preprocessing.minmax_scale(npVIg, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedVIg = np.round(signal.savgol_filter(rescaledVIg, 5, 1), decimals = 3)
##################################################################################################

##################################################################################################
#Region of Interest (ROI4) representing canopy level and far from Phenocam (horizon)
##################################################################################################
#Read all text files storing standardized VI values.
with open('avgVIg3Day.txt','r') as data:
    
    vig2 = []
    
    for lines in data:
        info = lines.split(',')
        
        #Extract VI information from text file
        VIg2 = float((info[1].split(':'))[1].strip())
        
        if VIg2 != 0.0:
            #Appending the ExG values
            vig2.append(VIg2)

#Converting lists to numpy array
npVIg2 = np.asarray(vig2, dtype=np.float32)

#Normalize the VI values to be within 0 and 1
rescaledVIg2 = sklearn.preprocessing.minmax_scale(npVIg2, feature_range=(0, 1), axis=0, copy=True)

#Filter with a window length of 5 and a 1st degree polynomial
smoothedVIg2 = np.round(signal.savgol_filter(rescaledVIg2, 5, 1), decimals = 3)
##################################################################################################

#Plotting the time series of VI
plt.subplot(313)
plt.plot(npDOY, smoothedVIg, linewidth=3, color='b', label = 'ROI1')
plt.plot(npDOY2, smoothedVIg2, linewidth=2, linestyle = '--', color='b', label = 'ROI4')  
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('VIgreen', fontsize = 18)
plt.legend(loc = 'upper right', fontsize = 14)   

###################################################################################################