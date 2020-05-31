%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Curve fitting for the UAV derived NDVI using Spline interpolation
%technique: Shangharsha Thapa
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Read from a .txt file that stores NDVI values 
%NDVI values for the year 2018
values = load('UAVSmooth18.txt');

%Empty vector to store the DOY
xdata = zeros(length(values), 1);

%Empty vector to store the NDVI values
ydata = zeros(length(values), 1);

%Looping to append the DOY and NDVI values to respective vectors
for i = 1:length(values)
    xdata(i) = values(i);
    ydata(i) = values(i, 2);
end

%Spline Interpolation to fit the time series NDVI
xi = 106:3:241; %2018
method ='spline'
yi=interp1(xdata,ydata,xi,method)

%Splitting the vector into two vectors representing green up and senescence
gup = yi(1:find(yi==max(yi), 1,'first'));
xdataup = xi(1:find(yi==max(yi), 1,'first'));
sen = yi(find(yi==max(yi), 1,'first'):end);
xdatasen = xi(find(yi==max(yi), 1,'first'):end);

%Plotting the green up and senescence
p1 = plot(xdataup,gup,'g-', 'color', [0 0.5 0], 'LineWidth',3)
text (120, 0.78, 'Green-up', 'color', [0 0.5 0], 'FontSize', 16)
hold on
p2 = plot(xdatasen, sen, '-', 'color', [ 0.91 0.41 0.17], 'LineWidth',3)
text (220, 0.78, 'Senescence', 'color', [ 0.91 0.41 0.17], 'FontSize', 16)

%Plot the initial original DOY and smoothed NDVI values
p3 = plot(xdata,ydata, 'ko','LineWidth',0.5, 'MarkerSize',12)
p3.MarkerFaceColor = 'y';
set(gca,'FontSize',12)
xlabel 'Day of Year (2018)'
ylabel 'Normalized Difference Vegetation Index (NDVI)'
grid on

%Compute first and second order derivative
dy = gradient(yi, xi);
dyy = gradient(dy, xi);

%Compute the curvature
k = abs(dyy) ./ (1 + dy.^2).^1.5;

%Normalize the data to appear between 0 an 1
rescaled = (k - min(k))./(max(k)-min(k));

%Also plot the curvature
%plot(xi, rescaled)

%Find local minima and maxima and plot it
minima = islocalmin(rescaled);
maxima = islocalmax(rescaled);

%Find the first two maxima
result = mink(find(maxima==1), 4);
mid = mink(find(minima==1), 2);

%Plot the vertical line through the two maxima
% Set current y-axis limits
ylim([0.7, 0.85]); 
p4 = plot([xi(result(1)) xi(result(1))],[0.7 0.85], 'color', [0 0.5 0], 'LineWidth',1.5)
p5 = plot(xi(result(1)), yi(result(1)), 'bo')
text (xi(result(1))-2, 0.696, '112', 'FontSize', 12)
p6 = plot([xi(mid(2)) xi(mid(2))],[0.7 0.85], 'color', [0 0.5 0],'linestyle','--', 'LineWidth',1.)
p7 = plot(xi(mid(2)), yi(mid(2)), 'bo')
text (xi(mid(2))-2, 0.696, '163', 'FontSize', 12)
p8 = plot([xi(28) xi(28)],[0.7 0.85], 'r', 'LineWidth',1.)
p9 = plot(xi(28), yi(28), 'bo')
text (xi(28)-2, 0.696, '187', 'FontSize', 12)
p12 = plot([xi(result(2)) xi(result(2))],[0.7 0.85], 'color', [0 0.5 0],'linestyle', '-.', 'LineWidth',1.)
p13 = plot(xi(result(2)), yi(result(2)), 'bo')
text (xi(result(2))-2, 0.696, '136', 'FontSize', 12)
p14 = plot([xi(result(3)) xi(result(3))],[0.7 0.85], '-.r', 'LineWidth',1.5)
p15 = plot(xi(result(3)), yi(result(3)), 'bo')
text (xi(result(3))-2, 0.696, '235', 'FontSize', 12)


hlegend1 = legend([p3, p4, p6, p8, p12, p14], {'Smoothed NDVI', 'Start of Season (SOS)',... 
    'End of Season (EOS)', 'Start of Fall (SOF)', 'Middle of Season (MOS)',...
    'Middle of Fall (MOF)'}, 'FontSize', 12, 'Location','NorthEast');
