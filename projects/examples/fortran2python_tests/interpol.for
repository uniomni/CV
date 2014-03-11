C     Last change:  ON   17 Nov 2004    5:00 pm

      SUBROUTINE polint(xa,ya,n,x,y,dy)
C
C       Cubic Interpolation 
C
      
        INTEGER n,NMAX
        REAL dy,x,y,xa(n),ya(n)
        PARAMETER (NMAX = 100)
        INTEGER i,m,ns
        REAL den,dif,dift,ho,hp,w,c(NMAX),d(NMAX)
        
Cf2py   intent(out) y, dy      
Cf2py   intent(in) xa, ya, x
Cf2py   integer intent(hide),depend(xa) :: n=shape(xa,0)
        
        nx = 1
        dif = abs(x-xa(1))
        do 11 i=1,n
            dift = abs(x-xa(i))
            if(dift .lt. dif) then
                ns = i
                dif = dift
            endif
            c(i) = ya(i)
            d(i) = ya(i)
11      ENDDO
        y = ya(ns)
        ns = ns - 1
        do 13 m=1,n-1
            do 12 i=1,n-m
                ho = xa(i)-x
                hp=xa(i+m)-x
                w=c(i+1)-d(i)
                den=ho-hp
                IF(den .EQ. 0.0) PAUSE 'failure in polint'
                den = w/den
                d(i) = hp*den
                c(i) = ho*den
12      end do
            if(2*ns .LT. n-m)then
               dy = c(ns+1)
            else
               dy = d(ns)
               ns = ns - 1
            endif
            y = y + dy
13      end do
        return
      end






