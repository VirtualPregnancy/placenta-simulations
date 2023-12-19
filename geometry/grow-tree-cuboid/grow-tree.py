#!/usr/bin/env python
import os
import placentagen as pg
import numpy as np
 
##########################################
# Parameters that define placental size #
##########################################
#Define the dimensions of the cuboid
x_dim = 10.0 #mm
y_dim = 10.0 #mm
z_dim = 10.0 #mm

###############################################################
# Parameters that define branching within the placenta volume #
###############################################################
#number of seed points
n_seed = 5000.
#Length of stem villi
sv_length = 2.0
#Maximum angle between two branches
angle_max_ft =  100 * np.pi /180
#Minimum angle between two branches
angle_min_ft = 0 * np.pi /180
#Fraction that the branch grows toward data group centre of mass at each iteration
fraction_ft =   0.4
#Minimum length of a branch
min_length_ft =  0.1 #mm
#minimum number of data points that can be in any group after a data splitting proceedure
point_limit_ft =  1

###################
# Export controls #
###################
#If you want to see how each step in the process builds on the last set this to be true
export_intermediates = False
#If you want final results set this to be true
export_results = True
#Define a directory to export (do not write over expected-results unless you have made a (peer-reviewed) change to the process)
export_directory = 'output'

if(export_intermediates or export_results):
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)


seed_geom = {}
seed_geom["nodes"] = np.asarray([[0,0,0,-z_dim/2.],[1,0,0,-z_dim/2.+sv_length],[2,0,fraction_ft*y_dim/4.,(-1+fraction_ft)*z_dim/2.+(1-fraction_ft)*sv_length],[3,0,-fraction_ft*y_dim/4,(-1+fraction_ft)*z_dim/2.+(1-fraction_ft)*sv_length]])
seed_geom["elems"] = np.asarray([[0,0,1],[1,1,2],[2,1,3]])

elem_connectivity = pg.element_connectivity_1D(seed_geom["nodes"][:,1:4], seed_geom["elems"])
seed_geom["elem_up"]= elem_connectivity["elem_up"]
seed_geom["elem_down"] = elem_connectivity["elem_down"]

#Define data points that represent the density of villous tissue, equispaced within an ellipsoidal geometry    
datapoints_villi=pg.equispaced_data_in_cuboid(n_seed,x_dim,y_dim,z_dim)
if(export_intermediates):
    export_file = export_directory + '/villous_data'
    pg.export_ex_coords(datapoints_villi,'villous',export_file,'exdata')


#Now grow a tree to these data points, optimised for larger trees
random_seed = 1
full_geom=pg.grow_large_tree(angle_max_ft, angle_min_ft, fraction_ft, min_length_ft, point_limit_ft, 0, 0, 0, datapoints_villi, seed_geom, random_seed)

print(full_geom['nodes'][:,1:6])
print(full_geom['elems'])
# Export the final results
if(export_results or export_intermediates):
    export_file = export_directory + '/full_tree'
    pg.export_ex_coords(full_geom['nodes'],'placenta', export_file,'exnode')
    pg.export_exelem_1d(full_geom['elems'],'placenta', export_file)
    export_file = export_directory + '/terminals'
    pg.export_ex_coords(full_geom['term_loc'],'villous',export_file,'exdata')

