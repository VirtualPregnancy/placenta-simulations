=======================================
Example 1 - Model from Allerkamp et al.
=======================================

This example is found in the directory placenta-simulations/uterus/allerkamp2022

The example requires that you have the `placentagen <https://github.com/VirtualPregnancy/placentagen>`_. libraries installed on your machine.
These libraries can be installed with a simple *pip* command that links to the Github repository, and more detailed instructions can be found at the library home.

The model calls one specific placentagen function which can be called in python file using


.. code-block:: console

    import placentagen as pg

    diameter = pg.diameter_from_pressure(passive_params,myo_params, flow_params, fixed_flow_params, pressure,verbose)

In this call to the :code:`pg.diameter_from_pressure` there are a number of input arrays defining model parameters and a single value output
which is the :code:`diameter` (:math:`\mu` m) at a given :code:`pressure` (kPa).

The :code:`passive_params` array contains the parameters that pertain to the passive mechanics of the vessel wall. The structure
of the array is :math:`[D_0,C_{pass},C'_{pass}]`, where we use units of length of :math:`\mu` m. So we define in the following units
:math:`[D_0 (\mu m),C_{pass} (N.m \times 1000),C'_{pass} \text{(no units)}]`.

The :code:`myo_params` array contains all the parameters that relate to myogenic response (with no flow).

