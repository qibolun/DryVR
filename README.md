DryVR software of hybrid system verification. This software is currently provided for evaluation  only with limited technical support. For details, contact the authors of the accompanying paper:

DRYVR:Data-driven verification and compositional reasoning for automotive systems {cfan10,bolunqi2,mitras,vmahesh}@illinois.edu

Status
======
March 23. The tool is being tested on Ubuntu 16 (64 bit version). We will update this note when it is ready.

Installation
============
To install the required packages, please run:

sudo ./installRequirement

To install packages indepently, the following will be required:

python 2.7

Numpy

Scipy

Sympy

Matplotlib

python Igraph

python Z3

glpk(4.39 or ealier eversion)

pyglpk

python-cairo

python tk

gmpc

We recommend to install this software on a clean installed Ubuntu 16.04.

Run
===

python main.py inputFile/[input_file]

for example:

python main.py inputFile/input_carovertake

Plotter
===
After you run the our tool, a reachTube.txt file will be generated in output folder unless the model is determined unsafe during simulation test.

To plot the reachtube, please run:

python tubePlotter.py [dimension Number]

for example:

python tubePlotter.py 1

Note that the dimension 0 is local time and last dimension is global time

Result interpretation 
===
The tool will print background information like the current mode, transition time, initial set and discrepancy function information on the run. The final result will be printed at the last:

When the system is safe, the final result will look like

System is Safe!

System has been refined for * Times

Simulation safety check is * (seconds)

Verification safety check is * (seconds)

When the system is unsafe, the final result will look like

Simulation safety check is * (seconds)

System Unsafe from simulation, halt verification

The unsafe simulation trajectory will be stored as "unsafeSim" in the output folder.





