// Solve a tridiagonal linear system of size N x N.
// The coefficient matrix is assumed to be diagonally dominant.
//
//  tri (ind, N, A, B, C, D, V);
//
// Input:
//
//   tri (int):  1  LU factorization 
//               2  Forward substitution (assuming prev factorization)
//               3  Both
//
//   N (int):    length of A, B, C, and D
//
//   A{2:N)   (double): Elements in the lower off-diagonal   
//   B(1:N)   (double): Elements in the diagonal   
//   C(1:N-1) (double): Elements in the upper off-diagonal   
//
//   D(1:N)   (double): Right hand side   
// 
// Output:
//
//   tri (int):  -1     Error condition (division by zero)
//
//   A,B,C (double):    Represent the factorization if tri 
//                      was previously called with ind = 1 or 3
//
//   D(1:N) (double):   The solution vector (if ind = 2 or 3)
//   V (double):        Growth factor. V must be small for solution
//                      to be reliable.
//
//  
// Ole Moller Nielsen - 1994

#include <math.h>
#include "tri.h"

tri (int &ind, int N, double *A, double *B, double *C, double *D, double &V)
{
  const minint = -32767;
  int   i;
  double S1, S2;

  if (ind==1 || ind==3)
  {
    S1 = minint;
    for (i=2; i<N+1;   i++) if (S1 < fabs(A[i])) S1 = fabs(A[i]);
    for (i=1; i<N+1;   i++) if (S1 < fabs(B[i])) S1 = fabs(B[i]);
    for (i=1; i<N;     i++) if (S1 < fabs(C[i])) S1 = fabs(C[i]);

    if (B[1] == 0.0) ind = -1;
    i = 2;
    while (ind != -1 && i < N+1)
    {
       A[i] = A[i] / B[i-1];
       B[i] = B[i] - A[i] * C[i-1];
       if (B[i] == 0.0) ind = -1;
       i++;
    }

    if (ind!=-1)
    {
      S2 = S1;
      for (i=1; i<N+1; i++) if (S2 < fabs(B[i])) S2 = fabs(B[i]);
      V  = S1 / S2;
    }
  };


  if (ind==2 || ind==3)
  {
    for (i=2; i<N+1; i++)
    {
      D[i] = D[i] - A[i]*D[i-1];
    }

    D[N] = D[N] / B[N];

    for (i=N-1; i>0; i--)
    {
      D[i] = (D[i] - C[i]*D[i+1]) / B[i];
    }
  }
}




