==========
The theory
==========
Please remember to cite appropriate work, when using our methodologies. Below we provide a list of key articles that will
help you orient yourself with the theory and applications that relate to generation of tree structures representing the
anatomy of the placenta (vascular and villous).

Publications containing detailed descriptions of the theory employed in this model:

#. Clark AR, Lin M, Tawhai M, Saghian R, James JL. `Multiscale modelling of the feto–placental vasculature <https://doi.org/10.1098/rsfs.2014.0078>`_. Interface focus. 2015 Apr 6;5(2):20140078.

#. Tawhai MH, Pullan AJ, Hunter PJ. `Generation of an anatomically based three-dimensional model of the conducting airways <https://doi.org/10.1114/1.1289457>`_. Annals of biomedical engineering. 2000 Jul;28:793-802.

#. Tawhai MH, Hunter P, Tschirren J, Reinhardt J, McLennan G, Hoffman EA. `CT-based geometry analysis and finite element models of the human and ovine bronchial tree <https://doi.org/10.1152/japplphysiol.00520.2004>`_. Journal of applied physiology. 2004 Dec;97(6):2310-21.

Publications using previous iterations of these models, implemented in a legacy software (CMISS, Matlab) include:

#. Tun WM, Yap CH, Saw SN, James JL, Clark AR. `Differences in placental capillary shear stress in fetal growth restriction may affect endothelial cell function and vascular network formation <https://doi.org/10.1038/s41598-019-46151-6>`_. Scientific Reports. 2019 Jul 8;9(1):9876.

#. Clark AR, Lin M, Tawhai M, Saghian R, James JL. `Multiscale modelling of the feto–placental vasculature <https://doi.org/10.1098/rsfs.2014.0078>`_. Interface focus. 2015 Apr 6;5(2):20140078.

#. Lin M, Mauroy B, James JL, Tawhai MH, Clark AR. `A multiscale model of placental oxygen exchange: The effect of villous tree structure on exchange efficiency <https://doi.org/10.1016/j.jtbi.2016.06.037>`_. Journal of theoretical biology. 2016 Nov 7;408:1-2.

Publications using current python-based implementations of these models

#. Byrne M, Aughwane R, James JL, Hutchinson JC, Arthurs OJ, Sebire NJ, Ourselin S, David AL, Melbourne A, Clark AR. `Structure-function relationships in the feto-placental circulation from in silico interpretation of micro-CT vascular structures <https://doi.org/10.1016/j.jtbi.2021.110630>`_. Journal of theoretical biology. 2021 May 21;517:110630.

Theses reporting this work:

#. Win Min Tun, PhD, 2019, `Shear stress and oxygen in placental vascular development <https://researchspace.auckland.ac.nz/handle/2292/47678>`_.

#. Monika Byrne, ME, 2019, `Modelling Human Feto-Placental Circulation Based on Imaging <https://researchspace.auckland.ac.nz/handle/2292/46392>`_.

#. Mabelle Lin, PhD, 2017, `Multiscale modelling of blood flow and transport in the human placenta <https://researchspace.auckland.ac.nz/handle/2292/32067>`_.


==========
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



