
#include "Python.h"


PyObject* default_action(PyObject *self, PyObject *args) {

  double x, y;

  // Convert Python argument to C  
  if (!PyArg_ParseTuple(args, "dd", &x, &y))
    return NULL;

  return Py_BuildValue("d", x-y);    
}	


PyObject* doit(PyObject *self, PyObject *args) {

  PyObject *func, *R;
  double x, y;

  // Convert Python argument to C  
  if (!PyArg_ParseTuple(args, "Odd", &func, &x, &y))
    return NULL;

  // Either is OK
  R = PyObject_CallFunction(func, "dd", x*x, y*y);
  //R = PyObject_CallObject(func, Py_BuildValue("dd", x*x, y*y));    

  return R;
}	
	


// Method table for python module
static struct PyMethodDef MethodTable[] = {
  {"doit", doit, METH_VARARGS},  
  {"default_action", default_action, METH_VARARGS},    
  {NULL, NULL}
};


// Module initialisation   
void initcallback_ext(void){
  Py_InitModule("callback_ext", MethodTable);
};

	
