  
c-------------------------------------------------
c Subroutines to convert latitudes and longitudes to
c northings and eastings or longitude and latitudes
c to northings and eastings using the Redfearn's
c formulae. Ref. Geocentric Datum of Australia
c Technical Manual, Version 2.2, ICSM
c (Inter governmental Committee on Surveying and
c Mapping), Australia. (see Geoscience Australia)
c
c Adapted for Python by OMN, GA - August 2003
c-------------------------------------------------


      subroutine ne2ll(northing, easting, zone, hemisphere, lati, longi)            

c-------------------------------------------------
c Conversion from northing-
c easting to Latitude-Longitude 
c-------------------------------------------------

c       Inputs:
c example        Cf2py   integer check(0<=j && j<mm),depend(mm) :: j
Cf2py   real *8 intent(in) :: northing
Cf2py   real *8 intent(in) :: easting
Cf2py   integer check(zone>=0),intent(in) :: zone
Cf2py   character intent(in) :: hemisphere
Cf2py   real *8 intent(out) :: lati
Cf2py   real *8 intent(out) :: longi

     
      implicit none
      
      integer zone
      real*8 lati,m,a,f,b,e,x,phi,sigma,dsec,
     .       pi,rho,nu,psi,Term1,Term2,Term3,g,n,easting_dash,
     .       Term4,k0,omega,northing_dash,northing,easting,
     .       t,longi,lambda0,false_easting,false_northing

      character hemisphere*1
           
      dsec(x) = 1.d0/dcos(x)
   
c     CONSTANTS      
      pi = 4.d0*datan(1.d0)
      
c-------------------------------------------------
c Scale factor on the central meridian
c-------------------------------------------------
      k0 = 0.9996d0

c-------------------------------------------------
c Ellipsoid semi-major axis
c-------------------------------------------------
      a = 6378137.d0

c-------------------------------------------------
c Flattening
c-------------------------------------------------
      f = 1.d0/298.257222101d0

c-------------------------------------------------
c Ellipsoid semi-minor axis; b = a(1 - f)
c-------------------------------------------------
      b = a*(1.d0 - f)

c-------------------------------------------------
c Eccentricity
c-------------------------------------------------
      e = dsqrt((a*a - b*b)/a**2)

c------------------------------------------------
c false easting and northing
c------------------------------------------------
      false_easting = 500000.d0

      if(hemisphere.eq.'S')then
         false_northing = 10000000.d0
      else
         false_northing = 0.d0        
      end if

      northing_dash = northing - false_northing
      easting_dash = easting - false_easting

      
c-------------------------------------------------
c Geodetic longitude of the central meridian
c-------------------------------------------------
      lambda0 = float(zone)*6.d0 - 183.d0
      lambda0 = lambda0*pi/180.d0

c-------------------------------------------------
c Arc of the meridian m = N'/k0
c-------------------------------------------------
      m = northing_dash/k0

c-------------------------------------------------
c Foot-point Latitude
c-------------------------------------------------
      n = f/(2.d0 - f)
      G = a*(1.d0 - n)*(1.d0 - n*n)*(1.d0 + 9.d0/4.d0*n*n
     .      + 225.d0/64.d0*n**4)*pi/180.d0
      sigma = m*pi/180.d0/G
      Term1 = ((3.d0*n/2.d0) - (27.d0*n**3/32.d0))*dsin(2.d0*sigma)
      Term2 = ((21.d0*n*n/16.d0)
     .           - (55.d0*n**4/32.d0))*dsin(4.d0*sigma)
      Term3 = (151.d0*n**3/96.d0)*dsin(6.d0*sigma)
      Term4 = (1097.d0*n**4/512.d0)*dsin(8.d0*sigma)
      phi = sigma + Term1 + Term2 + Term3 + Term4
      
c-------------------------------------------------
c Radius of curvature
c-------------------------------------------------
      rho = a*(1.d0 - e*e)/dsqrt((1.d0 - (e*dsin(phi))**2)**3.)
      nu = a/dsqrt(1.d0 -(e*dsin(phi))**2)
      psi = nu/rho

      x = easting_dash/(k0*nu)
      t = dtan(phi)

c-------------------------------------------------
c Latitude of the point of interest
c-------------------------------------------------
      Term1 = t/(k0*rho)*x*easting_dash/2.d0
      Term2 = t/(k0*rho)*(easting_dash*x**3/24.d0)*(-4.d0*psi**2
     .                    + 9.d0*psi*(1.d0 - t*t) + 12.d0*t*t)
      Term3 = t/(k0*rho)*(easting_dash*x**5/720.d0)*(8.d0*psi**4
     .                    *(11.d0 - 24.d0*t*t) - 12.d0*psi**3*(21.d0
     .                    - 71.d0*t*t) + 15.d0*psi*psi*(15.d0
     .                    - 98.d0*t*t + 15.d0*t**4)
     .                    + 180.d0*psi*(5.d0*t*t - 3.d0*t**4)
     .                    + 360.d0*t**4)
      Term4 = t/(k0*rho)*(easting_dash*x**7/40320.d0)*(1385.d0
     .                    + 3633.d0*t*t + 4095.d0*t**4 + 1575.d0*t**6)
      lati = phi - Term1 + Term2 -Term3 + Term4
      lati = 180.d0*lati/pi
      
c-------------------------------------------------
c Longitude of the point of interest
c-------------------------------------------------
      Term1 = x*dsec(phi)
      Term2 = x**3/6.d0*dsec(phi)*(psi + 2.d0*t*t)
      Term3 = x**5/120.d0*dsec(phi)*(-4.d0*psi**3*(1.d0 - 6.d0*t*t)
     .          + psi**2*(9.d0 - 68.d0*t*t) + 72.d0*psi*t**2
     .          + 24.d0*t**4)
      Term4 = x**7/5040.d0*dsec(phi)*(61.d0 + 662.d0*t*t
     .          + 1320.d0*t**4 + 720.d0*t**6)
      omega = Term1 - Term2 +Term3 + Term4
      longi = lambda0 + omega
      longi = 180.d0*longi/pi
            
C      write(*,*)lati,longi,zone

      return
      
      end

