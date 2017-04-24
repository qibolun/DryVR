DryVR is a software for hybrid system verification. Please find the documentation at 

http://dryvr.readthedocs.io/en/latest/index.html

Quick start
==================
We create a script to evaluate all the examples automatically in the inputFile folder. Please open DryVR folder and run 

./runThis

-------------------------------------------------------------
To run separate examples in the inputFile folder, please run 

python main.py inputFile/[input_file]

for example:

python main.py inputFile/input_AEB

The examples descriptions can be found in the online (and Html) documentation
------------------------------------------------------------
To plot the reachtube, please run:

python tubePlotter.py [dimension Number]

for example:

python tubePlotter.py 1

Note that the dimension 0 is local time and last dimension is global time










