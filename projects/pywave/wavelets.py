"""wavelets.py - module for discrete (Daubechies) wavelet transforms

Functions provided are

fwt:    1D Forward transform
ifwt:   1D Inverse transform
fwt2:   2D Forward transform
ifwt2:  2D Inverse transform

scaleenergy: Energies at all detail scales


See individual docstrings for more info

See also my dissertation for all the background:
http://datamining.anu.edu.au/~ole/work/publications/thesis.html


"""


from daubfilt import daubfilt, number_of_filters

def fwt(X, D=4, depth=None):
    """fwt - Fast Discrete Periodized Wavelet Transform.
    
    X = fwt(X, D, depth)

    Input
      X:      Matrix, where columns are the vectors to be transformed.
      D:      Wavelet genus - optional, default D=4.
      depth:  Depth of the transform (lambda) - optional.
              Default is largest possible depth.

    Output
      Y:  Matrix, where columns are the transformed vectors.

    The number of rows in X should have a power of 2 as a factor. 

    See also ifwt and daubfilt

    Ole Moller Nielsen - 21 July 1995.
    Adapted for Python by Ole M N at Geoscience Australia 2003 
    """

    import exceptions   
    class LengthOneException(exceptions.Exception):
        def __init__(self, args=None):
            self.args = args

    
    # Parameter check

    if D % 2 == 0 and 2 <= D <= 50:
        lp, hp = daubfilt(D)
    else:
        msg = 'ERROR (fwt): Wavelet genus D must be an even number betweeen 2 and 50'
        raise msg        

    N = X.shape[0]
    if len(X.shape) == 1:
        cols = 1
    elif len(X.shape) == 2:    
        N, cols = X.shape   # N is Length of each column
    else:
        msg = 'Array must be either 1D or 2D'
        raise msg

    if N < 1 or cols < 1:
        msg = 'Zero length vector specified'
        raise msg
    
    if N < 2:
        msg = 'Length 1 vector, no transform made'
        raise LengthOneException, msg


    Y = X.copy() #colfwt destroys input matrix
    try:
        from fwt_ext import colfwt #C-extension
    except:
        #Use Python version
        Y = colfwt_python(Y, lp, hp, depth)        
    else:
        #Use C-extension
        Y = colfwt(Y, lp, hp, depth)
        
    return Y

def fwt2(X, D=4, depth1 = None, depth2 = None):
    #FIXME: Can be optimised by using mfwt to avoid one copy operation
    import Numeric

    X1 = fwt(X, D, depth1)
    X1 = Numeric.transpose(X1)
    Y = fwt(X1, D, depth2)
    Y = Numeric.transpose(Y)    

    return Y




def ifwt(X, D=4, depth=None):
    """ifwt - Fast Inverse Discrete Periodized Wavelet Transform.
    
    X = ifwt(X, D, depth)

    Input
      X:      Matrix, where columns are the vectors to be transformed.
      D:      Wavelet genus - optional, default D=4.
      depth:  Depth of the transform (lambda) - optional.
              Default is largest possible depth.            

    Output
      Y:  Matrix, where columns are the transformed vectors.

    The number of rows in X should have a power of 2 as a factor. 

    See also ifwt and daubfilt    

    Ole Moller Nielsen - 21 July 1995.
    Adapted for Python by Ole M N at Geoscience Australia 2003 
    """

    import exceptions   
    class LengthOneException(exceptions.Exception):
        def __init__(self, args=None):
            self.args = args

    # Parameter check

    if D % 2 == 0 and 2 <= D <= 50:
        lp, hp = daubfilt(D)
    else:
        msg = 'ERROR (fwt): Wavelet genus D must be an even number betweeen 2 and 50'
        raise msg        

    N = X.shape[0]
    if len(X.shape) == 1:
        cols = 1
    elif len(X.shape) == 2:    
        N, cols = X.shape   # N is Length of each column
    else:
        msg = 'Array must be either 1D or 2D'
        raise msg

    if N < 1 or cols < 1:
        msg = 'Zero length vector specified'
        raise msg
    
    if N < 2:
        msg = 'Length 1 vector, no transform made'
        raise LengthOneException, msg

    Y = X.copy() #icolfwt destroys input matrix
    try:
        from ifwt_ext import icolfwt #C-extension
    except:
        #Use Python version
        Y = icolfwt_python(Y, lp, hp, depth)        
    else:
        #Use C-extension
        Y = icolfwt(Y, lp, hp, depth)

    return Y



def ifwt2(X, D=4, depth1 = None, depth2 = None):
    #FIXME: Can be optimised by using mfwt to avoid one copy operation    
    import Numeric

    X1 = ifwt(X, D, depth1)
    X1 = Numeric.transpose(X1)
    Y = ifwt(X1, D, depth2)
    Y = Numeric.transpose(Y)    

    return Y


def scale_energy(Wy, depth = None):
    """scale_energy - Compute energies at all detail scales starting with the finest (0)

       If DC term is wanted add one to depth in the call:
         scale_energy(Wy, depth+1)
         
    """

    import Numeric, math


    if depth is None:
        depth = int(math.log(len(Wy))/math.log(2))  # Maximal depth
    
    #M = depth+1  # Noof energies
    M = depth  # Noof energies    
    E = Numeric.zeros(M, Numeric.Float)

    N = len(Wy)

    Etot = Numeric.innerproduct(Wy,Wy)

    last = N
    for j in range(M):
        first = last/2

        if j == M-1:
            v = Wy[:last]
        else:    
            v = Wy[first:last]
        E[j] = Numeric.innerproduct(v,v)
  
        last = first 

    E = E/Etot;
    return E
		   


#--------------------------------
# Python versions of C-extensions


def colfwt_python(X, lp, hp, depth):
    """Columnwise fast wavelet transform
    """


    N = len(X)           #Elements in 1d vector or rows in matrix

    if depth is None:
        Coarsest_level = 1
    else:    
        Coarsest_level = max(N/2**depth, 1)
        

    while N%2 == 0 and N > Coarsest_level:   # Allow for N=2^m*K
        X, NH = colpwt (X, N, lp, hp)
        N     = NH                        # Reduce N to N/2 for next level

    return X


def colpwt(X, N, lp, hp):
    """%PWT Partial (Single stage) Wavelet Transform.

    X, NH = pwt (X, N, lp, hp)

    Perform one step of the wavelet transform 
    on the first N components of each column of X.
    the vectors lp and hp contain the wavelet filter coefficients.

    Ole Moller Nielsen - 16 April 1997.
    """

    import Numeric

    NH  = N/2
    
    D   = len (lp)
    if D != len(hp):
        msg =  'ERROR (pwt): Filters should be of same length. Pad shortest one with zeros.'
        raise msg

    T  = Numeric.zeros(X.shape, Numeric.Float)  # Workspace
    
    for k in range(D):           # Loop over wavelet coefficients
        for i in range(NH):  
            r      = (k+2*i) % N   # Row number in X
            j      = i+NH          # Row number in second half of result
            if len(X.shape) == 2:  # Columnwise transform                
                T[i,:] += lp[k]*X[r,:]
                T[j,:] += hp[k]*X[r,:]
            else:                  # Elementwise (1d)
                T[i] += lp[k]*X[r]
                T[j] += hp[k]*X[r]
                

    # Copy wavelet transform at level N back into X
    if len(X.shape) == 2:
        X[:N,:] = T[:N,:]       
    else:
        X[:N] = T[:N]


    return X, NH



def icolfwt_python(X, lp, hp, depth):
    """Inverse columnwise fast wavelet transform
    """


    N = len(X)           #Elements in 1d vector or rows in matrix

    if depth is None:
        Coarsest_level = 1
    else:    
        Coarsest_level = max(N/2**depth, 1)
        
    FinalN = N           # Factor N=K*2^m
    while N%2==0:        # Get smallest even N
        N = N/2

    N=max(N, Coarsest_level)
    N=2*N


    while N <= FinalN:   # Inverse pyramid algorithm starting with finest scale
        X = icolpwt(X, N, lp, hp)
        N = 2*N

    return X


def icolpwt(X, N, lp, hp):
    """Inverse Partial (Single stage) Wavelet Transform.

    X, NH = ipwt (X, N, lp, hp)

    Perform one step of the wavelet transform 
    on the first N components of each column of X.
    the vectors lp and hp contain the wavelet filter coefficients.

    Ole Moller Nielsen - 16 April 1997.
    """

    import Numeric
    from math import ceil


    D   = len (lp)
    if D != len(hp):
        msg =  'ERROR (pwt): Filters should be of same length. Pad shortest one with zeros.'
        raise msg

    NH  = N/2
    mul = ceil(float(D-2)/2/NH)
    NH_multiple = int(mul * NH)    # Nearest multiple of NH gt (k-i)/2 forall k,i

    T = Numeric.zeros(X.shape, Numeric.Float) #Workspace
    
    for k in range(0, D, 2):
        k1 = k+1
        for i in range(0, N, 2):
            i1 = i+1
            j = (i-k)/2
            r  = (NH_multiple + j) % NH

            if len(X.shape) == 2:  # Columnwise transform
                T[i,:]  += lp[k] *X[r,:] + hp[k] *X[r+NH,:]
                T[i1,:] += lp[k1]*X[r,:] + hp[k1]*X[r+NH,:]
            else: #Elementwaise (1d)
                T[i]  += lp[k] *X[r] + hp[k] *X[r+NH]
                T[i1] += lp[k1]*X[r] + hp[k1]*X[r+NH]                
      

    # Copy inverse wavelet transform at level N back into X             
    if len(X.shape) == 2:
        X[:N,:] = T[:N,:] 
    else:
        X[:N] = T[:N]         

        
    return X


#----------------------------------
#Make sure that c-extensions are correct (Important for Win - Cygwin)


# Take care of situation where module is part of package
import os, string, os.path
dirname = os.path.dirname(string.replace(__name__,'.',os.sep)).strip()

if not dirname:
    dirname = '.'
    
if dirname[-1] != os.sep:
    dirname += os.sep   

curdir = os.getcwd()
os.chdir(dirname)

cmdstring = '"import fwt_ext, ifwt_ext"'
s = 'python -c %s ' %cmdstring
error = os.system(s)

if error:
    print "Trying to recompile c-extensions"

    #Remove any previous extensions
    extensions = ['fwt_ext.dll', 'ifwt_ext.dll', 'fwt_ext.so', 'ifwt_ext.so']

    for ext in extensions:
        try:
            os.remove(ext)
        except:
            pass


    from compile import compile
    compile('fwt_ext.c', verbose = 1)
    compile('ifwt_ext.c', verbose = 1)
    
os.chdir(curdir)

