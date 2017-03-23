DryVR software of hybrid system verification. This software is currently provided for evaluation  only with limited technical support. For details, contact the authors of the accompanying paper:
DRYVR:Data-driven verification and compositional reasoning for automotive systems
{cfan10,bolunqi2,mitras,vmahesh}@illinois.edu

March 23. The tool is being tested on Ubuntu 16 (64 bit version). We will update this note when it is ready.

Installation
============
To install the required packages, please run:

sudo ./installRequirement

To install packages indepently, the following will be required:

python 2.*
python igraph
Z3
glpk for python

Run
===

python main.py inputFile/[input_file]

for example:

python main.py inputFile/input_carovertake





