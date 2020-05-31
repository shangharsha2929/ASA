"""
Created on Sat Apr 25 12:18:31 2020
This code uses the .txt file storing the temperature and precipitation data for year 2018
and 2019 respectively. It calculates the 3-day average temperature and precipitation and 
finally plot it as bar diagram.
@author: Shangharsha
"""
#Importing required modules
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

##########################################################################################
#2018
##########################################################################################

#Reading .txt file to extract TimeStamp, temperature & precipitation for 2018
#.txt file should be in the same path as the .py files or users shall provide full path to file 
with open('met2018.txt','r') as data:
    
    #Empty list to store the corresponding values from the text file
    timeStamp = []
    airTemp = []
    precip = []
    
    #Iterating through the text file line by line & storin values in lists
    for lines in data:
        
        #Splitting a string based on space
        info = lines.split(' ')
        
        #Assisgn the values to its corresponding categories
        tS = float(info[0])
        aT = float(info[1])
        pT = float(info[2])
        
        #Appending the values to the empty list declared at the very first
        timeStamp.append(tS)
        airTemp.append(aT)
        precip.append(pT)
        
#List comprehension to store every 48 elements in a separate list
temp_list = [airTemp[x:x+48] for x in range(0, len(airTemp), 48)]
precp_lst = [precip[x:x+48] for x in range(0, len(precip), 48)]

#Empty list to store the temperature & precipitation data other than NODATA
tempCleaned = []
precCleaned = []

#Removing NODATA values from all lists
for item in temp_list:
    cleaned_list = [ x for x in item if x != -9999.0]
    cleaned0 = [ x for x in cleaned_list if x != 0.0]
    tempCleaned.append(cleaned0)

for item in precp_lst:
    cleaned_list = [ x for x in item if x != -9999.0]
    cleaned0 = [ x for x in cleaned_list if x != 0.0]
    precCleaned.append(cleaned0)
    
#Empty dictionary to store the DOY and associated temperature values
tempDict = {}
precDict = {}

#Iterating day wise and updating the dictionary with key value pair
for i in range(1, 366):
    tempDict[i] = tempCleaned[i-1]
    precDict[i] = precCleaned[i-1]

#Average temperature computation per day
avgTemp = {}
avgPrecp = {}

#Iterate over all dictionary keys and average the items
for k,v in tempDict.iteritems():
    
    #Check if the list is empty
    if v:
        avgTemp[k] = round(sum(v)/ float(len(v)), 3)
    else:
        avgTemp[k] = 0.000

for k, v in precDict.iteritems():
    if v:
        avgPrecp[k] = round(sum(v)/ float(len(v)), 3)
    else:
        avgPrecp[k] = 0.0
         
#Computing 3day average temperature
temp3Day = [avgTemp.values()[x:x+3] for x in range(0, len(avgTemp.values()), 3)]
precip3D = [avgPrecp.values()[x:x+3] for x in range(0, len(avgPrecp.values()), 3)]

#Writing DOY and 3day average temperature as a dictionary
doy = list(range(3, 367, 3))

#Removing 0 and averaging the data
avgtemp3Day = []
avgppt3Day = []
for sublist in temp3Day:
    cleaned0 = [ x for x in sublist if x != 0.0]
    mTemp = round(sum(cleaned0)/ float(len(cleaned0)), 3)
    avgtemp3Day.append(mTemp)

#Remove the list with all 0s and average the list with non zero elements only
for precplist in precip3D:
    cleaned0 = [ x for x in precplist if x != 0.0]
    if cleaned0:
        mPpt = round(sum(cleaned0)/ float(len(cleaned0)), 3)
        avgppt3Day.append(mPpt)
    else: 
        avgppt3Day.append(0.0)

avgPrecip3Day = {}
#Create a dictionary with DOY at an iterval of every 3 days
for i in range(3, 367, 3):
    avgPrecip3Day[i] = []

#Iterating over the keys and updating the key with its associated value
for nbr, itm in enumerate(avgPrecip3Day.keys()):
    avgPrecip3Day[itm] = avgppt3Day[nbr]

#Delete key if value is 0
for k,v in avgPrecip3Day.items():
    if v == 0.0:
       del avgPrecip3Day[k]
    
#Plotting the 3 day averaged temperature
plt.rcParams['figure.figsize'] = (10,5)
fig, axs = plt.subplots(2, 2)
xcor, ycor = 117, -15
xcor1, ycor1 = 155, -15
plt.figure(0)
plt.subplot(211)
plt.bar(doy, avgtemp3Day, align='center', width = 1.5, color = 'r', label = '3 Day Average')
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((xcor, ycor), 0, 45, linestyle = '-.', alpha = 0.5, linewidth = 2, fill=None))
currentAxis.add_patch(Rectangle((xcor1, ycor1), 0, 45, linestyle = ':', alpha = 0.5, linewidth = 2, fill=None))
plt.grid(alpha = 0.2)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tick_params(labelbottom=False)  
plt.ylabel('Temperature (Celsius)', fontsize = 10)
plt.legend(loc = 'best', fontsize = 8) 
    
plt.subplot(212)
plt.bar(avgPrecip3Day.keys(), avgPrecip3Day.values(), align = 'center', width = 1.5, color='b', label = '3 Day Average')    
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((xcor, ycor), 0, 35, linestyle = '-.', alpha = 0.5, linewidth = 2, fill=None))
currentAxis.add_patch(Rectangle((xcor1, ycor1), 0, 35, linestyle = ':', alpha = 0.5, linewidth = 2, fill=None))
plt.grid(alpha = 0.2)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Day of Year (2018)', fontsize = 10)
plt.ylabel('Precipitation (mm)', fontsize = 10)
plt.legend(loc = 'best', fontsize = 8) 

##########################################################################################
#2019
##########################################################################################
#Reading .txt file to extract TimeStamp, temperature & precipitation for 2018
#.txt file should be in the same path as the .py files or users shall provide full path to file 
with open('met2019.txt','r') as data:
    
    #Empty list to store the corresponding values from the text file
    timeStamp = []
    airTemp = []
    precip = []
    
    #Iterating through the text file line by line & storin values in lists
    for lines in data:
        
        #Splitting a string based on space
        info = lines.split(' ')
        
        #Assisgn the values to its corresponding categories
        tS = float(info[0])
        aT = float(info[1])
        pT = float(info[2])
        
        #Appending the values to the empty list declared at the very first
        timeStamp.append(tS)
        airTemp.append(aT)
        precip.append(pT)
        
#List comprehension to store every 48 elements in a separate list
temp_list = [airTemp[x:x+48] for x in range(0, len(airTemp), 48)]
precp_lst = [precip[x:x+48] for x in range(0, len(precip), 48)]

#Empty list to store the temperature & precipitation data other than NODATA
tempCleaned = []
precCleaned = []

#Removing NODATA values from all lists
for item in temp_list:
    cleaned_list = [ x for x in item if x != -9999.0]
    cleaned0 = [ x for x in cleaned_list if x != 0.0]
    tempCleaned.append(cleaned0)

for item in precp_lst:
    cleaned_list = [ x for x in item if x != -9999.0]
    cleaned0 = [ x for x in cleaned_list if x != 0.0]
    precCleaned.append(cleaned0)

#Empty dictionary to store the DOY and associated temperature values
tempDict = {}
precDict = {}

#Iterating day wise and updating the dictionary with key value pair
for i in range(1, 366):
    tempDict[i] = tempCleaned[i-1]
    precDict[i] = precCleaned[i-1]

#Average temperature computation per day
avgTemp = {}
avgPrecp = {}

#Iterate over all dictionary keys and average the items
for k,v in tempDict.iteritems():
    
    #Check if the list is empty
    if v:
        avgTemp[k] = round(sum(v)/ float(len(v)), 3)
    else:
        avgTemp[k] = 0.000

for k, v in precDict.iteritems():
    if v:
        avgPrecp[k] = round(sum(v)/ float(len(v)), 3)
    else:
        avgPrecp[k] = 0.0

#Computing 3day average temperature
temp3Day = [avgTemp.values()[x:x+3] for x in range(0, len(avgTemp.values()), 3)]
precip3D = [avgPrecp.values()[x:x+3] for x in range(0, len(avgPrecp.values()), 3)]

#Writing DOY and 3day average temperature as a dictionary
doy = list(range(3, 367, 3))

#Removing 0 and averaging the data
avgtemp3Day = []
avgppt3Day = []
for sublist in temp3Day:
    cleaned0 = [ x for x in sublist if x != 0.0]
    if cleaned0:
        mTemp = round(sum(cleaned0)/ float(len(cleaned0)), 3)
        avgtemp3Day.append(mTemp)
    else:
        avgtemp3Day.append(0.0)

#Remove the list with all 0s and average the list with non zero elements only
for precplist in precip3D:
    cleaned0 = [ x for x in precplist if x != 0.0]
    if cleaned0:
        mPpt = round(sum(cleaned0)/ float(len(cleaned0)), 3)
        avgppt3Day.append(mPpt)
    else: 
        avgppt3Day.append(0.0)

#Plotting the 3 day averaged temperature
plt.rcParams['figure.figsize'] = (10,5)
xcor, ycor = 120, -10
xcor1, ycor1 = 167, -10
plt.figure(1)
plt.subplot(211)
plt.bar(doy, avgtemp3Day, align='center', width = 1.5, color = 'r', label = '3 Day Average')
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((xcor, ycor), 0, 40, linestyle = '-.', alpha = 0.5, linewidth = 2, fill=None))
currentAxis.add_patch(Rectangle((xcor1, ycor1), 0, 40, linestyle = ':', alpha = 0.5, linewidth = 2, fill=None))
plt.grid(alpha = 0.2)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tick_params(labelbottom=False) 
plt.ylabel('Temperature (Celsius)', fontsize = 10)
plt.legend(loc = 'best', fontsize = 8) 
    
plt.subplot(212)
plt.bar(doy, avgppt3Day, align = 'center', color='b', width = 1.5, label = '3 Day Average')    
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((xcor, ycor), 0, 40, linestyle = '-.', alpha = 0.5, linewidth = 2, fill=None))
currentAxis.add_patch(Rectangle((xcor1, ycor1), 0, 40, linestyle = ':', alpha = 0.5, linewidth = 2, fill=None))
plt.grid(alpha = 0.2)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Day of Year (2019)', fontsize = 10)
plt.ylabel('Precipitation (mm)', fontsize = 10)
plt.legend(loc = 'best', fontsize = 8) 

#Note: Vertical lines in the plot refer to Start and End Of Season for Spruce forest in Spring
###############################################################################################