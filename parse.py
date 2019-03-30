import sys
import csv
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np

def main():

    file = sys.argv[0]

    with open(file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')

        frame = []
        xval = []
        yval = []
        zval = []

        for row in reader:
            frame.append(float(row[0]))
            xval.append(float(row[2]))
            yval.append(float(row[3]))
            zval.append(float(row[4]))
        
    n = 15 # Increase this for more smoothing
    b = [1.0 / n] * n
    a = 1

    xval_smoothed = lfilter(b,a,xval)
    yval_smoothed = lfilter(b,a,yval)
    zval_smoothed = lfilter(b,a,zval)

    xvel = np.diff(xval) / np.diff(frame)
    yvel = np.diff(yval) / np.diff(frame)
    zvel = np.diff(zval) / np.diff(frame)
    frameprime = (np.array(frame)[:-1] + np.array(frame)[1:]) / 2

    xdist = np.diff(xvel) / np.diff(frameprime)
    ydist = np.diff(xvel) / np.diff(frameprime)
    zdist = np.diff(zvel) / np.diff(frameprime)
    frameprimeprime = (np.array(frameprime)[:-1] + np.array(frameprime)[1:]) / 2

    plt.plot(frame,xval,label="X Acceleration")
    plt.plot(frame,yval,label="Y Acceleration")
    plt.plot(frame,zval,label="Z Acceleration")

    # plt.plot(frame,xval_smoothed,label="X Acceleration Smoothed")
    # plt.plot(frame,yval_smoothed,label="Y Acceleration Smoothed")
    # plt.plot(frame,zval_smoothed,label="Z Acceleration Smoothed")

    plt.plot(frameprime,xvel,label="X Velocity")
    plt.plot(frameprime,yvel,label="Y Velocity")
    plt.plot(frameprime,zvel,label="Z Velocity")

    plt.plot(frameprimeprime,xdist,label="X Position")
    plt.plot(frameprimeprime,ydist,label="Y Position")
    plt.plot(frameprimeprime,zdist,label='Z Position')

    plt.xlabel('Time (1/40 sec)')
    plt.ylabel('Acceleration Values')
    plt.title('Acceleration over time')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()   