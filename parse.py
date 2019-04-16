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
def removeNoise(xacc,yacc,zacc,file):

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

    print(xav)
    print(yav)
    print(zav)

    # Remove gravity from the correct
    if xav == max(xav,yav,zav):
        print("X axis is gravity")
        new_average = 0
        for i in range(len(xacc)):
            xacc[i] = xacc[i] - xav
            new_average += xacc[i]
        xav = new_average/len(xacc)
    elif yav == max(xav,yav,zav):
        print("Y axis is gravity")
        new_average = 0
        for i in range(len(yacc)):
            yacc[i] = yacc[i] - yav
            new_average += yacc[i]
        yav = new_average/len(yacc)
    else:
        print("Z axis is gravity")
        new_average = 0
        for i in range(len(zacc)):
            zacc[i] = zacc[i] - zav
            new_average += zacc[i]
        zav = new_average/len(zacc)
        print(zav)

    for i in range(len(xacc)):
        if xacc[i] < abs(xav):
            xacc[i] = 0
    for i in range(len(yacc)):
        if yacc[i] < abs(yav):
            yacc[i] = 0
    for i in range(len(zacc)):
        if zacc[i] < abs(zav):
            zacc[i] = 0

    return xacc,yacc,zacc

#Removing gravity without reading from the file again.
""" Edit - removed due to problem: This only works if
    average movement acceleration is less than gravity.
    This should be the case, but can't be ensured.
    Because of which, we HAVE to use the calibration
    data involving the phone staying still.

    Update: RemoveNoise now removes gravity as well
    as noise. Separate functions are no longer needed.
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
"""

def main():

    # get filename to use
    calibrateFile = sys.argv[1]
    file = sys.argv[2]

    # Create lists of time, x/y/z acceleration values
    frame,xacc,yacc,zacc = importData(file)

    # Find the axis affected by gravity, remove the gravity readings
    #xacc,yacc,zacc = removeGravity(xacc,yacc,zacc,calibrateFile)

    # Find the axis affected by gravity, remove the gravity readings
    # Update: This removes gravity AND noise now!
    xacc,yacc,zacc = removeNoise(xacc,yacc,zacc,calibrateFile)

    #Find noise values, set the noise values to zero
    # xacc,yacc,zacc = ignoreNoise(xacc, yacc, zacc, calibrateFile)

    # Smoothed versions of acceleration data. Currently unused, but available 
    # xacc_smoothed,yacc_smoothed,zacc_smoothed = smoothData(xacc,yacc,zacc)

    # Integrate the values to get velocity
    xvel,yvel,zvel = integrate_data(xacc,yacc,zacc,frame)

    # Integrate the velocity to get distance
    xdist,ydist,zdist = integrate_data(xvel,yvel,zvel,frame)

    # Is this close to the correct distance??
    xdistsm,ydistsm,zdistsm = smoothData(xdist,ydist,zdist)

    # total distances
    x = xdist[-1]
    y = ydist[-1]    
    z = zdist[-1]

    # total distances, smoothed
    xsm = xdistsm[-1]
    ysm = ydistsm[-1]    
    zsm = zdistsm[-1]

    # Distances, measured differently
    totaldistance = math.sqrt(x*x + y*y + z*z)
    totaldistance_no_z = math.sqrt(x*x + y*y)
    totaldistancesm = math.sqrt(xsm*xsm + ysm*ysm + zsm*zsm)
    totaldistancesm_no_z = math.sqrt(xsm*xsm + ysm*ysm)

    print("\nresults:")
    print("Total Distance: %f" % totaldistance)
    print("Total Distance (no Z): %f" % totaldistance_no_z) # This one seems the most accurate!
    print("Total Distance, Smoothed: %f" % totaldistancesm)
    print("TotalDistance, smoothed (no Z): %f" % totaldistancesm_no_z)

    # Plotting the data to a graph to view
    plot(frame,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist)
    return

if __name__ == "__main__":
    main()   