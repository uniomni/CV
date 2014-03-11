""" This script runs everything needed to produce the 
Australian Tsunami Hazard Map

Ole Nielsen 2008
"""
        
import os

#s = '/bin/rm -rf data'
#print s
#os.system(s)
#
#s = 'svn up'
#print s
#os.system(s)

tasks = []

tasks.append(['extract_hazard_map_data.py', 
             'data/hazard_maps/wave_amplitude.txt',
             'amplitude_config.py'])
             
             
tasks.append(['extract_hazard_map_data.py', 
             'data/hazard_maps/probability_of_exceedance.txt',
             'probability_config.py'])             

ddir = 'data/deaggregations'             
for filename in os.listdir(ddir):
    if filename.startswith('deaggregation-'):
    
        #if filename.startswith('DP-grn-rp-'):
        #location_id = filename.split('-')[-1]
        #newname = 'deaggregation-%s' %location_id + '.txt'
        #print os.path.join(ddir, filename), os.path.join(ddir, newname)
        #os.rename(os.path.join(ddir, filename), os.path.join(ddir, newname))
        
        tasks.append(['extract_deaggregation_data.py', 
                      '%s' %os.path.join(ddir, filename),
                      'deaggregation_config.py'])                         
                       

                                    
for task in tasks:
    command = 'python '
    command += '%s %s ' %(task[0], task[1])
    command += '--config %s' %task[2]

    print
    print '=================================='
    print command
    print '=================================='    
    os.system(command)

    command = 'rsync -avz --exclude ".svn" --exclude "*.txt" data/* '
    command += """onielsen@cyclone:'"nhip/tsunami/National Hazard/PTHA08_Google_Earth_files"'"""
    print command
    os.system(command + ' &')
