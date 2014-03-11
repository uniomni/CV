"""Extract deaggregation data from files such as

    deaggregation-3727
    
where 3727 is the id of the gauge that has been deaggregated.

The header of this format is as follows

lon lat depth return-periods....


The data lines have the format

lon lat ? values.....

To use:

python extract_deaggregation_data.py deaggregation-3727 --config deaggregation_config.py


"""

import sys, os
from getopt import gnu_getopt, GetoptError

def convert_deaggregation_file(filename, config_filename):

    basename, ext = os.path.splitext(filename)
    if ext == '': ext = '.txt'
    
    fid = open(filename)
    lines = fid.readlines()
    fid.close()

    header = lines[0].split()

    deagg_longitude = float(header[0]) 
    deagg_latitude = float(header[1])     

    location_id = int(basename.split('-')[-1])
    print "location_id", location_id
    
    # Name and open files
    outfiles = []
    outfilenames = []
    for val in header[3:]:
        outfilename = basename + '_lon%.3f_lat%.3f'\
            %(deagg_longitude, deagg_latitude)\
            + '_%s' %float(val) + ext
            
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
            val = fields[i+2] # Values start in the second column
            # FIXME (Ole): Format may change.

            fid.write('%s %s %s\n' %(lon, lat, val))

    # Close
    for fid in outfiles:
        fid.close()
        
    # Hey let's do the KML conversion too
    print 'Now convert them all to KML'
    for outfilename in outfilenames:
        print
        s = 'python convert_xyz2kml.py %s' %outfilename

        # Strip value from filename (hardwired to hazard maps)
        basename, ext = os.path.splitext(outfilename)        
        i0 = basename.rfind('_')
        slice = basename[i0+1:]
        header_value = float(slice)
        
        if header_value > 10000: continue
        
        if config_filename is not None:
            s += ' --config %s' %config_filename

        # Create name - Note this cannot be too long due to limitations in psscale
        kml_name = 'Deaggregation at %.3f, %.3f for RP %d years'\
            %(deagg_longitude, deagg_latitude, int(header_value))

        s += ' --kml_name "%s"' %kml_name
        s += ' --additional_point "%f, %f"' %(deagg_longitude, deagg_latitude)
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


    convert_deaggregation_file(sys.argv[1], config_filename)

                           
