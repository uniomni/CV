/*
 * fwt.c - columnwise wavelet transform for use in Python 
 * e.g. by itself (1d) or by 2d wavelet transform (fwt2.py). 
 *
 * This is a C extension for Python optimized for speed as follows
 *   - Input and output workspaces are alternated to reduce copying.
 *   - Inner loops address data consecutively to make good use of cache.
 *   - Loops that may cause wrapping are separated into fast 'bulk' loops
 *     that don't wrap and special cases where wrapping may occur.
 *
 * When compiled this routine can be called from
 * Python as follows:
 *
 *   Y = colfwt(X, lp, hp, depth);  
 *
 * where
 *   X is an N x columns Numeric matrix
 *   depth is the number of desired transform steps (or None)
 *   lp is a wavelet low-pass filter 
 *   hp is the corresponding high pass filter (e.g. lp,hp=daubfilt(8))
 *
 *   Y is a matrix of same size as X containing the wavelet transform
 *     of all *columns* of X.
 * 
 * NB! The input matrix X is used as workspace and will be destroyed.
 *     It is the responsibility of the caller to make a copy if necessary.
 *
 * NNB! Matrices in Matlab are stored columnwise, hence the Matlab version 
 * transformed along rows to be able to vectorise columns.
 * Python Numerical arrays are store rowwise so dimensions are swapped 
 * to retain the high performance of adressing elements consecutively.
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


void print_int_array(PyArrayObject *x) {  
  int i;
  for (i=0; i<x->dimensions[0]; i++) {
    printf("%d ", *(int*) (x->data + i*x->strides[0]));
  }
  printf("\n");  
}

void print_int_matrix(PyArrayObject *x) {  
  int i, j;
  
  printf("Strides: %d, %d\n", x->strides[0], x->strides[1]);
  printf("Dims:    %d, %d\n", x->dimensions[0], x->dimensions[1]);  
  for (i=0; i<x->dimensions[0]; i++) {
    for (j=0; j<x->dimensions[1]; j++) {  
      printf("%e ", *(double*) (x->data + i*x->strides[0] + j*x->strides[1]));
    }
    printf("\n");    
  }
  printf("\n");  
}

void print_matrix_flat(PyArrayObject *x) {  
  int i, N0, N1;
  double* X;
  
  printf("Strides: %d, %d\n", x->strides[0], x->strides[1]);
  printf("Dims:    %d, %d\n", x->dimensions[0], x->dimensions[1]);  
  
  X = (double *) x -> data;
  
  N0 = x->dimensions[0];
  N1 = x->dimensions[1];
  
  for (i=0; i < N0*N1; i++) {
    //printf("%e ", *(double*) (X + i));
    printf("%e ", X[i]);
  }
  printf("\n");  
}


/*********************************************************************/
/****************** ONE STEP OF THE WAVELET TRANSFORM ****************/
/*********************************************************************/
/*
 * pwt performs one step of the wavelet transform of length N on 
 * all columns of the Nxcolumns matrix X using filters lp and hp each of length D.
 * The result is returned in the first N rows of Y
 *
 * Mathematically, Y(1:N,:) = W*X(1:N,:), 
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

int colpwt (double *X, int N, int columns, double *lp, double *hp, int D, double *Y)
{
  int i,j,k,col,NH,r,NH1,crossover,indexr,indexi,indexj;

  NH  = N/2;
  NH1 = NH+1;
  

  /*************************************************/
  /*  Take special care of two first coefficients  */
  /*************************************************/
  for (i=0;i<NH;i++) {          /* Element number in first half of result */
    r  = 2*i;                   /* Element number in X corresp to k=0 */
    j  = i+NH;                  /* Element number in second half of result */
    
    indexr = r*columns;
    indexi = i*columns;
    indexj = j*columns;
    for (col = 0; col < columns; col++) {
      Y[indexi] = lp[0]*X[indexr] + lp[1]*X[indexr + columns];
      Y[indexj] = hp[0]*X[indexr] + hp[1]*X[indexr + columns];

      indexr++;
      indexi++;
      indexj++;          
    }  
  }

  
  /***********************************************/
  /*  Compute part that does not wrap - the bulk */
  /***********************************************/
    
  crossover = (D-2)/2;  /* Index r will wrap when i >= N/2-crossover*/    
    
  for (i=0; i<NH-crossover; i++){ /* Element number in first half of result */
    for (k=2;k<D;k++) {           
      r      = k+2*i;         /* Element number in X */
      j      = i+NH;          /* Element number in second half of result */
      
      indexr = r*columns;
      indexi = i*columns;
      indexj = j*columns;
      for (col = 0; col < columns; col++) {
        Y[indexi] = Y[indexi] + lp[k]*X[indexr];
        Y[indexj] = Y[indexj] + hp[k]*X[indexr];
        indexr++;
        indexi++;
        indexj++;          
      }  
    }
  }

  
  /*********************************************************************/
  /* Compute wrapping part - only a fraction of the time is spent here */
  /*********************************************************************/

  for (i=max(NH - crossover,0);i<NH;i++) {
    for (k=2;k<D;k++) {
      r = (k+2*i) % N;    /* This will wrap, possibly multiple times */
      j = i+NH;              
      
      indexr = r*columns;
      indexi = i*columns;
      indexj = j*columns;
      for (col = 0; col < columns; col++) {
        Y[indexi] = Y[indexi] + lp[k]*X[indexr];
        Y[indexj] = Y[indexj] + hp[k]*X[indexr];
        indexr++;
        indexi++;
        indexj++;          
      }  
    }
  }

  return(NH);          /* Return N/2 for use in outer loop */
  
} /* end colpwt - one step wavelet transform */		 


int _colfwt (double *X, int N, int columns, double *lp, double *hp, int D, 
	  int Coarsest_level, double *Y)
{
  /***************************************/	
  /* Outer loop of the wavelet transform */
  /***************************************/	

  int k, NH, index;
  int dir, col;  
  
  dir = 0; /* Alternate transform direction to save space */
  
  while (N % 2 == 0 && N > Coarsest_level) { /* Transform for decreasing N */ 
    dir = 1 - dir;
    if (dir == 1) {    
      NH = colpwt (X, N, columns, lp, hp, D, Y);  /* One-step transform X -> Y */      
    } else {
      NH = colpwt (Y, N, columns, lp, hp, D, X);  /* One-step transform Y -> X */      
      for (k = NH; k < N; k++) {          /* Copy partial result to Y  */ 
	index = k*columns;      
        for (col = 0; col < columns; col++) {
	  Y[index] = X[index];
	  index++;
	}    
      }   
    }
    N = NH;                               /* N = N/2 */
  }
  
  if (dir == 0) {                    /* If last transform was backwards */
    for (k = 0; k < N; k++) {
      index = k*columns;      
      for (col = 0; col < columns; col++) {
    	Y[index] = X[index];         /* then copy dc term to Y */
    	index++;
      }    
    } 
  }    
  
  return 0;
} /* end colfwt */		   



    
 
/**********************************************************/
/* The Gateway routine                                    */
/*   Y = colfwt(X, lp, hp, lambda)                          */
/*                                                        */
/**********************************************************/
static PyObject *colfwt(PyObject *self, PyObject *args) {
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
    N = X->dimensions[0];                //Rows in matrix
    columns = X->dimensions[1];
  } else if (X -> nd == 1) {
    N = X->dimensions[0];                //Elements in 1d vector
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
  	
  _colfwt ((double *) X -> data, N, columns, 
	(double *) lp -> data, (double *) hp -> data, 
	D, Coarsest_level, (double *) Y -> data);  
  
  
  return PyArray_Return(Y); 
}

 
/**********************************/
/* Method table for python module */
/**********************************/

static struct PyMethodDef MethodTable[] = {
  {"colfwt", colfwt, METH_VARARGS},
  {NULL, NULL}
};


/***************************/
/* Module initialisation   */
/***************************/


void initfwt_ext(void){
  PyObject *m;
  
  m = Py_InitModule("fwt_ext", MethodTable);
  
  import_array();     //Necessary for handling of NumPY structures  
}

 
