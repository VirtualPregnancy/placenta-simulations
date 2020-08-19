==========
The theory
==========

Publications containing detailed descriptions of the theory employed in this model:

 - `Clark et al. Interface, 2015 <http://rsfs.royalsocietypublishing.org/content/5/2/20140078>`_.
 - `Tawhai et al. Journal of Applied Physiology, 2004 <https://www.physiology.org/doi/abs/10.1152/japplphysiol.00520.2004>`_.
 
Please remember to cite these papers if using our softwares.

.. Publications using these models include:


Publications using previous iterations of these models, implemented in a legacy software (CMISS) include:

 - `Clark et al. Interface, 2015 <http://rsfs.royalsocietypublishing.org/content/5/2/20140078>`_.
 - `Lin et al. Journal of Theoretical Biology, 2016 <https://www.sciencedirect.com/science/article/pii/S0022519316301710>`_.


The basics
==========

With a 'stem' of tree elements (blood vessels identified from images, or defined from population statistics), and a representation  of the volume of our geometry, we can generate a tree structure that fills the volume using what is termed a volume filling branching algorithm (VFBA).

First, the volume is filled with seed points which may be uniformly spaced, randomly spaced with a target seed point density, or even spaced with some prescribed density distribution.

The algorithm then:
    (1) Splits the seed points into two groups defined by
		 2D the line between the starting point of the growing and the centre of mass of the seed points,
		 
		 3D the plane defined by this line and the vector in the direction of the parent branch, and the centre
		 of mass of the seed points.
		 
	(2) Calculates the centres of mass of the two new subregions.
	
	(3) Grows a new branch a fixed distance from the startpoint toward each subregion centre of mass.
	
	(4) Checks whether branching angles and vessel lengths are within predefined limits
		If not, reduces branch angle/vessel length/terminates growing at this branch.
		
	(5) Checks whether the branch is fully in the volume of interest
	
	(6) Repeats steps 1-5 until only one seed point is left in each subregion.

.. With assumptions 1 & 2 defined above, the strain energy density function of the lungs and air is as given below:

.. :math:`W = \frac{\xi}{2} \cdot e^{(aJ_{1}^2 + bJ_{2})}`,			(1)

`Next step: Grow into a cuboid <growintocuboid.html>`_.



