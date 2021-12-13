=======================================
Example 1 - Model from Allerkamp et al.
=======================================

This example is found in the directory placenta-simulations/uterus/allerkamp2022

The example requires that you have the `placentagen <https://github.com/VirtualPregnancy/placentagen>`_. libraries installed on your machine.
These libraries can be installed with a simple *pip* command that links to the Github repository, and more detailed instructions can be found at the library home.

Further python requirements (installable by pip are)

   - numpy
   - matplotlib
   - csv
   - os

The model calls one specific placentagen function which can be called in python file using


.. code-block:: python

    import placentagen as pg

    diameter = pg.diameter_from_pressure(passive_params,myo_params, flow_params, fixed_flow_params, pressure,verbose)

In this call to the :code:`pg.diameter_from_pressure` there are a number of input arrays defining model parameters and a single value output
which is the :code:`diameter` (:math:`\mu` m) at a given :code:`pressure` (kPa). The :code:`verbose` parameter is a logical (True/False), which if true will print any error or warning messages to screen
if a suitable solution cannot be found.

The :code:`passive_params` array contains the parameters that pertain to the passive mechanics of the vessel wall. The structure
of the array is :math:`[D_0,C_{pass},C'_{pass}]`, where we use units of length of :math:`\mu` m. So we define in the following units
:math:`[D_0 (\mu m),C_{pass} (N.m \times 1000),C'_{pass} \text{(no units)}]`.

The :code:`myo_params` array contains all the parameters that relate to myogenic response (with no flow). The structure of the array is
:math:`[C_{act} (N.m \times 1000),C'_{act} \text{(no units)},C''_act \text{(no units)}, C_{myo} (m/N / 1000),C'_{tone} \text{(no units)}]`. The myogenic response can be excluded from the model
by zeroing this array.

The :code:`flow_params` contains the the parameters that relate to the active response of the vessel in the presence of flow. It is limited to parameters that define active
response (i.e. not defining resistance or flow, which are stored in the :code:`fixed_flow_params`). The structure of this array is
:math:`[C_{shear} (1/Pa),C'_{shear} (1/Pa),\tau_1 (Pa),\tau_2 (Pa)]`. The shear response can be excluded from the model by zeroing this array.

The :code:`fixed_flow_params` defines the parameters that define pressure-flow-resistance calculations. The structure of this array is 
:math:`[\mu \text{ (Pa.s)}, \text{vessel length } \mu m, \text{flow or pressure drop}, \text{system resistance}, \text{0 indicates flow and 1 indicates pressure drop} ]`.
If a pressure drop across the vessel is prescribed, it should have units of Pa - if a flow is prescribed this is in units of :math:`m^3`/s.

The provided python file runs this function several times using model parameters fit in the paper by Allerkamp et al. describing uterine radial artery reactivity. This functionality creates several 
of the published figures exactly as per that paper, namely the figures that include model-based results.

To run the code navidate to placenta-simulations/uterus/allerkamp2022

Then simply run the python script in this folder

.. code-block:: console

    python allerkamp2022.py
	
	
The code will create an *output* directory and save figures to that directory.