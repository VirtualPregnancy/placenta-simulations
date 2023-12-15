================================================================
Example 2 - Model from Byrne et al. 2020, two umbilical arteries
================================================================

The previous example predicted steady state blood flow in a branching vascular network with one inlet. Mathematically
this is simple, but physiologically the fetoplacental circulation has two inlets (the two umbilical arteries). This
example solves the same model as example 1, but allows for two umbilical arteries with an anastomosis between them.

This example is found in the directory placenta-simulations/fetoplacental/two_umb_arteries

The example requires that you have the repsrosim libraries installed on your machine.

If you work in virtual environments, activate a virtual environment in which reprosim is installed and execute the following:

.. code-block:: console

    python bloodflow_two_umb_arteries.py

The major differences between this example and the previous one are in the definition of the umbilical arteries and
the anastomosis between them. Here you have an option to read in a geometry with or without an anastomosis. You will
see in the sample_geometry directory that there are two .ipelem files, one includes an anastomosis and one does not.
You can chose between these two geometries using the logical 'anastomosis', if this logical is true you need to tell
the code 1) which element your anastomosis is, and 2) its radius. In the code, this looks like this:

.. code-block:: python

     Anastomosis = False
     print('Anastomosis: ' + str(Anastomosis))
     anast_elem = 3
     anast_radius = 1.0

You will see further down the code, that this logical tells the code to read in the appropriate .ipelem file, and
that an optional argument to the define_1d_element_placenta function in reprosim then tells that codebase whether to include
an anastomosis or not.

.. code-block:: python

     if(Anastomosis):
         define_1d_element_placenta('sample_geometry/FullTree.ipelem',anast_elem)
         export_directory = 'output_anast'
     else:
         define_1d_element_placenta('sample_geometry/FullTreeNoAnast.ipelem')
         export_directory = 'output'

The only other major difference now is that you have two inlets, if you copied this geometry as veins you'd then have
two outlets. This is non-physiological, but you can chose to merge the two copied outlets in to a single, more
physiological umbilical vein. You just have to then let the code know which vessels are to be replaced on the venous
side:

.. code-block:: python

     umbilical_elem_option = 'single_umbilical_vein'
     if(Anastomosis):
         umbilical_elements = [1,2,3,4,5]
     else:
         umbilical_elements = [1,2,3,4]


The alternate umbilical_elem_option, which invokes a direct copy is as follows (as per the previous example):

.. code-block:: python

    umbilical_elem_option = 'same_as_arterial'

.. `Next step: Arterial compliance, or fareus lindquist <unknown.html>`_.