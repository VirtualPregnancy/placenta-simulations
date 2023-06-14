Allerkamp 2022 
--------------

This repository contains code that reproduces  Allerkamp et al. (https://doi.org/10.1152/ajpheart.00693.2021)

The code reproduces computational modelling results which appear in Figures 3, 4, and 6:
- Figure 3, A (PassiveFitsNonNormalised.png),  B (PassiveFitsNormalisedTo10mmHg.png), C (CpassComparison.png), D (CpassdashComparison.png)
- Figure 4 A (ExperimentalDataActiveNoFlow.png) B (ActiveNoFlowFits.png), C (CmyoComparison.png), and D (Cact Comparison.png)
- Figure 6 B (FlowImpactNonPregnant.png) and C (FlowImpactPregnant.png)


Requirements
------------

You will need python >3 (tested with version 3.9), with the following packages installed:

- numpy
- matplotlib
- os
- csv
- placentagen (https://github.com/virtualpregnancy/placentagen)


Running
-------
Simply run the python code in alllerkamp2022.py, and the figures will be written to the 'output' directory.



For more information on how this code works, please see the documentation for this model
at https://placenta-simulator.readthedocs.io/en/latest/Models/uterus/singlevessel_index.html

