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

`python parse.py [calibrateFile] [filenames (Recommended: 5 separate measurements)]`

## Current Status

With measurements taken within 5-6 seconds, can yield measurement results approximately between 92% and 99% accuracy

Anything with long distances or time measured will yield poor results, due to both human hand movement and sensitive accelerometers.