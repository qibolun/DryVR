Create New Model
==============================

This is step by step guidence for creating new model and upruning with DryVR

Create a folder in DryVR root directory for your new model and enter it. ::
	
	mkdir Thermostats
	cd Thermostats

Inside your model folder, create a python script for your model. ::
	
	vim Thermostats_ODE.py

Create a function 'TC_Simulate'. This function will be used by DryVR to generate simulation trace. In example, we use odeint simulator from Scipy, but you can have any kind of simulators as long as you create this function that takes input from DryVR and return trace back to DryVR. ::
	
	TC_Simulate(Mode,initialCondition,time_bound)
	Input:
		Mode (string) -- a string indicates the model you want to simulate. Ex. "On"
		initialCondition (list of float) -- a list contains the initial condition. Ex. "[32.0]"
		time_bound (float) -- a float indicates the time horizon for simulation. EX. '10.0'
	Output:
		Trace (list of list of float) -- a list of list contains the trace from simulation. 
		Each indices represents the simulation for certain time step.Represents as [time, v1, v2, ........]. 
		Ex. "[[0.0,32.0],[0.1,32.1],[0.2,32.2]........[10.0,34.3]]"

Inside your model folder, create a python initiate script. ::

	vim __init__.py

Then import file with function 'TC_Simulate'. ::
	
	from Thermostats_ODE import *

Go to input file folder and create input file for your new model. The input file format is discussed in :ref:`_input-format-label`. ::

	vertex:["On","Off","On"]
	edge:[(0,1),(1,2)]
	transtime:[(1,1.1),(1,1.1)]
	initialSet:[[75.0],[76.0]]
	unsafeSet:@Allmode:And(v1>90)
	timeHorizon:3.5
	directory:Thermostats/


Finally, you can use your new model via following command. ::

	python main.py inputFile/input_thermo 
