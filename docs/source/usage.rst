Usage
===================

Run DryVR
^^^^^^^^^^^^^^^

To run DryVR, please run: ::

	python main.py inputFile/[input_file]

for example: ::

	python main.py inputFile/input_AEB


Plotter
^^^^^^^^^^^^^^^

After you run the our tool, a reachTube.txt file will be generated in output folder unless the model is determined unsafe during simulation test.

To plot the reachtube, please run: ::

	python tubePlotter.py [dimension Number]

for example: ::

	python tubePlotter.py 1

Note that the dimension 0 is local time and last dimension is global time

More plot results can be found at the :ref:`example-label` page.