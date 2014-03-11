/*
 * mfwt.c - multiple rowwise wavelet transform for use in MATLAB 
 * e.g. by the 2d wavelet transform (fwt2.m). 
 *
 * This is a MEX-file for MATLAB optimized for speed as follows
 *   - Input and output workspaces are alternated to reduce copying.
 *   - Inner loops address data consecutively to make good use of cache.
 *   - Loops that may cause wrapping are separated into fast 'bulk' loops
 *     that don't wrap and special cases where wrapping may occur.
 *
 * When compiled (using mex mfwt.c) this routine can be called from
 * MATLAB as follows:
 *
 *   Y = mfwt(X, lambda, lp, hp);  
 *
 * where
 *   X is an M x N matrix
 *   lambda is the number of desired transform steps
 *   lp is a wavelet low-pass filter 
 *   hp is the corresponding high pass filter (e.g. [lp,hp]=daubfilt(8))
 *
 *   Y is a matrix of same size as X containing the wavelet transform
 *     of all rows of X.
 * 
 * NB! The input matrix X is used as workspace and will be destroyed.
 *     It is the responsibility of the caller to make a copy if necessary.
 *
 *
 * Ole Nielsen, ANU, 1999
 *
 */

	

#include "mex.h"



/*********************************************************************/
/****************** ONE STEP OF THE WAVELET TRANSFORM ****************/
/*********************************************************************/
/*
 * mpwt performs one step of the wavelet transform of length N on 
 * all ROWS of the MxN matrix X using filters lp and hp each of length D.
 * The result is returned in the first N columns of Y
 *
 * Mathematically, Y(:,1:N) = X(:,1:N) * W', 
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

int mpwt (double *X, int M, int N, double *lp, double *hp, int D, double *Y)
{
  int i,j,k,row,NH,r,r1,NH1,crossover,indexr,indexi,indexj;

  NH  = N/2;
  NH1 = NH+1;
  

  /*************************************************/
  /*  Take special care of two first coefficients  */
  /*************************************************/
  for (i=0;i<NH;i++) {          /* Column number in first half of result */
    r  = 2*i;                   /* Column number in X corresp to k=0 */
    j  = i+NH;                  /* Column number in second half of result */
    
    indexr = r*M;
    indexi = i*M;
    indexj = j*M;
    for (row = 0; row < M; row++) {
      Y[indexi] = lp[0]*X[indexr] + lp[1]*X[indexr + M];
      Y[indexj] = hp[0]*X[indexr] + hp[1]*X[indexr + M];

      indexr++;
      indexi++;
      indexj++;          
    }  
  }

  
  /***********************************************/
  /*  Compute part that does not wrap - the bulk */
  /***********************************************/
    
  crossover = (D-2)/2;  /* Index r will wrap when i >= N/2-crossover*/    
    
  for (i=0; i<NH-crossover; i++){ /* Column number in first half of result */
    for (k=2;k<D;k++) {           
      r      = k+2*i;         /* Column number in X */
      j      = i+NH;          /* Column number in second half of result */
      
      indexr  = r*M;
      indexi = i*M;
      indexj = j*M;
      for (row = 0; row < M; row++) {
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
      
      indexr = r*M;
      indexi = i*M;
      indexj = j*M;
      for (row = 0; row < M; row++) {
        Y[indexi] = Y[indexi] + lp[k]*X[indexr];
        Y[indexj] = Y[indexj] + hp[k]*X[indexr];
        indexr++;
        indexi++;
        indexj++;          
      }  
    }
  }

  return(NH);          /* Return N/2 for use in outer loop */
  
} /* END ONE-STEP WAVELET TRANSFORM */		 




/*****************************************/
/* MATLAB GATEWAY ROUTINE AND OUTER LOOP */
/*****************************************/
/*
 * This is the interface between MATLAB and C
 *
 * Parameters are extracted and the outer loop of the
 * wavelet transform is carried out here. 
 *
 */

void mexFunction(int nlhs, mxArray *plhs[],
                 int nrhs, const mxArray *prhs[])
{
  int i, j, k, M, N, NH, index, D, lambda, Coarsest_level, pwr;
  int dir, row;
  double *X, *Y, *lp, *hp;
  

  /****************************/  
  /* A very basic input check */
  /****************************/
  if ( nrhs != 4 )
    mexErrMsgTxt("Four inputs required!");
  else if ( nlhs > 1 )
    mexErrMsgTxt("Too many output arguments!");  
    

  /*******************************************/
  /* Get input matrix from MATLAB argument 1 */
  /*******************************************/
  M = mxGetM(prhs[0]);   /* Number of rows         */
  N = mxGetN(prhs[0]);   /* Number of columns      */
  X = mxGetPr(prhs[0]);	 /* The input M x N matrix */			 

  
  /***************************************************************/  
  /* Get wavelet transform depth, lambda, from MATLAB argument 2 */
  /***************************************************************/
  lambda = (int) mxGetScalar(prhs[1]);
  if (mxIsInf(mxGetScalar(prhs[1])))
    {                      /* If requested depth == Inf then */         
      Coarsest_level = 1;    /* take as many steps as possible */
  } else
  {
    pwr = pow(2,lambda);      
    Coarsest_level = max((int) (N/ (float) pwr), 1);      
  }
  
  /****************************************************/
  /* Get wavelet filters from MATLAB argument 3 and 4 */
  /****************************************************/  
  D = max(mxGetM(prhs[2]),mxGetN(prhs[2]));   /* Filter length */
  if (D != max(mxGetM(prhs[3]),mxGetN(prhs[3]))) 
    mexErrMsgTxt("Filters must have same length. Pad with zeros!");      
  
  lp = mxGetPr(prhs[2]); /* Low pass filter  */
  hp = mxGetPr(prhs[3]); /* High pass filter */
  
  /************************************************************/
  /* Create output array. This will also be used as workspace */
  /************************************************************/  
  plhs[0] = mxCreateDoubleMatrix(M, N, mxREAL);
  Y = mxGetPr(plhs[0]);	   
  	

  /***************************************/	
  /* Outer loop of the wavelet transform */
  /***************************************/	
  
  dir = 0; /* Alternate transform direction to save space */
  
  while (N % 2 == 0 && N > Coarsest_level) { /* Transform for decreasing N */ 
    dir = 1 - dir;
    if (dir == 1) {    
      NH = mpwt (X, M, N, lp, hp, D, Y);  /* One-step transform X -> Y */      
    } else {
      NH = mpwt (Y, M, N, lp, hp, D, X);  /* One-step transform Y -> X */      
      for (k = NH; k < N; k++) {          /* Copy partial result to Y  */ 
	index = k*M;      
        for (row = 0; row < M; row++) {
	  Y[index] = X[index];
	  index++;
	}    
      }   
    }
    N = NH;                               /* N = N/2 */
  }
  
  if (dir == 0) {                    /* If last transform was backwards */
    for (k = 0; k < N; k++) {
      index = k*M;      
      for (row = 0; row < M; row++) {
    	Y[index] = X[index];         /* then copy dc term to Y */
    	index++;
      }    
    } 
  }    
} /* END MATLAB GATEWAY ROUTINE */		 





/***********************************************************/
/****************** MISC AUXILIARY ROUTINES ****************/
/***********************************************************/
int max(int a, int b)
{
  if (a > b)
    return(a);
  else
    return(b);  
}

/*
int pow(int a, int k)
{
  int d, res;
  
  if (k<=0) res = 1;
  else {
    res = 1;
    for (d=0;d<k;d++) {  
      res = res*a;  
    }   
  }
  return(res);
} */


