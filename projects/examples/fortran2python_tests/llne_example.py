"""Example of how to convert between latlons and northing-eastings.

  This routine relies on the fortran functions ne2ll.f and ll2ne.f
  that must be compiled with f2py as follows

  Windows:
    f2py -c -m ne2ll ne2ll.f

  Linux
    f2py -c --fcompiler=Gnu -m ne2ll ne2ll.f


  (and similar for ll2ne.f).    
"""

#Convert from latlons to UTM

from ll2ne import ll2ne

#Canberra
lat = -35.2231249415
lon = 143.9264955278

northing, easting, zone, hemisphere = ll2ne(lat, lon)

print 'Canberra:'
print '---------------------'
print 'Latitude:\t', lat
print 'Longitude:\t', lon
print 'UTM Zone:\t', zone
print 'Easting:\t', easting
print 'Northing:\t', northing
print 'Hemisphere:\t', hemisphere


#Convert from UTM to latlons

from ne2ll import ne2ll

latitude, longitude = ne2ll(northing, easting, zone, hemisphere)

print
print 'Check:'
print '---------------------'
print 'Latitude:\t', latitude
print 'Longitude:\t', longitude
