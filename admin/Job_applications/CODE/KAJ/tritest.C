// Test and demo program for tri.C
// Solve
//
//  |   5    -1     0     0|  x1       1
//  |  -1     5    -1     0|  x2       1
//  |   0    -1     5    -1|  x3   =   1
//  |   0     0    -1     5|  x4       1
//
// which has the solution
//
// 0.263158 
// 0.315789 
// 0.315789 
// 0.263158 
//
//
// OMN - 1994

#include <stdio.h>
#include <math.h>
#include "tri.h"

main()
{
  double *A, *B, *C, *D, *XREF;
  int    i, N, ind;
  double  alpha = 5.0, V;

  N = 4;

  A = new double[N+1];
  B = new double[N+1];
  C = new double[N+1];
  D = new double[N+1];
  XREF = new double[N+1];
  
  XREF[1] = 0.263158; 
  XREF[2] = 0.315789; 
  XREF[3] = 0.315789; 
  XREF[4] = 0.263158; 

  for (i=1; i<N+1; i++)
  {
     A[i] = -1;          // Lower off-diagonal
     B[i] =  alpha;      // Diagonal 
//     B[i] =  0;
     C[i] = -1;          // Upper off-diagonal
     D[i] =  1;          // Right hand side
  }

  ind = 3;  // Factorize AND solve in one process
  tri (ind, N, A, B, C, D, V);


  if (ind==-1) printf("Division by zero in step one");
  else
  {
    printf("Error is : \n \n");
    for (i=1; i<N+1; i++)
    {
      printf("%f \n", fabs(D[i] - XREF[i]));
    }
    printf("\n V = %f \n", V);
  }

  return 0;
}


