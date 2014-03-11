"""Convert xyz to kml

Convert text file with format

Longitude (degrees) Latitude (degrees) Amplitude (metres)

into a kml file for use with Google Earth showing amplitudes as bargraphs.

"""

import sys
import os.path
import time
import math
from Numeric import array, allclose
from getopt import gnu_getopt, GetoptError
from gmt_interface import CPT


#Rectangular region of interest 

# Australia
# northern_boundary = 0
# southern_boundary = -80
# western_boundary = 80
# eastern_boundary = 180

# World
northern_boundary = southern_boundary = western_boundary = eastern_boundary = None


def read_file(filename):
    """Read file and return list of triplets:
    [longitude, latitude, amplitude]
    """

    base, ext = os.path.splitext(filename)
    #print 'ext', ext
    if ext == '.csv':
        sep = ','
    else:
        sep = None
        
    
    points = []
    fid = open(filename)
    for line in fid.readlines():
        fields = line.split(sep)
        
        try:
            lon = float(fields[0])
        except:
            # Probably a header
            continue
        
        if lon > 180: lon -= 360 # Put into [-180, 180]
        
        lat = float(fields[1])
        try:
            amp = float(fields[2])
        except:
            # No amplitude present
            amp = 1

        if western_boundary is not None and\
           easter_boundary is not None and\
           northern_boundary is not None and\
           southern_boundary is not None:
               if western_boundary < lon < eastern_boundary and\
                      southern_boundary < lat < northern_boundary: 
                   points.append([lon, lat, amp])
        else:
            points.append([lon, lat, amp])            
            
                
    fid.close()    

    return points



def float2hexstring(x):    
    """Convert to hexadecimal strings 
    """

    n = int(x)
    assert 0 <= n <= 255

    s = str(hex(n))[2:] #strip leading '0x'

    if len(s) == 1:
        s = '0' + s #Append leading 0
        
    return s    



def generate_kml_header(filename, 
                        kml_name, 
                        additional_point=None):
                        
    s = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
  <name>%s</name>
  <open>1</open>
  <description><![CDATA[Converted from file %s on %s]]></description>
  """ %(kml_name, filename, time.ctime())

    if additional_point is not None:
        # Use special point to set initial view using LookAt
        s += """<LookAt>
  <longitude>%f</longitude>      
  <latitude>%f</latitude>        
  <altitude>0</altitude>        
  <heading>0</heading>          
  <tilt>5</tilt>                
  <range>1000000</range>               
  <altitudeMode>relativeToGround</altitudeMode>
</LookAt>
""" %(additional_point[0], additional_point[1])

    return s
  
def generate_kml_footer():
    return """</Document>
</kml>"""    



def generate_one_colour_style(point, min_amp, max_amp, cpt,
                              colour_override=None,
                              transparency='AA'):
    """Generate colours based on amplitude
    
    colour_override: Use this colour irrespective of amplitude
    transparency: 00 is tranparent, FF is solid. Default = 'AA'
    """
   
    amp = float(point[2])

    if colour_override is None:
        if allclose(min_amp, max_amp):
            # All amplitudes are equal
            normalised_amp = min_amp
            
            if allclose(normalised_amp, 0.0):
                colour = '333333' # Dark Grey
            else:                 
                colour = '999999' # Grey 
        else:    
            normalised_amp = (amp-min_amp)/(max_amp-min_amp) # In [0,1]
            normalised_amp = math.sqrt(normalised_amp) # Bias upwards
            
            red, green, blue = cpt.get_color(normalised_amp)
            
            RED = float2hexstring(red)
            BLUE = float2hexstring(blue)
            GREEN = float2hexstring(green)    
            
            colour = (BLUE + GREEN + RED).upper() # The order used in KML
            
        style_id = '%.3f' %amp    
    else:
        colour = colour_override
        style_id = 'override'

            


    kml = """  <Style id="%s">
    <LineStyle>
      <color>FF%s</color>
      <width>0.4</width>
    </LineStyle>
    <PolyStyle>
      <outline>1</outline>
      <fill>1</fill>
      <color>%s%s</color>
    </PolyStyle>
    <IconStyle>  
      <scale>0.1</scale>                    
      <Icon><href>1_pixel_white.png</href></Icon>      
    </IconStyle>
    <BalloonStyle>
      <color>FFA56A</color>
    </BalloonStyle>           
  </Style>
"""  %(style_id, colour, transparency, colour)


    return kml


    
def generate_one_bar(point, width, scale, description=None,
                     use_override=False):

    # Extract values
    lon = float(point[0])
    lat = float(point[1])
    amp = float(point[2])

    
    if use_override is True:
        style_id = 'override'    
    else:        
        style_id = '%.3f' %amp    



        
    # Define extent of polygon
    west = lon - width
    east = lon + width
    north = lat + width
    south = lat - width

    height = amp*scale

    if description is not None:
        # Use template from config file.
        # It assumes string interpolation with one float
        try:
            s = description %amp
        except ValueError, e:
            msg = 'Legend string must have one and only one string interpolator of the form %f:'
            msg += ' I got "%s". ' %description
            msg += 'ValueError: ' + str(e)
            raise ValueError, msg
        except TypeError, e:
            # Not all arguments converted - string might not have a interpolator.
            # In this case use it as is.
            s = description
        
            
        caption = '<h1><table width="500"><tr><td>%s</td></tr></table></h1>' %s
    else:
        caption = ''
        
    kml = """
       <Placemark>
         <name></name>
         <description><![CDATA[%s]]></description>
         <styleUrl>#%s</styleUrl>
         <MultiGeometry>
         <Polygon>
           <extrude>1</extrude>
           <altitudeMode>relativeToGround</altitudeMode>
           <outerBoundaryIs>
           <LinearRing>
             <coordinates>
               %.5f,%.5f,%.1f
               %.5f,%.5f,%.1f
               %.5f,%.5f,%.1f
               %.5f,%.5f,%.1f
               %.5f,%.5f,%.1f               
             </coordinates>
           </LinearRing>
           </outerBoundaryIs>
         </Polygon>
         <Point>
           <Visibility>1</Visibility>
           <altitudeMode>relativeToGround</altitudeMode>
           <coordinates>%.5f,%.5f,%.1f</coordinates>
         </Point>
         </MultiGeometry>
       </Placemark>""" %(caption, style_id,
                         west, north, height,
                         west, south, height,
                         east, south, height,
                         east, north, height,
                         west, north, height,
                         (west+east)/2, (south+north)/2, height)

    return kml


def create_kml_code(points, width, scale, cpt, 
                    kml_name,
                    legend_string,
                    additional_point=None,
                    directory='.',
                    units=''):
    """Create kml code based on points (lat, lon, amplitude)
    """

    # Determine range of amplitudes
    min_amp = points[0][2]
    max_amp = min_amp
    for point in points:
        if point[2] > max_amp: max_amp = point[2]
        if point[2] < min_amp: min_amp = point[2]        

    print 'Minimum amplitude = ', min_amp
    print 'Maximum amplitude = ', max_amp
    #print 'Scale =             ', scale
    
    
    kml_code = ''
    # Generate colour styles
    for point in points:
        kml_code += generate_one_colour_style(point, min_amp, max_amp, cpt,
                                              transparency='AA')    
    
    if additional_point is not None:
        # Use white for special point
        kml_code += generate_one_colour_style(additional_point, 0.0, 0.0, cpt,
                                              colour_override='FFFFFF',
                                              transparency='FF')        

    # Generate bars
    kml_code += """  <Folder>
    <name>Tsunami hazard map</name>
    <open>0</open>"""

    for point in points:
        kml_code += generate_one_bar(point, width, scale, 
                                     kml_name + '.<br>' +\
                                         legend_string + '.')    

    if additional_point is not None:
        kml_code += generate_one_bar(additional_point, 
                                     2*width,
                                     scale,
                                     kml_name + '. Target Point.',
                                     use_override=True)
                                     
                                     
    # Create legend for colour coding
    legend_filename = cpt.create_legend_for_colour_coding(min_amp, 
                                                          max_amp, 
                                                          kml_name,
                                                          units=units,
                                                          directory=directory)

     
    # Strip pathname off    
    _, legend_filename = os.path.split(legend_filename)
    
    legend =\
'''\n
    <ScreenOverlay id="khScreenOverlay756">
        <name>legend</name>
            <Icon>
                <href>%s</href>
            </Icon>
            <overlayXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>
            <screenXY x="0.15" y="0.13" xunits="fraction" yunits="fraction"/>
            <size x="0.25" y="0" xunits="fraction" yunits="fraction"/>
    </ScreenOverlay>''' %legend_filename

    kml_code += legend


    # End kml code and return
    kml_code += """  </Folder>"""
    return kml_code


def write_file(kml_code, filename):
    fid = open(filename, 'w')
    fid.write(kml_code)
    fid.close()
    

def usage():
    s = 'Usage:\n'
    s += '  python %s filename --config config_file.py --kml_name kml_name' %sys.argv[0]
    return s
    

if __name__ == '__main__':

    try:
        optlist, args = gnu_getopt(sys.argv[1:], 'hc:k:a:', ['help', 
                                                           'config=', 
                                                           'kml_name=',
                                                           'additional_point='])
    except GetoptError, err:
        # print help information and exit:        
        msg = str(err) + '\n' + usage() 
        raise Exception, msg

    if len(args) == 0:
        msg = usage() 
        raise Exception, msg        
        
    in_filename = args[0]
    output = None
    verbose = False
    config_filename = None
    kml_name = ''
    additional_point = '' # Additional reference point (e.g. for deaggregation maps)
    for o, a in optlist:
        if o == '-v':
            verbose = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--config'):
            config_filename = a
        elif o in ('-k', '--kml_name'):
            kml_name = a
        elif o in ('-a', '--additional_point'):
            additional_point = a            
        else:
            msg = 'unhandled option'
            raise Exception, msg

        
    if config_filename is not None:
        # Import configuration file
        config, ext = os.path.splitext(config_filename)
        config=__import__(config)
        
        # Bar dimensions 
        scale = config.vertical_scale
        width = config.bar_width

        # Colour scheme
        palette_file = config.palette_file
        cpt = CPT(palette_file)

        # Legend template
        legend_string = config.legend_string 
        
        # Units shown in legend and balloons
        units = config.units
    else:
        # Make some defaults
        scale = 300000
        width = 0.03
        cpt = CPT()
        cpt.segments.append([array([0., 1.]),
                             array([0., 0., 0.]),
                             array([1., 1., 1.])])
        legend_string = ''
        units = ''

    
    # Assign filenames and extensions
    base, ext = os.path.splitext(in_filename)
    if ext == '': in_filename = base + '.txt'
    out_filename = base + '.kml'

    directory, _ = os.path.split(base)
    
    
    # Read data    
    print 'Reading from file %s' %in_filename
    points = read_file(in_filename)

    if additional_point != '':
        fields = additional_point.split(',')
        longitude = float(fields[0])
        latitude = float(fields[1])        
        
        print 'Got additional point: %f, %f' %(longitude, latitude)
        
        #points.append([longitude, latitude, 0.0])
        additional_point = [longitude, latitude, 0.0]
    else:
        additional_point = None
                                     
    
    
    # Generate KML
    kml_header = generate_kml_header(in_filename, 
                                     kml_name,
                                     additional_point)
    #print kml_header

    
    
    kml_code = create_kml_code(points, width, scale, cpt, 
                               kml_name,
                               legend_string,
                               additional_point=additional_point,
                               directory=directory,
                               units=units)
    #print kml_code
    
    kml_footer = generate_kml_footer()
    #print kml_footer

    print 'Writing to file %s' %out_filename
    write_file(kml_header + kml_code + kml_footer, out_filename)



