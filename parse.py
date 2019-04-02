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

        #Manipulate this to remove noisy data, perhaps?
        cutoff = -1000
        for row in reader:
            frame.append(float(row[0])/410)
            if float(row[2]) < cutoff:
                xacc.append(0.0)
            else:
                xacc.append(float(row[2]))
            if float(row[3]) < cutoff:
                yacc.append(0.0)
            else:
                yacc.append(float(row[3]))
            if float(row[4]) < cutoff:
                zacc.append(0.0)
            else:
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
    # plt.plot(frame,zacc,label="Z Acceleration")

    plt.plot(frame,xvel,label="X Velocity")
    plt.plot(frame,yvel,label="Y Velocity")
    # plt.plot(frame,zvel,label="Z Velocity")

    plt.plot(frame,xdist,label="X Position")
    plt.plot(frame,ydist,label="Y Position")
    # plt.plot(frame,zdist,label="Z Position")

    plt.xlabel('Time (1/40 sec)')
    plt.ylabel('Acceleration Values')
    plt.title('Acceleration over time')
    plt.legend()

    plt.show()
    return

def main():

    # get filename to use
    file = sys.argv[1]

    # Create lists of time, x/y/z acceleration values
    frame,xacc,yacc,zacc = importData(file)

    # Smoothed versions of acceleration data. Currently unused, but available 
    xacc_smoothed,yacc_smoothed,zacc_smoothed = smoothData(xacc,yacc,zacc)

    # Integrate the values to get velocity
    xvel,yvel,zvel = integrate_data(xacc_smoothed,yacc_smoothed,zacc_smoothed,frame)

    # Integrate the velocity to get distance
    xdist,ydist,zdist = integrate_data(xvel,yvel,zvel,frame)

    # Plotting the data to a graph to view
    plot(frame,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist)
    return

if __name__ == "__main__":
    main()   