# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:12:35 2020
This code extracts mean DN values over defined region of interest, use those mean DN values to
compute mean GCC, ExG and VIgreen values over all images. Finally, from these values, 3-day 
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
thePath = r'F:\MasterThesis\ASA\Phenocam\2019\Result'

#################################################################################################
#Make a list of all DOYs for a year from 1 - 365
#################################################################################################

oneDay = []
for i in xrange(1,366):
    #Type conversion
    if i < 10:
        keyToCompare = '00' + str(i)
        oneDay.append(keyToCompare)
        
    elif i >= 10 and i < 100:
        keyToCompare = '0' + str(i)
        oneDay.append(keyToCompare)
        
    else:
        keyToCompare = str(i)
        oneDay.append(keyToCompare)

#################################################################################################
#Initializing the empty dictionary for each vegetation indices to save the DOY as Key
#################################################################################################
        
GCCdict1day = {}
ExGdict1day = {}
VIgdict1day = {}

#################################################################################################
#Iterating over the list to assign each element as a separate key to the dictionary
#################################################################################################

for list_val in oneDay:
    GCCdict1day[list_val] = [] 
    ExGdict1day[list_val] = []
    VIgdict1day[list_val] = []
    
#################################################################################################
#Display Region of Interest (ROI) Selection in the image  
#################################################################################################

#Change the path of one of the image of your working site

#Assign directory of one of image file to show the extent of ROI
imgDir = r'F:\MasterThesis\ASA\Phenocam\2018\all_images\Asa_20180521_141_0500.jpg'

#Loading image from the specified file
img = cv2.imread(imgDir)

#Multiple ROI definition for the image

ROI1 = img [1100:1700, 250:800]
#ROI2 = img [1000:1700, 1500:2300]
#ROI3 = img [200:1700, 820:1700]
#ROI4 = img [200:750, 200:2400]
#ROI5 = img [200:1700, 200:2400]
#################################################################################################
#Draw ROI on top of image to give visual representaion of ROI location 
#################################################################################################

#Rectangle coordinates are given in the order (Xmin, Ymin) & (Xmax, Ymax)

cv2.rectangle(img,(250,1100),(800,1700),(0,0,255),7)
#cv2.rectangle(img,(1500,1000),(2300,1700),(0,255,255),7)
#cv2.rectangle(img,(820,200),(1700,1700),(255,0,0),7)
#cv2.rectangle(img,(200,200),(2400,750),(0,255,0),7)
#cv2.rectangle(img, (200,200),(2400,1700),(0,0,255),7)

#OpenCV represents image in reverse order BGR; so convert it to appear in RGB mode and plot it
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

#################################################################################################
#Automatically creating folders in the directory to save results into
#################################################################################################

#Try-except block is to pass overwrite directories if exists
folders = ['3DPlot','3DTxt']
for folder in folders:
    try:
        os.mkdir(os.path.join(thePath, folder))
    except:
        pass

#################################################################################################
#Assigning path to create text file 
#################################################################################################        
pathGCC = os.path.join(thePath + r'\3DTxt\GCC1Day.txt')
pathExG = os.path.join(thePath + r'\3DTxt\ExG1Day.txt')
pathVIg = os.path.join(thePath + r'\3DTxt\VIg1Day.txt')

#Open a file for writing the image name, corresponding DOY and vegetation indices
f1 = open(pathGCC, 'w')
f2 = open(pathExG, 'w')
f3 = open(pathVIg, 'w')

#################################################################################################
#Vegetation indices calculation within given ROI for all valid images
#################################################################################################
    
#Iterating all images
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/ROI1/all_images/*.jpg"):
    #print img
   
    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    #print imgName
    
    #Day of Year information (DOY) extraction from image file name
    dayOfYear = imgName[13:16]
    #print dayOfYear
    DOY.append(dayOfYear)

    #Defining Region of Interest
    ROI = cv_img [1100:1700, 250:800]
    
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
    v = round(((Gm - Rm)/(Gm + Rm)), 3)
    
    #Appending GCC, ExG and VIgreen values for each iterated images
    GCC.append(g)
    ExG.append(e)
    VIgreen.append(v)
    
    #Time series of vegetation indices saved as a text file in the given directory
    f1.write('IMG: {}, DOY: {}, GCC: {}\n'.format(imgName, dayOfYear, g))
    f2.write('IMG: {}, DOY: {}, ExG: {}\n'.format(imgName, dayOfYear, e))
    f3.write('IMG: {}, DOY: {}, VIg: {}\n'.format(imgName, dayOfYear, v))
    
    #Update dictionary with DOY and its associated multiple vegetation indices values
    GCCdict1day[dayOfYear].append(g)
    ExGdict1day[dayOfYear].append(e)
    VIgdict1day[dayOfYear].append(v)    
   
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
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/ROI1/Snow/*.jpg"):
   
    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    
    #Day of Year information (DOY) extraction from image file name
    dayOfYear = imgName[13:16]
    
    #Defining Region of Interest
    ROI = cv_img [1100:1700, 250:800]
    
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
    
#################################################################################################
#Finding the average of each 3 day vegetation indices values 
#################################################################################################
    
#Make a list of all DOYs for a year from 1 - 365
thirdDay = []
for i in xrange(3,366,3):
    #Type conversion
    if i < 10:
        keyToCompare = '00' + str(i)
        thirdDay.append(keyToCompare)
        
    elif i >= 10 and i < 100:
        keyToCompare = '0' + str(i)
        thirdDay.append(keyToCompare)
        
    else:
        keyToCompare = str(i)
        thirdDay.append(keyToCompare)

#Empty dictionary to store indices values as lists for each 3 day time step
GCCdict3day = {}
ExGdict3day = {}
VIgdict3day = {}

#Creating dictionary with list of values for each 3 day time step GCC values as lists
for nbr, items in enumerate(thirdDay):
    
    #Condition to be satisfied for DOY as mentioned.
    if items < '010':
        #Last list to be assigned
        first = thirdDay[nbr]
        
        #Second list to be assigned
        second = '00' + str(int(thirdDay[nbr]) - 1)
        
        #First list to be assigned
        third = '00' + str(int(thirdDay[nbr]) - 2)
        
        #Assign first, second and last lists as list of values to the current key 
        GCCdict3day[thirdDay[nbr]] = [GCCdict1day[x] for x in (third, second, first)]
        ExGdict3day[thirdDay[nbr]] = [ExGdict1day[x] for x in (third, second, first)]
        VIgdict3day[thirdDay[nbr]] = [VIgdict1day[x] for x in (third, second, first)]
        
    elif items >= '010' and items < '100':
        first = thirdDay[nbr]
        second = '0' + str(int(thirdDay[nbr]) - 1)
        third = '0' + str(int(thirdDay[nbr]) - 2)
        
        #Assign first, second and last lists as list of values to the current key 
        GCCdict3day[thirdDay[nbr]] = [GCCdict1day[x] for x in (third, second, first)]
        ExGdict3day[thirdDay[nbr]] = [ExGdict1day[x] for x in (third, second, first)]
        VIgdict3day[thirdDay[nbr]] = [VIgdict1day[x] for x in (third, second, first)]
    
    else:
        first = thirdDay[nbr]
        second = str(int(thirdDay[nbr]) - 1)
        third = str(int(thirdDay[nbr]) - 2)
        
        #Assign first, second and last lists as list of values to the current key 
        GCCdict3day[thirdDay[nbr]] = [GCCdict1day[x] for x in (third, second, first)]
        ExGdict3day[thirdDay[nbr]] = [ExGdict1day[x] for x in (third, second, first)]
        VIgdict3day[thirdDay[nbr]] = [VIgdict1day[x] for x in (third, second, first)]

#Empty dictionary to populate with average indices values at each 3 day time step
avgGCC3day = {}
avgExG3day = {}
avgVIg3day = {}

#Assigning path to create new text file for storing daily averaged indices values
path_avgGCC = os.path.join(thePath + r'\3DTxt\avgGCC3Day.txt')
path_avgExG = os.path.join(thePath + r'\3DTxt\avgExG3Day.txt')
path_avgVIg = os.path.join(thePath + r'\3DTxt\avgVIg3Day.txt')

#Open a file for writing the corresponding DOY and vegetation indices
f4 = open(path_avgGCC, 'w')
f5 = open(path_avgExG, 'w')
f6 = open(path_avgVIg, 'w')

#Iterating each keys of dictionary storing each 3 day list of indices values
for items in sorted(GCCdict3day.keys()):
    
    #Initialization of variables as '0' to calculate sum and finally average indices per key
    initial_gsum = 0
    initial_esum = 0
    initial_vsum = 0
    
    #This variable counts the total number of values used in average calculation 
    total_items = 0

    #Iterating over each individual list stored as values in dictionary    
    for i in range(len(GCCdict3day[items])):
        
        #Get sum of each list stored as a value for a given key
        gsum = sum(GCCdict3day[items][i])
        esum = sum(ExGdict3day[items][i])
        vsum = sum(VIgdict3day[items][i])
        
        #Count number of items only in case sum of list is non zero
        if gsum != 0:
            nbr_items = len(GCCdict3day[items][i])
            total_items = total_items + nbr_items
        
        #Partial sum of indices values used for average calculation
        initial_gsum = initial_gsum + gsum
        initial_esum = initial_esum + esum
        initial_vsum = initial_vsum + vsum
    
    if initial_gsum==0 and total_items==0:
        
        # Assign 0 as values to given DOY which do not have any valid image data
        avgGCC3day[items] = 0
        avgExG3day[items] = 0
        avgVIg3day[items] = 0
        
        #Time series of daily average VIs saved as a text file in the given directory
        f4.write('DOY: {}, 3 Day Average GCC: {}\n'.format(items, avgGCC3day[items]))
        f5.write('DOY: {}, 3 Day Average ExG: {}\n'.format(items, avgExG3day[items]))
        f6.write('DOY: {}, 3 Day Average VIg: {}\n'.format(items, avgVIg3day[items]))
        
    else:
        #Average calculation with the final sum and total number of items
        temp_avgGCC = round(initial_gsum/float(total_items), 3)
        temp_avgExG = round(initial_esum/float(total_items), 3)
        temp_avgVIg = round(initial_vsum/float(total_items), 3)
        
        #Assign the average value as values to the dictionary storing avg values for given key
        avgGCC3day[items] = temp_avgGCC
        avgExG3day[items] = temp_avgExG 
        avgVIg3day[items] = temp_avgVIg
        
        #Time series of daily average VIs saved as a text file in the given directory
        f4.write('DOY: {}, 3 Day Average GCC: {}\n'.format(items, avgGCC3day[items]))
        f5.write('DOY: {}, 3 Day Average ExG: {}\n'.format(items, avgExG3day[items]))
        f6.write('DOY: {}, 3 Day Average VIg: {}\n'.format(items, avgVIg3day[items]))

#Close the file when done 
f4.close()
f5.close()
f6.close()

#################################################################################################
#Any keys that do not have values will be removed
#################################################################################################
        
finalGCC = {k:avgGCC3day[k] for k in avgGCC3day if avgGCC3day[k]}
finalExG = {k:avgExG3day[k] for k in avgExG3day if avgExG3day[k]}
finalVIg = {k:avgVIg3day[k] for k in avgVIg3day if avgVIg3day[k]}

#################################################################################################
#Time series of daily averaged vegetation indices plotted against corresponding DOY   
#################################################################################################

#Plotting time series of GCC vegetation index
plt.figure(1)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], GCC, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image GCC')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(finalGCC.keys())], [finalGCC[x] for x in sorted(finalGCC.keys())], 
         'r^', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.plot([int(j) for j in sorted(avgGCCSnow.keys())], [avgGCCSnow[x] for x in sorted(avgGCCSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image GCC')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Green Chromatic Coordinate (GCC)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/3DPlot/GCC_3Day.jpg')
#plt.show()

#Plotting time series of ExG vegetation index
plt.figure(2)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], ExG, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image ExG')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(finalExG.keys())], [finalExG[x] for x in sorted(finalExG.keys())], 
         'ko', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.plot([int(j) for j in sorted(avgExGSnow.keys())], [avgExGSnow[x] for x in sorted(avgExGSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image ExG')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Excess Green Index (ExG)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/3DPlot/ExG_3Day.jpg')
#plt.show()

#Plotting time series of VIgreen vegetation index
plt.figure(3)
plt.rcParams['figure.figsize'] = (16,8)
plt.plot([int(i) for i in DOY], VIgreen, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All image VIg')
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(j) for j in sorted(finalVIg.keys())], [finalVIg[x] for x in sorted(finalVIg.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.plot([int(j) for j in sorted(avgVIgSnow.keys())], [avgVIgSnow[x] for x in sorted(avgVIgSnow.keys())],
          'bo', mfc = 'none', label = 'Snowy image VIgreen')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Normalized Difference of G & R (VIgreen)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2019/Result/3DPlot/VIg_3Day.jpg')
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