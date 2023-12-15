import os
import numpy as np
import placentagen as pg
import csv
from reprosim.diagnostics import set_diagnostics_level
from reprosim.indices import perfusion_indices, get_ne_radius
from reprosim.geometry import append_units,define_node_geometry, define_1d_element_geometry,define_1d_element_placenta,define_rad_from_geom,add_matching_mesh, \
        define_capillary_model,define_rad_from_file
from reprosim.repro_exports import export_1d_elem_geometry, export_node_geometry, export_1d_elem_field,export_node_field,export_terminal_perfusion
from reprosim.fetal import assign_fetal_arrays, fetal_model

################################################
# Set up a folder to export to
################################################
#Define a directory to export (do not write over expected-results unless you have made a (peer-reviewed) change to the process)
export_directory = 'output'
if not os.path.exists(export_directory):
    os.makedirs(export_directory)


####################################################################
# Define timestep and number of heart beats that are to be simulated
####################################################################
dt=0.0001 #s, time step
num_heart_beats=30 #number of heart beats to simulate
############################################################
#Define model parameters related to the heart
############################################################
T_beat = 0.43 # heart beat period (s)
T_vs  = 0.215 # Time period of ventricular contraction (s)
T_as = 0.1075 #Time period of atrial contraction (s)
T_v_delay = 0.1075 #delay in ventrial contraction (compare to atria) (s)
U0RV = 5332.89 #Pa
EsysRV = 0.399967 #Pa/mm3
EdiaRV = 0.0399967 #Pa/mm3
RvRV = 0.010665 #Pa.s/mm3
U0LV = 5332.89 #Pa
EsysLV =0.399967 #Pa/mm3
EdiaLV =0.0399967 #Pa/mm3
RvLV = 0.010665 #Pa.s/mm3
U0A = 399.967 #Pa
V0V = 8000.  # mm3 - volume of ventricles (initial)
V0A = 3000.  # mm3 - volume of atria (initial)
human_weight = 3.0255 #kg Not used, but current parameterisation assumes an average fetal weight and allometric scaling may be useful in future

#########################################################################
#Read and export element properties from file to reprosim readable format
#########################################################################
elem_file = 'elemProperties.csv'
file = open(elem_file)
elem_properties = csv.reader(file)
header = next(elem_properties)
rows = []
for row in elem_properties:
    rows.append(row)
file.close()
elem_identifiers = np.empty(len(rows),dtype=np.dtype('U10'))
elems = np.empty((len(rows),3),dtype=int)
group = np.empty(len(rows),dtype=int)
resistance = np.empty(len(rows),dtype=np.dtype('d'))
L= np.empty(len(rows),dtype=np.dtype('d'))
K = np.empty(len(rows),dtype=np.dtype('d'))
for i in range(0,len(rows)):
    elem_identifiers[i] = rows[i][0]
    elems[i,0]=int(rows[i][1])-1
    elems[i,1]=int(rows[i][2])-1
    elems[i,2]=int(rows[i][3])-1
    resistance[i]=np.double(rows[i][header.index('R')])
    group[i]=int(rows[i][header.index('group')])
    L[i]=np.double(rows[i][header.index('L')])
    K[i]=np.double(rows[i][header.index('K')])

pg.export_ipelem_1d(elems, 'fetal', export_directory + '/fetal')
pg.export_exfield_1d_linear(resistance, 'fetal', 'resistance', export_directory +'/R')
pg.export_exfield_1d_linear(group, 'fetal', 'group', export_directory + '/group')
pg.export_exfield_1d_linear(L, 'fetal', 'L', export_directory + '/L')
pg.export_exfield_1d_linear(K, 'fetal', 'K', export_directory + '/K')

########################################################################
#Read and export node properties from file to reprosim readable format
########################################################################

node_file = 'nodeProperties.csv'
file = open(node_file)
node_properties = csv.reader(file)
header = next(node_properties)
rows = []
for row in node_properties:
    rows.append(row)
file.close()
nodes = np.empty((len(rows),4),dtype=np.dtype('d'))
node_identifiers = np.empty(len(rows),dtype=np.dtype('U10'))
for i in range(0,len(rows)):
    node_identifiers[i] = rows[i][0]
    nodes[i,0]=np.double(rows[i][1])-1
    nodes[i,1]=np.double(rows[i][header.index('group')])
    nodes[i,2]=np.double(rows[i][header.index('press')])
    nodes[i,3]=np.double(rows[i][header.index('comp')])

pg.export_ip_coords(nodes[:,1:4], 'fetal', export_directory +'/fetal')
def main():
    set_diagnostics_level(0)  # level 0 - no diagnostics; level 1 - only prints subroutine names (default); level 2 - prints subroutine names and contents of variables


    # define model geometry and indices
    perfusion_indices()
    define_node_geometry(export_directory +'/fetal.ipnode')
    define_1d_element_geometry(export_directory + '/fetal.ipelem')
    assign_fetal_arrays()

    define_node_geometry('sample_geometry/placenta.ipnode')
    define_1d_element_placenta('sample_geometry/placenta.ipelem')
    append_units()

    # creates a mesh that converges (a venous mesh)
    umbilical_elem_option = 'same_as_arterial'
    umbilical_elements = []
    add_matching_mesh(umbilical_elem_option, umbilical_elements)

    # define radius by Strahler order in diverging (arterial mesh)
    s_ratio = 1.38  # rate of decrease in radius at each order of the arterial tree  1.38
    inlet_rad = 1.5  # inlet radius
    order_system = 'strahler'
    order_options = 'arterial'
    name = 'inlet'
    define_rad_from_geom(order_system, s_ratio, name, inlet_rad, order_options, '')
    # defines radius by STrahler order in converging (venous mesh)
    s_ratio_ven = 1.46  # rate of decrease in radius at each order of the venous tree 1.46
    inlet_rad_ven = 2.7  # inlet radius
    order_system = 'strahler'
    order_options = 'venous'
    first_ven_no = ''  # number of elements read in plus one
    last_ven_no = ''  # 2x the original number of elements + number of connections
    define_rad_from_geom(order_system, s_ratio_ven, first_ven_no, inlet_rad_ven, order_options, last_ven_no)

    num_convolutes = 10  # number of terminal convolute connections
    num_generations = 3  # number of generations of symmetric intermediate villous trees
    num_parallel = 6  # number of capillaries per convolute
    define_capillary_model(num_convolutes, num_generations, num_parallel, 'interface2015')


    fetal_model(dt,num_heart_beats,T_beat,T_vs,T_as,T_v_delay,U0RV,EsysRV,EdiaRV,RvRV,U0LV,EsysLV,EdiaLV,RvLV,U0A,V0V,V0A)


if __name__ == '__main__':
    main()
