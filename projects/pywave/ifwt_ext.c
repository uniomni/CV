/*
 * ifwt.c - inverse columnwise wavelet transform for use in Python 
 * e.g. by itself (1d) the inverse 2d wavelet transform (ifwt2.py). 
 *
 * This is a C-extension for Python optimized for speed as follows
 *   - Input and output workspaces are alternated to reduce copying.
 *   - Inner loops address data consecutively to make good use of cache.
 *   - Loops that may cause wrapping are separated into fast 'bulk' loops
 *     that don't wrap and special cases where wrapping may occur.
 *
 * When compiled (using mex imfwt.c) this routine can be called from
 * Python as follows:
 *
 *   Y = imfwt(X, lp, hp, depth);  
 *
 * where
 *   X is an N x columns Numeric matrix
 *   depth is the number of desired transform steps
 *   lp is a wavelet low-pass filter 
 *   hp is the corresponding high pass filter (e.g. lp,hp=daubfilt(8))
 *
 *   Y is a matrix of same size as X containing the inverse 
 *   wavelet transform of all *columns* of X.
 * 
 * NB! The input matrix X is used as workspace and will be destroyed.
 *     It is the responsibility of the caller to make a copy if necessary.
 *
 *
 * Ole Nielsen, ANU, 1999
 * Adapted for Python by Ole Nielsen, GA, 2003 
 *
 */

	
#include "Python.h"
#include "Numeric/arrayobject.h"
#include "math.h"


/***********************************************************/
/*  AUXILIARY ROUTINES                                     */
/***********************************************************/
int max(int a, int b)
{
  if (a > b)
    return(a);
  else
    return(b);  
}





/*********************************************************************/
/************ ONE STEP OF THE INVERSE WAVELET TRANSFORM **************/
/*********************************************************************/
/*
 * icolpwt performs one step of the inverse wavelet transform of length N on 
 * all columns of the Nxcolumns matrix X using filters lp and hp each of length D.
 * The result is returned in the first N columns of Y
 *
 * Mathematically, Y(1:N, :) = W'*X(1:N,:), 
 * where W has the form (shown here for N=8 and D=4) 
 *
 *   | lp[0] lp[1] lp[2] lp[3]                          |
 *   |             lp[0] lp[1] lp[2] lp[3]              |
 *   |                         lp[0] lp[1] lp[2] lp[3]  |
 *   | lp[2] lp[3]                         lp[0] lp[1]  |  
 *   | hp[0] hp[1] hp[2] hp[3]                          |
 *   |             hp[0] hp[1] hp[2] hp[3]              |
 *   |                         hp[0] hp[1] hp[2] hp[3]  |
 *   | hp[2] hp[3]                         hp[0] hp[1]  |  
 * 
 *
 *
 * Ole Nielsen, ANU, 1999 
 *
 */

int icolpwt (double *X, int N, int columns, double *lp, double *hp, int D, double *Y)
{
  int i,j,k,l,col, NH,r,NHcolumns,columns2,crossover,mul,NH_multiple;
  int index,indexi,indexh,index1,indexr,kstart;

  
  NH  = N/2;
  NHcolumns = NH*columns;
  columns2 = 2*columns;
  
  kstart = 2;  /*2: takes special care of two first coefs, 0 don't */ 
  
  mul = (int) (D-2)/2/NH+1;
  NH_multiple = mul * NH; /* Nearest multiple of NH > (k-i)/2 forall k,i */
  
  if (kstart < 2) {
    for (i = 0; i < N; i++) {
      index = i*columns;      
      for (col = 0; col < columns; col++) {
        Y[index] = 0.0;   /* Reset result matrix */
        index++;
      }
    }
  } else {
  
    /* Take special care of the two first filter coefficients */
    k = 0;
    l = 1;
    
    r = 0;
    indexi = 0;
    indexr = 0;
    for (i = 0; i < N-1; i=i+2) {
      indexi = i*columns; 
      indexr = r*columns; 
            
      index1 = indexi + columns;      
      indexh = indexr + NHcolumns;    
      for (col = 0; col < columns; col++) { 
        Y[indexi]= lp[k]*X[indexr] + hp[k]*X[indexh];
        Y[index1]= lp[l]*X[indexr] + hp[l]*X[indexh];
	indexi++;
	indexr++;
	index1++;
	indexh++;
      }
      r  = r+1;   /* r  = (i-k)/2  */
    }         
  }
  
  
  for (k=kstart; k<D-1; k=k+2) {        
    if (k > N) {      /* Separate those i, where i-k<0 */
      crossover = N;
    } else {
      crossover = k; 
    }  
        
    l = k+1;
                   
    /*--- Modulus phase  - only a fraction of the total time is spent here */ 

    for(i=0; i<crossover-1; i=i+2) {
      j  = (i-k)/2;                    
      r  = (NH_multiple + j) % NH;          
      
      
      indexi = i*columns;      
      index1 = indexi+columns;
      indexr = r*columns;
      indexh = (r+NH)*columns;
      for (col = 0; col < columns; col++) {
        Y[indexi] = Y[indexi] + lp[k]*X[indexr] + hp[k]*X[indexh];
        Y[index1] = Y[index1] + lp[l]*X[indexr] + hp[l]*X[indexh];   
	indexi++;
	indexr++;
	index1++;
	indexh++;
      }
    }     

    /* Linear phase - Most of the time is spent here */
    r = 0;
    for (i = crossover; i < N-1; i=i+2) {
      indexi = i*columns;
      index1 = indexi+columns;      
      indexr = r*columns;
      indexh = (r+NH)*columns;            
      for (col = 0; col < columns; col++) { 
        Y[indexi]=Y[indexi] + lp[k]*X[indexr] + hp[k]*X[indexh];
        Y[index1]=Y[index1] + lp[l]*X[indexr] + hp[l]*X[indexh];
	indexi++;
	indexr++;
	index1++;
	indexh++;
      }
      r  = r+1;   /* r  = (i-k)/2  */
    }     
  }  
  return 0;
}


int _icolfwt (double *X, int N, int columns, double *lp, double *hp, int D, 
	  int Coarsest_level, double *Y)
{
  /***********************************************/	
  /* Outer loop of the inverse wavelet transform */
  /***********************************************/	

  
  int k, NH, index;
  int dir, col, FinalN;

  
  

  /* Find initial transform size */
  FinalN = N;   
  dir = 0;          /* Alternate transform direction to save space */    
  while ( (N%2 == 0) & (N > Coarsest_level) ){
    dir = 1-dir;  
    N=N/2;
  }
  NH = N;

  if (dir == 0){                /* Begin transform in Y */
    for (k = 0; k < NH; k++) {  /* Move dc terms to Y */
      index = k*columns;      
      for (col = 0; col < columns; col++) {
    	Y[index] = X[index];  
    	index++;
      }    
    } 
  }
  
  
  /*Inverse pyramid algorithm starting with finest scale*/
  while (NH < FinalN){  
    N  = 2*NH;  
  
    if (dir == 1) {    
      icolpwt (X, N, columns, lp, hp, D, Y);  /* X -> Y */      
    } else {  
      for (k = NH; k < N; k++) {  /* Move differences from X to Y */
        index = k*columns;      
        for (col = 0; col < columns; col++) {
    	  Y[index] = X[index];  
    	  index++;
        }
      }
      icolpwt (Y, N, columns, lp, hp, D, X);  /* Y -> X */            	    
    } 
    NH  = N;
    dir = 1-dir;
  }  
  
  return 0;
} /* end _icolfwt */		   
  

  
 
/**********************************************************/
/* The Gateway routine                                    */
/*   Y = imfwt(X, lp, hp, lambda)                          */
/*                                                        */
/**********************************************************/
static PyObject *icolfwt(PyObject *self, PyObject *args) {
  PyObject *pyX, *pylp, *pyhp, *pylambda;
  PyArrayObject *X, *Y, *lp, *hp;
  
  int D, columns, N, pwr, lambda, Coarsest_level = 1;
  char *msg;

    
  /* process the parameters */
  if (!PyArg_ParseTuple(args, "OOOO", &pyX, &pylp, &pyhp, &pylambda))
    return NULL;
  
  /* Make Numeric array from general sequence types (no cost if already Numeric)*/    
  X = (PyArrayObject *)
    PyArray_ContiguousFromObject(pyX, PyArray_DOUBLE, 0, 0);

  lp = (PyArrayObject *)
    PyArray_ContiguousFromObject(pylp, PyArray_NOTYPE, 0, 0);
    
  hp = (PyArrayObject *)
    PyArray_ContiguousFromObject(pyhp, PyArray_NOTYPE, 0, 0);    
    

  D = lp->dimensions[0];        
  if (X -> nd == 2) {  
    N = X->dimensions[0];         // Number of rows in matrix
    columns = X->dimensions[1];
  } else if (X -> nd == 1) {
    N = X->dimensions[0];         // Number of elements in vector
    columns = 1;
  } else {
      msg = "Input array must have dimension 1 or 2"; 
      PyErr_SetString(PyExc_ValueError, msg); //raise ValueError
      return NULL;      
  }  
  
  //Make Y a Numeric array same dims as X    
  Y = (PyArrayObject *) PyArray_FromDims(X -> nd, X -> dimensions, X -> descr -> type_num);

  if (PyInt_Check(pylambda)) {    
    lambda = PyInt_AsLong(pylambda);
    pwr = pow(2,lambda); 
    Coarsest_level = max((int) (N/ (float) pwr), 1);            
  }    
  
  _icolfwt ((double *) X -> data, N, columns, 
	    (double *) lp -> data, (double *) hp -> data, 
	    D, Coarsest_level, (double *) Y -> data);  
  
  
  return PyArray_Return(Y); 
}

 
/**********************************/
/* Method table for python module */
/**********************************/

static struct PyMethodDef MethodTable[] = {
  {"icolfwt", icolfwt, METH_VARARGS},
  {NULL, NULL}
};


/***************************/
/* Module initialisation   */
/***************************/


void initifwt_ext(void){
  PyObject *m;
  
  m = Py_InitModule("ifwt_ext", MethodTable);
  
  import_array();     //Necessary for handling of NumPY structures  
}






