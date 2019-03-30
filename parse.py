import sys
import csv
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from scipy.signal import lfilter
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
            frame.append(float(row[0]))
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

def plot(masterData):

    plt.plot(masterData[0],masterData[3],label="X Acceleration")
    plt.plot(masterData[0],masterData[4],label="Y Acceleration")
    plt.plot(masterData[0],masterData[5],label="Z Acceleration")

    plt.plot(masterData[1],masterData[6],label="X Velocity")
    plt.plot(masterData[1],masterData[7],label="Y Velocity")
    plt.plot(masterData[1],masterData[8],label="Z Velocity")

    plt.plot(masterData[2],masterData[9],label="X Position")
    plt.plot(masterData[2],masterData[10],label="Y Position")
    plt.plot(masterData[2],masterData[11],label="Z Position")

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
    # xacc_smoothed,yacc_smoothed,zacc_smoothed = smoothData(xacc,yacc,zacc)

    ''' 
        This is incorrect and needs fixing
        Rather than derive, we should be integrating.
        While I attempted to get velocity, I actually calculated "jerk", or,
        the change in acceleration over time
    '''
    xvel,yvel,zvel = derive(xacc,yacc,zacc,frame)
    frameprime = (np.array(frame)[:-1] + np.array(frame)[1:]) / 2

    ''' This is the same problem as above '''
    xdist,ydist,zdist = derive(xvel,yvel,zvel,frameprime)
    frameprimeprime = (np.array(frameprime)[:-1] + np.array(frameprime)[1:]) / 2

    # Creating a list of the data
    masterData = [frame,frameprime,frameprimeprime,xacc,yacc,zacc,xvel,yvel,zvel,xdist,ydist,zdist]

    # Plotting the data to a graph to view
    plot(masterData)
    return

if __name__ == "__main__":
    main()   