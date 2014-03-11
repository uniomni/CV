! A Fortran-90 subroutine for solving a linear system of equations whose 
! coefficient matrix A has symmetric band form. It is assumed that only the 
! upper part of the band is stored in A in a format of the following form:
!
!                a11 a12 a13
!                a22 a23 a24
!                a33 a34 a35
!                a44 a45 a46
!                a55 a56 a57
!                a66 a67
!                a77    
!
!
! The solution method is Gaussian elimibation without pivoting. This process 
! is stable if the matrix is definite or diagonally dominant. 
!  
! Floating point arithmetic is done in double precision corresponding to the
! kind parameter long = selected_real_kind(12), i.e. with at least 12 
! significant digits.  
!
! The subroutine is invoked by the statement
! 
!   call symsl(A, b, case)
!
! Input arguments:
!-----------------
! A     The original matrix (case = 1, 3). 
!       The factorized matrix (case = 2).
! b     Right-hand side vector in the system to be solved (case = 2, 3)     
! case  case=1: symsl factorizes the matrix but does not solve the system.
!       case=2: symsl solves using a previously computed factorization.
!       case=3: symsl both factorizes the matrix and solves the system.
!
! Output arguments:
!------------------
! A    The factorized form of the matrix (case = 1, 3)
! b    The solution of the system (case = 2, 3)
!

! Ole Moller Nielsen, Dec 1996

subroutine symsl(A, b, case)
  implicit none                
  
  integer, parameter :: long = selected_real_kind(12)  
  real(long)         :: A(:,:), b(:), c
  integer            :: case, M, HBW, i, j, i1, j1, k
                
  ! Get dimensions and extends from dummy array arguments.
  ! This feature is particular to Fortran-90
  !
  M   = size(A,1)    ! Number of equations in the system
  HBW = size(A,2)    ! Half bandwidth of the original symmetric matrix

  if (M /= size(b)) then
    write(*,*) 'ERROR (symsl.f90): A and b do not have compatible dimensions'
    stop
  end if 
  
  !
  ! Factorize A  (LU decomposition)
  !
  if (case == 1 .or. case == 3) then       
    do i = 1, M                                          
      do j = 2, HBW                                         
        i1 = i+j-1                                          
        if(M < i1 .or. A(i,j) == 0.0) exit                           

        c  = A(i,j)/A(i,1)                    ! Pivot                  
        j1 = 0                                                    
        do k = j, HBW                                         
          j1 = j1+1                                                
          A(i1,j1) = A(i1,j1) - c*A(i,k)      ! Compute "U"
        end do
        A(i, j) = c                           ! Store element in "L"
      end do
    end do 
  end if
   
  !
  ! Solve Ax=b using decomposition of A
  !
  if (case == 2 .or. case == 3) then 
    do i = 1, M                               ! Forward substitution 
      do j = 2, HBW                                         
        i1 = i+j-1  
        if(M < i1 .or. A(i,j) == 0.0) exit
            
        b(i1) = b(i1) - A(i,j)*b(i)
      end do                                                 
      b(i) = b(i)/A(i,1)                              
    end do
  
    do i = M, 1, -1                           ! Backward substitution
      do j = 2, HBW                  
        i1 = i+j-1                                          
        if(M < i1 .or. A(i,j) == 0.0) exit                           

        b(i) = b(i) - A(i,j)*b(i1)                   
      end do 
    end do                     
  end if
end                                                      





