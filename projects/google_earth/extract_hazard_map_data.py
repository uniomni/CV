"""Extract hazard map data from files such as

    probability_of_exceedance.txt
    wave_amplitude.txt


This script creates output files based on the first two columns of the input file (lon, lat) and one of the data columns (3, 4, 5, ....).

This script will use information in the first line to name each output file

Use amplitude_config.py with wave_amplitude.txt and probability_config.py with
probability_of_exceedance.txt.

It is assumed that that the three first columns are lon, lat, depth


To use:

python extract_hazard_map_data.py wave_amplitude.txt --config amplitude_config.py
python extract_hazard_map_data.py probability_of_exceedance.txt --config probability_config.py


"""

import sys, os
from getopt import gnu_getopt, GetoptError

def convert_hazard_file(filename, config_filename):

    basename, ext = os.path.splitext(filename)
    fid = open(filename)
    lines = fid.readlines()
    fid.close()

    header = lines[0].split()

    # Name and open files
    outfiles = []
    outfilenames = []
    for val in header:
        outfilename = basename + '_%s' %float(val) + ext
        outfilenames.append(outfilename)

        print 'Opening %s for writing' %outfilename
        outfile = open(outfilename, 'w')
        outfiles.append(outfile)

    # Output selected data
    print 'Writing'
    for line in lines[1:]:
        fields = line.split()

        lon = fields[0]
        lat = fields[1]
        depth = fields[2]

        for i, fid in enumerate(outfiles):
            val = fields[i+3] # Values start in the third column

            fid.write('%s %s %s\n' %(lon, lat, val))

    # Close
    for fid in outfiles:
        fid.close()
        
    # Hey let's do the KML conversion too
    print 'Now convert them all to KML'
    for outfilename in outfilenames:
        s = 'python convert_xyz2kml.py %s' %outfilename

        # Strip value from filename (hardwired to hazard maps)
        basename, ext = os.path.splitext(outfilename)        
        i0 = basename.rfind('_')
        slice = basename[i0+1:]
        header_value = float(slice)
        
        if config_filename is not None:
            s += ' --config %s' %config_filename

            # Infer kml name from name of config file and
            # omit certain values.
            # This bit is rather hardwired
            if config_filename.startswith('amplitude'):
            
                if int(header_value) > 10000: continue
                
                kml_name = 'Exceedance return period = %d years'\
                 %int(header_value)
            elif config_filename.startswith('probability'):
            
                if float(header_value) > 6.0: continue                
            
                kml_name = 'Wave amplitude %.1f m' %float(header_value)                
            else:
                kml_name = 'Header = %s' %str(header_value)
        else:
            kml_name = 'Header = %s' %str(header_value)                


        s += ' --kml_name "%s"' %kml_name
        print s
        os.system(s)

        

def usage():
    s = 'Usage:\n'
    s += '  python %s filename --config config_file.py' %sys.argv[0]
    return s
    


if __name__ == '__main__':


    try:
        optlist, args = gnu_getopt(sys.argv[1:], 'hc:', ['help', 'config='])
    except GetoptError, err:
        # print help information and exit:        
        msg = str(err) + '\n' + usage() 
        raise Exception, msg


    in_filename = args[0]

    config_filename = None
    for o, a in optlist:
        if o == '-v':
            verbose = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--config'):
            config_filename = a
        else:
            msg = 'unhandled option'
            raise Exception, msg


    convert_hazard_file(sys.argv[1], config_filename)

                           
