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

`python parse.py [filename]`

## Things that need to be done

The script is incorrectly deriving instead of integrating.

This means that its "velocity" is actually "jerk" (m/s^3), and its "acceleration" is actually "snap" (m/s^4)

### Possible Solution

We are already using the scipy library, which has function calls for this. Perhaps the second option listed [here](https://stackoverflow.com/questions/17602076/how-do-i-integrate-two-1-d-data-arrays-in-python)?

