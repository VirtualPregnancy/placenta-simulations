=================================
Example 1 - Allerkamp et al. 2023
=================================

This example is found in the directory placenta-simulations/uterus/allerkamp2023

The example requires that you have the `placentagen <https://github.com/VirtualPregnancy/placentagen>`_. libraries installed on your machine.
These libraries can be installed with a simple *pip* command that links to the Github repository, and more detailed instructions can be found at the library home.

Further python requirements (installable by pip are)

   - numpy
   - matplotlib
   - os


To run the code navigate to placenta-simulations/uterus/allerkamp2023

Then simply run the python scripts in this folder to generate the figure of interest in the paper (the modelling results are replicated here, you will need to replace {X} with the figure you want)

.. code-block:: console

    python allerkamp2023_Fig{X}.py
	
	
The code will create an *output* directory and save figures to that directory, you can modify this output directory if you want to save results in different configurations.
Any directory name starting with *output* is ignored by github on this repository.

To create a uterine geometry you need to define the generations of vessels present in the uterus, including the number of vessels in a generation, a radius value for that generation
and a length value for that generation.

For example:

.. code-block::

        vessels = np.array([(1, 1, 1.4, 100.0, 'Uterine'),
                        (2, 2, 0.403, 9.0, 'Arcuate'),
                        (3, 50, 0.257, 6.0, 'Radial'),
                        (4, 50, 0.1, 6.5, 'Anastomose'),
                        (5, 50, 0.3, 7, 'Spiral_tube'),
                        (6, 50, 0.241, 3, 'Spiral_channel')],
                       dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                              ('vessel_type', 'U15')])

defines 6 generations of arterial segments comprising 1 uterine artery (radius, 1.4 mm, length 100 mm), 2 arcuate arteries (radius 0.043 mm, length 9.0 mm), and so on.

To complete the description of the model, fluid properties, plug properties, and boundary conditions must be defined. The myometrium not feeding the placenta is assumed to have a fixed resistance, as is the intervillous space (IVS).

.. code-block::

    myometrial_resistance = 25.8  # Pa.s/mm3
    IVS_resistance = 1.3  # Pa.s/mm3=
    IVS_num = 1.
    terminals = np.array([IVS_resistance, IVS_num, myometrial_resistance])

Next we define the physical properties of blood:

.. code-block::

    # Blood viscosity (Pa.s)
    mu = 3.4e-3

Then the properties of plugs identified at a given gestation (see Allerkamp et al. in preparation)

.. code-block::

    porosity = 0.164  # porosity of plug or porous medium in channel
    dp = 4.e-2  # mm, particle diameter
    channel_rad = 0.16  # mm inner radius, outer radius defined in vessels


Finally we define boundary conditions (pressure at the uterine artery and total blood flow to the uterus:

.. code-block::

    # Define a mean uterine artery pressure
    StaticPressure = 84. * 133.
    # steady flow component (baseline) in ml/min - will be scaled with resistance
    SteadyFlow = 39.5  # ml/min

Terminal vessel properties are set as an arrays with a defined format:

.. code-block::

    terminals = np.array([IVS_resistance,IVS_num,myometrial_resistance])
    boundary_conds = np.array([('flow',StaticPressure,SteadyFlow)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('inlet_q','f8')])

The model is now defined and can be simulated using the following command in python:

.. code-block::

    [TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)

The output of the simulation is a series of arrays (total resistance = overall resistance, venous resistance = estimated venous contribution to resistance, shear = shear stress at each generation,
resistance = resistance per generation, flow = flow per generation, pressure_out = pressure at the terminal end of each vessel generation). You can then manipulate these arrays and data you have put into
the system to interpret your results. The example scripts show some ways to do this!

