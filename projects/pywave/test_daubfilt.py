import unittest

from Numeric import zeros, ones, allclose, sqrt, sum, Float, reshape, dot

def mvmul(A, x):
  """Multiply matrix A onto vector x
  """

  from Numeric import dot, reshape

  x = reshape(x, (A.shape[1], 1)) #Make x a column vector             
  return dot(A, x)

 
def ortho(n,v,w=None):
    """ortho -  Test orthogonality condition of filter coefficients.

    s=ortho(n,v,w) 
    Computes s = \sum_i v(i)*w(i+2n)  
    
    s=ortho(n,v) 
    Computes s = \sum_i v(i)*v(i+2n)  


    Ex: ortho(1,v):   s = v(1)*v(3) + v(2)*v(4) + ...

        ortho(1,v,w): s = v(1)*w(3) + v(2)*w(4) + ... +
                          w(1)*v(3) + w(2)*v(4) + ...

    See also daubfilt, test_daubfilt

    Ole Moller Nielsen, NYU, 03/18/96.
    Translated from Matlab to Python by OMN, GA, May 2003
    """

    k = 2*n

    Dv = len(v);
    if w is None:
        Dw = Dv
        w = v
    else:    
        Dw = len(w)

    D = max(Dv,Dw)
    dif = abs(Dw-Dv)

    if dif > 0:
        #Pad smallest vector with zeros
        x = zeros(D, Float)
        if Dw > Dv:
            x[:Dv] = v
            v = x
            #v[Dv+1:Dw]
        else:
            print x
            print w
            print x[:Dw]
            x[:Dw] = w
            w = x
            #w[Dw+1:Dv]
  
    s = 0
    if Dw > 0:   #
        for i in range(D-k):
            s = s + v[i]*w[i+k] + w[i]*v[i+k];
        s = s/2;
    else:        
        for i in range(1, D-k+1):
            s = s + v[i]*v[i+k]

    return s



class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    

    def test_module(self):
        """Import module daubfilt.py"""

        import daubfilt
        
        
    def test_filterlength(self):

        from daubfilt import daubfilt
        
        for p in range(1,26):
            D=2*p
            lp, hp = daubfilt(D)
            if len(lp) != D:      # Test number of coefficients
                S = 'Bad filter length (%d), D = %d' %(length(lp), D) 
                raise S

    def test_orthogonality(self):
        """Test that coefficients in lp satisfy orthogonality condition
        """ 

        from daubfilt import daubfilt, number_of_filters

        for p in range(number_of_filters):
            D = 2*(p+1)
            P = D/2  # Number of vanishing moments
            N = P-1  # Dimension of nullspace of the matrix A            

            lp, hp = daubfilt(D)
            
            for k in range(1, N+1):  #FIXME: use P
                o = ortho(k,lp);              
                if k==0:
                    o = 1-o
                err = abs(o)
 
                #assert abs(err) <= epsilon, 'Error == %e' %err
                assert allclose(err, 0), 'Error == %e' %err    
 

    def test_vanishing_moments(self):
        """Test that coefficients in lp satisfy the
           vanishing moments condition
        """ 

        from daubfilt import daubfilt, number_of_filters

        for i in range(number_of_filters):
            D = 2*(i+1)

            P = D/2  # Number of vanishing moments
            N = P-1  # Dimension of nullspace of the matrix A
            R = P+1  # Rank of A, R = D-N = P+1 equations
        
            lp, hp = daubfilt(D)


            # Condition number of A grows with P, so we test only
            # the first 6 (and eps is slightly larger than machine precision)

            A    = zeros((R,D), Float)  # D unknowns, D-N equations
            b    = zeros((R,1), Float)  # Right hand side
            b[0] = sqrt(2)                
  
            A[0,:] = ones(D, Float)   # Coefficients must sum to sqrt(2)
            for p in range(min(P,6)): # the p'th vanishing moment (Cond Ap)
                for k in range(D):            
                    m=D-k;
                    A[p+1,k] = (-1)**m * k**p;

            assert allclose(b, mvmul(A,lp))         
            #err = norm(b-mvmul(A,lp))
            #assert abs(err) <= 1.0e-10, 'D = %d, Error == %e' %(D, err)
        

    def test_conservation_of_area(self):
        """Test that coefficients in lp satisfy the dilation equation
        """ 

        from daubfilt import daubfilt, number_of_filters

        for p in range(number_of_filters):
            D = 2*(p+1)
            lp, hp = daubfilt(D)

            err = abs(sum(lp)-sqrt(2))
            #assert abs(err) <= epsilon, 'Error == %e' %err
            assert allclose(err, 0), 'Error == %e' %err    

        
if __name__ == '__main__':
    mysuite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(mysuite)








