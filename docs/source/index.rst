
Welcome to DryVR's user manual!
==================================
:Release: 0.1
:Date: 04/18/2017


DryVR is a framework for verifying cyber-physical systems. It specifically handles systems that are described by a combination of a :ref:`black-box-label` for trajectories and a white-box :ref:`transition-graph-label` specifying mode switches. The framework uses a probabilistic algorithm for learning sensitivity of the continuous trajectories from simulation data and includes a bounded reachability analysis algorithm that uses the learned sensitivity.

.. toctree::
   :maxdepth: 2

   status
   installtion
   usage
   dryvr's_language
   example
   publications
   people
   contact
   

.. raw:: html

    <script type="text/javascript">
    if (String(window.location).indexOf("readthedocs") !== -1) {
        window.alert('The documentation has moved. I will redirect you to the new location.');
        window.location.replace('https://dryvrtool.readthedocs.io/en/latest/');
    }
    </script>
