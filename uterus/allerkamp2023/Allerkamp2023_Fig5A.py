import numpy as np
from matplotlib import pyplot as plt
import placentagen as pg
import os

## Create a directory to output figures
export_directory = 'output'
if not os.path.exists(export_directory):
    os.makedirs(export_directory)
###6-8 weeks normal###

# Definition of geometry
# Generation |Number of vessels at this level | Vessel Radius (mm) | Vessel length (mm) |
# To eliminate anastomoses simply give them zero length (note you also need to do this in baseline case)
# Spiral artery geometry, tube part 1 JZ spiral artery, tube part 2 decidual spiral, plug
num_radial = 50
default_radial_radius = 0.112
vessels = np.array([(1, 1, 0.95, 100.0,'Uterine'),(2, 2, 0.249, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4, num_radial, 0.032, 6.5,'Anastomose'),
          (5, num_radial, 0.036, 7, 'Spiral_tube'),
          (6, num_radial, 0.123, 1.7, 'Spiral_funnel'),(7, num_radial, 0.123, 1.3, 'Spiral_plug')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])
                          
vessels_noplug = np.array([(1, 1, 0.95, 100.0,'Uterine'),(2, 2, 0.249, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4, num_radial, 0.032, 6.5,'Anastomose'),
          (5, num_radial, 0.036, 7, 'Spiral_tube'),
          (6, num_radial, 0.123, 3.0, 'Spiral_funnel')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])


# Blood viscosity (Pa.s)
mu = 3.4e-3
porosity = 0.28 #porosity of plug or porous medium in channel
dp = 4.e-2 #mm, particle diameter
channel_rad=0 #mm inner radius, outer radius defined in vessels

# Define a mean uterine artery pressure
StaticPressure = 80. * 133.
#steady flow component (baseline) in ml/min - will be scaled with resistance
SteadyFlow=24.2 #ml/min


myometrial_resistance = 25.8 #Pa.s/mm3

# spirals and IVS are defined by  resistance (Pa.s/mm^3) and number of units
IVS_resistance = 1.3#Pa.s/mm3
IVS_num = 1.
terminals = np.array([IVS_resistance,IVS_num,myometrial_resistance])

boundary_conds = np.array([('flow',StaticPressure,SteadyFlow)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('inlet_q','f8')])

for i in range(0, np.size(vessels)):
    if (vessels['vessel_type'][i] == 'Anastomose'):
        anast_index = i
    elif (vessels['vessel_type'][i] == 'Radial'):
        radial_index = i
    elif (vessels['vessel_type'][i] == 'Spiral_tube'):
        spiral_index = i


## Calculate total resistance of the system and compare to baseline (flow decreases by this factor as resistance increases assuming a constant driving pressure)
num_assess = 10
radius = np.linspace(0.1,0.2, num_assess)
radial_shear = np.zeros(len(radius))
radial_shear_noplug = np.zeros(len(radius))

for k in range(0, num_assess):
    vessels['radius'][radial_index] = radius[k]
    vessels_noplug['radius'][radial_index] = radius[k]
    print("setting radial radius" + str(vessels['radius'][radial_index]))  # 0=uterine, 1=arcuate,2=radial
    [TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
    radial_shear[k] = shear[radial_index]*10 #dyn/cm^2
    [TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
    radial_shear_noplug[k] = shear[radial_index]*10 #dyn/cm^2


# Set the default text font size
plt.rc('font', size=14)
# Set the axes title font size
plt.rc('axes', titlesize=10)
# Set the axes labels font size
plt.rc('axes', labelsize=14)
# Set the font size for x tick labels
plt.rc('xtick', labelsize=14)
# Set the font size for y tick labels
plt.rc('ytick', labelsize=14)
# Set the legend font size
plt.rc('legend', fontsize=14)
# Set the font size of the figure title
plt.rc('figure', titlesize=16)

plt.plot(radius, radial_shear, color="black", label='Plugged')
plt.plot(radius, radial_shear_noplug, color="black", linestyle='dashed', label='Not Plugged')
plt.ylim([0, 15])
plt.yticks(np.arange(0, 15.01, step=2.5))
vessels['radius'][radial_index] = default_radial_radius
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
radial_shear= shear[radial_index]

vessels_noplug['radius'][radial_index] = default_radial_radius
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
radial_shear_noplug= shear[radial_index]

plt.plot(default_radial_radius,radial_shear*10,'+k', mew=2, ms=15, label='Physiol. radius plugged')
plt.plot(default_radial_radius,radial_shear_noplug*10,'ok', mew=2, ms=8, label='Physiol. radius not plugged')

plt.xlabel('Radial artery radius (mm)')
plt.ylabel('Radial artery shear stress (dyn/$\mathregular{cm^{2}}$)')
plt.legend()
print("Radial artery shear stress PLUGGED: " +  str(radial_shear) + " Pa, " + str(radial_shear*10) + " dyne/cm2")
print("Radial artery shear stress UNPLUGGED: " +  str(radial_shear_noplug) + " Pa, " + str(radial_shear_noplug*10) + " dyne/cm2")

#export plot
plt.savefig(export_directory + '/Allerkamp2023_Fig5A.png')
plt.show()
