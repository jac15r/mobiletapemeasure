# Mobile Tape Measure

A proof-of-concept attempt to use a phone's accelerometer to measure distance.

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

* Improve accuracy of readings
* Analyze data more
* Improve capabilities beyond 2 meters

## Current Status

Accuracy between 1 and 2 meters (averaged):

* with `average * 2.5` filter and Z, 110% the distance
* with `average * 2.5` filter and no Z, roughly 100-110% distance
* Average of these values roughly 110%
* with `average * 2.75` filter and Z, between 92-107% distance
* with `average * 2.75` and no Z, between 88-107% distance
* Average of these values roughly 107%

These two total averages weighted equally and re-averaged gives us:

* Near exact measurements for 1 meter, 109% measurements for 2 meters.