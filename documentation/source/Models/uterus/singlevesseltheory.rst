==========
The theory
==========

Publications containing detailed descriptions of the theory employed in this model:

 - `Carlson and Secombe Micro-circulation, 2005 <https://www.tandfonline.com/doi/abs/10.1080/10739680590934745>`_.
 - `Carlson et al. Am J Physiol - Heart Circ Physiol, 2008 <https://journals.physiology.org/doi/full/10.1152/ajpheart.00262.2008>`_.
 - `Allerkamp et al. Am J Physiol - Heart Circ Physiol, 2022 <https://doi.org/10.1152/ajpheart.00693.2021>`_.

Please remember to cite these papers if using these models.

The basics
==========

This model represents vessel tension-pressure-diameter relationships in a single isolated vessel.

We assume a total tension (:math:`T_{tot}`) as a function of passive tension  (:math:`T_{act}`), smooth muscle activation (:math:`A`), and maximum active tension (:math:`T_{act}`)

:math:`T_{tot}=T_{pass}+AT_{actmax}`

where A lies between 0 and 1. The tension in the vessel wall is then related to pressure, P, and vessel diameter, D,  by Laplace’s law, :math:`Ttot = PD/2`.

The passive tension-diameter relationship is defined empirically following Carlson and Secombe as

:math:`T_{pass}=C_{pass} \exp \left(C'_{pass}\frac{D}{D_0} - 1\right)`

where :math:`D_0` is the passive diameter of the vessel at a pressure of 100 mmHg, :math:`C_{pass}` is the tension at this pressure, and :math:`C’_{pass}` determines the steepness of the exponential curve.

The maximal active tension is defined as

:math:`T_{maxact}=C_{act} \exp \frac{\left( - \frac{D}{D_0} - C'_{act}\right)}{C''_{act}}`
,

where Cact controls maximum tension, C''act controls the diameter at which peak active tension occurs, and C''act controls the width of the Gaussian curve.
Smooth muscle activation, A, is defined as

:math:`A=\frac{1}{1+\exp (-S_{tone})}`

where

:math:`S_{tone}=S_{myo}+S_{shear}+C'_{tone}`


where :math:`S_{myo} = C_{myo}T` controls the strength of the myogenic response,
:math:`S_{shear}` controls the strength of the shear response, and
:math:`C'_{tone}` is a constant parameter.

Shear (:math:`\tau`) impacts the uterine radial arteries in a particular way, based on myography data.
Here

:math:`S_{shear} = 0`, if :math:`\tau < \tau_1`,

:math:`S_{shear} = C_{shear}(\tau-\tau_1)`, if :math:`\tau_1 < \tau < \tau_2`,

and

:math:`S_{shear} = - C'_{shear}\left( \tau -\frac{C_{shear}}{C'_{shear}}(\tau_1-\tau_2)+\tau_2\right)`, if :math:`\tau_2 < \tau`,


