
import numpy as np
from matplotlib import pyplot as plt
import placentagen as pg

###10-12 weeks, scenario A normal###

# Definition of geometry
# Generation |Number of vessels at this level | Vessel Radius (mm) | Vessel length (mm) |
# To eliminate anastomoses simply give them zero length (note you also need to do this in baseline case)
# Spiral artery geometry, tube part 1 JZ spiral artery, tube part 2 decidual spiral, channel

num_radial = 50
default_radial_radius = 0.181
vessels = np.array([(1, 1, 1.18, 100.0,'Uterine'),(2, 2, 0.32, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4,num_radial, 0.05, 6.5,'Anastomose'),
          (5, num_radial, 0.124, 7, 'Spiral_tube'),
          (6, num_radial, 0.175, 1.6, 'Spiral_funnel'),(7, 50, 0.175, 1.4, 'Spiral_channel')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])
                          
vessels_noplug = np.array([(1, 1, 1.18, 100.0,'Uterine'),(2, 2, 0.32, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4,num_radial, 0.05, 6.5,'Anastomose'),
          (5, num_radial, 0.124, 7, 'Spiral_tube'),
          (6, num_radial, 0.175, 3.0, 'Spiral_funnel')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])

# spirals and IVS are defined by  resistance (Pa.s/mm^3) and compliance (/Pa) [R|C|0=off 1=on]
# To remove these from the model (eg post partum) set third parameter to be zero, otherwise set as 1
myometrial_resistance = 25.8 #Pa.s/mm3
IVS_resistance = 1.3 #Pa.s/mm3
IVS_compliance = 1e-8
IVS_num = 1.
terminals = np.array([IVS_resistance,IVS_compliance,IVS_num,myometrial_resistance])

# Blood viscosity (Pa.s)
mu = 3.4e-3
porosity = 0.123 #porosity of plug (area) or porous medium in channel (adj)
dp = 4.e-2 #mm, particle diameter
channel_rad= 0.034 #mm inner radius, outer radius defined in vessels

# Define a mean uterine artery pressure
StaticPressure = 82. * 133.
#steady flow component (baseline) in ml/min - will be scaled with resistance
SteadyFlow=27.2 #ml/min
boundary_conds = np.array([('flow',StaticPressure,SteadyFlow)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('inlet_q','f8')])

#StaticPressureOut = 10.0*133 #Outlet pressure (uterine veins)
#boundary_conds = np.array([('pressure',StaticPressure,StaticPressureOut)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('outlet_p','f8')])

for i in range(0, np.size(vessels)):
    if (vessels['vessel_type'][i] == 'Anastomose'):
        anast_index = i
    elif (vessels['vessel_type'][i] == 'Radial'):
        radial_index = i
    elif (vessels['vessel_type'][i] == 'Spiral_tube'):
        spiral_index = i


## Calculate total resistance of the system and compare to baseline (flow decreases by this factor as resistance increases assuming a constant driving pressure)

## Calculate total resistance of the system and compare to baseline (flow decreases by this factor as resistance increases assuming a constant driving pressure)
num_assess = 10
radius = np.linspace(0.1, 0.2, num_assess)
radial_shear = np.zeros(len(radius))
radial_shear_noplug = np.zeros(len(radius))

for k in range(0, num_assess):
    vessels['radius'][radial_index] = radius[k]
    vessels_noplug['radius'][radial_index] = radius[k]
    print("setting radial radius" + str(vessels['radius'][radial_index]))  # 0=uterine, 1=arcuate,2=radial
    [TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
    radial_shear[k] = shear[radial_index] #Pa
    [TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
    radial_shear_noplug[k] = shear[radial_index] #Pa

plt.plot(radius, radial_shear,label='Plugged')
plt.plot(radius, radial_shear_noplug,label='Not Plugged')

vessels['radius'][radial_index] = default_radial_radius
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
radial_shear= shear[radial_index]

vessels_noplug['radius'][radial_index] = default_radial_radius
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
radial_shear_noplug= shear[radial_index]

plt.plot(default_radial_radius,radial_shear,'+k',label='Default radius plugged')
plt.plot(default_radial_radius,radial_shear_noplug,'+r',label='Default radius not plugged')

plt.xlabel('Radial artery radius (mm)')
plt.ylabel('Radial artery shear stress (Pa)')
plt.title('Radial artery radius vs shear stress')
plt.legend()
print("Radial artery shear stress PLUGGED: " +  str(radial_shear) + " Pa")
print("Radial artery shear stress UNPLUGGED: " +  str(radial_shear_noplug) + " Pa")
plt.show()



