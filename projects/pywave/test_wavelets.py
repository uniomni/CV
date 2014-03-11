import unittest
import Numeric
from wavelets import fwt, fwt2, ifwt, ifwt2, number_of_filters, scale_energy
from math import sqrt


class TestCase(unittest.TestCase):

    def setUp(self):
        pass


    def test_callfwt(self):
        """test that fwt can be called"""
        
        X = Numeric.array([[1,2,1],[3,4,3], [5,6,5], [7,8,7], [9.0,10,9]])
        Y=fwt(X)

    def test_callifwt(self):
        """test that ifwt can be called"""
        
        X = Numeric.array([[1,2,1],[3,4,3], [5,6,5], [7,8,7], [9.0,10,9]])
        Y=ifwt(X)


    def test_ifwt1D_basic(self):
        """test that ifwt1D works basically"""

        X = Numeric.ones(8, Numeric.Float)
        Y = fwt(X)
        X1 = ifwt(Y)
        assert Numeric.allclose(X-X1, 0)        
        
        
    def test_fwt1Da(self):
        """test that fwt1D works on constant vector: ones"""

        for j in range(1,9):
            N = 2**j
            for P in range(number_of_filters):
                D = 2*(P+1)

                X = Numeric.ones(N, Numeric.Float)
                Y = fwt(X, D)
                
                Y[0] -= sqrt(len(Y))
                assert Numeric.allclose(Y, 0)


    def test_ifwt1D_inverse_a(self):
        """test that ifwt1D works as an inverse to fwt"""

        for j in range(1,9):
            N = 2**j
            for P in range(number_of_filters):
                D = 2*(P+1)

                X = Numeric.ones(N, Numeric.Float)            
                Y = fwt(X, D)

                X1 = ifwt(Y, D)
                assert Numeric.allclose(X-X1, 0)


    def test_ifwt1D_inverse_b(self):
        """test that fwt1D works as an inverse to ifwt"""

        for j in range(1,9):
            N = 2**j
            for P in range(number_of_filters):
                D = 2*(P+1)

                X = Numeric.ones(N, Numeric.Float)            
                Y = ifwt(X, D)

                X1 = fwt(Y, D)
                assert Numeric.allclose(X-X1, 0)


    def test_fail_1D_length1(self):

        #from wavelets import LengthOneException
        
        N = 1
        X = Numeric.ones(N, Numeric.Float)

        self.assertRaises(Exception, fwt, X) 


    def test_fwt1Db(self):
        """test that fwt1D works on example vectors"""

        D = 4
        N = 8
        X = Numeric.zeros(N, Numeric.Float)

        for i in range(len(X)):
            X[i] = i+1
            
        Y = fwt(X, D)

        Y = Y - Numeric.array([12.72792206135786, -4.38134139536131,
                               0.36602540378444, -3.83012701892219,
                               0.0, 0.0, 0.0, -2.82842712474619]) 
        assert Numeric.allclose(Y, 0)



        
    def test_fwt1Dc(self):
        """test that fwt1D works as a 2D vector"""
        
        X = Numeric.ones(8, Numeric.Float)
        X = Numeric.reshape(X, (8,1))

        Y=fwt(X)

        Y[0][0] -= sqrt(len(Y))
        assert Numeric.allclose(Y, 0)        

    def test_fwt1Dc4(self):
        """test that fwt1D works on a 'random' vector, D=4"""

        #Matlab random vector
        X = Numeric.array([0.81797434083925, 0.66022755644160,\
                           0.34197061827022, 0.28972589585624,\
                           0.34119356941488, 0.53407901762660,\
                           0.72711321692968, 0.30929015979096])

        #Result from fwt(X, 4) in Matlab
        Y_ref = Numeric.array([1.42184125586417, -0.15394808354817,\
                               0.05192707167183, 0.37115044369886,\
                               -0.10770249228974, -0.08172091206233,\
                               0.29500215027890, 0.20196258114742])

        Y=fwt(X, 4)
        assert Numeric.allclose(Y-Y_ref, 0)        
                

    def test_fwt1Dc6(self):
        """test that fwt1D works on a 'random' vector, D=6"""

        #Matlab random vector
        X = Numeric.array([0.81797434083925, 0.66022755644160,\
                           0.34197061827022, 0.28972589585624,\
                           0.34119356941488, 0.53407901762660,\
                           0.72711321692968, 0.30929015979096])

        #Result from fwt(X, 6) in Matlab
        Y_ref = Numeric.array([1.42184125586417, -0.27979815817808,\
                               0.21836186329686, 0.17939935114879,\
                               0.00345049516774, 0.22893484261518,\
                               0.25762577687352, -0.18246978758220])

        Y=fwt(X, 6)
        assert Numeric.allclose(Y-Y_ref, 0)        
                



    def test_fwt1Dc8(self):
        """test that fwt1D works on a 'random' vector, D=8"""

        #Matlab random vector
        X = Numeric.array([0.81797434083925, 0.66022755644160,\
                           0.34197061827022, 0.28972589585624,\
                           0.34119356941488, 0.53407901762660,\
                           0.72711321692968, 0.30929015979096])

        #Result from fwt(X, 8) in Matlab
        Y_ref = Numeric.array([1.42184125586417, -0.27774330567583,\
                               0.26539391030148, 0.02521137886213,\
                               0.13638973750197, 0.31441497909028,\
                               -0.20260945655043, 0.05934606703242])


        Y=fwt(X, 8)
        assert Numeric.allclose(Y-Y_ref, 0)        
                

    def test_columnwise_fwt_a(self):
        """test thath columnwise fwt works"""
        
        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))


        Y=fwt(X)

        
        rows, cols = Y.shape
        for i in range(cols):
            Y[0,i] -= sqrt(rows)

        assert Numeric.allclose(Y, 0)
        
        
    def test_columnwise_fwt_b(self):
        """test thath columnwise fwt works"""
        
        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))

        for i in range(8):
            X[i,0] = i+1
            X[i,1] = 1
            X[i,2] = i+1
            X[i,3] = 2

        #Numeric.transpose(X))                    
        Y=fwt(X)

        Y_ref = Numeric.array([[12.72792206135786, sqrt(8), 12.72792206135786, sqrt(32)],
                               [-4.38134139536131, 0.0,     -4.38134139536131, 0.0],
                               [0.36602540378444,  0.0,     0.36602540378444,  0.0],   
                               [ -3.83012701892219, 0.0,     -3.83012701892219, 0.0],  
                               [ 0.0,               0.0,     0.0,               0.0],   
                               [ 0.0,               0.0,     0.0,               0.0],   
                               [ 0.0,               0.0,     0.0,               0.0],   
                               [ -2.82842712474619, 0.0,     -2.82842712474619, 0.0]])     
            
        Y -= Y_ref
        assert Numeric.allclose(Y, 0)
                               

    def test_fwt2a(self):
        """Simple 2D test.....
        """

        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))

        Y=fwt2(X)

        Y[0][0] -= sqrt(Numeric.product(Y.shape))
        assert Numeric.allclose(Y, 0)        
        
    

    def test_fwt2b(self):
        """Simple 2D test.....
        """

        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))

        Y=fwt2(X)

        Y[0][0] -= sqrt(Numeric.product(Y.shape))
        assert Numeric.allclose(Y, 0)        
        
    

    def test_fwt2c(self):


        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))

        for i in range(8):
            X[i,0] = 1
            X[i,1] = 2
            X[i,2] = 3
            X[i,3] = 4


        Y_ref = Numeric.array([[14.14213562373095, -4.89897948556636, 0.0, -4.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0],
                               [ 0.0,               0.0,     0.0,               0.0]])

        Y = fwt2(X)


        Y -= Y_ref
        assert Numeric.allclose(Y, 0)
        
        

    def test_fwt2d(self):


        X = Numeric.ones(8*4, Numeric.Float)
        X = Numeric.reshape(X, (8,4))

        for i in range(8):
            X[i,0] = i+1
            X[i,1] = 1
            X[i,2] = i+1
            X[i,3] = 2



        Y_ref = Numeric.array([[16.97056274847714, -1.93185165257814, 5.63397459621556, 6.3660254037844],
                               [-4.38134139536131, 0.0, -3.09807621135332, -3.09807621135332],
                               [ 0.36602540378444, 0.0, 0.25881904510252, 0.25881904510252],
                               [-3.83012701892219, 0.0, -2.70830878788570, -2.70830878788570], 
                               [ 0.0, 0.0,     0.0, 0.0],
                               [ 0.0, 0.0,     0.0, 0.0],
                               [ 0.0, 0.0,     0.0, 0.0],                               
                               [-2.82842712474619, 0.0, -2.0, -2.0]])     

        Y = fwt2(X)

        Y -= Y_ref
        assert Numeric.allclose(Y, 0)



    def test_ifwt2a(self):

        from RandomArray import seed, random

        seed(13, 17)

        X = random((8,4))

        Y = fwt2(X)
        X1 = ifwt2(Y)
        assert Numeric.allclose(X-X1, 0)        
        

    def test_ifwt2b(self):

        from RandomArray import seed, random

        seed(13, 17)

        X = random((8,4))

        Y = fwt2(X)
        Y = fwt2(Y)        
        
        Y = ifwt2(Y)
        X1 = ifwt2(Y)        
        assert Numeric.allclose(X-X1, 0)


    def test_ifwt2c(self):

        from RandomArray import seed, random

        seed(13, 17)

        X = random((8,4))

        Y = ifwt2(X)
        Y = ifwt2(Y)        
        
        Y = fwt2(Y)
        X1 = fwt2(Y)        
        assert Numeric.allclose(X-X1, 0)                

    def test_big(self):
        from RandomArray import seed, random

        seed(13, 17)

        X = random((1024,512))

        Y = fwt2(X)
        X1 = ifwt2(Y)        
        assert Numeric.allclose(X-X1, 0)                


    def test_scale_energy(self):
        D = 4
        N = 8
        d = 3
        
        X = Numeric.zeros(N, Numeric.Float)

        for i in range(len(X)):
            X[i] = i+1
            
        Wx = fwt(X, D, d)

        
        Evec = scale_energy(Wx, d+1) #All details + avg

        Evec_ref = Numeric.array([0.03921568627451, 0.07256788028085,\
                                  0.09409878638582, 0.79411764705882])
        
        assert Numeric.allclose(Evec-Evec_ref, 0)
                                 
if __name__ == '__main__':
    mysuite = unittest.makeSuite(TestCase, 'test')
    #mysuite = unittest.makeSuite(TestCase, 'test_big')    
    runner = unittest.TextTestRunner()
    runner.run(mysuite)








