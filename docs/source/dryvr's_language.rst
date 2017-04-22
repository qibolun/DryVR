DryVR's Language
=======================

In DryVR,  hybrid systems are modeled as as a combination of a white-box that specifies the mode switches (:ref:`transition-graph-label`) and a black-box that can  simulate the continuous evolution in each mode (:ref:`black-box-label`). 


.. _black-box-label:

Black-box Simulator
^^^^^^^^^^^^^^^^^^^^^^^^
The black-box simulator for a (deterministic and prefix-closed) set $\TL$
of trajectories labeled by $\L$ is a function (or a program)
$\simulator$ that takes as input a mode label $\ell \in \L$, an
initial state $x_0 \in \TL_{\sf init,\ell}$, and a finite
sequence of time points $t_1, \ldots, t_k$, and returns a sequence of
states $\simulator(x_0,\ell,t_1), \ldots, \simulator(x_0,\ell, t_k)$
such that there exists $\langle\tau,\ell\rangle \in \TL$ with
$\tau.\fstate = x_0$ and for each $i\in \{1,\ldots, k\}$,
$\simulator(x_0,\ell,t_i) = \tau(t_i)$.

.. _transition-graph-label:

Transition Graph
^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: curgraph.png
	:scale: 60%
	:align: right
	:alt: transition graph

	The transition of Automatic Emergency Braking System


A transition graph is a labeled, directed acyclic graph as shown on the right. The vertex labels (red nodes in the graph) specify the modes of the system, and the edge labels specify the transition time from the predecessor node to the successor node. 

The transition graph shown on the right defines an automatic emergency braking system. Car1 is driving ahead of Car2 on a straight lane. Initially both car1 and car2 are in the constand speed mode (Const;Const). Within short amount of time ([0,0.1]s) Car1 transite into brake mode while Car2 remains in the cuise mode (Brk;Const). After [0.8,0.9]s, Car2 will react by braking as well so both cars are in the brake mode (Brk;Brk).

The transition graph will be generated automatically by DryVR and stored in the tool's root directory as curgraph.png

.. _input-format-label: 

Input Format
^^^^^^^^^^^^^^^^^^^^^^^^^

The input for DryVR should be like ::

	vertex:[transition graph vertex labels (modes)]
	edge:[transition graph edges, (i,j) means there is a directed edge from vertex i to vertex j]
	transtime:[transition graph edge labels (transition times)]
	initialSet:[two arrays defining the lower and upper bound of each variable]
	unsafeSet:@[mode name]:[unsafe region]
	timeHorizon:[Time bound for the verificaiton]
	directory:[Diirectory for your model]

Example input for the Automatic Emergency Braking System ::

	vertex:["Const;Const","Brk;Const","Brk;Brk"]
	edge:[(0,1),(1,2)]
	transtime:[(0,0.1),(0.8,0.9)]
	initialSet:[[0.0,-23.0,0.0,1.0,0.0,-15.0,0.0,1.0],[0.0,-22.8,0.0,1.0,0.0,-15.0,0.0,1.0]]
	unsafeSet:@Allmode:And(v2-v6<3,v6-v2<3)
	timeHorizon:5
	directory:ExamplesPython/


Output Interpretation
^^^^^^^^^^^^^^^^^^^^^^^^^

The tool will print background information like the current mode, transition time, initial set and discrepancy function information on the run. The final result about safe/unsafe will be printed at the bottom.

When the system is safe, the final result will look like ::

	System is Safe!
	System has been refined for * Times
	Simulation safety check is * (seconds)
	Verification safety check is * (seconds)

When the system is unsafe, the final result will look like ::

	Simulation safety check is * (seconds)
	System Unsafe from simulation, halt verification

The unsafe simulation trajectory will be stored as "unsafeSim" in the output folder.
