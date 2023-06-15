==========
The theory
==========

Publications containing detailed descriptions of the theory employed in this model:

 -  `Clark et al. Interface, 2015 (same theory but applied to complex fetoplacental networks) <http://rsfs.royalsocietypublishing.org/content/5/2/20140078>`_.
 -  `Clark et al. 2018 (the static component of this model follows similar theory) <https://doi.org/10.1016/j.placenta.2018.05.001>`_.
 -  `James et al. 2018 (plug models without channels) <https://doi.org/10.1093/humrep/dey225>`_.
 -  `Allerkamp et al. 2021 (anatomical structure of the uterus) <https://doi.org/10.1093/humrep/deaa303>`_.
 - Allerkamp et al. 2023 (introduced trophoblast plugs with channels) in preparation.

Please remember to cite these papers if using these models.

The basics
==========
This model employs an electrical circuit analogy model for the uterine circulation.
For more details see :doc:`../fetoplacental/steadyflowtheory`


To simulate flow through the system, we need to have a realistic mechanical description of the resistance of each vessel. If we assume that flow in the vessels is steady (which is required to use the DC circuit analogy), that flow is laminar and fully developed we can use a Poiseuille approximation to determine the resistance of each blood vessel. Any blood vessel with certain length and radius has resistance given by:

 :math:`R = \frac{8\mu L}{\pi r^4}`
where :math:`\mu` is viscosity of blood, L is the length of the blood vessel and r is the radius of the blood vessel.


If w consider the electrical resistance of any conductor (blood vessel in this case), we can see how the definition of Poiseuille resistance makes sense:

 :math:`R = \frac{\rho L}{A}`
where  :math:`\rho` is the conductivity, R is the electrical resistance,  L is the length of the vessel and A is the area of cross section of the vessel.

Now, after re-writing the poiseuille's resistance in terms of electrical resistance would result in:


 :math:`R = \frac{8\mu L}{\pi r^2}`
where :math:`\mu` is the blood viscosity, R is the electrical resistance,  L is the length of the vessel, A is the area of cross section of the vessel and r is the radius of the vessel.

