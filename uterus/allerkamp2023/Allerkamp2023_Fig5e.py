import numpy as np
from matplotlib import pyplot as plt
import placentagen as pg
import os

## Create a directory to output figures
export_directory = 'output'
if not os.path.exists(export_directory):
    os.makedirs(export_directory)

def six_week_models():
    ###6-8 weeks normal###

    # Definition of geometry
    # Generation |Number of vessels at this level | Vessel Radius (mm) | Vessel length (mm) |
    # To eliminate anastomoses simply give them zero length (note you also need to do this in baseline case)
    # Spiral artery geometry, tube part 1 JZ spiral artery, tube part 2 decidual spiral, plug
    num_radial = 50
    default_radial_radius = 0.112
    reduced_radial_radius = 0.85*default_radial_radius
    vessels = np.array([(1, 1, 0.95, 100.0,'Uterine'),(2, 2, 0.249, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4, num_radial, 0.032, 6.5,'Anastomose'),
          (5, num_radial, 0.036, 7, 'Spiral_tube'),
          (6, num_radial, 0.123, 1.7, 'Spiral_funnel'),(7, num_radial, 0.123, 1.3, 'Spiral_plug')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])
                          
    vessels_noplug = np.array([(1, 1, 0.95, 100.0,'Uterine'),(2, 2, 0.249, 9.0,'Arcuate'),(3, num_radial, default_radial_radius, 6.0,'Radial'),(4, num_radial, 0.032, 6.5,'Anastomose'),
          (5, num_radial, 0.036, 7, 'Spiral_tube'),
          (6, num_radial, 0.123, 3.0, 'Spiral_funnel')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),  ('vessel_type', 'U15')])

    vessels_red = np.array([(1, 1, 0.95, 100.0, 'Uterine'), (2, 2, 0.249, 9.0, 'Arcuate'),
                    (3, num_radial, reduced_radial_radius, 6.0, 'Radial'), (4, num_radial, 0.032, 6.5, 'Anastomose'),
                    (5, num_radial, 0.036, 7, 'Spiral_tube'),
                    (6, num_radial, 0.123, 1.7, 'Spiral_funnel'), (7, num_radial, 0.123, 1.3, 'Spiral_plug')],
                   dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                          ('vessel_type', 'U15')])

    vessels_noplug_red = np.array([(1, 1, 0.95, 100.0, 'Uterine'), (2, 2, 0.249, 9.0, 'Arcuate'),
                           (3, num_radial, reduced_radial_radius, 6.0, 'Radial'),
                           (4, num_radial, 0.032, 6.5, 'Anastomose'),
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

    return StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad

def ten_week_models():
    ###10-12 weeks, scenario A normal###

    # Definition of geometry
    # Generation |Number of vessels at this level | Vessel Radius (mm) | Vessel length (mm) |
    # To eliminate anastomoses simply give them zero length (note you also need to do this in baseline case)
    # Spiral artery geometry, tube part 1 JZ spiral artery, tube part 2 decidual spiral, channel

    num_radial = 50
    default_radial_radius = 0.181
    reduced_radial_radius = 0.85*default_radial_radius
    vessels = np.array([(1, 1, 1.18, 100.0, 'Uterine'), (2, 2, 0.32, 9.0, 'Arcuate'),
                        (3, num_radial, default_radial_radius, 6.0, 'Radial'), (4, num_radial, 0.05, 6.5, 'Anastomose'),
                        (5, num_radial, 0.124, 7, 'Spiral_tube'),
                        (6, num_radial, 0.175, 1.6, 'Spiral_funnel'), (7, 50, 0.175, 1.4, 'Spiral_channel')],
                       dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                              ('vessel_type', 'U15')])

    vessels_noplug = np.array([(1, 1, 1.18, 100.0, 'Uterine'), (2, 2, 0.32, 9.0, 'Arcuate'),
                               (3, num_radial, default_radial_radius, 6.0, 'Radial'),
                               (4, num_radial, 0.05, 6.5, 'Anastomose'),
                               (5, num_radial, 0.124, 7, 'Spiral_tube'),
                               (6, num_radial, 0.175, 3.0, 'Spiral_funnel')],
                              dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                                     ('vessel_type', 'U15')])
    vessels_red = np.array([(1, 1, 1.18, 100.0, 'Uterine'), (2, 2, 0.32, 9.0, 'Arcuate'),
                        (3, num_radial, reduced_radial_radius, 6.0, 'Radial'), (4, num_radial, 0.05, 6.5, 'Anastomose'),
                        (5, num_radial, 0.124, 7, 'Spiral_tube'),
                        (6, num_radial, 0.175, 1.6, 'Spiral_funnel'), (7, 50, 0.175, 1.4, 'Spiral_channel')],
                       dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                              ('vessel_type', 'U15')])

    vessels_noplug_red = np.array([(1, 1, 1.18, 100.0, 'Uterine'), (2, 2, 0.32, 9.0, 'Arcuate'),
                               (3, num_radial, reduced_radial_radius, 6.0, 'Radial'),
                               (4, num_radial, 0.05, 6.5, 'Anastomose'),
                               (5, num_radial, 0.124, 7, 'Spiral_tube'),
                               (6, num_radial, 0.175, 3.0, 'Spiral_funnel')],
                              dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                                     ('vessel_type', 'U15')])

    # spirals and IVS are defined by  resistance (Pa.s/mm^3) and number of units
    myometrial_resistance = 25.8  # Pa.s/mm3
    IVS_resistance = 1.3  # Pa.s/mm3=
    IVS_num = 1.
    terminals = np.array([IVS_resistance, IVS_num, myometrial_resistance])

    # Blood viscosity (Pa.s)
    mu = 3.4e-3
    porosity = 0.123  # porosity of plug (area) or porous medium in channel (adj)
    dp = 4.e-2  # mm, particle diameter
    channel_rad = 0.034  # mm inner radius, outer radius defined in vessels

    # Define a mean uterine artery pressure
    StaticPressure = 82. * 133.
    # steady flow component (baseline) in ml/min - will be scaled with resistance
    SteadyFlow = 27.2  # ml/min

    return StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad
def sixteen_week_models():
    ###16-20 weeks, scenario B normal###

    # Definition of geometry
    # Generation |Number of vessels at this level | Vessel Radius (mm) | Vessel length (mm) |
    # To eliminate anastomoses simply give them zero length (note you also need to do this in baseline case)
    # Spiral artery geometry, tube part 1, channel
    num_radials = 50
    default_radial_radius = 0.257
    reduced_radial_radius = 0.85*default_radial_radius
    vessels = np.array([(1, 1, 1.4, 100.0, 'Uterine'), (2, 2, 0.403, 9.0, 'Arcuate'),
                        (3, num_radials, default_radial_radius, 6.0, 'Radial'),
                        (4, num_radials, 0.1, 6.5, 'Anastomose'),
                        (5, num_radials, 0.3, 7, 'Spiral_tube'),
                        (6, num_radials, 0.241, 3, 'Spiral_channel')],
                       dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                              ('vessel_type', 'U15')])

    vessels_noplug = np.array([(1, 1, 1.4, 100.0, 'Uterine'), (2, 2, 0.403, 9.0, 'Arcuate'),
                               (3, num_radials, default_radial_radius, 6.0, 'Radial'),
                               (4, num_radials, 0.1, 6.5, 'Anastomose'),
                               (5, num_radials, 0.3, 10, 'Spiral_funnel')],
                              dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                                     ('vessel_type', 'U15')])
    vessels_red = np.array([(1, 1, 1.4, 100.0, 'Uterine'), (2, 2, 0.403, 9.0, 'Arcuate'),
                        (3, num_radials, reduced_radial_radius, 6.0, 'Radial'),
                        (4, num_radials, 0.1, 6.5, 'Anastomose'),
                        (5, num_radials, 0.3, 7, 'Spiral_tube'),
                        (6, num_radials, 0.241, 3, 'Spiral_channel')],
                       dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                              ('vessel_type', 'U15')])

    vessels_noplug_red = np.array([(1, 1, 1.4, 100.0, 'Uterine'), (2, 2, 0.403, 9.0, 'Arcuate'),
                               (3, num_radials, reduced_radial_radius, 6.0, 'Radial'),
                               (4, num_radials, 0.1, 6.5, 'Anastomose'),
                               (5, num_radials, 0.3, 10, 'Spiral_funnel')],
                              dtype=[('generation', 'i4'), ('number', 'i4'), ('radius', 'f8'), ('length', 'f8'),
                                     ('vessel_type', 'U15')])

    # spirals and IVS are defined by  resistance (Pa.s/mm^3) and compliance (/Pa) [R|C|0=off 1=on]
    # To remove these from the model (eg post partum) set third parameter to be zero, otherwise set as 1
    # spirals and IVS are defined by  resistance (Pa.s/mm^3) and number of units
    myometrial_resistance = 25.8  # Pa.s/mm3
    IVS_resistance = 1.3  # Pa.s/mm3=
    IVS_num = 1.
    terminals = np.array([IVS_resistance, IVS_num, myometrial_resistance])

    # Blood viscosity (Pa.s)
    mu = 3.4e-3
    porosity = 0.164  # porosity of plug or porous medium in channel
    dp = 4.e-2  # mm, particle diameter
    channel_rad = 0.16  # mm inner radius, outer radius defined in vessels

    # Define a mean uterine artery pressure
    StaticPressure = 84. * 133.
    # steady flow component (baseline) in ml/min - will be scaled with resistance
    SteadyFlow = 39.5  # ml/min
    return StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad

StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad = six_week_models()
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

[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
radial_shear= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
radial_shear_noplug= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_red, terminals,boundary_conds,channel_rad)
radial_shear_red= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug_red, terminals,boundary_conds,channel_rad)
radial_shear_noplug_red= shear[radial_index]

X = ['6-8 weeks', '10-12 weeks', '16-18 weeks']
Yplug = [radial_shear_noplug/radial_shear,1,1]
Yreduced = [radial_shear_red/radial_shear,1,1]
Yreducedplug = [radial_shear_noplug_red/radial_shear,1,1]

Zbaseline = np.asarray([radial_shear,1,1])
Zplug = np.asarray([radial_shear_noplug,1,1])
Zreduced = np.asarray([radial_shear_red,1,1])
Zreducedplug = np.asarray([radial_shear_noplug_red,1,1])

print(radial_shear, radial_shear_noplug, radial_shear_red, radial_shear_noplug_red)



StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad = ten_week_models()


boundary_conds = np.array([('flow',StaticPressure,SteadyFlow)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('inlet_q','f8')])

for i in range(0, np.size(vessels)):
    if (vessels['vessel_type'][i] == 'Anastomose'):
        anast_index = i
    elif (vessels['vessel_type'][i] == 'Radial'):
        radial_index = i
    elif (vessels['vessel_type'][i] == 'Spiral_tube'):
        spiral_index = i

[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
radial_shear= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
radial_shear_noplug= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_red, terminals,boundary_conds,channel_rad)
radial_shear_red= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug_red, terminals,boundary_conds,channel_rad)
radial_shear_noplug_red= shear[radial_index]

Yplug[1] = radial_shear_noplug/radial_shear
Yreduced[1] = radial_shear_red/radial_shear
Yreducedplug[1] = radial_shear_noplug_red/radial_shear

Zbaseline[1] = radial_shear
Zplug[1] = radial_shear_noplug
Zreduced[1] = radial_shear_red
Zreducedplug[1] = radial_shear_noplug_red

StaticPressure,SteadyFlow,mu,dp,porosity,vessels,vessels_noplug,vessels_red,vessels_noplug_red, channel_rad = sixteen_week_models()


boundary_conds = np.array([('flow',StaticPressure,SteadyFlow)],dtype=[('bc_type', 'U12'),('inlet_p','f8'),('inlet_q','f8')])

for i in range(0, np.size(vessels)):
    if (vessels['vessel_type'][i] == 'Anastomose'):
        anast_index = i
    elif (vessels['vessel_type'][i] == 'Radial'):
        radial_index = i
    elif (vessels['vessel_type'][i] == 'Spiral_tube'):
        spiral_index = i

[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels, terminals,boundary_conds,channel_rad)
radial_shear= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug, terminals,boundary_conds,channel_rad)
radial_shear_noplug= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_red, terminals,boundary_conds,channel_rad)
radial_shear_red= shear[radial_index]
[TotalResistance, VenousResistance, shear,resistance,flow,pressure_out] = pg.human_total_resistance(mu,dp,porosity,vessels_noplug_red, terminals,boundary_conds,channel_rad)
radial_shear_noplug_red= shear[radial_index]

Yplug[2] = radial_shear_noplug/radial_shear
Yreduced[2] = radial_shear_red/radial_shear
Yreducedplug[2] = radial_shear_noplug_red/radial_shear

Zbaseline[2] = radial_shear
Zplug[2] = radial_shear_noplug
Zreduced[2] = radial_shear_red
Zreducedplug[2] = radial_shear_noplug_red


Zbaseline = Zbaseline*10.
Zplug = Zplug*10.
Zreduced = Zreduced*10.
Zreducedplug = Zreducedplug*10.

np.set_printoptions(precision=1)
print('---------------------------------------------')
print('     Table 2  (shear stress in dyne/cm2)     ')
print('---------------------------------------------')
print('Shear stress at  :', X)
print('Baseline:        :',Zbaseline)
print('Plug removed     :',Zplug)
print('0.85 radius      :',Zreduced)
print('0.85 rad, no plug:', Zreducedplug)

X_axis = np.arange(len(X))
plt.ylim([0, 6])
plt.xlim([-0.4,X_axis[len(X)-1]+.4])
plt.bar(X_axis - 0.2, Yplug, 0.2, label='Trophoblast plug removed')
plt.bar(X_axis, Yreduced, 0.2, label='Radial artery radius reduced')
plt.bar(X_axis + 0.2, Yreducedplug, 0.2, label='Combined effects')
plt.plot([-0.4,X_axis[len(X)-1]+.4],[1,1],color='k')
plt.xticks(X_axis, X)
plt.xlabel("Gestation range")
plt.ylabel("x-fold change")
plt.legend()

plt.savefig(export_directory + '/Allerkamp2023_Fig5E.png')
plt.show()

