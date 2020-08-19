#!/usr/bin/env python
import os
import placentagen as pg
import numpy as np
 
##########################################
# Parameters that define placental shape #
##########################################
#volume of ellipsoid 
volume=427.0*1000 #mm^3
#thickness of ellipsoid (z-axis dimension)
thickness=24.8 #mm
#ellipticity  - ratio of y to x axis dimensions
ellipticity=1.00 #no units

###########################################
# Parameters that define the initial tree #
###########################################
#x and y coordinates of cord insertion point
cord_insertion_x=0.0
cord_insertion_y=0.0
#distance between the two umbilical arteries
umb_artery_distance=20.0 #mm
#length of umbilical artery included in the model
umb_artery_length=20.0


###############################################################
# Parameters that define branching over the chorionic surface #
###############################################################
#Number of chorionic seed points targeted
n_chorion=32
#Maximum angle between two branches
angle_max =  90 * np.pi /180
#Minimum angle between two branches
angle_min = 5 * np.pi /180
#Fraction that the branch grows toward data group centre of mass at each iteration
fraction_chorion =   0.5
#Minimum length of a branch
min_length =  5.0 #mm
#minimum number of data points that can be in any group after a data splitting proceedure
point_limit =  1
#Length of stem villi
sv_length = 2.0

###############################################################
# Parameters that define branching within the placenta volume #
###############################################################
#Number of seed points targeted for growing tree
n_seed=32000
#Maximum angle between two branches
angle_max_ft =  100 * np.pi /180
#Minimum angle between two branches
angle_min_ft = 0 * np.pi /180
#Fraction that the branch grows toward data group centre of mass at each iteration
fraction_ft =   0.4
#Minimum length of a branch
min_length_ft =  1.0 #mm
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

 
#Create seed points on the chorionic surface of the ellipsoid
datapoints_chorion=pg.uniform_data_on_ellipsoid(n_chorion,volume,thickness,ellipticity,0)
if(export_intermediates):
    export_file = export_directory + '/chorion_data'
    pg.export_ex_coords(datapoints_chorion,'chorion', export_file,'exdata')
 
#Establish a seed geometry from which to grow, this needs to have at least two generations of branching and can be read in, or generated
#from libraries.
seed_geom=pg.umbilical_seed_geometry(volume,thickness,ellipticity,cord_insertion_x,cord_insertion_y,umb_artery_distance,umb_artery_length,datapoints_chorion)

if(export_intermediates):
    export_file = export_directory + '/umbilical_geom'
    pg.export_ex_coords(seed_geom['nodes'],'umb',export_file,'exnode')
    pg.export_exelem_1d(seed_geom['elems'],'umb',export_file)
 
#Conduct an on surface branching algorithm that grows over the chorionic surface
chorion_geom=pg.grow_chorionic_surface(angle_max, angle_min, fraction_chorion, min_length, point_limit,volume, thickness, ellipticity, datapoints_chorion, seed_geom,'surface')
 
if(export_intermediates):
    export_file = export_directory + '/chorion_geom'
    pg.export_ex_coords(chorion_geom['nodes'],'chorion',export_file,'exnode')
    pg.export_exelem_1d(chorion_geom['elems'],'chorion',export_file)

#Refine once from defined element number (dont refine umbilical cord)
from_elem=5
#define whether to project onto an ellipsoidal surface (refine code works without projection too, but will just keep split elements with their original structure)
project={}
project['status'] = True
project['z_radius'] =thickness/2.0
project['x_radius']=np.sqrt(volume * 3.0 / (4.0 * np.pi * ellipticity * project['z_radius'] ))
project['y_radius'] =ellipticity * project['x_radius']
#actual refine step.
refined_geom=pg.refine_1D(chorion_geom,from_elem,project)
if(export_intermediates):
    export_file = export_directory + '/refined_chorion_geom'
    pg.export_ex_coords(refined_geom['nodes'],'chorion',export_file,'exnode')
    pg.export_exelem_1d(refined_geom['elems'],'chorion',export_file)

#Add stem villi
if(export_results):
    export_file = export_directory + '/stem_xy.txt'
    chorion_and_stem = pg.add_stem_villi(refined_geom,from_elem,sv_length,True, export_file)
else:
    chorion_and_stem = pg.add_stem_villi(refined_geom,from_elem,sv_length,False, 'stem_xy.txt')
if(export_intermediates):
    export_file = export_directory + '/final_chorion_geom'
    pg.export_ex_coords(chorion_and_stem['nodes'],'chorion',export_file,'exnode')
    pg.export_exelem_1d(chorion_and_stem['elems'],'chorion',export_file)
    
#Define data points that represent the density of villous tissue, equispaced within an ellipsoidal geometry    
datapoints_villi=pg.equispaced_data_in_ellipsoid(n_seed,volume,thickness,ellipticity)
if(export_intermediates):
    export_file = export_directory + '/villous_data'
    pg.export_ex_coords(datapoints_villi,'villous',export_file,'exdata')


#Now grow a tree to these data points, optimised for larger trees
full_geom=pg.grow_large_tree(angle_max_ft, angle_min_ft, fraction_ft, min_length_ft, point_limit_ft, volume, thickness, ellipticity, datapoints_villi, chorion_and_stem)

# Export the final results
if(export_results or export_intermediates):
    export_file = export_directory + '/full_tree'
    pg.export_ex_coords(full_geom['nodes'],'placenta', export_file,'exnode')
    pg.export_exelem_1d(full_geom['elems'],'placenta', export_file)
    export_file = export_directory + '/terminals'
    pg.export_ex_coords(full_geom['term_loc'],'villous',export_file,'exdata')
