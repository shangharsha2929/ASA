% Extract required records from .mat file (for eg: timestamp, airTemp and 
% precipitation)of Asa storing meteorological variables and export it as 
% a separate .txt files. Author: Shangharsha Thapa

%Define the path of the data
folder = 'F:\MasterThesis\ASA\Meteorological'; 

%Define the file name you want to load in the path
%fileName = fullfile(folder,  'SE-Asa_LFdata_2018_new.mat');
fileName = fullfile(folder,  'SE-Asa_LFdata_2019_new.mat');

data = load(fileName);

%Extract the required fields mainly temperature and precipitation from the
%structure
timeStamp = data.SE_Asa_LFdata.rawdata(:, 1);
airTemp = data.SE_Asa_LFdata.rawdata(:, 8);
precip = data.SE_Asa_LFdata.rawdata(:, 11);

%Write extracted values to a .txt file
%fileID = fopen('met2018.txt','w');
fileID = fopen('met2019.txt','w');

for k = 1:length(timeStamp)
    fprintf(fileID, '%d %.3f %.3f\n', timeStamp(k), airTemp(k), precip(k));
end

fclose(fileID);

    