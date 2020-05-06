"""
Created on Tue Feb 18 13:29:32 2020
Author: Shangharsha
This python code calculates the solar elevation angle and removes all night/dark images. 
At the sametime, it also removes the very dark and very bright images from phenology
analysis to the respective folders created automatically by the code.
"""
#################################################################################################
#Module Declaration
#################################################################################################

import glob
import os
import pytz, datetime
import ephem
import shutil
import cv2
import numpy as np

#################################################################################################
#Automatic folder creation, path definition for cutting and pasting night time images
#################################################################################################

#Make a folder named 'Filtered' in your working directory before changing the path
thePath = r'F:\MasterThesis\ASA\Phenocam\2019\Filtered'

#Automatically creating folders in the directory to store images under different folders
#Try-except block is to pass overwrite directories if exists
folders = ['Night', 'Dark', 'Bright']
for folder in folders:
    try:
        os.mkdir(os.path.join(thePath, folder))
    except:
        pass

#Defining the path for saving night, dark and bright images
#Change the path similar to 'thePath' variable, base path being the same        
dest_night = r'F:\MasterThesis\ASA\Phenocam\2019\Filtered\Night'
dest_dark = r'F:\MasterThesis\ASA\Phenocam\2019\Filtered\Dark'
dest_bright = r'F:\MasterThesis\ASA\Phenocam\2019\Filtered\Bright'

#################################################################################################
#Solar elevation of all images calculation in order to filter very bright and dark images
#################################################################################################

print 'Filtering out night images and very dark images......'

#Iterating all images
#Change the path to folder storing images other than filtered
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/all_images/*.jpg"):
    
    #Extracting image file name
    dt_info = os.path.basename(img)
    
    #Extracting file size for each image
    fileSize =  os.path.getsize(img)/float(1048576)
    
    #Day of Year information (DOY) extraction from image file name
    ymdt = dt_info[4:21]
    
    #Date. TimeStamp information extraction from combined Year, Month, Day and time
    year = ymdt[0:4]
    month = ymdt[4:6]
    day = ymdt[6:8]
    hour = ymdt[13:15]
    imgDate = year + '-' + month + '-' + day 
    imgTime = hour + ':00' + ':00'
    
    timeStamp = imgDate + ' ' + imgTime
    
    #Setting up timezone of study area
    local = pytz.timezone ("Europe/Stockholm")
    
    #Construct a timezone object out of it, manipulate and attach it to the asa_dt datetime 
    asa_dt = datetime.datetime.strptime (timeStamp, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(asa_dt, is_dst=None)
    
    #Convert dateTime to UTC
    utc_dst = local_dt.astimezone(pytz.utc)
    
    #Formatting UTC time as datetime format
    UTCTime = utc_dst.strftime ("%Y-%m-%d %H:%M:%S")
    tb_used = datetime.datetime.strptime (UTCTime, "%Y-%m-%d %H:%M:%S")
    
    #Print the UTC time of all images
    #print tb_used
    
    obs=ephem.Observer()
    #Latitude and Longitude of Asa research Station. Always change this for working in new areas.
    #Note that Latitude and Longitude in DMS (Degree, Minute, Second) system
    obs.lat='57:08:57.55'
    obs.long='14:44:19.92'
    obs.date = tb_used
    #print obs
    
    sun = ephem.Sun(obs)
    sun.compute(obs)
    #Convert Radians to Degrees
    sun_angle = float(sun.alt) * 57.2957795 
    dec2_sun_angle = round(sun_angle, 2)
    
#################################################################################################
#Check to move all night images to its respective destination folder
#################################################################################################        
    
    if (dec2_sun_angle < 0) and (fileSize <= 2.0):
        shutil.move(img, dest_night) 

#################################################################################################
#Check to move all very dark images to its respective destination folder
#################################################################################################
    
    elif ((dec2_sun_angle > 0 and dec2_sun_angle < 5) and (fileSize <= 2.0)):
        shutil.move(img, dest_dark)
        
#################################################################################################
#Check the total DN of given ROI to apply a threshold to move all very bright images
#################################################################################################

print 'Filtering out very bright images......'

#Iterating through all the images to calculate total DN within given ROI
for img in glob.glob("F:/MasterThesis/ASA/Phenocam/2019/all_images/*.jpg"):
   
    #Reading image one by one
    cv_img = cv2.imread(img)
    
    #Extracting image file name
    imgName = os.path.basename(img)
    
    #3 region of interests are defined as the images were burned on upper part only
    #Burned part appeared on three regions. However, one common region of interest 
    #can be drawn to filter the very bright image. Coordinates can be adjusted as per
    #needed.
    ROI1 = cv_img [0:500, 0:500]
    ROI2 = cv_img [0:500, 2000:3000]
    ROI3 = cv_img [0:200, 500:2000]
    
    #Splitting RGB image into separate bands
    R1, G1, B1 = cv2.split(ROI1)
    R2, G2, B2 = cv2.split(ROI2)
    R3, G3, B3 = cv2.split(ROI3)
    
    #Finding out mean DN of RGB bands within ROI 
    Rm1 = np.mean(R1)
    Gm1 = np.mean(G1)
    Bm1 = np.mean(B1)
    
    Rm2 = np.mean(R2)
    Gm2 = np.mean(G2)
    Bm2 = np.mean(B2)
    
    Rm3 = np.mean(R3)
    Gm3 = np.mean(G3)
    Bm3 = np.mean(B3)

    #Total mean DN of ROI 
    TotalDN_ROI1 = Rm1 + Gm1 + Bm1
    TotalDN_ROI2 = Rm2 + Gm2 + Bm2
    TotalDN_ROI3 = Rm3 + Gm3 + Bm3
    
    #Applying threshold to filter out bright images; threshold values can be adjusted
    if (TotalDN_ROI1 >= 550) or (TotalDN_ROI2 >= 550) or (TotalDN_ROI3 >= 550):
        shutil.move(img, dest_bright)
        
##################################################################################################
