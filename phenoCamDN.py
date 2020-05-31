"""
Created on Mon Mar  9 16:00:12 2020
This script plots the band-wise average RGB values of all available images for a given ROI in a
daily basis. At the same time, saves the corresponding values in .txt files which can be handled
later using other softwares or programming languages.  
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

##################################################################################################
#Image Region of Interest (ROI) Selection   
##################################################################################################

#Assign directory of one of image file to show the extent of ROI
imgDir = r'F:\MasterThesis\ASA\Phenocam\2018\all_images\Asa_20180521_141_0500.jpg'

#Loading image from the specified file
img = cv2.imread(imgDir)

#ROI definition for the same image
ROI4 = img [100:1850, 100:2500]

##################################################################################################
#Draw ROI on top of image to give visual representaion of ROI location 
##################################################################################################
#Rectangle coordinates are given in the order (Xmin, Ymin) & (Xmax, Ymax)
cv2.rectangle(img,(100,100),(2500,1850),(0,255,0),7)

#OpenCV represents image in reverse order BGR; so convert it to appear in RGB mode and plot it
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

#Always don't forget to change the directory for 'Result' folder
thePath = r'F:\MasterThesis\ASA\Phenocam\2018\Result'

#Initializing the empty dictionary to save the DOY as Key and GCC values from valid images
REDdict1day = {'001':[]}
GREENdict1day = {'001':[]}
BLUEdict1day = {'001':[]}

#Iterating all images
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2018/PhenoCamDN/*.jpg"):
    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    
    #Day of Year information (DOY) extraction from image file name
    dayOfYear = imgName[13:16]
    
    #Defining Region of Interest
    ROI = cv_img [100:1850, 100:2500]
    
    #Splitting RGB image into separate bands
    R, G, B = cv2.split(ROI)
    
    #Finding out mean DN of RGB bands within ROI 
    Rm = round(np.mean(R), 3)
    Gm = round(np.mean(G), 3)
    Bm = round(np.mean(B), 3)
        
    #Update dictionary with DOY and its associated multiple vegetation indices values
    if dayOfYear in REDdict1day:
        REDdict1day[dayOfYear].append(Rm)
        GREENdict1day[dayOfYear].append(Gm)
        BLUEdict1day[dayOfYear].append(Bm)
        
    else:
        REDdict1day[dayOfYear] = [Rm]
        GREENdict1day[dayOfYear] = [Gm]
        BLUEdict1day[dayOfYear] = [Bm]
        
#Dictionaries to store mean indices per day from valid images (Excluding no data values for a DOY)
avgR = {}
avgG = {}
avgB = {}

#Assigning path to create new text file for storing daily averaged indices values
path_avgR = os.path.join(thePath + r'\1DTxt\avgR1Day.txt')
path_avgG = os.path.join(thePath + r'\1DTxt\avgG1Day.txt')
path_avgB = os.path.join(thePath + r'\1DTxt\avgB1Day.txt')

#Open a file for writing the corresponding DOY and vegetation indices
txt1 = open(path_avgR, 'w')
txt2 = open(path_avgG, 'w')
txt3 = open(path_avgB, 'w')

#Iterating over all dictionary keys, value pairs and average the items
for (k, v), (k1, v1), (k2, v2) in zip(sorted(REDdict1day.iteritems()), 
     sorted(GREENdict1day.iteritems()), sorted(BLUEdict1day.iteritems())):
    #v, v1, v2 is the lists of R, G & B values of all valid images on that DOY
    avgR[k] = round(sum(v)/float(len(v)), 3)
    avgG[k1] = round(sum(v1)/float(len(v1)), 3)
    avgB[k2] = round(sum(v2)/float(len(v2)), 3)
    
    #Time series of daily average VIs saved as a text file in the given directory
    txt1.write('DOY: {}, Daily Average Red: {}\n'.format(k, avgR[k]))
    txt2.write('DOY: {}, Daily Average Green: {}\n'.format(k1, avgG[k1]))
    txt3.write('DOY: {}, Daily Average Blue: {}\n'.format(k2, avgB[k2]))

#Close the file when done 
txt1.close()
txt2.close()
txt3.close()

#Plotting time series of GCC vegetation index
plt.figure(1)
plt.rcParams['figure.figsize'] = (16,8)
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot([int(i) for i in sorted(avgR.keys())], [avgR[x] for x in sorted(avgR.keys())], 
         'ro', markersize = 6, label = 'Red')
plt.plot([int(j) for j in sorted(avgG.keys())], [avgG[y] for y in sorted(avgG.keys())], 
         'go', markersize = 6, label = 'Green')
plt.plot([int(k) for k in sorted(avgB.keys())], [avgB[z] for z in sorted(avgB.keys())], 
         'bo', markersize = 6, label = 'Blue')
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Phenocam DNs', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
#plt.savefig(r'F:/MasterThesis/ASA/Phenocam/2018/Result/1DPlot/GCC_1Day.jpg')
plt.show()

#################################################################################################
#Find out the total elapsed time and print out on the screen
#################################################################################################

end = datetime.now()
time_taken = end - start

#These line of codes will print out the total elapsed time
print '\n'
print ('Time elapsed: {}').format(time_taken)      

#################################################################################################