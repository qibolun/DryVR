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

To plot the reachtube, please run in the DryVR root directory: ::

	python tubePlotter.py [dimension Number]

Where [dimension number] is the dimension you want to plot reachtube. Note that the dimension 0 is the local time for each mode and last dimension is the global time. 

For example, input_AEB's has 8 dimentions: :math:`sx_1,sy_1,vx_1,vy_1,sx_2,sy_2,vx_2,vy_2` (refer to :ref:`ADAS-label` for more details).
You can choose to plot dimension from 0 to 9. Dimension 0 is the local time for each mode and dimension 9 is the global time. Dimension 1~8 corresponds to the state variables as above. 

For example, to plot the reachtube for :math:`sx_1`, please run ::

	python tubePlotter.py 1



**Note** please do not use the tubePlotter function when system is checked to be Unsafe or Unknown (when no more refinement can be used). 

When system is checked to be **Unsafe**, the counter-example simulation trace is stored in the output folder as **unsafeSim**.

More plot results can be found at the :ref:`example-label` page.
