import sys
import csv
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from scipy import integrate
import numpy as np

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

    plt.plot(frame,xacc,label="X Acceleration")
    plt.plot(frame,yacc,label="Y Acceleration")
    plt.plot(frame,zacc,label="Z Acceleration")

    # plt.plot(frame,xvel,label="X Velocity")
    # plt.plot(frame,yvel,label="Y Velocity")
    # plt.plot(frame,zvel,label="Z Velocity")

    # plt.plot(frame,xdist,label="X Position")
    # plt.plot(frame,ydist,label="Y Position")
    # plt.plot(frame,zdist,label="Z Position")

    plt.xlabel('Time (1/40 sec)')
    plt.ylabel('Acceleration Values')
    plt.title('Acceleration over time')
    plt.legend()

    plt.show()
    return

"""def removeGravity(xacc,yacc,zacc,file):

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
        print(total)

    # One of these is gravity   
    xav = xav/total
    yav = yav/total
    zav = zav/total

    # Remove gravity from the correct
    if xav == max(xav,yav,zav):
        print("X axis is gravity")
        for i in range(len(xacc)):
            xacc[i] = xacc[i] - xav
    elif yav == max(xav,yav,zav):
        print("Y axis is gravity")
        for i in range(len(yacc)):
            yacc[i] = yacc[i] - yav
    else:
        print("Z axis is gravity")
        for i in range(len(zacc)):
            zacc[i] = zacc[i] - zav

    return xacc,yacc,zacc """

#Removing gravity without reading from the file again.
def removeGravity2(xacc,yacc,zacc):

    total = len(xacc)
    xavg = 0
    yavg = 0
    zavg = 0

    i = 0
    while i < total:
        xavg += xacc[i]
        yavg += yacc[i]
        zavg += zacc[i]
        i += 1

    xavg = xavg/total
    yavg = yavg/total
    zavg = zavg/total

    if xavg == max(xavg,yavg,zavg):
        print("X axis is gravity")
        for i in range(len(xacc)):
            xacc[i] = xacc[i] - xavg
    elif yavg == max(xavg,yavg,zavg):
        print("Y axis is gravity")
        for i in range(len(yacc)):
            yacc[i] = yacc[i] - yavg
    else:
        print("Z axis is gravity")
        for i in range(len(zacc)):
            zacc[i] = zacc[i] - zavg
    
    return xacc,yacc,zacc

def ignoreNoise(xacc, yacc, zacc, file):

    total = len(xacc)
    i = 0
    while i < total:
        if(xacc[i] <= 3 and xacc[i] >= -3):
            xacc[i] = 0
        if(yacc[i] <= 3 and yacc[i] >= -3):
            yacc[i] = 0
        if(zacc[i] <= 3 and zacc[i] >= -3):
            zacc[i] = 0
        i += 1
    
    return xacc,yacc,zacc

def main():

    # get filename to use
    calibrateFile = sys.argv[1]
    file = sys.argv[2]

    # Create lists of time, x/y/z acceleration values
    frame,xacc,yacc,zacc = importData(file)

    # Find the axis affected by gravity, remove the gravity readings
    #xacc,yacc,zacc = removeGravity(xacc,yacc,zacc,calibrateFile)

    # Find the axis affected by gravity, remove the gravity readings
    xacc,yacc,zacc = removeGravity2(xacc,yacc,zacc)

    #Find noise values, set the noise values to zero
    xacc,yacc,zacc = ignoreNoise(xacc, yacc, zacc, file)

    # Smoothed versions of acceleration data. Currently unused, but available 
    # xacc_smoothed,yacc_smoothed,zacc_smoothed = smoothData(xacc,yacc,zacc)

    # Integrate the values to get velocity
    xvel,yvel,zvel = integrate_data(xacc,yacc,zacc,frame)

    # Integrate the velocity to get distance
    xdist,ydist,zdist = integrate_data(xvel,yvel,zvel,frame)

    # Plotting the data to a graph to view
    plot(frame,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist)
    return

if __name__ == "__main__":
    main()   