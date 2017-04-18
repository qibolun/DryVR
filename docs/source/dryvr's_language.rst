DryVR's Language
=======================

Transition Graph
^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: curgraph.png
	:scale: 50%
	:align: right

sadwadadssa

Input Interpretation
^^^^^^^^^^^^^^^^^^^^^^^^^

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
