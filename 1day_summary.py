# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 21:34:13 2020
This code extracts mean DN values over defined region of interest, use those mean DN values to
compute mean GCC, ExG and VIgreen values over all images. Finally, from these values, daily 
average of VIs are computed and both saved as well as plotted. Text file storing the daily average
is also done by the code. Note: Change the base path everywhere in the code where there is path.
@author: Shangharsha
"""
#################################################################################################
#Module Declaration
#################################################################################################

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from datetime import datetime
from itertools import islice 

#################################################################################################
#Get time now. This helps to compute total elapsed time for running the code.
#################################################################################################
start = datetime.now()

#################################################################################################
#Empty lists to store the corresponding vegetation indices value
#################################################################################################

GCC = []
ExG = []
VIgreen = []
DOY = []

#Before running the code, make new folder named 'Result'

#Always don't forget to change the directory for 'Result' folder
thePath = r'F:\MasterThesis\ASA\Phenocam\2019\Result\ROI5'

#Initializing the empty dictionary to save the DOY as Key and GCC values from valid images
GCCdict1day = {'001':[]}
ExGdict1day = {'001':[]}
VIgdict1day = {'001':[]}

#################################################################################################
#Display Region of Interest (ROI) Selection in the image  
#################################################################################################

#Change the path of one of the image of your working site

#Assign directory of one of image file to show the extent of ROI
imgDir = r'F:\MasterThesis\ASA\Phenocam\2018\all_images\Asa_20180521_141_0500.jpg'

#Loading image from the specified file
img = cv2.imread(imgDir)

#Multiple ROI definition for the image

#ROI1 = img [1100:1700, 250:800]
#ROI2 = img [1000:1700, 1500:2300]
#ROI3 = img [200:1700, 820:1700]
#ROI4 = img [200:750, 200:2400]
ROI5 = img [200:1700, 200:2400]

#################################################################################################
#Draw ROI on top of image to give visual representaion of ROI location 
#################################################################################################

#Rectangle coordinates are given in the order (Xmin, Ymin) & (Xmax, Ymax)

#cv2.rectangle(img,(250,1100),(800,1700),(0,0,255),7)
#cv2.rectangle(img,(1500,1000),(2300,1700),(0,255,255),7)
#cv2.rectangle(img,(820,200),(1700,1700),(255,0,0),7)
#cv2.rectangle(img,(200,200),(2400,750),(0,255,0),7)
cv2.rectangle(img, (200,200),(2400,1700),(0,0,255),7)

#OpenCV represents image in reverse order BGR; so convert it to appear in RGB mode and plot it
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

#################################################################################################
#Automatically creating folders in the directory to save results into
#################################################################################################

#Try-except block is to pass overwrite directories if exists
folders = ['1DPlot','1DTxt']
for folder in folders:
    try:
        os.mkdir(os.path.join(thePath, folder))
    except:
        pass

#################################################################################################
#Assigning path to create text file 
#################################################################################################        
pathGCC = os.path.join(thePath + r'\1DTxt\GCC1Day.txt')
pathExG = os.path.join(thePath + r'\1DTxt\ExG1Day.txt')
pathVIg = os.path.join(thePath + r'\1DTxt\VIg1Day.txt')

#Open a file for writing the image name, corresponding DOY and vegetation indices
f1 = open(pathGCC, 'w')
f2 = open(pathExG, 'w')
f3 = open(pathVIg, 'w')

#################################################################################################
#Vegetation indices calculation within given ROI for all valid images
#################################################################################################

#Iterating all images
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/ROI5/all_images/*.jpg"):
    #print img

    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    #print imgName
    
    #Day of Year information (DOY) extraction from image file name
    dayOfYear = imgName[13:16]
    DOY.append(dayOfYear)
    
    #Defining Region of Interest
    ROI = cv_img [200:1700, 200:2400]
    
    #Splitting RGB image into separate bands
    R, G, B = cv2.split(ROI)
    
    #Finding out mean DN of RGB bands within ROI 
    Rm = np.mean(R)
    Gm = np.mean(G)
    Bm = np.mean(B)

    #Total mean DN of ROI 
    TotalDN_ROI = Rm + Gm + Bm

    #Evaluation of visible band based vegetation indices
    #Green Chromatic Coordinate (GCC)
    g = round((Gm/(TotalDN_ROI)),3)
    
    #Excess Green Index (ExG)
    e = round(((2*Gm)-(Rm + Bm)), 3)
    
    #Normalized Difference of Green and Red (VIgreen)
    v = round(((Gm-Rm)/(Gm + Rm)), 3)
    
    #Appending GCC values for the images
    GCC.append(g)
    ExG.append(e)
    VIgreen.append(v)
    
    #Time series of vegetation indices saved as a text file in the given directory
    f1.write('IMG: {}, DOY: {}, GCC: {}\n'.format(imgName, dayOfYear, g))
    f2.write('IMG: {}, DOY: {}, ExG: {}\n'.format(imgName, dayOfYear, e))
    f3.write('IMG: {}, DOY: {}, VIg: {}\n'.format(imgName, dayOfYear, v))
    
    #Update dictionary with DOY and its associated multiple vegetation indices values
    if dayOfYear in GCCdict1day:
        GCCdict1day[dayOfYear].append(g)
        ExGdict1day[dayOfYear].append(e)
        VIgdict1day[dayOfYear].append(v)
        
    else:
        GCCdict1day[dayOfYear] = [g]
        ExGdict1day[dayOfYear] = [e]
        VIgdict1day[dayOfYear] = [v]

#################################################################################################
#Close the file when done 
#################################################################################################
f1.close()
f2.close()
f3.close()

#################################################################################################  
#Empty dictionaries to store the corresponding vegetation indices value for images with snow cover
#################################################################################################
GCCSnow1day = {}
ExGSnow1day = {}
VIgSnow1day = {}

#################################################################################################
#Block of code to calculate VI values for the images covered with Snow
#################################################################################################

#Iterating images with snow cover to find out VI values
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/ROI5/Snow/*.jpg"):
   
    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    
    #Day of Year information (DOY) extraction from image file name
    dayOfYear = imgName[13:16]
    
    #Defining Region of Interest
    ROI = cv_img [200:1700, 200:2400]
    
    #Splitting RGB image into separate bands
    R, G, B = cv2.split(ROI)
    
    #Finding out mean DN of RGB bands within ROI 
    Rm = np.mean(R)
    Gm = np.mean(G)
    Bm = np.mean(B)

    #Total mean DN of ROI 
    TotalDN_ROI = Rm + Gm + Bm

    #Evaluation of visible band based vegetation indices
    #Green Chromatic Coordinate (GCC)
    g = round((Gm/(TotalDN_ROI)), 3)
    
    #Excess Green Index (ExG)
    e = round(((2*Gm)-(Rm + Bm)), 3)
    
    #Normalized Difference of Green and Red (VIgreen)
    v = round(((Gm-Rm)/(Gm + Rm)), 3)

    #Update dictionary with DOY and its associated multiple vegetation indices values
    if dayOfYear in GCCSnow1day:
        GCCSnow1day[dayOfYear].append(g)
        ExGSnow1day[dayOfYear].append(e)
        VIgSnow1day[dayOfYear].append(v)
        
    else:
        GCCSnow1day[dayOfYear] = [g]
        ExGSnow1day[dayOfYear] = [e]
        VIgSnow1day[dayOfYear] = [v]

#Dictionaries to store mean indices for snowy image
avgGCCSnow = {}
avgExGSnow = {}
avgVIgSnow = {}

#Iterating over all dictionary keys, value pairs and average the items
for (key, val), (key1, val1), (key2, val2) in zip(sorted(GCCSnow1day.iteritems()), 
     sorted(ExGSnow1day.iteritems()), sorted(VIgSnow1day.iteritems())):
    #val, val1, val2 is the lists of GCC, ExG & VIgreen values of all valid images on that DOY
    avgGCCSnow[key] = round(sum(val)/float(len(val)), 3)
    avgExGSnow[key1] = round(sum(val1)/float(len(val1)), 3)
    avgVIgSnow[key2] = round(sum(val2)/float(len(val2)), 3)
        
###################################################################################################
#Finding mean vegetation indices values from all valid images within a given DOY
###################################################################################################
        
#Dictionaries to store mean indices per day from valid images (Excluding no data values for a DOY)
avgGCC = {}
avgExG = {}
avgVIg = {}

#Assigning path to create new text file for storing daily averaged indices values
path_avgGCC = os.path.join(thePath + r'\1DTxt\avgGCC1Day.txt')
path_avgExG = os.path.join(thePath + r'\1DTxt\avgExG1Day.txt')
path_avgVIg = os.path.join(thePath + r'\1DTxt\avgVIg1Day.txt')

#Open a file for writing the corresponding DOY and vegetation indices
f4 = open(path_avgGCC, 'w')
f5 = open(path_avgExG, 'w')
f6 = open(path_avgVIg, 'w')

#Iterating over all dictionary keys, value pairs and average the items
for (key, val), (key1, val1), (key2, val2) in zip(sorted(GCCdict1day.iteritems()), 
     sorted(ExGdict1day.iteritems()), sorted(VIgdict1day.iteritems())):
    #val, val1, val2 is the lists of GCC, ExG & VIgreen values of all valid images on that DOY
    avgGCC[key] = round(sum(val)/float(len(val)), 3)
    avgExG[key1] = round(sum(val1)/float(len(val1)), 3)
    avgVIg[key2] = round(sum(val2)/float(len(val2)), 3)
    
    #Time series of daily average VIs saved as a text file in the given directory
    f4.write('DOY: {}, Daily Average GCC: {}\n'.format(key, avgGCC[key]))
    f5.write('DOY: {}, Daily Average ExG: {}\n'.format(key1, avgExG[key1]))
    f6.write('DOY: {}, Daily Average VIg: {}\n'.format(key2, avgVIg[key2]))

#Close the file when done 
f4.close()
f5.close()
f6.close()
     
#################################################################################################
#Time series of daily averaged vegetation indices plotted against corresponding DOY   
#################################################################################################

#Plotting time series of GCC vegetation index
plt.figure(1)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], GCC, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image GCC')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(avgGCC.keys())], [avgGCC[x] for x in sorted(avgGCC.keys())], 
         'r^', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.plot([int(j) for j in sorted(avgGCCSnow.keys())], [avgGCCSnow[x] for x in sorted(avgGCCSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image GCC')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Green Chromatic Coordinate (GCC)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/GCC_1Day.jpg')
#plt.show()

#Plotting time series of ExG vegetation index
plt.figure(2)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], ExG, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image ExG')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(avgExG.keys())], [avgExG[x] for x in sorted(avgExG.keys())], 
         'ko', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.plot([int(j) for j in sorted(avgExGSnow.keys())], [avgExGSnow[x] for x in sorted(avgExGSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image ExG')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Excess Green Index (ExG)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/ExG_1Day.jpg')
#plt.show()

#Plotting time series of VIgreen vegetation index
plt.figure(3)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], VIgreen, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image VIg')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(avgVIg.keys())], [avgVIg[x] for x in sorted(avgVIg.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.plot([int(j) for j in sorted(avgVIgSnow.keys())], [avgVIgSnow[x] for x in sorted(avgVIgSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image VIgreen')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Normalized Difference of G & R (VIgreen)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/VIg_1Day.jpg')
#plt.show()

#################################################################################################
#2nd Part of Code
#################################################################################################
#Percentile VI values calculated across a 3 day moving window (Tends to track mode)
#################################################################################################
#################################################################################################

#Dictionaries to store mean indices per day from valid images (Excluding no data values for a DOY)
avgGCC1day = {}
avgExG1day = {}
avgVIg1day = {}

# Iterating through each keys of dictionary storing indices values from all daily valid images
for items in sorted(GCCdict1day.keys()):
    
    # Only calculate average values for non-empty values for a given key
    if len(GCCdict1day[items]) != 0:
        
        # Calculate daily average for a given key of dictionary storing indices of all daily images
        temp_avgGCC = round((sum(GCCdict1day[items])/float(len(GCCdict1day[items]))), 3)
        temp_avgExG = round((sum(ExGdict1day[items])/float(len(GCCdict1day[items]))), 3)
        temp_avgVIg = round((sum(VIgdict1day[items])/float(len(GCCdict1day[items]))), 3)
        
        # Assign thus calculated average value to the dictionary storing daily averages
        avgGCC1day[items] = temp_avgGCC
        avgExG1day[items] = temp_avgExG 
        avgVIg1day[items] = temp_avgVIg
    
    else:
        # Assign 0 as values to given DOY which do not have any valid image data
        avgGCC1day[items] = 0
        avgExG1day[items] = 0
        avgVIg1day[items] = 0

# Empty dictionary to save the percentile values calculated across 3 day moving window
GCC50_percentile = {}
GCC75_percentile = {}
GCC90_percentile = {}
ExG50_percentile = {}
ExG75_percentile = {}
ExG90_percentile = {}
VIg50_percentile = {}
VIg75_percentile = {}
VIg90_percentile = {}

# Empty list to save percentile calculation over 3 day moving window
p_GCCtest50 = []
p_GCCtest75 = []
p_GCCtest90 = []
p_ExGtest50 = []
p_ExGtest75 = []
p_ExGtest90 = []
p_VIgtest50 = []
p_VIgtest75 = []
p_VIgtest90 = []

# Empty list initialization to save VI values available in dictionary storing daily average VIs
GCC1day_values = []
ExG1day_values = []
VIg1day_values = []

# Appending VI values corresponding to the DOY in the list 
for items in sorted(avgGCC1day.iterkeys()):
    GCC1day_values.append(avgGCC1day[items])
    ExG1day_values.append(avgExG1day[items])
    VIg1day_values.append(avgVIg1day[items])
  
# Storing daily average VI values across 3 day moving window as tuples
zip_listGCC = zip(*(islice(GCC1day_values, i, None) for i in range(3)))
zip_listExG = zip(*(islice(ExG1day_values, i, None) for i in range(3))) 
zip_listVIg = zip(*(islice(VIg1day_values, i, None) for i in range(3)))

# Iterating over the zip_listGCC for different percentile calculation
for nbr in range(len(zip_listGCC)):
      
    # Converting each tuples to temporary lists
    temp_listGCC = list(zip_listGCC[nbr])
    temp_listExG = list(zip_listExG[nbr])
    temp_listVIg = list(zip_listVIg[nbr])

    # Converting thus type-casted list as temporary array to suffice percentile calculation
    npa_GCC = np.array(temp_listGCC)
    npa_ExG = np.array(temp_listExG)
    npa_VIg = np.array(temp_listVIg)
    
    # Calculate the 50th(Median), 75th and 90th percentile of GCC values
    percentile50 = round(np.percentile(npa_GCC, 50), 3)
    percentile75 = round(np.percentile(npa_GCC, 75), 3) 
    percentile90 = round(np.percentile(npa_GCC, 90), 3)
    
    # Feeding list with calculated percentile of GCC across 3 day moving window
    p_GCCtest50.append(percentile50)
    p_GCCtest75.append(percentile75)
    p_GCCtest90.append(percentile90)
    
    ########FILES##################################################################
    # Updating the dictionary key with the corresponding percentile as values
    GCC50_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile50
    GCC75_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile75
    GCC90_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile90
    
    # Calculate the 50th(Median), 75th and 90th percentile of ExG values
    percentile50 = round(np.percentile(npa_ExG, 50), 3)
    percentile75 = round(np.percentile(npa_ExG, 75), 3) 
    percentile90 = round(np.percentile(npa_ExG, 90), 3)
    
    # Feeding list with calculated percentile of ExG across 3 day moving window
    p_ExGtest50.append(percentile50)
    p_ExGtest75.append(percentile75)
    p_ExGtest90.append(percentile90)
    
    # Updating the dictionary key with the corresponding percentile as values
    ExG50_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile50
    ExG75_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile75
    ExG90_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile90
    
    # Calculate the 50th(Median), 75th and 90th percentile of VIg values
    percentile50 = round(np.percentile(npa_VIg, 50), 3)
    percentile75 = round(np.percentile(npa_VIg, 75), 3) 
    percentile90 = round(np.percentile(npa_VIg, 90), 3)
           
    p_VIgtest50.append(percentile50)
    p_VIgtest75.append(percentile75)
    p_VIgtest90.append(percentile90)
    
    #Updating the dictionary key with the corresponding percentile as values
    VIg50_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile50
    VIg75_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile75
    VIg90_percentile[sorted(avgGCC1day.keys())[nbr]] = percentile90
    
#Any keys that do not have values will be removed from all dictionaries storing VI
finalGCC50 = {k:GCC50_percentile[k] for k in GCC50_percentile if GCC50_percentile[k]}
finalGCC75 = {k:GCC75_percentile[k] for k in GCC75_percentile if GCC75_percentile[k]}
finalGCC90 = {k:GCC90_percentile[k] for k in GCC90_percentile if GCC90_percentile[k]}

finalExG50 = {k:ExG50_percentile[k] for k in ExG50_percentile if ExG50_percentile[k]}
finalExG75 = {k:ExG75_percentile[k] for k in ExG75_percentile if ExG75_percentile[k]}
finalExG90 = {k:ExG90_percentile[k] for k in ExG90_percentile if ExG90_percentile[k]}

finalVIg50 = {k:VIg50_percentile[k] for k in VIg50_percentile if VIg50_percentile[k]}
finalVIg75 = {k:VIg75_percentile[k] for k in VIg75_percentile if VIg75_percentile[k]}
finalVIg90 = {k:VIg90_percentile[k] for k in VIg90_percentile if VIg90_percentile[k]}

#################################################################################################
#Time series plot of 90th percentile calculated across 3 day moving window against associated DOY   
#################################################################################################

#Plotting 50th percentile of GCC computed over 3 day moving window
plt.figure(4)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], GCC, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image GCC')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(finalGCC50.keys())], [finalGCC50[x] for x in sorted(finalGCC50.keys())], 
         'r^', markersize = 6, mfc = 'none', label = '50th Percentile')
plt.plot([int(j) for j in sorted(avgGCCSnow.keys())], [avgGCCSnow[x] for x in sorted(avgGCCSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image GCC')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Green Chromatic Coordinate (GCC)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/GCC_50%3Day.jpg')
#plt.show()

#Plotting 75th percentile of GCC computed over 3 day moving window
plt.figure(5)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], GCC, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image GCC') 
plt.plot([int(j) for j in sorted(finalGCC75.keys())], [finalGCC75[x] for x in sorted(finalGCC75.keys())], 
         'r^', markersize = 6, mfc = 'none', label = '75th Percentile')
plt.plot([int(j) for j in sorted(avgGCCSnow.keys())], [avgGCCSnow[x] for x in sorted(avgGCCSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image GCC') 
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Green Chromatic Coordinate (GCC)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/GCC_75%3Day.jpg')
#plt.show()

#Plotting 90th percentile of GCC computed over 3 day moving window
plt.figure(6)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], GCC, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image GCC') 
plt.plot([int(j) for j in sorted(finalGCC90.keys())], [finalGCC90[x] for x in sorted(finalGCC90.keys())], 
         'r^', markersize = 6, mfc = 'none', label = '90th Percentile')
plt.plot([int(j) for j in sorted(avgGCCSnow.keys())], [avgGCCSnow[x] for x in sorted(avgGCCSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image GCC')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Green Chromatic Coordinate (GCC)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/GCC_90%3Day.jpg')
#plt.show()

#Plotting 50th percentile of ExG computed over 3 day moving window
plt.figure(7)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], ExG, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image ExG') 
plt.plot([int(j) for j in sorted(finalExG50.keys())], [finalExG50[x] for x in sorted(finalExG50.keys())], 
         'ko', markersize = 6, mfc = 'none', label = '50th Percentile')
plt.plot([int(j) for j in sorted(avgExGSnow.keys())], [avgExGSnow[x] for x in sorted(avgExGSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image ExG')  
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Excess Green Index (ExG)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/ExG_50%3Day.jpg')
#plt.show()

#Plotting 75th percentile of ExG computed over 3 day moving window
plt.figure(8)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], ExG, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image ExG') 
plt.plot([int(j) for j in sorted(finalExG75.keys())], [finalExG75[x] for x in sorted(finalExG75.keys())], 
         'ko', markersize = 6, mfc = 'none', label = '75th Percentile')
plt.plot([int(j) for j in sorted(avgExGSnow.keys())], [avgExGSnow[x] for x in sorted(avgExGSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image ExG')  
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Excess Green Index (ExG)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/ExG_75%3Day.jpg')
#plt.show()

#Plotting 90th percentile of ExG computed over 3 day moving window
plt.figure(9)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], ExG, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image ExG') 
plt.plot([int(j) for j in sorted(finalExG90.keys())], [finalExG90[x] for x in sorted(finalExG90.keys())], 
         'ko', markersize = 6, mfc = 'none', label = '90th Percentile')
plt.plot([int(j) for j in sorted(avgExGSnow.keys())], [avgExGSnow[x] for x in sorted(avgExGSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image ExG')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Excess Green Index (ExG)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/ExG_90%3Day.jpg')
#plt.show()

#Plotting 50th percentile of VIg computed over 3 day moving window
plt.figure(10)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], VIgreen, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image VIg') 
plt.plot([int(j) for j in sorted(finalVIg50.keys())], [finalVIg50[x] for x in sorted(finalVIg50.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '50th Percentile')
plt.plot([int(j) for j in sorted(avgVIgSnow.keys())], [avgVIgSnow[x] for x in sorted(avgVIgSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image VIgreen') 
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Normalized Difference of G & R (VIgreen)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/VIg_50%3Day.jpg')
#plt.show()

#Plotting 75th percentile of VIg computed over 3 day moving window
plt.figure(11)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], VIgreen, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image VIg') 
plt.plot([int(j) for j in sorted(finalVIg75.keys())], [finalVIg75[x] for x in sorted(finalVIg75.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '75th Percentile')
plt.plot([int(j) for j in sorted(avgVIgSnow.keys())], [avgVIgSnow[x] for x in sorted(avgVIgSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image VIgreen') 
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Normalized Difference of G & R (VIgreen)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/VIg_75%3Day.jpg')
#plt.show()

#Plotting 90th percentile of VIg computed over 3 day moving window
plt.figure(12)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45)
plt.plot([int(i) for i in DOY], VIgreen, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image VIg') 
plt.plot([int(j) for j in sorted(finalVIg90.keys())], [finalVIg90[x] for x in sorted(finalVIg90.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '90th Percentile')
plt.plot([int(j) for j in sorted(avgVIgSnow.keys())], [avgVIgSnow[x] for x in sorted(avgVIgSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image VIgreen')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Normalized Difference of G & R (VIgreen)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/ROI5/1DPlot/VIg_90%3Day.jpg')
#plt.show()

#################################################################################################
#Find out the total elapsed time and print out on the screen
#################################################################################################

end = datetime.now()
time_taken = end - start

#These line of codes will print out the total elapsed time
print '\n'
print ('Time elapsed: {}').format(time_taken)      

#################################################################################################