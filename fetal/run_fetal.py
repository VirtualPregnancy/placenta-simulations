import os
import numpy as np
import placentagen as pg
import csv

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

#if __name__ == '__main__':
#    main()
