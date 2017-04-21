DryVR's Language
=======================

The Autonomous Vehicle Benchmark
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Due to the MATLAB license issue, we are not able to release the Simulink benchmarks we have used in the publications. We have since reproduced the ADAS and autonomous vehicle benchmark in Python and connect it with DryVR as a simulator. We are hoping to move more examples to Python in the near future.

The hybrid system for a scenario is constructed by putting together several individual vehicles. The higher-level decisions (paths) followed by the vehicles are captured by the transition graphs discussed in the next session.

Each vehicle has the following modes

- cruise: move forward at constant speed, 
- speedup: constant acceleration,
- brake: constant (slow) deceleration,
- em\_brake: constant (hard) deceleration.
- ch\_left and ch\_right:  the acceleration and steering are controlled in such a manner that the vehicle switches to its left (resp. right) lane in a certain amount of time. 

The mode for the entire system consists of n vehicles are the mode of each vehicle separated by semicolon. For example, cruise;ch\_left means the first car is in the cuise mode, while the second car is in the ch\_left mode.
For each vehicle, we mainly analyze four variables: absolute position
($sx$) and velocity ($vx$) orthogonal to the road direction
($x$-axis), and absolute position ($sy$) and velocity ($vy$) along the
road direction ($y$-axis). The throttle and steering is captured using
the four variables. 

For more details, please refer to Section 2.5 of the accompanying paper.



Transition Graph
^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure:: curgraph.jpg
	:scale: 60%
	:align: right
	:alt: transition graph

	The transition of Automatic Emergency Braking System


A transition graph is a labeled, directed acyclic graph as shown on the right. The vertex labels (red nodes in the graph) specify the modes of the system, and the edge labels specify the transition time from the predecessor node to the successor node. 

The transition graph shown on the right defines an automatic emergency braking system. Car1 is driving ahead of Car2 on a straight lane. Initially both car1 and car2 are in the cruise mode (Const;Const). Within short amount of time ([0,0.1]s) Car1 transite into brake mode while Car2 remains in the cuise mode (Brake;Const). After [0.8,0.9]s, Car2 will react by braking as well (Brake;Brake).

The transition graph will be generated automatically by DryVR and stored in the tool's root directory as curgraph.png

Input Format
^^^^^^^^^^^^^^^^^^^^^^^^^

The input for DryVR should be like ::

	vertex:[transition graph vertex labels (modes)]
	edge:[transition graph edges, (i,j) means there is a directed edge from vertex i to vertex j]
	transtime:[transition graph edge labels (transition times)]
	initialSet:[two arrays defining the lower and upper bound of each variable]
	unsafeSet:@[mode name]:[unsafe region]
	timeHorizon:[Time bound for the verificaiton]

Example input for the Automatic Emergency Braking System ::

	vertex:['Const;Const', 'Brake;Const', 'Brake;Brake']
	edge:[(0, 1), (1, 2)]
	transtime:[(0, 0.1), (0.1, 0.2)]
	initialSet:[[-10.0, 30.0, 33.0, -10.0, 30.0, 0.0], [-10.0, 31.0, 33.1, -10.0, 31.0, 0.0]]
	unsafeSet:@Allmode:And(v3-v6<0.02,v6-v3<0.02)
	timeHorizon:40

Output Interpretation
^^^^^^^^^^^^^^^^^^^^^^^^^

The tool will print background information like the current mode, transition time, initial set and discrepancy function information on the run. The final result will be printed at the last:

When the system is safe, the final result will look like ::

	System is Safe!
	System has been refined for * Times
	Simulation safety check is * (seconds)
	Verification safety check is * (seconds)

When the system is unsafe, the final result will look like ::

	Simulation safety check is * (seconds)
	System Unsafe from simulation, halt verification

The unsafe simulation trajectory will be stored as "unsafeSim" in the output folder.
