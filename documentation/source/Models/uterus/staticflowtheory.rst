==========
The theory
==========

Publications containing detailed descriptions of the theory employed in this model:

 - `Clark et al. Interface, 2015 (same theory but applied to complex fetoplacental networks) <http://rsfs.royalsocietypublishing.org/content/5/2/20140078>`_.
 -  `Clark et al. 2018 (the static component of this model follows similar theory) <https://doi.org/10.1016/j.placenta.2018.05.001>`_.
 -  `James et al. 2018 (plug models without channels) <https://doi.org/10.1093/humrep/dey225>`_.
 -  `Allerkamp et al. 2021 (anatomical structure of the uterus) <https://doi.org/10.1093/humrep/deaa303>`_.
 - Allerkamp et al. 2023 (introduced trophoblast plugs with channels) in preparation.

Please remember to cite these papers if using these models.

The basics
==========
This page discusses the basics of the modelling work but does not provide a comprehensive summary. Please refer to the papers and theses above to understand the detail of the models.
This model employs an electrical circuit analogy model for the uterine circulation.
For more details see :doc:`here </Models/fetoplacental/steadyflow_index>`.

In the uterine circulation we typically see small vessels and low Reynold's number flows. So, we assume each vessel is characterised by a resistance (:math:`R`). Most vessels within the uterine circulation are modelled
as cylindrical vessels characterised by their radius :math:`r` and their length :math:`L`. The resistance in this case is defined as a Poiseuille resistance.

However, in the uterus, there are specialised arteries, called spiral arteries that are initially plugged by trophoblast cells, and later form channels within these plugs, and finally open to the surface of the placenta in a funnel like structure. The resistance in these vessels is determined both by the structure of the vessel, and also by the
structure of the plug within it.

Cylindrical vessel segments
---------------------------
Where there is no plug resistance is defined as a Poiseuille resistance

:math:`R = \frac{8\mu L}{\pi r^4}`

where :math:`\mu` is viscosity of blood, L is the length of the blood vessel and r is the radius of the blood vessel.

Funnel like vessel segments
---------------------------
Resistance in funnel-like segments (see `Burton et al. 2009 <https://doi.org/10.1016/j.placenta.2009.02.009>`_) is defined by

:math:`R=\frac{8\mu}{\pi r_a^4} \frac{(r_a/3c-(r_a^4)}{(3c(r_a+cL)^3 ))}`

where :math:`L` is the length of the funneled section, :math:`r_a` is the radius of the vessel at the start of the funnel, :math:`r_b` is the (larger) radius of the vessel at the end
of the funnelled section and :math:`c=(r_b-r_a)/L`.


Completely plugged vessel segments
----------------------------------
In completely plugged vessel segments (see `James et al. 2018 <https://doi.org/10.1093/humrep/dey225>`_), resistance is

:math:`R=\frac{\mu L}{K\pi r^2} \left(1-2\left(\frac{\sqrt{K/\gamma}}{r}\frac{I_1 \left(\sqrt{\gamma/K} r\right)}{ I_0 \left( \sqrt{\gamma/K} r \right) }\right)\right)`

where  :math:`I_0` and :math:`I_1` are modified Bessel functions of the first kind, :math:`K` is plug permeability, which is calculated using the Carman-Kozney formula (see `Kavainy <https://doi.org/10.1007/978-1-4612-4254-3>`_).

Plugs containing channels
-------------------------
Here, we assume that the channels reside in the centre of the plugged region. The theory driving this resistance is more complex, and is derived in full in
Appendix A of `this thesis <https://auckland.primo.exlibrisgroup.com/permalink/64UAUCK_INST/831b8u/alma99265536381202091>`_.

:math:`R = \frac{\Delta p}{Q_1 + Q_2} = \frac{1}{\bar{Q}_1 + \bar{Q}_2 }`

where :math:`Q_1` is flow through the channel, :math:`Q_2` is flow through the porous surrounding plug, and :math:`\Delta p` is the pressure drop through the plugged portion of the artery.


:math:`Q_1 =  \frac{2\pi\Delta p}{\mu L}  \left(\bar{c}_2\frac{r_1^2}{2}- \frac{r_1^4}{16}  \right)`

:math:`\bar{c}_2 = \frac{1}{2\sqrt{\delta}} \frac{ \left( -2k\sqrt{\delta}K_1(\sqrt{\delta}r_1)-r_1K_0(\sqrt{\delta}r_2) \right)I_0(\sqrt{\delta}r_1) }{\left(  K_0(\sqrt{\delta}r_2)I_1(\sqrt{\delta}r_1) + K_1(\sqrt{\delta}r_1)I_0(\sqrt{\delta}r_2) \right)} \\
-\frac{1}{2\sqrt{\delta}} \frac{\left( 2\sqrt{\delta}k I_1(\sqrt{\delta}r_1) -  r_1 I_0(\sqrt{\delta}r_2)\right)K_0(\sqrt{\delta}r_1)}{\left(  K_0(\sqrt{\delta}r_2)I_1(\sqrt{\delta}r_1) + K_1(\sqrt{\delta}r_1)I_0(\sqrt{\delta}r_2) \right)} \\
+k + \frac{r_1^2}{4}`

:math:`Q_2 =  \frac{2\pi\Delta p}{\sqrt{\delta}\mu L}  \left(\bar{c}_3 (r_2 I_1(\sqrt{\delta}r_2)-r_1 I_1(\sqrt{\delta}r_1)) - \bar{c}_4 (r_2 K_1(\sqrt{\delta}r_2)-r_1 K_1(\sqrt{\delta}r_1))  +  k\frac{r_2^2-r_1^2}{2}\right)`

:math:`\bar{c}_3 =\frac{1}{2\sqrt{\delta}} \frac{ \left( -2k\sqrt{\delta}K_1(\sqrt{\delta}r_1)-r_1K_0(\sqrt{\delta}r_2) \right)}{\left(  K_0(\sqrt{\delta}r_2)I_1(\sqrt{\delta}r_1) + K_1(\sqrt{\delta}r_1)I_0(\sqrt{\delta}r_2) \right)}`

:math:`\bar{c}_4 =-\frac{1}{2\sqrt{\delta}} \frac{\left( 2\sqrt{\delta}k I_1(\sqrt{\delta}r_1) -  r_1 I_0(\sqrt{\delta}r_2)\right)}{\left(  K_0(\sqrt{\delta}r_2)I_1(\sqrt{\delta}r_1) + K_1(\sqrt{\delta}r_1)I_0(\sqrt{\delta}r_2) \right)}`

where :math:`\delta=\gamma/K`,  :math:`I_0` and :math:`I_1` are modified Bessel functions of the first kind, and  :math:`K_0` and :math:`K_1` are modified Bessel functions of the second kind, :math:`r_1` is the radius of the channel, and :math:`r_2` is the radius of the vessel.



Total network resistance
-------------------------
One is able to assess total network resistance, and the distribution of blood pressure and flow in the system by considering any network as a combination of vessel segments via one of the resistance calculations above. Considering each vessel generation in turn one can sum the resistances
of all :math:`N` vessels in that generation in parallel and then total resistance of all generations can be summed in series.


