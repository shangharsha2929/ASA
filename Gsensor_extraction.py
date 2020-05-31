"""
Created on Tue Mar 10 23:53:28 2020
Python code to calculate PRI, NDVI above canopy and NDVI on ground from sensor mounted on Tower and
plot the corresponding indices values averaged over a single day or 3 day.
This python code handles 2 years data at once, if users are supposed to plot the data for a single year
then the code shall be modified.
@author: Shangharsha
"""
################################################################################################################################################
#Importing required modules
################################################################################################################################################
import csv
import datetime
import matplotlib.pyplot as plt
import os

################################################################################################################################################
#Empty dictionary to store Date as key and corresponding values
################################################################################################################################################
#Radiance for red and NIR measured by above and down looking sensor for 2018 and 2019 (FOR PRI)
dict18_PRIUP531 = {'1/1/2018':[]}
dict18_PRIDN531 = {'1/1/2018':[]}
dict19_PRIUP531 = {'1/1/2019':[]}
dict19_PRIDN531 = {'1/1/2019':[]}
dict18_PRIUP570 = {'1/1/2018':[]}
dict18_PRIDN570 = {'1/1/2018':[]}
dict19_PRIUP570 = {'1/1/2019':[]}
dict19_PRIDN570 = {'1/1/2019':[]}

#Radiance for red and NIR measured by above and down looking sensor for 2018 and 2019 (FOR NDVI)
dict18_UPTWR650 = {'1/1/2018':[]}
dict18_DNTWR650 = {'1/1/2018':[]}
dict19_UPTWR650 = {'1/1/2019':[]}
dict19_DNTWR650 = {'1/1/2019':[]}
dict18_UPTWR810 = {'1/1/2018':[]}
dict18_DNTWR810 = {'1/1/2018':[]}
dict19_UPTWR810 = {'1/1/2019':[]}
dict19_DNTWR810 = {'1/1/2019':[]}

dict18_UPgrd650 = {'1/1/2018':[]}
dict18_DNgrd650 = {'1/1/2018':[]}
dict19_UPgrd650 = {'1/1/2019':[]}
dict19_DNgrd650 = {'1/1/2019':[]}
dict18_UPgrd810 = {'1/1/2018':[]}
dict18_DNgrd810 = {'1/1/2018':[]}
dict19_UPgrd810 = {'1/1/2019':[]}
dict19_DNgrd810 = {'1/1/2019':[]}

################################################################################################################################################
#Read, extract and save the radiances values in respective dictionaries for 2018 - 2019 data
################################################################################################################################################    
#Set the path for the .dat file
#Don't forget to change for other file
thePath1 = r'F:\MasterThesis\ASA\GroundSensor\Nybygget_CR1000_Minutes10_2018-201900322.dat'

#Read the .csv file from the directory
with open(thePath1) as f:
    
    #Pull data from a CSV file using reader function
    reader = csv.reader(f, delimiter="\t")
    
    #Avoid header
    next(reader, None)
    
    #Iterating over lines in the given csvfiles
    for line in reader:
        
        #Extract date information from each line of csv file
        #Split at first whitespace and extract the first element
        mmddyy = line[0].split()[0]
        
        #Get the hour information from each line of csv file
        hhmm = int(line[0].split()[1].split(':')[0])
        
        #Data to be extracted from the .dat file
        priup531 = float(line[2])
        priup570 = float(line[3])
        pridn531 = float(line[5])
        pridn570 = float(line[6])
            
        ndviuptwr650 = float(line[8])
        ndviuptwr810 = float(line[9])
        ndvidntwr650 = float(line[11])
        ndvidntwr810 = float(line[12])
            
        ndviupgrd650 = float(line[14])
        ndviupgrd810 = float(line[15])
        ndvidngrd650 = float(line[17])
        ndvidngrd810 = float(line[18])
               
        #Extract values for 2018 and 2019 separately and only between 8 AM and 19PM
        if (int(mmddyy.split('/')[2]) != 2019) and (hhmm >= 8 and hhmm <= 19):
        
            #Update dictionary with DOY and its associated values
            if mmddyy in dict18_PRIUP531:
                dict18_PRIUP531[mmddyy].append(priup531)
                dict18_PRIDN531[mmddyy].append(pridn531)
                dict18_PRIUP570[mmddyy].append(priup570)
                dict18_PRIDN570[mmddyy].append(pridn570)
                
                dict18_UPTWR650[mmddyy].append(ndviuptwr650)
                dict18_DNTWR650[mmddyy].append(ndvidntwr650)
                dict18_UPTWR810[mmddyy].append(ndviuptwr810)
                dict18_DNTWR810[mmddyy].append(ndvidntwr810)
                
                dict18_UPgrd650[mmddyy].append(ndviupgrd650)
                dict18_DNgrd650[mmddyy].append(ndvidngrd650)
                dict18_UPgrd810[mmddyy].append(ndviupgrd810)
                dict18_DNgrd810[mmddyy].append(ndvidngrd810)
                           
            else:
                dict18_PRIUP531[mmddyy] = [priup531]
                dict18_PRIDN531[mmddyy] = [pridn531]
                dict18_PRIUP570[mmddyy] = [priup570]
                dict18_PRIDN570[mmddyy] = [pridn570]
                
                dict18_UPTWR650[mmddyy] = [ndviuptwr650]
                dict18_DNTWR650[mmddyy] = [ndvidntwr650]
                dict18_UPTWR810[mmddyy] = [ndviuptwr810]
                dict18_DNTWR810[mmddyy] = [ndvidntwr810]
                
                dict18_UPgrd650[mmddyy] = [ndviupgrd650]
                dict18_DNgrd650[mmddyy] = [ndvidngrd650]
                dict18_UPgrd810[mmddyy] = [ndviupgrd810]
                dict18_DNgrd810[mmddyy] = [ndvidngrd810]
        
        elif (int(mmddyy.split('/')[2]) == 2019) and (hhmm >= 8 and hhmm <= 19):
            
            #Update dictionary with DOY and its associated values
            if mmddyy in dict19_PRIUP531:
                #Data for PRI indices from up and down looking sensors
                dict19_PRIUP531[mmddyy].append(priup531)
                dict19_PRIDN531[mmddyy].append(pridn531)
                dict19_PRIUP570[mmddyy].append(priup570)
                dict19_PRIDN570[mmddyy].append(pridn570)
                
                #Red and NIR band radiances for above canopy 
                dict19_UPTWR650[mmddyy].append(ndviuptwr650)
                dict19_DNTWR650[mmddyy].append(ndvidntwr650)
                dict19_UPTWR810[mmddyy].append(ndviuptwr810)
                dict19_DNTWR810[mmddyy].append(ndvidntwr810)
                
                #Red and NIR band radiances for near ground  
                dict19_UPgrd650[mmddyy].append(ndviupgrd650)
                dict19_DNgrd650[mmddyy].append(ndvidngrd650)
                dict19_UPgrd810[mmddyy].append(ndviupgrd810)
                dict19_DNgrd810[mmddyy].append(ndvidngrd810)
                           
            else:
                dict19_PRIUP531[mmddyy] = [priup531]
                dict19_PRIDN531[mmddyy] = [pridn531]
                dict19_PRIUP570[mmddyy] = [priup570]
                dict19_PRIDN570[mmddyy] = [pridn570]
                
                dict19_UPTWR650[mmddyy] = [ndviuptwr650]
                dict19_DNTWR650[mmddyy] = [ndvidntwr650]
                dict19_UPTWR810[mmddyy] = [ndviuptwr810]
                dict19_DNTWR810[mmddyy] = [ndvidntwr810]
                
                dict19_UPgrd650[mmddyy] = [ndviupgrd650]
                dict19_DNgrd650[mmddyy] = [ndvidngrd650]
                dict19_UPgrd810[mmddyy] = [ndviupgrd810]
                dict19_DNgrd810[mmddyy] = [ndvidngrd810]
              
################################################################################################################################################
#Read, extract and save the radiances values in respective dictionaries for 2019 data
################################################################################################################################################                
#Set the path for the second .dat file
#File format and naming convention is different. So, a new loop for extracting rest of 2019 data
thePath1 = r'F:\MasterThesis\ASA\GroundSensor\Nybygget_CR1000_SWE-ASA-NYB-For-F01_20190322-2020.dat'

#Read the .csv file from the directory
with open(thePath1) as f1:
    
    #Pull data from a CSV file using reader function
    reader = csv.reader(f1, delimiter="\t")
    
    #Avoid header
    next(reader, None)
    
    #Iterating over lines in the given csvfiles
    for line in reader:
        #Extract date information from each line of csv file
        #Split at first whitespace and extract the first element
        mmddyy = line[0].split()[0]
        
        #Get the hour information from each line of csv file
        hhmm = int(line[0].split()[1].split(':')[0])
        
        #Change this with required data to be extracted
        priup531 = float(line[4])
        priup570 = float(line[5])
        pridn531 = float(line[7])
        pridn570 = float(line[8])
            
        ndviuptwr650 = float(line[10])
        ndviuptwr810 = float(line[11])
        ndvidntwr650 = float(line[13])
        ndvidntwr810 = float(line[14])
            
        ndviupgrd650 = float(line[16])
        ndviupgrd810 = float(line[17])
        ndvidngrd650 = float(line[19])
        ndvidngrd810 = float(line[20])
       
        if (int(mmddyy.split('/')[2]) == 2019) and ((hhmm >= 8 and hhmm <= 19)):
        
            #Update dictionary with DOY and its associated values
            if mmddyy in dict19_PRIUP531:
                dict19_PRIUP531[mmddyy].append(priup531)
                dict19_PRIDN531[mmddyy].append(pridn531)
                dict19_PRIUP570[mmddyy].append(priup570)
                dict19_PRIDN570[mmddyy].append(pridn570)
                    
                dict19_UPTWR650[mmddyy].append(ndviuptwr650)
                dict19_DNTWR650[mmddyy].append(ndvidntwr650)
                dict19_UPTWR810[mmddyy].append(ndviuptwr810)
                dict19_DNTWR810[mmddyy].append(ndvidntwr810)
                    
                dict19_UPgrd650[mmddyy].append(ndviupgrd650)
                dict19_DNgrd650[mmddyy].append(ndvidngrd650)
                dict19_UPgrd810[mmddyy].append(ndviupgrd810)
                dict19_DNgrd810[mmddyy].append(ndvidngrd810)
                               
            else:
                dict19_PRIUP531[mmddyy] = [priup531]
                dict19_PRIDN531[mmddyy] = [pridn531]
                dict19_PRIUP570[mmddyy] = [priup570]
                dict19_PRIDN570[mmddyy] = [pridn570]
                    
                dict19_UPTWR650[mmddyy] = [ndviuptwr650]
                dict19_DNTWR650[mmddyy] = [ndvidntwr650]
                dict19_UPTWR810[mmddyy] = [ndviuptwr810]
                dict19_DNTWR810[mmddyy] = [ndvidntwr810]
                    
                dict19_UPgrd650[mmddyy] = [ndviupgrd650]
                dict19_DNgrd650[mmddyy] = [ndvidngrd650]
                dict19_UPgrd810[mmddyy] = [ndviupgrd810]
                dict19_DNgrd810[mmddyy] = [ndvidngrd810]

################################################################################################################################################
#Converting date information of 2018 into corresponding DOY    
################################################################################################################################################
#Get dictionary keys as list
dkeys18 = dict18_PRIUP531.keys()
            
#Converting date information of 2018 into corresponding DOY
for keys in dkeys18:
    dtime = keys.split('/')
    yymmdd = dtime[2] + '-' + dtime[0] + '-' + dtime[1]
    
    #Converting string to datetime datatype
    yymmddDT = datetime.datetime.strptime(yymmdd, '%Y-%m-%d')
    
    #Converting to corresponding DOY
    dayOfYear = yymmddDT.strftime('%j')
    
    #Rename corresponding key with DOY information
    dict18_PRIUP531[dayOfYear] = dict18_PRIUP531.pop(keys)
    dict18_PRIDN531[dayOfYear] = dict18_PRIDN531.pop(keys)
    dict18_PRIUP570[dayOfYear] = dict18_PRIUP570.pop(keys)
    dict18_PRIDN570[dayOfYear] = dict18_PRIDN570.pop(keys)
    
    dict18_UPTWR650[dayOfYear] = dict18_UPTWR650.pop(keys)
    dict18_DNTWR650[dayOfYear] = dict18_DNTWR650.pop(keys)
    dict18_UPTWR810[dayOfYear] = dict18_UPTWR810.pop(keys)
    dict18_DNTWR810[dayOfYear] = dict18_DNTWR810.pop(keys)
    
    dict18_UPgrd650[dayOfYear] = dict18_UPgrd650.pop(keys)
    dict18_DNgrd650[dayOfYear] = dict18_DNgrd650.pop(keys)
    dict18_UPgrd810[dayOfYear] = dict18_UPgrd810.pop(keys)
    dict18_DNgrd810[dayOfYear] = dict18_DNgrd810.pop(keys)

################################################################################################################################################
#Converting date information of 2019 into corresponding DOY    
################################################################################################################################################
#Get dictionary keys as list
dkeys19 = dict19_PRIUP531.keys()

#Iterating over the keys from above list
for keys in dkeys19:
    dtime = keys.split('/')
    yymmdd = dtime[2] + '-' + dtime[0] + '-' + dtime[1]
    
    #Converting string to datetime datatype
    yymmddDT = datetime.datetime.strptime(yymmdd, '%Y-%m-%d')
    
    #Converting to corresponding DOY
    dayOfYear = yymmddDT.strftime('%j')
    
    #Rename corresponding key with DOY information
    dict19_PRIUP531[dayOfYear] = dict19_PRIUP531.pop(keys)
    dict19_PRIDN531[dayOfYear] = dict19_PRIDN531.pop(keys)
    dict19_PRIUP570[dayOfYear] = dict19_PRIUP570.pop(keys)
    dict19_PRIDN570[dayOfYear] = dict19_PRIDN570.pop(keys)
    
    dict19_UPTWR650[dayOfYear] = dict19_UPTWR650.pop(keys)
    dict19_DNTWR650[dayOfYear] = dict19_DNTWR650.pop(keys)
    dict19_UPTWR810[dayOfYear] = dict19_UPTWR810.pop(keys)
    dict19_DNTWR810[dayOfYear] = dict19_DNTWR810.pop(keys)
    
    dict19_UPgrd650[dayOfYear] = dict19_UPgrd650.pop(keys)
    dict19_DNgrd650[dayOfYear] = dict19_DNgrd650.pop(keys)
    dict19_UPgrd810[dayOfYear] = dict19_UPgrd810.pop(keys)
    dict19_DNgrd810[dayOfYear] = dict19_DNgrd810.pop(keys)    

################################################################################################################################################    
#Calculate reflectance from radiance for the year 2018 and 2019
################################################################################################################################################    
# division of lists using zip() + list comprehension 
PRI531R18 = {k: [i / j for i, j in zip(dict18_PRIDN531[k], dict18_PRIUP531[k])] for k in dict18_PRIUP531.keys() and dict18_PRIDN531.keys()}    
PRI570R18 = {k: [i / j for i, j in zip(dict18_PRIDN570[k], dict18_PRIUP570[k])] for k in dict18_PRIUP570.keys() and dict18_PRIDN570.keys()}
    
redR18_twr = {k: [i / j for i, j in zip(dict18_DNTWR650[k], dict18_UPTWR650[k])] for k in dict18_UPTWR650.keys() and dict18_DNTWR650.keys()}    
nirR18_twr = {k: [i / j for i, j in zip(dict18_DNTWR810[k], dict18_UPTWR810[k])] for k in dict18_UPTWR810.keys() and dict18_DNTWR810.keys()}

redR18_grd = {k: [i / j for i, j in zip(dict18_DNgrd650[k], dict18_UPgrd650[k])] for k in dict18_UPgrd650.keys() and dict18_DNgrd650.keys()}    
nirR18_grd = {k: [i / j for i, j in zip(dict18_DNgrd810[k], dict18_UPgrd810[k])] for k in dict18_UPgrd810.keys() and dict18_DNgrd810.keys()}

PRI531R19 = {k: [i / j for i, j in zip(dict19_PRIDN531[k], dict19_PRIUP531[k])] for k in dict19_PRIUP531.keys() and dict19_PRIDN531.keys()}    
PRI570R19 = {k: [i / j for i, j in zip(dict19_PRIDN570[k], dict19_PRIUP570[k])] for k in dict19_PRIUP570.keys() and dict19_PRIDN570.keys()}
    
redR19_twr = {k: [i / j for i, j in zip(dict19_DNTWR650[k], dict19_UPTWR650[k])] for k in dict19_UPTWR650.keys() and dict19_DNTWR650.keys()}    
nirR19_twr = {k: [i / j for i, j in zip(dict19_DNTWR810[k], dict19_UPTWR810[k])] for k in dict19_UPTWR810.keys() and dict19_DNTWR810.keys()}

redR19_grd = {k: [i / j for i, j in zip(dict19_DNgrd650[k], dict19_UPgrd650[k])] for k in dict19_UPgrd650.keys() and dict19_DNgrd650.keys()}    
nirR19_grd = {k: [i / j for i, j in zip(dict19_DNgrd810[k], dict19_UPgrd810[k])] for k in dict19_UPgrd810.keys() and dict19_DNgrd810.keys()}

#################################################################################################################################################
#PRI, NDVI calculation for 2018 and 2019 from respective bands
#################################################################################################################################################
#Calculate PRI over the years
pri018 = {k: [(i - j)/(i + j) for i, j in zip(PRI531R18[k], PRI570R18[k])] for k in PRI531R18.keys() and PRI570R18.keys()}
pri019 = {k: [(i - j)/(i + j) for i, j in zip(PRI531R19[k], PRI570R19[k])] for k in PRI531R19.keys() and PRI570R19.keys()}

#Calculate NDVI above canopy
#Note: abs() function is used because the RED and NIR band in .dat file is swapped.
ndvi018AC = {k: [(i - j)/(i + j) for i, j in zip(nirR18_twr[k], redR18_twr[k])] for k in nirR18_twr.keys() and redR18_twr.keys()}
ndvi019AC = {k: [abs((i - j)/(i + j)) for i, j in zip(nirR19_twr[k], redR19_twr[k])] for k in nirR19_twr.keys() and redR19_twr.keys()}

#Calculate NDVI near ground
ndvi018OG = {k: [(i - j)/(i + j) for i, j in zip(nirR18_grd[k], redR18_grd[k])] for k in nirR18_grd.keys() and redR18_grd.keys()}
ndvi019OG = {k: [(i - j)/(i + j) for i, j in zip(nirR19_grd[k], redR19_grd[k])] for k in nirR19_grd.keys() and redR19_grd.keys()}

#################################################################################################################################################
#Daily averaged PRI, NDVI calculation for both years
#################################################################################################################################################
avgPRI018 = {}
avgPRI019 = {}

#Daily averaged above canopy NDVI calculation
avgNDVI018_AC = {}
avgNDVI019_AC = {}

#Daily averaged ground NDVI calculation
avgNDVI018_OG = {}
avgNDVI019_OG = {}

#Always don't forget to change the directory for 'Result' folder
thePath = r'F:\MasterThesis\ASA\GroundSensor\TextFiles'

#Assigning path to create new text file for storing daily averaged indices values
path_avgPRI018 = os.path.join(thePath + r'\avgPRI018.txt')
path_avgNDVI018AC = os.path.join(thePath + r'\avgNDVI018AC.txt')
path_avgNDVI018OG = os.path.join(thePath + r'\avgNDVI018OG.txt')

path_avgPRI019 = os.path.join(thePath + r'\avgPRI019.txt')
path_avgNDVI019AC = os.path.join(thePath + r'\avgNDVI019AC.txt')
path_avgNDVI019OG = os.path.join(thePath + r'\avgNDVI019OG.txt')

#Open a file for writing the corresponding DOY and vegetation indices
txt1 = open(path_avgPRI018, 'w')
txt2 = open(path_avgNDVI018AC, 'w')
txt3 = open(path_avgNDVI018OG, 'w')

txt4 = open(path_avgPRI019, 'w')
txt5 = open(path_avgNDVI019AC, 'w')
txt6 = open(path_avgNDVI019OG, 'w')

#Iterating over all 2018 dictionary keys, value pairs and average the items
for (k, v), (k1, v1), (k2, v2) in zip(sorted(pri018.iteritems()), sorted(ndvi018AC.iteritems()), sorted(ndvi018OG.iteritems())):
    #val, val1, val2 is the lists of PRI, NDVI above canopy and on ground of all observations on that DOY
    avgPRI018[k] = round(sum(v)/len(v), 3)
    avgNDVI018_AC[k1] = round(sum(v1)/len(v1), 3)
    avgNDVI018_OG[k2] = round(sum(v2)/len(v2), 3)
    
    #Time series of daily average VIs saved as a text file in the given directory
    txt1.write('{}, {}\n'.format(k, avgPRI018[k]))
    txt2.write('{}, {}\n'.format(k1, avgNDVI018_AC[k1]))
    txt3.write('{}, {}\n'.format(k2, avgNDVI018_OG[k2]))

#Close the file when done 
txt1.close()
txt2.close()
txt3.close()
   
#Iterating over all 2019 dictionary keys, value pairs and average the items    
for (k3, v3), (k4, v4), (k5, v5) in zip(sorted(pri019.iteritems()), sorted(ndvi019AC.iteritems()), sorted(ndvi019OG.iteritems())):   
    
    avgPRI019[k3] = round(sum(v3)/len(v3), 3)
    avgNDVI019_AC[k4] = round(sum(v4)/len(v4), 3)
    avgNDVI019_OG[k5] = round(sum(v5)/len(v5), 3)
    
    #Time series of daily average VIs saved as a text file in the given directory
    txt4.write('{}, {}\n'.format(k3, avgPRI019[k3]))
    txt5.write('{}, {}\n'.format(k4, avgNDVI019_AC[k4]))
    txt6.write('{}, {}\n'.format(k5, avgNDVI019_OG[k5]))

#Close the file when done 
txt4.close()
txt5.close()
txt6.close()
    
#################################################################################################################################################
#Plotting daily overage on top of all valid data
#################################################################################################################################################
#Plotting time series of PRI 2018
plt.rcParams['figure.figsize'] = (16,8)
plt.figure(0)
xs, ys=zip(*((x, int(k)) for k in pri018 for x in pri018[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All PRI data')
plt.plot([int(j) for j in sorted(avgPRI018.keys())], [avgPRI018[x] for x in sorted(avgPRI018.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Photochemical Reflectance Index (PRI)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\PRI18_1Davg.jpg')
#plt.show()

#Plotting time series of above canopy NDVI 2018
plt.figure(1)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi018AC for x in ndvi018AC[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI018_AC.keys())], [avgNDVI018_AC[x] for x in sorted(avgNDVI018_AC.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\AC_NDVI18_1Davg.jpg')
#plt.show()

#Plotting time series of ground NDVI 2018
plt.figure(2)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi018OG for x in ndvi018OG[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI018_OG.keys())], [avgNDVI018_OG[x] for x in sorted(avgNDVI018_OG.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\Grd_NDVI18_1Davg.jpg')
#plt.show()

#Plotting time series of PRI 2019
plt.figure(3)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in pri019 for x in pri019[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All PRI data')
plt.plot([int(j) for j in sorted(avgPRI019.keys())], [avgPRI019[x] for x in sorted(avgPRI019.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Photochemical Reflectance Index (PRI)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\PRI19_1Davg.jpg')
#plt.show()

#Plotting time series of above canopy NDVI 2019
plt.figure(4)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi019AC for x in ndvi019AC[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI019_AC.keys())], [avgNDVI019_AC[x] for x in sorted(avgNDVI019_AC.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\AC_NDVI19_1Davg.jpg')
#plt.show()

#Plotting time series of ground NDVI 2019
plt.figure(5)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi019OG for x in ndvi019OG[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI019_OG.keys())], [avgNDVI019_OG[x] for x in sorted(avgNDVI019_OG.keys())], 
         'ro', markersize = 6, mfc = 'none', label = 'Daily Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\Grd_NDVI19_1Davg.jpg')
#plt.show()

#################################################################################################################################################
#3 day average of PRI, NDVI calculation for both years
#################################################################################################################################################
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
PRI3day2018 = {}
PRI3day2019 = {}
NDVI3AC2018 = {}
NDVI3AC2019 = {}
NDVI3OG2018 = {}
NDVI3OG2019 = {}

#Add DOY with 0 values that is not available on dictionary storing average values
for i in xrange(1, 366):
    if (i not in [int(j) for j in sorted(avgPRI018.keys())]) and (i not in [int(j) for j in sorted(avgNDVI018_AC.keys())]) and \
    (i not in [int(j) for j in sorted(avgNDVI018_OG.keys())]):
        if i < 10:
            addkey = '00'+ str(i)
            avgPRI018[addkey] = float('nan')
            avgNDVI018_AC[addkey] = float('nan')
            avgNDVI018_OG[addkey] = float('nan')
            
        elif i >= 10 and i < 100:
            addkey = '0'+ str(i)
            avgPRI018[addkey] = float('nan')
            avgNDVI018_AC[addkey] = float('nan')
            avgNDVI018_OG[addkey] = float('nan')
    
        else:
            addkey = str(i)
            avgPRI018[addkey] = float('nan')
            avgNDVI018_AC[addkey] = float('nan')
            avgNDVI018_OG[addkey] = float('nan')

for i in xrange(1, 366):
    if (i not in [int(j) for j in sorted(avgPRI019.keys())]) and (i not in [int(j) for j in sorted(avgNDVI019_AC.keys())]) and \
    (i not in [int(j) for j in sorted(avgNDVI019_OG.keys())]):
        if i < 10:
            addkey = '00'+ str(i)
            avgPRI019[addkey] = float('nan')
            avgNDVI019_AC[addkey] = float('nan')
            avgNDVI019_OG[addkey] = float('nan')
            
        elif i >= 10 and i < 100:
            addkey = '0'+ str(i)
            avgPRI019[addkey] = float('nan')
            avgNDVI019_AC[addkey] = float('nan')
            avgNDVI019_OG[addkey] = float('nan')
    
        else:
            addkey = str(i)
            avgPRI019[addkey] = float('nan')
            avgNDVI019_AC[addkey] = float('nan')
            avgNDVI019_OG[addkey] = float('nan')   
            
#Creating dictionary with list of values for each 3 day time step PRI, NDVI values as lists
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
        PRI3day2018[thirdDay[nbr]] = [avgPRI018[x] for x in (third, second, first)]
        NDVI3AC2018[thirdDay[nbr]] = [avgNDVI018_AC[x] for x in (third, second, first)]
        NDVI3OG2018[thirdDay[nbr]] = [avgNDVI018_OG[x] for x in (third, second, first)]
        
        PRI3day2019[thirdDay[nbr]] = [avgPRI019[x] for x in (third, second, first)]
        NDVI3AC2019[thirdDay[nbr]] = [avgNDVI019_AC[x] for x in (third, second, first)]
        NDVI3OG2019[thirdDay[nbr]] = [avgNDVI019_OG[x] for x in (third, second, first)]
        
    elif items >= '010' and items < '100':
        first = thirdDay[nbr]
        second = '0' + str(int(thirdDay[nbr]) - 1)
        third = '0' + str(int(thirdDay[nbr]) - 2)
        
        #Assign first, second and last lists as list of values to the current key 
        PRI3day2018[thirdDay[nbr]] = [avgPRI018[x] for x in (third, second, first)]
        NDVI3AC2018[thirdDay[nbr]] = [avgNDVI018_AC[x] for x in (third, second, first)]
        NDVI3OG2018[thirdDay[nbr]] = [avgNDVI018_OG[x] for x in (third, second, first)]
        
        PRI3day2019[thirdDay[nbr]] = [avgPRI019[x] for x in (third, second, first)]
        NDVI3AC2019[thirdDay[nbr]] = [avgNDVI019_AC[x] for x in (third, second, first)]
        NDVI3OG2019[thirdDay[nbr]] = [avgNDVI019_OG[x] for x in (third, second, first)]
    
    else:
        first = thirdDay[nbr]
        second = str(int(thirdDay[nbr]) - 1)
        third = str(int(thirdDay[nbr]) - 2)
        
        #Assign first, second and last lists as list of values to the current key 
        PRI3day2018[thirdDay[nbr]] = [avgPRI018[x] for x in (third, second, first)]
        NDVI3AC2018[thirdDay[nbr]] = [avgNDVI018_AC[x] for x in (third, second, first)]
        NDVI3OG2018[thirdDay[nbr]] = [avgNDVI018_OG[x] for x in (third, second, first)]
        
        PRI3day2019[thirdDay[nbr]] = [avgPRI019[x] for x in (third, second, first)]
        NDVI3AC2019[thirdDay[nbr]] = [avgNDVI019_AC[x] for x in (third, second, first)]
        NDVI3OG2019[thirdDay[nbr]] = [avgNDVI019_OG[x] for x in (third, second, first)]

#Empty dictionary to populate with average indices values at each 3 day time step
avgPRI3_18 = {}
avgNDVI3AC_18 = {}
avgNDVI3OG_18 = {}
avgPRI3_19 = {}
avgNDVI3AC_19 = {}
avgNDVI3OG_19 = {}

#Assigning path to create new text file for storing daily averaged indices values
path_avg3PRI018 = os.path.join(thePath + r'\avg3PRI018.txt')
path_avg3NDVI018AC = os.path.join(thePath + r'\avg3NDVI018AC.txt')
path_avg3NDVI018OG = os.path.join(thePath + r'\avg3NDVI018OG.txt')

path_avg3PRI019 = os.path.join(thePath + r'\avg3PRI019.txt')
path_avg3NDVI019AC = os.path.join(thePath + r'\avg3NDVI019AC.txt')
path_avg3NDVI019OG = os.path.join(thePath + r'\avg3NDVI019OG.txt')

#Open a file for writing the corresponding DOY and vegetation indices
txt1 = open(path_avg3PRI018, 'w')
txt2 = open(path_avg3NDVI018AC, 'w')
txt3 = open(path_avg3NDVI018OG, 'w')

txt4 = open(path_avg3PRI019, 'w')
txt5 = open(path_avg3NDVI019AC, 'w')
txt6 = open(path_avg3NDVI019OG, 'w')

#Iterating each keys of dictionary storing each 3 day list of indices values
for items in sorted(PRI3day2018.keys()):
    #Get average of each keys
    avgPRI3_18[items] = round(sum(PRI3day2018[items])/3, 3)
    avgPRI3_19[items] = round(sum(PRI3day2019[items])/3, 3)
    avgNDVI3AC_18[items] = round(sum(NDVI3AC2018[items])/3, 3)
    avgNDVI3AC_19[items] = round(sum(NDVI3AC2019[items])/3, 3)
    avgNDVI3OG_18[items] = round(sum(NDVI3OG2018[items])/3, 3)
    avgNDVI3OG_19[items] = round(sum(NDVI3OG2019[items])/3, 3)
    
    #Time series of daily average VIs saved as a text file in the given directory
    txt1.write('{}, {}\n'.format(items, avgPRI3_18[items]))
    txt2.write('{}, {}\n'.format(items, avgNDVI3AC_18[items]))
    txt3.write('{}, {}\n'.format(items, avgNDVI3OG_18[items]))
    
    txt4.write('{}, {}\n'.format(items, avgPRI3_19[items]))
    txt5.write('{}, {}\n'.format(items, avgNDVI3AC_19[items]))
    txt6.write('{}, {}\n'.format(items, avgNDVI3OG_19[items]))
    
#Close the file when done 
txt1.close()
txt2.close()
txt3.close()
txt4.close()
txt5.close()
txt6.close()

#################################################################################################################################################
#Plotting 3 day overage on top of all valid data
#################################################################################################################################################
#Plotting time series of PRI 2018
plt.figure(6)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in pri018 for x in pri018[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All PRI data')
plt.plot([int(j) for j in sorted(avgPRI3_18.keys())], [avgPRI3_18[x] for x in sorted(avgPRI3_18.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Photochemical Reflectance Index (PRI)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\PRI18_3Davg.jpg')
#plt.show()

#Plotting time series of above canopy NDVI 2018
plt.figure(7)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi018AC for x in ndvi018AC[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI3AC_18.keys())], [avgNDVI3AC_18[x] for x in sorted(avgNDVI3AC_18.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\AC_NDVI18_3Davg.jpg')
#plt.show()

#Plotting time series of ground NDVI 2018
plt.figure(8)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi018OG for x in ndvi018OG[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI3OG_18.keys())], [avgNDVI3OG_18[x] for x in sorted(avgNDVI3OG_18.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2018)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\Grd_NDVI18_3Davg.jpg')
#plt.show()

#Plotting time series of PRI 2019
plt.figure(9)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in pri019 for x in pri019[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All PRI data')
plt.plot([int(j) for j in sorted(avgPRI3_19.keys())], [avgPRI3_19[x] for x in sorted(avgPRI3_19.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (DOY)', fontsize = 18)
plt.ylabel('Photochemical Reflectance Index (PRI)', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\PRI19_3Davg.jpg')
#plt.show()

#Plotting time series of above canopy NDVI 2019
plt.figure(10)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi019AC for x in ndvi019AC[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI3AC_19.keys())], [avgNDVI3AC_19[x] for x in sorted(avgNDVI3AC_19.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\AC_NDVI19_3Davg.jpg')
#plt.show()

#Plotting time series of ground NDVI 2019
plt.figure(11)
plt.rcParams['figure.figsize'] = (16,8)
xs, ys=zip(*((x, int(k)) for k in ndvi019OG for x in ndvi019OG[k]))
plt.xticks(range(0, 365, 10), rotation = 45) 
plt.plot(ys, xs, 'o', color = 'grey', markersize = 4, alpha = 0.1, label = 'All NDVI data')
plt.plot([int(j) for j in sorted(avgNDVI3OG_19.keys())], [avgNDVI3OG_19[x] for x in sorted(avgNDVI3OG_19.keys())], 
         'ro', markersize = 6, mfc = 'none', label = '3 Day Average')
plt.grid(alpha = 0.2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Day of Year (2019)', fontsize = 18)
plt.ylabel('NDVI', fontsize = 18)
plt.legend(loc = 'upper left', fontsize = 14)
plt.savefig(r'F:\MasterThesis\ASA\GroundSensor\Graphs\Grd_NDVI19_3Davg.jpg')
#plt.show()

#######################################################################################################################