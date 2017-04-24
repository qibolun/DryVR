DryVR is a software for hybrid system verification. Please find the documentation at 

http://dryvr.readthedocs.io/en/latest/index.html

Quick start
==================
We create a script to evaluate all the examples automatically in the inputFile folder. Please open DryVR folder and run 

./runThis.sh

You should expect ~40 mins to finish all the examples.
-------------------------------------------------------------
To run separate examples in the inputFile folder, please run 

python main.py inputFile/[input_file]

for example:

python main.py inputFile/input_AEB

The examples descriptions can be found in the documentation. Please note that as the verification algorithm uses probabilistic method, the verification result may vary for different runs.
------------------------------------------------------------

To plot the reachtube, please run:

python tubePlotter.py [dimension Number]

for example:

python tubePlotter.py 1

Note that dimension 0 is the local time for each mode and last dimension is the global time. 
When the system is Unsafe or Unknown, please do not use the plotter. Otherwise, it will break or plot the result for the last example.









