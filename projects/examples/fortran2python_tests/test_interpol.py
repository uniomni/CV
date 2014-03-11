"""Test passing arrays from python to f77 using f2py

 This is a cubic spline interpolation routine 

 O Nielsen, GA - Sep 2003.
 Revised Nov 2004
 
"""


try:
    import interpol
except:    
    #Attempt to compile the fortran code using f2py
    import f2py2e, os
    s = os.sep
    cmd = 'python C:%cPython23%cScripts%cf2py.py -c -m %s --compiler=mingw32 %s'\
      %(s,s,s,'interpol', 'interpol.for')
    os.system(cmd)


from interpol import polint

print 'Doc string for fortran function interpol'
print polint.__doc__

#Create Python Numeric arrays (quadratic)
xa = [1,2,3,4,5,6,7,8,9]
ya = [1,4,9,16,25,36,49,64,81]

#Interpolation point
x = 5.5

#Pass it on to polint
y, dy = polint(xa, ya, x)

#Print result
print 'Results'
print y, dy  #Error should be zero




