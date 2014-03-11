"""Test passing arrays from python to f77 using f2py

To compile:
  f2py -c -m array_test array_test.f

To test:
  python array_test.py
  
 O Nielsen, GA - Sep 2003.
 Revised Nov 2004
 
"""


#First compile the fortran code using f2py
from Numeric import allclose

import f2py2e, os
#f2py2e.main()

s = os.sep

cmd = 'python C:%cPython23%cScripts%cf2py.py -c -m %s --compiler=mingw32 %s'\
      %(s,s,s,'array_test', 'array_test.f')

print cmd 
os.system(cmd)


from array_test import foo

print 'Doc string for fortran function foo'
print foo.__doc__

#Create Python Numeric array
A = [[1,2,3],[4,5,6]]

#Pass it on to foo
B=foo(A)

#Print result
print 'Result 1'
print B


#Various introspective tricks
print B.iscontiguous()

#Do it again
C=foo(B) # even if a is proper-contiguous
         # and has proper type, a copy is made
         # forced by intent(copy) attribute
         # to preserve its original contents

print
print 'Result 2'
print B    #Original array is preserved
print C
assert not allclose(B, C), 'B and C should have been different'


#Do it again with overwrite False
C=foo(B, overwrite_a=False) 

print
print 'Result 2'
print B    #Original array is preserved
print C
assert not allclose(B, C), 'B and C should have been different'



#Do it again but this time overwrite original array
C=foo(B, overwrite_a=True) 

print
print 'Result 3'
print B    #Original array is the same as new array
print C

assert allclose(B, C), 'B and C should have been identical'
assert B is C  # B and C are actually the same objects



