=========================================================
Example 1 - Model from Clark et al. Interface Focus, 2015
=========================================================

This example is found in the directory placenta-simulations/fetoplacental/interface2015

The example requires that you have the repsrosim libraries installed on your machine.

If you work in virtual environments, activate a virtual environment in which reprosim is installed and execute the following:

.. code-block:: console

    python bloodflow_interface2015.py
	
	
This executes the file that runs the example (bloodflow_interface2015.py). If you open this file you'll see that the code has a requirement

.. code-block:: python 

	import os

These are packages you should have installed on your computer. The os package often comes with your python install, but if not can be installed using pip. The next lines of code tell you which parts of the reprosim libraries we are going to use:

.. code-block:: python

	from reprosim.diagnostics import set_diagnostics_level
	from reprosim.indices import perfusion_indices, get_ne_radius
	from reprosim.geometry import append_units,define_node_geometry, define_1d_element_placenta,define_rad_from_geom,add_matching_mesh, \
        calc_capillary_unit_length
	from reprosim.exports import export_1d_elem_geometry, export_node_geometry, export_1d_elem_field,export_node_field,export_terminal_perfusion
	from reprosim.pressure_resistance_flow import evaluate_prq, calculate_stats
	
The main portion of the code comes next. Within reprosim, we can chose how much diagnostic information we want to print to screen as we run the code. Thre are three levels of diagnostics (level 0 - no diagnostics; level 1 - only prints subroutine names (default); level 2 - prints subroutine names and contents of variables). To set this level we simply use:

.. code-block:: python

	set_diagnostics_level(0)
	
The next lines of code are here to allow you to define the directory you want to export results to, they define the directory name, and if it doesnt exist on your system creates the directory.

.. code-block:: python

    export_directory = 'output'
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
	
We then set up the perfusion model - this part of the code simply tells the solver we are looking at a perfusion simulation and allows it to determine how much memory is needed to do this:

.. code-block:: python

	    perfusion_indices()
		
Next we set up the geometry that we are going to solve the model in. This involves reading in, or generating a tree-like structure. In this example we read in a geometry from the 'sample_geometry' directory:

.. code-block:: python

    define_node_geometry('sample_geometry/FullTree.ipnode')
    define_1d_element_placenta('sample_geometry/FullTree.ipelem')
	append_units()

Here, nodes are the location of the start and end points of branches in our geometry and elements define the centrelines of these branches. The append_units command tells the code where our capillary bed sits within our geometry.

In many cases we have a really good description of what our arteral geometry looks like, but we need to make some assumptions about what the veins look like. In this case we simply copy the arteries:

.. code-block:: python

    umbilical_elem_option = 'same_as_arterial'
    umbilical_elements = []
    add_matching_mesh(umbilical_elem_option,umbilical_elements)
	
We now have a mesh that includes arteries, capillaries and veins, and we have to define the size of these vessels. We do this using Strahler ordering systems:

.. code-block:: python 

    # define radius by Strahler order in diverging (arterial mesh)
    s_ratio = 1.38  # rate of decrease in radius at each order of the arterial tree  1.38
    inlet_rad = 1.8  # inlet radius
    order_system = 'strahler'
    order_options = 'arterial'
    name = 'inlet'
    define_rad_from_geom(order_system, s_ratio, name, inlet_rad, order_options, '')
    #defines radius by STrahler order in converging (venous mesh)
    s_ratio_ven= 1.46 #rate of decrease in radius at each order of the venous tree 1.46
    inlet_rad_ven=4.0 #inlet radius
    order_system = 'strahler'
    order_options = 'venous'
    first_ven_no='' #number of elements read in plus one
    last_ven_no='' #2x the original number of elements + number of connections
    define_rad_from_geom(order_system, s_ratio_ven, first_ven_no, inlet_rad_ven, order_options,last_ven_no)
    
    num_convolutes = 6  # number of terminal convolute connections
    num_generations = 3  # number of generations of symmetric intermediate villous trees
    calc_capillary_unit_length(num_convolutes,num_generations)
	
We then define boundary conditions, we can specify pressure at the inlet and outlet of the system, or flow at the inlet and pressure at the outlet. The choice depends on whether you know one or the other of blood pressure or flow, or whether your model assumptions rely on one or the other being fixed:

.. code-block:: python

    #Call solve
    bc_type = 'pressure' # 'pressure' or 'flow'
    if  bc_type == 'pressure':
        inlet_pressure = 6650 #Pa (~50mmHg)
        outlet_pressure = 2660 #Pa (~20mmHg)
        inlet_flow = 0 #set to 0 for bc_type = pressure;
    
    if  bc_type == 'flow':
        inlet_pressure = 0
        outlet_pressure = 2660
        inlet_flow = 111666.7 # mm3/s
 
 Finally, we solve the model (bringing in information about the mesh and the boundary conditions):
 
.. code-block:: python 
 
 	evaluate_prq(mesh_type,bc_type,inlet_flow,inlet_pressure,outlet_pressure)
	
The remainder of the code exports relavent information to be analysed or visualised (either on screen or in CMGUI) -
an example visualisation file is given in the expected-results folder.
.. `Next step: Two umbilical arteries <byrne2020.html>`_.