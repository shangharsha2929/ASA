%Double Logistic function to calculate the seasonality events from time
%series of VIs. Initial guess parameters should be supplied by the users
%and it differs from data to data. 
%Author: Shangharsha Thapa
values = load('avg_sGCC3day.txt');
xdata = zeros(length(values), 1);
ydata = zeros(length(values), 1);
for i = 1:length(values)
    xdata(i) = values(i);
    ydata(i) = values(i, 2);
end

%Define double logistic models
fun = @(x)x(1)+x(2).*((1./(1+exp(-x(3).*(xdata-x(4)))))-((1./(1+exp(-x(5).*(xdata-x(6)))))))-ydata;

x0 = [0, 0.8, 1, 130, -1, 180];
%x0 = [0, 0.05, 1, 130, -1, 180];
options = optimoptions(@lsqnonlin,'Algorithm','levenberg-marquardt');
[x,resnorm,residual,exitflag,output,lambda,jacobian] = lsqnonlin(fun,x0,[],[],options);

glist = x(1)+x(2).*((1./(1+exp(-x(3).*(xdata-x(4)))))-((1./(1+exp(-x(5).*(xdata-x(6)))))));

%Splitting the vector into two vectors representing green up and senescence
gup = glist(1:find(glist==max(glist), 1,'first'));
xdataup = xdata(1:find(glist==max(glist), 1,'first'));
sen = glist(find(glist==max(glist), 1,'first'):end);
xdatasen = xdata(find(glist==max(glist), 1,'first'):end);

%Plotting the green up and senescence
p1 = plot(xdataup,gup,'g-', 'color', [0 0.5 0], 'LineWidth',3)
text (60, 0.5, 'Green-up', 'color', [0 0.5 0], 'FontSize', 18)
hold on
p2 = plot(xdatasen, sen, '-', 'color', [ 0.91 0.41 0.17], 'LineWidth',3)
text (265, 0.5, 'Senescence', 'color', [ 0.91 0.41 0.17], 'FontSize', 18)

p3 = plot(xdata,ydata,'ko','LineWidth',0.5, 'MarkerSize',8)
p3.MarkerFaceColor = 'y';
set(gca,'FontSize',12)
xlabel 'Day of Year (2018)'
ylabel 'Green Chromatic Coordinate (GCC)'
%ylabel 'Excess Green Index (ExG)'
% ylabel 'Normalized Difference of Green & Red (VIgreen)'
grid on

%Compute first and second order derivative
dy = gradient(glist, xdata);
dyy = gradient(dy, xdata);

%Compute the curvature
k = abs(dyy) ./ (1 + dy.^2).^1.5;

%Normalize the data to appear between 0 an 1
rescaled = (k - min(k))./(max(k)-min(k));

%Also plot the curvature
%plot(xdata, rescaled)

%Find local minima and maxima and plot it
minima = islocalmin(rescaled);
maxima = islocalmax(rescaled);

%Find the first two maxima
result = mink(find(maxima==1), 4);
mid = mink(find(minima==1), 2);

%Plot the vertical line through the two maxima
y = ylim; % Set current y-axis limits

p4 = plot([xdata(result(1)) xdata(result(1))],[y(1) y(2)], 'color', [0 0.5 0], 'LineWidth',1.5)
p5 = plot(xdata(result(1)), glist(result(1)), 'bo')
p6 = plot([xdata(result(2)) xdata(result(2))],[y(1) y(2)], 'color', [0 0.5 0],'linestyle','--', 'LineWidth',1.5)
p7 = plot(xdata(result(2)), glist(result(2)), 'bo')
p8 = plot([xdata(result(3)) xdata(result(3))],[y(1) y(2)], '--r', 'LineWidth',1.5)
p9 = plot(xdata(result(3)), glist(result(3)), 'bo')
%The variables p10 and p11 might be different for other data except the one
%used for this case.
p10 = plot([xdata(36) xdata(36)],[y(1) y(2)], 'r-', 'LineWidth',1.5)
p11 = plot(xdata(36), glist(36), 'bo')

p12 = plot([xdata(mid(1)) xdata(mid(1))],[y(1) y(2)], 'color', [0 0.5 0],'linestyle', '-.', 'LineWidth',1.5)
p13 = plot(xdata(mid(1)), glist(mid(1)), 'bo')
p14 = plot([xdata(mid(2)) xdata(mid(2))],[y(1) y(2)], '-.r', 'LineWidth',1.5)
p15 = plot(xdata(mid(2)), glist(mid(2)), 'bo')

hlegend1 = legend([p3, p4, p6, p8, p10, p12, p14], {'Original GCC', 'Start of Season (SOS)',... 
    'End of Season (EOS)', 'End of Fall (EOF)', 'Start of Fall (SOF)', 'Middle of Season (MOS)',...
    'Middle of Fall (MOF)'}, 'FontSize', 12, 'Location','NorthEast');
