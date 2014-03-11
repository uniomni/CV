import unittest

from gmt_interface import CPT, format_string
from Numeric import zeros, array, allclose
from tempfile import mkstemp

import os
test_filename = 'test_palette.cpt'


class Test_gmt(unittest.TestCase):
    def setUp(self):
        fid = open(test_filename, 'w')
        fid.write('# cpt file created by unit test\n')
        fid.write('#COLOR_MODEL = RGB\n')
        fid.write('#\n')
        fid.write('0 0 0 0 3 85 85 85 L\n')
        fid.write('3 85 85 85 6 170 170 170\n')
        fid.write('6 170 170 170 9 255 255 255 U\n')
        fid.write('B 0 0 0\n')
        fid.write('F 255 255 255\n')
        fid.write('N 128 128 128\n')
        fid.close()
        

    def tearDown(self):
        os.remove(test_filename)


    def test_that_cpt_can_be_read(self):
        
        cpt = CPT(test_filename)

        assert allclose(cpt.background_color, [0,0,0])
        assert allclose(cpt.foreground_color, [255,255,255])
        assert allclose(cpt.nan_color, [128,128,128])        
        assert cpt.color_model == 'RGB'
                

        assert allclose(cpt.segments[0].lower_bound, 0)
        assert allclose(cpt.segments[0].upper_bound, 3)
        
        assert allclose(cpt.segments[1].lower_bound, 3)
        assert allclose(cpt.segments[1].upper_bound, 6)        
        
        assert allclose(cpt.segments[2].lower_bound, 6)
        assert allclose(cpt.segments[2].upper_bound, 9)                
                
        assert allclose(cpt.segments[0].rgb_min, [0,0,0])
        assert allclose(cpt.segments[0].rgb_dif, [85,85,85])
        
        assert allclose(cpt.segments[1].rgb_min, [85,85,85])        
        assert allclose(cpt.segments[1].rgb_dif, [170-85,170-85,170-85])        
        
        assert allclose(cpt.segments[2].rgb_min, [170,170,170])
        assert allclose(cpt.segments[2].rgb_dif, [85,85,85])        
        
        assert cpt.segments[0].color_segment_boundary == 'L'
        assert cpt.segments[1].color_segment_boundary == ''
        assert cpt.segments[2].color_segment_boundary == 'U'                
        
                        
    def test_cpt_interpolation(self):
        
        cpt = CPT(test_filename)

        assert allclose(cpt.get_color(0), 0)
        assert allclose(cpt.get_color(3), 85) 
        assert allclose(cpt.get_color(6), 170)
        assert allclose(cpt.get_color(9), 255)
                 
        assert allclose(cpt.get_color(1), 28.3333333333) 
        assert allclose(cpt.get_color(1.5), 42.49999999)
        assert allclose(cpt.get_color(4.5), 85+42.49999999)        
        

        #How does this work?
        #assert allclose(cpt.get_color(-1000), 0)                              
        #assert allclose(cpt.get_color(1000), 0)                                      

    def test_generation_of_cpt_file(self):
        """test_generation_of_cpt_file

        This is a test of __repr__ being the inverse of __init__        
        """

        cpt1 = CPT(test_filename)
        
        tmp_fd , tmp_name = mkstemp(suffix='.cpt', dir='.')
        fid = os.fdopen(tmp_fd, 'w')
        
        fid.write(str(cpt1))
        fid.close()


        # Read it back
        cpt2 = CPT(tmp_name)
        
        assert cpt2.segments[0].color_segment_boundary == 'L'
        assert cpt2.segments[1].color_segment_boundary == ''
        assert cpt2.segments[2].color_segment_boundary == 'U'                
                

        # ... and compare
        assert str(cpt1) == str(cpt2)

        # Clean up
        os.remove(tmp_name)

    def test_remapping(self):
        """Test that threshold values can be rescaled
        """

        cpt = CPT(test_filename)        

        cpt.normalise()
        
        assert allclose(cpt.segments[0].lower_bound, 0)
        assert allclose(cpt.segments[0].upper_bound, 1./3)
        
        assert allclose(cpt.segments[1].lower_bound, 1./3)
        assert allclose(cpt.segments[1].upper_bound, 2./3)        
        
        assert allclose(cpt.segments[2].lower_bound, 2./3)
        assert allclose(cpt.segments[2].upper_bound, 1.0)                
        
        # Test that colours and flags are unchanged
        assert allclose(cpt.segments[0].rgb_min, [0,0,0])
        assert allclose(cpt.segments[0].rgb_dif, [85,85,85])
        
        assert allclose(cpt.segments[1].rgb_min, [85,85,85])        
        assert allclose(cpt.segments[1].rgb_dif, [170-85,170-85,170-85])        
        
        assert allclose(cpt.segments[2].rgb_min, [170,170,170])
        assert allclose(cpt.segments[2].rgb_dif, [85,85,85])        
        
        assert cpt.segments[0].color_segment_boundary == 'L'
        assert cpt.segments[1].color_segment_boundary == ''
        assert cpt.segments[2].color_segment_boundary == 'U'                


        cpt.rescale(-10, 20)
        assert allclose(cpt.segments[0].lower_bound, -10)
        assert allclose(cpt.segments[0].upper_bound, 0)
        
        assert allclose(cpt.segments[1].lower_bound, 0)
        assert allclose(cpt.segments[1].upper_bound, 10)        
        
        assert allclose(cpt.segments[2].lower_bound, 10)
        assert allclose(cpt.segments[2].upper_bound, 20)                        
        

        # Test that colours and flags are unchanged
        assert allclose(cpt.segments[0].rgb_min, [0,0,0])
        assert allclose(cpt.segments[0].rgb_dif, [85,85,85])
        
        assert allclose(cpt.segments[1].rgb_min, [85,85,85])        
        assert allclose(cpt.segments[1].rgb_dif, [170-85,170-85,170-85])        
        
        assert allclose(cpt.segments[2].rgb_min, [170,170,170])
        assert allclose(cpt.segments[2].rgb_dif, [85,85,85])        
        
        assert cpt.segments[0].color_segment_boundary == 'L'
        assert cpt.segments[1].color_segment_boundary == ''
        assert cpt.segments[2].color_segment_boundary == 'U'                


        

    def test_create_legend(self):
        """Test that this can run and that file is generated
        """
        
        cpt = CPT(test_filename)        
        legend_filename = cpt.create_legend_for_colour_coding(-10, 20, 
                                                               'Test legend')


        assert os.path.exists(legend_filename)
        
        # Cleanup
        os.remove(legend_filename)
        

    def test_format_string(self):
        
        f = format_string(10)
        assert f == '%.f'
        
        f = format_string(204)
        assert f == '%.f'        
        
        f = format_string(1.0)
        assert f == '%.f'        
        
        f = format_string(0.0)
        assert f == '%.f'                
        
        f = format_string(0.2)
        assert f == '%.1f'                
        
        f = format_string(0.212)
        assert f == '%.1f'                        
        
        f = format_string(0.267)
        assert f == '%.1f'                                
        
        f = format_string(0.03267)
        assert f == '%.2f'                                                
        
        f = format_string(0.07267)
        assert f == '%.2f' 
        
        f = format_string(0.00267)
        assert f == '%.3f'                                        
        
        f = format_string(0.00867)
        assert f == '%.3f'                                        
        
        f = format_string(0.000567)
        assert f == '%.4f'        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_gmt, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
        
