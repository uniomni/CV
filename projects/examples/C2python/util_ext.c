// Python - C extension for finite_volumes util module.
//
// To compile (Python2.3):
//  gcc -c util_ext.c -I/usr/include/python2.3 -o util_ext.o -Wall -O
//  gcc -shared util_ext.o  -o util_ext.so
//
// See the module util.py
//
//
// Ole Nielsen, GA 2004
//


#include <float.h>

#include "Python.h"
#include "Numeric/arrayobject.h"
#include "math.h"

PyObject *hello(PyObject *self, PyObject *args) {
  char *text="None";
  
  // Convert Python arguments to C
  if (!PyArg_ParseTuple(args, "s", &text)) {
    PyErr_SetString(PyExc_RuntimeError, 
		    "hello could not parse input");      
    return NULL;
  }
  
  printf("%s\n", text);
  
  return Py_BuildValue("");
}


int _gradient(double x0, double y0, 
	      double x1, double y1, 
	      double q0, double q1, 
	      double *a, double *b) {
  /*Compute gradient (a,b) between two points (x0,y0) and (x1,y1) 
  with values q0 and q1 such that the plane is constant in the direction 
  orthogonal to (x1-x0, y1-y0).
  
  Extrapolation formula
    q(x,y) = q0 + a*(x-x0) + b*(y-y0)                    (1)
  
  Substituting the known values for q1 into (1) yields an 
  under determined  equation for a and b 
      q1-q0 = a*(x1-x0) + b*(y1-y0)                      (2)
      
      
  Now add the additional requirement that the gradient in the direction 
  orthogonal to (x1-x0, y1-y0) should be zero. The orthogonal direction 
  is given by the vector (y0-y1, x1-x0).
  
  Define the point (x2, y2) = (x0 + y0-y1, y0 + x1-x0) on the orthognal line. 
  Then we know that the corresponding value q2 should be equal to q0 in order 
  to obtain the zero gradient, hence applying (1) again    
      q0 = q2 = q(x2, y2) = q0 + a*(x2-x0) + b*(y2-y0)
                          = q0 + a*(x0 + y0-y1-x0) + b*(y0 + x1-x0 - y0)
			  = q0 + a*(y0-y1) + b*(x1-x0)
			  
  leads to the orthogonality constraint
     a*(y0-y1) + b*(x1-x0) = 0                           (3) 
     
  which closes the system and yields
  
  /               \  /   \   /       \  
  |  x1-x0  y1-y0 |  | a |   | q1-q0 |
  |               |  |   | = |       | 
  |  y0-y1  x1-x0 |  | b |   |   0   |
  \               /  \   /   \       /
   
  which is solved using the standard determinant technique    
      
  */

  double det, xx, yy, qq;
  
  xx = x1-x0;
  yy = y1-y0;
  qq = q1-q0;
    
  det = xx*xx + yy*yy;  //FIXME  catch det == 0
  *a = xx*qq/det;
  *b = yy*qq/det;
        
  return 0;
}


PyObject *gradient(PyObject *self, PyObject *args) {
  //
  // a,b = gradient(x0, y0, x1, y1, q0, q1)
  //

  double x0, y0, x1, y1, q0, q1, a, b;
  PyObject *result;

  // Convert Python arguments to C
  if (!PyArg_ParseTuple(args, "dddddd", &x0, &y0, &x1, &y1, &q0, &q1)) {
    PyErr_SetString(PyExc_RuntimeError, 
		    "gradient could not parse input");      
    return NULL;
  }


  // Call underlying routine
  _gradient(x0, y0, x1, y1, q0, q1, &a, &b);

  // Return values a and b
  result = Py_BuildValue("dd", a, b);
  return result;
}

PyObject * double_precision(PyObject * self, PyObject * args){
  // Get the precision of the double datatype on this system.
  return Py_BuildValue("i", DBL_DIG);
}

// Method table for python module
static struct PyMethodDef MethodTable[] = {
  /* The cast of the function is necessary since PyCFunction values
   * only take two PyObject* parameters, and rotate() takes
   * three.
   */

  //{"rotate", (PyCFunction)rotate, METH_VARARGS | METH_KEYWORDS, "Print out"},
  {"gradient", gradient, METH_VARARGS, "Print out"},
  {"hello", hello, METH_VARARGS, "Print out"},  
  {"double_precision", double_precision, METH_VARARGS, "Precision of this machine\'s \'double\' type"},
  {NULL, NULL, 0, NULL}   /* sentinel */
};



// Module initialisation
void initutil_ext(void){
  Py_InitModule("util_ext", MethodTable);

  import_array();     //Necessary for handling of NumPY structures
}




