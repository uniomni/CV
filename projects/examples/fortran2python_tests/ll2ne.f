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
     
      subroutine ll2ne(lati, longi, northing, easting, zone, hemisphere)
c-------------------------------------------------
c Conversion from Latitude-Longitude to northing-
c easting
c-------------------------------------------------

c       Inputs:
c example        Cf2py   integer check(0<=j && j<mm),depend(mm) :: j
Cf2py   real *8 check(lati >= -90 && lati <= 90),intent(in) :: lati
Cf2py   real *8 check(longi >= -180 && longi <= 180),intent(in) :: longi
Cf2py   real *8 intent(out) :: northing
Cf2py   real *8 intent(out) :: easting
Cf2py   integer intent(out) :: zone
Cf2py   character intent(out) :: hemisphere

      implicit none

      integer zone
      real*8 lati,m,A0,A2,A4,A6,a,f,b,e,
     .       pi,rho,nu,psi,Term1,Term2,Term3,
     .       Term4,k0,omega,northing_dash,northing,easting,easting_dash,
     .       t,longi,lambda0,false_easting,false_northing

      character hemisphere*1
     

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

      if(lati .lt. 0) then
        hemisphere = 'S' 
        false_northing = 10000000.d0
      else
        hemisphere = 'N'
        false_northing = 0.d0        
      end if


c-------------------------------------------------
c Longitude of western edge of zone zero is -186,
c central meridian of zone zero is -183, and zone
c width is 6 degrees. The zone of the point of
c interest is given by
c     zone = longitude/6 + 31 (integer arithmetic)
c-------------------------------------------------
      zone = int((longi + 183.d0)/6.d0)

c-------------------------------------------------
c Geodetic longitude of the central meridian
c-------------------------------------------------
      lambda0 = float(zone)*6.d0 - 183.d0
      lambda0 = lambda0*pi/180.d0

c-------------------------------------------------
c longi is the longitude of the point of interest
c positive eastward in radians
c phi 2 is the latitude positive northwards in radians
c-------------------------------------------------      
      longi = longi*pi/180.d0
      lati = lati*pi/180.d0       
       
c-------------------------------------------------
c Geodetic longitude difference measured from the
c central meridian, positive eastward
c-------------------------------------------------
      omega = longi - lambda0

c-------------------------------------------------
c Arc of the meridian
c-------------------------------------------------
      A0 = 1.d0 - (e*e/4) - (3.d0*e**4/64.d0) - (5.d0*e**6/256.d0)
      A2 = 3.d0/8.d0*(e*e + e**4/4.d0 + 15.d0*e**6/128.d0)
      A4 = 15.d0/256.d0*(e**4 + 3.d0*e**6/4.d0)
      A6 = 35.d0*e**6/3072.d0

      m = a*(A0*lati - A2*dsin(2.d0*lati) + A4*dsin(4.d0*lati)
     .               - A6*dsin(6.d0*lati))

c-------------------------------------------------
c Radius of curvature
c-------------------------------------------------
      rho = a*(1.d0 - e*e)/dsqrt((1.d0 - (e*dsin(lati))**2)**3.)
      nu = a/dsqrt(1.d0 -(e*dsin(lati))**2)
      psi = nu/rho

c-------------------------------------------------
c Calculation of easting
c-------------------------------------------------
      t = dtan(lati)
      Term1 = nu*omega*dcos(lati)
      Term2 = Term1*(omega*omega/6.d0*(dcos(lati))**2*(psi - t*t))
      Term3 = Term1*(omega**4/120.d0*(dcos(lati))**4
     .                               *(4.d0*psi**3*(1.d0 - 6.d0*t*t)
     .                               + psi*psi*(1.d0 + 8.d0*t*t)
     .                               - psi*2.d0*t*t + t**4))
      Term4 = Term1*(omega**6/5040d0*(dcos(lati))**6
     .                                 *(61.d0 - 479.d0*t*t
     .                                   +179.d0*t**4 - t**6))
      easting_dash = k0*(Term1 + Term2 + Term3 + Term4)
      easting = easting_dash + false_easting

c-------------------------------------------------
c Calculation of northing
c-------------------------------------------------
      Term1 = omega*omega/2.d0*nu*dsin(lati)*dcos(lati)
      Term2 = omega**4/24.d0*nu*dsin(lati)*(dcos(lati))**3
     .                          *(4.d0*psi**2 + psi - t*t)
      Term3 = omega**6/720d0*nu*dsin(lati)*(dcos(lati))**5
     .        *(8.d0*psi**4*(11.d0 - 24d0*t*t)
     .        - 28.d0*psi**3*(1.d0 - 6.d0*t*t)
     .        + psi*psi*(1.d0 - 32.d0*t*t)
     .        - psi*2.d0*t*t + t**4)
      Term4 = omega**8/40320d0*nu*dsin(lati)*(dcos(lati))**7
     .         *(1385.d0 - 3111.d0*t*t + 543.d0*t**4 - t**6)
      northing_dash = k0*(m + Term1 + Term2 + Term3 + Term4)
      northing = northing_dash + false_northing
            
c       write(*,*)northing,easting,zone
       
      return 
      end
