C FILE: ARRAY.F
      SUBROUTINE FOO(A,M,N)
C
C     INCREMENT THE FIRST ROW AND DECREMENT THE FIRST COLUMN OF A
C
      INTEGER M,N,I,J
      REAL*8 A(M,N)
Cf2py intent(in,out,copy) a
Cf2py integer intent(hide),depend(a) :: m=shape(a,0), n=shape(a,1)

C     PRINT INTPUT
      print *, 'I  J  A(I,J)'
      DO I=1,M
         DO J=1,N
            print *, I, J, A(I,J)
         ENDDO
      ENDDO

      DO J=1,M
         A(1,J) = A(1,J) + 1D0
      ENDDO
      DO I=1,N
         A(I,1) = A(I,1) - 1D0
      ENDDO
      END
C END OF FILE ARRAY.F
