# Mobile Tape Measure

A proof-of-concept attempt to use a phone's accelerometer

## Requirements

* Install python, pip
* Make sure both are in your system's PATH variable
* From a command-line, run:
    1. `pip install matplotlib`
    1. `pip install scipy`
    1. `pip install numpy`
    1. `pip install py-qt5agg`

## How to run

From a command-line,

`python parse.py [calibrateFile(try 'calibrate.tsv')] [filename]`

## Things that need to be done

Integration has been coded, but the readings are way too high for distance.

We need to look into ways of cleaning up acceleration readings. Perhaps a cutoff value to get rid of noise? Maybe **Kalman filtering**?

## Changes did

Added 'removenoise' function for filtering out noise.
Added 'removeGravity2' function that doesn't need to read from file again. Might be helpful in speeding up.

## What has been done

Using this information [here](https://stackoverflow.com/questions/17602076/how-do-i-integrate-two-1-d-data-arrays-in-python), we implemented a method of using the trapezoidal method of integration to get velocity and distance.