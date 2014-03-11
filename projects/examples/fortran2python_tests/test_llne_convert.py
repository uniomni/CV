"""Test of conversion modules ll2ne and ne2ll.
"""

import unittest

import sys
if sys.platform == 'win32':
    F2PY = 'f2py -c'
elif sys.platform == 'linux2':
    F2PY = 'f2py -c --fcompiler=Gnu'    


class TestCase(unittest.TestCase):

    def setUp(self):
        """Compile fortran extension using f2py
        """

        self.eps = 1.0e-11
        try:
            import ll2ne
        except:    
            import os
        
            cmd = F2PY + ' -m ll2ne ll2ne.f'
            print cmd
            os.system(cmd)
            import ll2ne    

        try:
            import ne2ll
        except:    
            import os
        
            cmd = F2PY + ' -m ne2ll ne2ll.f'
            print cmd
            os.system(cmd)
            import ne2ll    
        

    def xxxtest_compile(self):
        """Test compilation of fortran extension using f2py
        """

        import os
        
        cmd = 'f2py -c -m ll2ne ll2ne.f'
        print cmd
        err = os.system(cmd)

        assert err == 0
        
        try:
            import ll2ne            
        except:
            msg = 'Fortran extension could not be imported'
            raise msg
        

    def test_ll2ne(self):
        """Basic test of ll2ne"""
        
        from ll2ne import ll2ne #, ne2ll

        lat = -(37.0 + (39.0 + 10.15611/60.0)/60.0)
        lon = (143.0 + (55.0 + 35.383900/60.0)/60.0)

        northing, easting, zone, hemisphere = ll2ne(lat, lon)

        assert abs(northing - 5828674.33975)/abs(northing) < self.eps
        assert abs(easting - 758173.79727)/abs(easting) < self.eps
        assert zone == 54
        assert hemisphere == 'S'        


    def test_ll2ne_bounds(self):
        """test of ll2ne's bounds"""
        
        from ll2ne import ll2ne #, ne2ll

        northing, easting, zone, h = ll2ne(-90, 0)
        northing, easting, zone, h = ll2ne(90, 0)
        northing, easting, zone, h = ll2ne(0, -180)
        northing, easting, zone, h = ll2ne(0, 180)        

    def test_ll2ne_outofbounds(self):
        """Test that ll2ne gives an error if lat or lon are out of bounds
        """

        from ll2ne import ll2ne
        self.failUnlessRaises(Exception, ll2ne, -90.1, 0)
        self.failUnlessRaises(Exception, ll2ne, 90.1, 0)
        self.failUnlessRaises(Exception, ll2ne, 0, 180.1)
        self.failUnlessRaises(Exception, ll2ne, 0, -180.1)                        
        
    def test_ne2ll(self):
        """Basic test of ne2ll"""
        
        from ne2ll import ne2ll


        #Buninyong
        northing = 5828259.03807        
        easting = 228854.052
        zone = 55
        hemisphere = 'S'
       
        lat, lon = ne2ll(northing, easting, zone, hemisphere)
        
        lat_ref = -(37.0 + (39.0 + 10.15611/60.0)/60.0)
        lon_ref = (143.0 + (55.0 + 35.383900/60.0)/60.0)

        assert abs(lat - lat_ref)/abs(lat) < self.eps
        assert abs(lon - lon_ref)/abs(lon) < self.eps


    def test_ll2ne2ll(self):
        """Test conversions back and forward"""        

        from ne2ll import ne2ll
        from ll2ne import ll2ne

        eps = 1.0e-6  #Less accuracy
        
        latlons = [(-33.234, 149.32), (53.02,2.23421), (0,0), (40, -50),
                   (-36,0), (-50,-60), (-89.9,0), (-89,-2), (89.9,0),
                   (0, -180), (0, 180)]

        for lat, lon  in latlons:
            northing, easting, zone, hemisphere = ll2ne(lat, lon)            
            lat1, lon1 = ne2ll(northing, easting, zone, hemisphere)
            #print lat, lon, zone, easting, northing, hemisphere, lat1, lon1

            assert abs(lat - lat1) < eps, "%f, %f" %(lat, lat1)
            assert abs(lon - lon1) < eps, "%f, %f" %(lon, lon1)

            
    def xxxxtest_ne2ll2ne(self):
        """Test conversions back and forward"""        

        from ne2ll import ne2ll
        from ll2ne import ll2ne

        eps = 1.0e-6  #Less accuracy

        #Northings, eastings, zone and hemisphere
        nes = [(6320371.85657, 716174.605757, 55, 'S'),
               (1505230,345745,55,'N'), (1505230,345745,55,'S')] 
        for northing, easting, zone, hemisphere in nes:

            lat, lon = ne2ll(northing, easting, zone, hemisphere)
            northing1, easting1, zone1, hemisphere1 = ll2ne(lat, lon)

            print northing, northing1
            print easting, easting1
            
            assert abs(northing - northing1)/abs(northing) < eps,\
                   "%f %f" %(northing, northing1) 
            assert abs(easting - easting1)/abs(easting) < eps,\
                   "%f %f" %(easting, easting1)             
            assert zone == zone1
            assert hemisphere == hemisphere1
            
if __name__ == '__main__':
    mysuite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(mysuite)



