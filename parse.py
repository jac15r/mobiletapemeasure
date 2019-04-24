import sys
import csv
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from scipy import integrate
import numpy as np
import math

# Imports the data from the specified file
def importData(file):

    with open(file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')

        frame = []
        xacc = []
        yacc = []
        zacc = []

        for row in reader:
            frame.append(float(row[1])/1000)
            xacc.append(float(row[2]))
            yacc.append(float(row[3]))
            zacc.append(float(row[4]))

    return frame,xacc,yacc,zacc

# Falls lfilter on the 3 axes datasets and smooths the graph
# Tested on acceleration data, but could be used on any dataset
def smoothData(xdata,ydata,zdata):

    #smoothing
    n = 15 # Increase this for more smoothing
    b = [1.0 / n] * n
    a = 1

    return lfilter(b,a,xdata), lfilter(b,a,ydata), lfilter(b,a,zdata)

def derive(xdata,ydata,zdata,frame):

    return np.diff(xdata) / np.diff(frame), np.diff(ydata) / np.diff(frame), np.diff(zdata) / np.diff(frame)

def integrate_data(xdata,ydata,zdata,frame):

    return integrate.cumtrapz(xdata,frame, initial=0), integrate.cumtrapz(ydata,frame, initial=0), integrate.cumtrapz(zdata,frame, initial=0)

def plot(frame,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist):

    # plt.plot(frame,xacc,label="X Acceleration")
    # plt.plot(frame,yacc,label="Y Acceleration")
    # plt.plot(frame,zacc,label="Z Acceleration")

    # plt.plot(frame,xvel,label="X Velocity")
    # plt.plot(frame,yvel,label="Y Velocity")
    # plt.plot(frame,zvel,label="Z Velocity")

    plt.plot(frame,xdist,label="X Position")
    plt.plot(frame,ydist,label="Y Position")
    plt.plot(frame,zdist,label="Z Position")

    plt.xlabel('Milliseconds')
    plt.ylabel('Data Values')
    plt.title('Acceleration over time')
    plt.legend()

    plt.show()
    return

# This function removes noise AND gravity
def removeNoise(xacc,yacc,zacc,file,threshold):

    with open(file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')

        xav = 0
        yav = 0
        zav = 0
        total = 0

        for row in reader:
            xav += float(row[2])
            yav += float(row[3])
            zav += float(row[4])
            total = int(row[0])
        # print(total)

    # One of these is gravity   
    xav = xav/total
    yav = yav/total
    zav = zav/total

    # print(xav)
    # print(yav)
    # print(zav)

    # Remove gravity from the correct
    if xav == max(xav,yav,zav):
        # print("X axis is gravity")
        new_average = 0
        for i in range(len(xacc)):
            xacc[i] = xacc[i] - xav
            new_average += xacc[i]
        xav = new_average/len(xacc)
    elif yav == max(xav,yav,zav):
        # print("Y axis is gravity")
        new_average = 0
        for i in range(len(yacc)):
            yacc[i] = yacc[i] - yav
            new_average += yacc[i]
        yav = new_average/len(yacc)
    else:
        # print("Z axis is gravity")
        new_average = 0
        for i in range(len(zacc)):
            zacc[i] = zacc[i] - zav
            new_average += zacc[i]
        zav = new_average/len(zacc)
        # print(zav)

    for i in range(len(xacc)):
        if abs(xacc[i]) < abs(xav*threshold):
            xacc[i] = 0
    for i in range(len(yacc)):
        if abs(yacc[i]) < abs(yav*threshold):
            yacc[i] = 0
    for i in range(len(zacc)):
        if abs(zacc[i]) < abs(zav*threshold):
            zacc[i] = 0

    return xacc,yacc,zacc

def getDistance(file,calibrateFile,threshold=2.75):

    frame,xacc,yacc,zacc = importData(file)

    xacc,yacc,zacc = removeNoise(xacc,yacc,zacc,calibrateFile,threshold)
    xvel,yvel,zvel = integrate_data(xacc,yacc,zacc,frame)
    xdist,ydist,zdist = integrate_data(xvel,yvel,zvel,frame)

    x = xdist[-1]
    y = ydist[-1]    
    z = zdist[-1]

    totaldistance = math.sqrt(x*x + y*y + z*z)
    totaldistance_no_z = math.sqrt(x*x + y*y)

    return totaldistance,totaldistance_no_z

def main():

    # get filename to use
    calibrateFile = sys.argv[1]

    files = []

    for i in range(2,7):
        files.append(sys.argv[i])

    distancesWithZLow = []
    distancesNoZLow = []

    for file in files:
        dist,distNoZ = getDistance(file, calibrateFile, 2.5)
        distancesWithZLow.append(dist)
        distancesNoZLow.append(distNoZ)

    distancesWithZHigh = []
    distancesNoZHigh = []

    for file in files:
        dist,distNoZ = getDistance(file, calibrateFile, 2.75)
        distancesWithZHigh.append(dist)
        distancesNoZHigh.append(distNoZ)

    distancesWithZLowAverage = 0.0
    distancesNoZLowAverage = 0.0
    distancesWithZHighAverage = 0.0
    distancesNoZHighAverage = 0.0

    for i in range(len(files)):
        distancesWithZLowAverage += distancesWithZLow[i]
        distancesNoZLowAverage += distancesNoZLow[i]
        distancesWithZHighAverage += distancesWithZHigh[i]
        distancesNoZHighAverage += distancesNoZHigh[i]

    distancesWithZLowAverage /= len(files)
    distancesNoZLowAverage /= len(files)
    distancesWithZHighAverage /= len(files)
    distancesNoZHighAverage /= len(files)

    LowAverage = (distancesWithZLowAverage + distancesNoZLowAverage) / 2
    HighAverage = (distancesWithZHighAverage + distancesNoZHighAverage) / 2

    OverallAverage = (LowAverage + HighAverage) / 2

    print("\nresults:")
    print("2.5 Threshold Average: %f" % LowAverage)
    print("2.75 Threshold Average: %f" % HighAverage)
    print("Final Calculated Distance: %f" % OverallAverage)

    # file = sys.argv[2]

    # # Create lists of time, x/y/z acceleration values
    # frame,xacc,yacc,zacc = importData(file)

    # # Find the axis affected by gravity, remove the gravity readings
    # xacc,yacc,zacc = removeNoise(xacc,yacc,zacc,calibrateFile)

    # # Smoothed versions of acceleration data. Currently unused, but available 
    # # xacc_smoothed,yacc_smoothed,zacc_smoothed = smoothData(xacc,yacc,zacc)

    # # Integrate the values to get velocity
    # xvel,yvel,zvel = integrate_data(xacc,yacc,zacc,frame)

    # # Integrate the velocity to get distance
    # xdist,ydist,zdist = integrate_data(xvel,yvel,zvel,frame)

    # # Is this close to the correct distance??
    # # xdistsm,ydistsm,zdistsm = smoothData(xdist,ydist,zdist)

    # # total distances
    # x = xdist[-1]
    # y = ydist[-1]    
    # z = zdist[-1]

    # # total distances, smoothed
    # # xsm = xdistsm[-1]
    # # ysm = ydistsm[-1]    
    # # zsm = zdistsm[-1]

    # # Distances, measured differently
    # totaldistance = math.sqrt(x*x + y*y + z*z)
    # totaldistance_no_z = math.sqrt(x*x + y*y)
    # # totaldistancesm = math.sqrt(xsm*xsm + ysm*ysm + zsm*zsm)
    # # totaldistancesm_no_z = math.sqrt(xsm*xsm + ysm*ysm)

    # print("\nresults:")
    # print("X Distance: %f" % x)
    # print("Y Distance: %f" % y)
    # print("Z Distance: %f" % z)
    # print("Total Distance: %f" % totaldistance)
    # print("Total Distance (no Z): %f" % totaldistance_no_z) # This one seems the most accurate!
    # # print("Total Distance, Smoothed: %f" % totaldistancesm)
    # # print("TotalDistance, smoothed (no Z): %f" % totaldistancesm_no_z)

    # # Plotting the data to a graph to view
    # plot(frame,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist)
    return

if __name__ == "__main__":
    main()   