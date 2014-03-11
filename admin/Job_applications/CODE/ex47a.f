C     Course 8811, part 3, exercise 4.7a
C
C     Solves the heat equation on the unit square domain Omega
C
C        c U_t = lamb1 (U_xx + U_yy) + Q(x,y,t), (x,y) in Omega
C        U = f(x,y,t)                            (x,y) in Sigma 
C        U(x,y,0) = 
C
C     with
C        f(x,y)   = 
C        Q(x,y,t) = 
C
C     using the theta FEM method.
C
C
C     A convergence study depending on theta and dt is made
C
C     
      program ex47a
        implicit none
        integer neqmax, nelmax, hbwmax, nbmax
         parameter (neqmax = 65*65, nelmax=65*65*2, 
     &             hbwmax=70, nbmax=2*(100+100))

        integer noel, noeh, neq, noelm, hbw, nbnode, center
        integer i, j, p, d, n, lastn, glob(nelmax,3), bnode(nbmax) 

        double precision lamb1, lamb2, cc, order
        double precision dl, dh, delta, epsilon, endtime
        double precision dt, theta, d1, d2, temp
        double precision x(neqmax), y(neqmax)
        double precision A(neqmax, hbwmax), C(neqmax, hbwmax)
        double precision RA(neqmax, hbwmax), SA(neqmax, hbwmax)
        double precision rv(neqmax), U(neqmax), E(neqmax)
        double precision U1(neqmax), U2(neqmax)
        double precision abc(3,3), PI, f, df
        parameter (epsilon = 1.0e-12)
        parameter (PI=3.1415926535897926433)
        double precision analytic, maxabsdif
        logical belongs
        external analytic, maxabsdif, belongs

C       --------------------------------------------------------
C       PARAMETERS
C       --------------------------------------------------------
        dl = 1.D0       ! Length of domain
        dh = 1.D0       ! Height of domain
        noel  = 8       ! Number of rectangles in the x direction
        noeh  = 8       ! Number of rectangles in the y direction
        lamb1 = 1.D0    ! Heat conductivity in x direction
        lamb2 = 1.D0    ! Heat conductivity in x direction
        cc    = 10.D0   ! Specific heat
        theta = 0.5     ! Method parameter theta in [0,1]
        endtime = 1.D0  

        write (*,*) '------------- Exercise 4.7a -------'
        write (*,*) 'theta = ', theta, ', dt = 1/2^p '
        write (*,*) '  p     q'
        write (*,*) '-----------------------------------'

        neq    = (noel+1)*(noeh+1) ! Number of nodes
        noelm  = 2*noeh*noel       ! Number of elements
        nbnode = 2*(noeh+noel)     ! Number of Dirichlet bdry nodes
        center = (neq+1)/2

C       ------------------------------
C       Build FEM structure
C       ------------------------------
        call xy (neq, noel, noeh, dl, dh, x, y)
        call elmtab (nelmax, noelm, noel, noeh, glob, hbw)

C       ------------------------------
C       Record Dirichlet boundary nodes
C       ------------------------------
        d = 0
        do i = 0, noel        
          do j = 0, noeh  
            if (i .eq. noel .or. j .eq. noeh .or. 
     &          i .eq. 0    .or. j .eq. 0) then
              d = d + 1
              bnode(d) = i*(noeh+1)+j+1  ! Dirichlet node
            end if
          end do
        end do  
        if (d .ne. nbnode) then
           print *, 'ERROR: d /= nbnode'
           stop
        end if

C       ------------------------------
C       Perform computations for various dt         
C       ------------------------------
        dt   = 1.D0
        do p = 0, 12     
          d1    = dt*theta
          d2    = dt*(1-theta)
          lastn = endtime/dt   ! Number of timesteps

C         ------------------------------
C         Set initial condition
C         ------------------------------
          do j = 1, neq
            U(j) = sin(pi*x(j))*sin(pi*y(j))
          end do
          do j = 1, nbnode   ! Enforce boundary conditions at t = 0
            i = bnode(j)
            call boundary(x(i), y(i), 0.D0, f, df)
            U(i) = f                
          end do  

C         ------------------------------
C         Create matrices (without boundary conditions)
C         ------------------------------
          call saml (neqmax, neq, nelmax, noelm, x, y, glob, hbw, 
     &               delta, abc, lamb1, lamb2, cc, RA, SA, rv)


C         ------------------------------
C         Update R and S according to boundary conditions
C         Also compute rv at time = 0
C         ------------------------------
          call dirbc (neqmax, neq, hbw, nbnode, bnode, 
     &                RA, SA, A, C, rv, x, y)


C         ------------------------------
C         Compute matrices S = C - d2 A  and  
C                          R = S + dt A (R = C + d1 A)
C         ------------------------------
          do i = 1, neq        
            do j = 1, hbw  
              SA(i,j) = SA(i,j) - d2*RA(i,j) 
              RA(i,j) = SA(i,j) + dt*RA(i,j) 
            end do
          end do  

C         ------------------------------
C         Factorize matrix R
C         ------------------------------
          call symsl (neqmax, 1, RA, neq, hbw, rv)


C         ------------------------------
C         Take lastn timesteps, i.e. advance time until time = lastn*dt
C         ------------------------------
          do n = 1, lastn
            call symmul (neqmax, neq, hbw, SA, U, E)    ! Compute E = SA*U

C           -------------------------------------------
C           Boundary updates
C           -------------------------------------------
            do i = 1, neq
              E(i) = E(i) + d2*rv(i)
            end do

            call samlb (neqmax, neq, nelmax, noelm, x, y, n*dt, glob, 
     &                  delta, abc, lamb1, lamb2, cc, rv)
            call updateb (neqmax, neq, hbw, nbnode, bnode, 
     &                    A, C, rv, x, y, n*dt)

            do i = 1, neq
              U(i) = E(i) + d1*rv(i)
            end do

C           -------------------------------------------
C           Solve linear system 
C           -------------------------------------------
            call symsl (neqmax, 2, RA, neq, hbw, U)

C           -------------------------------------------
C           Enforce Dirichlet boundary conditions explicitly
C           -------------------------------------------
            do j = 1, nbnode
              i = bnode(j)
              call boundary(x(i), y(i), n*dt, f, df)
              U(i) = f                
            end do  
          end do

C         -------------------------------------------
C         Estimate order of convergence
C         -------------------------------------------
          if (p .ge. 2) then
            temp  = maxabsdif(neq, U1, U)
            order = maxabsdif(neq, U2, U1)/temp
            order = log(abs(order))/log(2.D0)

 9999       format(I4, F10.4)
            if (p .gt. 1) write (*,9999) p, order
          end if  

C         Save U values for subsequent estimates of order
          do i = 1, neq
            U2(i) = U1(i)      ! Coarsest solution      (4*dt)
            U1(i) = U (i)      ! Finer solution         (2*dt)
          end do  
          dt = dt/2 ! Decrease timestep 
        end do


C       ------------------------------------               
C       Output FEM solution
C       ------------------------------------               
        call output(neq,x,y,U,'dat')

C       ------------------------------------               
C       Output Analytic solution
C       ------------------------------------               

        do i=1, neq
          E(i) = analytic (lamb1, cc, x(i), y(i), endtime) 
        end do   

        call output(neq,x,y,E,'ana')
      end  











