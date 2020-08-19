#!/usr/bin/env python

#This routine runs through the examples that are completed, generally published, and known to work and checks that
# the output of these examples matches up to their expected results. This will take several hours to run,
# but will ensure that the full scale models actually do what they should be. Our suggestion is to only run this if
# necessary, and where possible write and use simple testing on the lungsim libraries to fully test your changes to
# the code. This is not a unit test, its a large-scale simulation test.

import os
import compare_results as cr

def main():
    export_directory = 'output'

    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    everything_worked = True
    mydir = os.getcwd() # would be the same path as a.py
    export_logs_dir = mydir + '/' +  export_directory + '/'
    #--------------------------------------------------
    #Test 1 - Perfusion model - run model and check
    #-------------------------------------------------
    mydir_example1 = os.chdir("../fetoplacental/interface2015")
    mydir_example1 =os.getcwd()
    os.system('rm -rf output/*') #remove any files in the output directory
    os.system('python bloodflow_interface2015.py > '+ export_logs_dir + 'clark2015.log') #run the model -> export
    # terminal output to log file
    os.chdir(mydir)
    perfusion_worked = cr.compare_perfusion_clark2015()
    if(perfusion_worked):
        print('The Clark 2015 perfusion model works as expected')
    else:
        print('ERROR: The Clark 2015 perfusion model has FAILED')
        everything_worked = False

    #--------------------------------------------------
    #Test 1 - Perfusion model - two anastomoses
    #-------------------------------------------------
    mydir_example1 = os.chdir("../fetoplacental/two_umb_arteries")
    mydir_example1 =os.getcwd()
    os.system('rm -rf output/*') #remove any files in the output directory
    os.system('python bloodflow_two_umb_arteries.py > '+ export_logs_dir + 'byrne2020.log') #run the model -> export
    os.chdir(mydir)
    # terminal output to log file
    perfusion_worked = cr.compare_perfusion_byrne2020()
    if(perfusion_worked):
        print('The Byrne 2020 perfusion model works as expected')
    else:
        print('ERROR: The Byrne 2020 perfusion model has FAILED')
        everything_worked = False





    if(everything_worked):
        print('SUCCESS! Everything ran as expected')
    else:
        print('FAILURE! Please check your models, with errors as indicated above')

if __name__ == '__main__':
    main()
