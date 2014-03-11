/* File: array_testmodule.c
 * This file is auto-generated with f2py (version:2.43.239_1844).
 * f2py is a Fortran to Python Interface Generator (FPIG), Second Edition,
 * written by Pearu Peterson <pearu@cens.ioc.ee>.
 * See http://cens.ioc.ee/projects/f2py2e/
 * Generation date: Wed Nov 17 15:51:46 2004
 * $Revision:$
 * $Date:$
 * Do not edit this file directly unless you know what you are doing!!!
 */
#ifdef __cplusplus
extern "C" {
#endif

/*********************** See f2py2e/cfuncs.py: includes ***********************/
#include "Python.h"
#include "fortranobject.h"
#include <math.h>

/**************** See f2py2e/rules.py: mod_rules['modulebody'] ****************/
static PyObject *array_test_error;

/*********************** See f2py2e/cfuncs.py: typedefs ***********************/
/*need_typedefs*/

/********************** See f2py2e/cfuncs.py: cppmacros **********************/
#if defined(PREPEND_FORTRAN)
#if defined(NO_APPEND_FORTRAN)
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) _##F
#else
#define F_FUNC(f,F) _##f
#endif
#else
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) _##F##_
#else
#define F_FUNC(f,F) _##f##_
#endif
#endif
#else
#if defined(NO_APPEND_FORTRAN)
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F
#else
#define F_FUNC(f,F) f
#endif
#else
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F##_
#else
#define F_FUNC(f,F) f##_
#endif
#endif
#endif

#define rank(var) var ## _Rank
#define shape(var,dim) var ## _Dims[dim]
#define old_rank(var) (((PyArrayObject *)(capi_ ## var ## _tmp))->nd)
#define old_shape(var,dim) (((PyArrayObject *)(capi_ ## var ## _tmp))->dimensions[dim])
#define fshape(var,dim) shape(var,rank(var)-dim-1)
#define len(var) shape(var,0)
#define flen(var) fshape(var,0)
#define size(var) PyArray_SIZE((PyArrayObject *)(capi_ ## var ## _tmp))
/* #define index(i) capi_i ## i */
#define slen(var) capi_ ## var ## _len

#define CHECKSCALAR(check,tcheck,name,show,var)\
  if (!(check)) {\
    PyErr_SetString(array_test_error,"("tcheck") failed for "name);\
    fprintf(stderr,show"\n",var);\
    /*goto capi_fail;*/\
  } else 
#ifdef DEBUGCFUNCS
#define CFUNCSMESS(mess) fprintf(stderr,"debug-capi:"mess);
#define CFUNCSMESSPY(mess,obj) CFUNCSMESS(mess) \
  PyObject_Print((PyObject *)obj,stderr,Py_PRINT_RAW);\
  fprintf(stderr,"\n");
#else
#define CFUNCSMESS(mess)
#define CFUNCSMESSPY(mess,obj)
#endif

#ifndef MAX
#define MAX(a,b) ((a > b) ? (a) : (b))
#endif
#ifndef MIN
#define MIN(a,b) ((a < b) ? (a) : (b))
#endif


/* See f2py2e/rules.py */
extern void F_FUNC(FOO,FOO)(double*,int*,int*);
/*eof externroutines*/

/************************ See f2py2e/cfuncs.py: cfuncs ************************/
static int int_from_pyobj(int* v,PyObject *obj,const char *errmess) {
  PyObject* tmp = NULL;
  if (PyInt_Check(obj)) {
    *v = (int)PyInt_AS_LONG(obj);
    return 1;
  }
  tmp = PyNumber_Int(obj);
  if (tmp) {
    *v = PyInt_AS_LONG(tmp);
    Py_DECREF(tmp);
    return 1;
  }
  if (PyComplex_Check(obj))
    tmp = PyObject_GetAttrString(obj,"real");
  else if (PyString_Check(obj))
    /*pass*/;
  else if (PySequence_Check(obj))
    tmp = PySequence_GetItem(obj,0);
  if (tmp) {
    PyErr_Clear();
    if (int_from_pyobj(v,tmp,errmess)) {Py_DECREF(tmp); return 1;}
    Py_DECREF(tmp);
  }
  {
    PyObject* err = PyErr_Occurred();
    if (err==NULL) err = array_test_error;
    PyErr_SetString(err,errmess);
  }
  return 0;
}


/********************* See f2py2e/cfuncs.py: userincludes *********************/
/*need_userincludes*/

/********************* See f2py2e/capi_rules.py: usercode *********************/


/******************* See f2py2e/cb_rules.py: buildcallback *******************/
/*need_callbacks*/

/*********************** See f2py2e/rules.py: buildapi ***********************/

/************************************ FOO ************************************/
static char doc_f2py_rout_array_test_FOO[] = "\
Function signature:\n\
  FOO(A,[N,M])\n\
Required arguments:\n"
"  A : input rank-2 array('d') with bounds (N,M)\n"
"Optional arguments:\n"
"  N := shape(A,0) input int\n"
"  M := shape(A,1) input int";
/* extern void F_FUNC(FOO,FOO)(double*,int*,int*); */
static PyObject *f2py_rout_array_test_FOO(const PyObject *capi_self,
                           PyObject *capi_args,
                           PyObject *capi_keywds,
                           void (*f2py_func)(double*,int*,int*)) {
  PyObject * volatile capi_buildvalue = NULL;
  volatile int f2py_success = 1;
/*decl*/

  double *A = NULL;
  int A_Dims[2] = {-1, -1};
  const int A_Rank = 2;
  PyArrayObject *capi_A_tmp = NULL;
  int capi_A_intent = 0;
  PyObject *A_capi = Py_None;
  int N = 0;
  PyObject *N_capi = Py_None;
  int M = 0;
  PyObject *M_capi = Py_None;
  static char *capi_kwlist[] = {"A","N","M",NULL};

/*routdebugenter*/
#ifdef F2PY_REPORT_ATEXIT
f2py_start_clock();
#endif
  if (!PyArg_ParseTupleAndKeywords(capi_args,capi_keywds,\
    "O|OO:array_test.FOO",\
    capi_kwlist,&A_capi,&N_capi,&M_capi))
    return NULL;
/*frompyobj*/
  /* Processing variable A */
  ;
  capi_A_intent |= F2PY_INTENT_IN;
  capi_A_tmp = array_from_pyobj(PyArray_DOUBLE,A_Dims,A_Rank,capi_A_intent,A_capi);
  if (capi_A_tmp == NULL) {
    if (!PyErr_Occurred())
      PyErr_SetString(array_test_error,"failed in converting 1st argument `A' of array_test.FOO to C/Fortran array" );
  } else {
    A = (double *)(capi_A_tmp->data);
  /* Processing variable M */
  if (M_capi == Py_None) M = shape(A,1); else
    f2py_success = int_from_pyobj(&M,M_capi,"array_test.FOO() 2nd keyword (M) can't be converted to int");
  if (f2py_success) {
  CHECKSCALAR(shape(A,1)==M,"shape(A,1)==M","2nd keyword M","FOO:M=%d",M) {
  /* Processing variable N */
  if (N_capi == Py_None) N = shape(A,0); else
    f2py_success = int_from_pyobj(&N,N_capi,"array_test.FOO() 1st keyword (N) can't be converted to int");
  if (f2py_success) {
  CHECKSCALAR(shape(A,0)==N,"shape(A,0)==N","1st keyword N","FOO:N=%d",N) {
/*end of frompyobj*/
#ifdef F2PY_REPORT_ATEXIT
f2py_start_call_clock();
#endif
/*callfortranroutine*/
        (*f2py_func)(A,&N,&M);
#ifdef F2PY_REPORT_ATEXIT
f2py_stop_call_clock();
#endif
/*end of callfortranroutine*/
    if (f2py_success) {
/*pyobjfrom*/
/*end of pyobjfrom*/
    CFUNCSMESS("Building return value.\n");
    capi_buildvalue = Py_BuildValue("");
/*closepyobjfrom*/
/*end of closepyobjfrom*/
    } /*if (f2py_success) after callfortranroutine*/
/*cleanupfrompyobj*/
  } /*CHECKSCALAR(shape(A,0)==N)*/
  } /*if (f2py_success) of N*/
  /* End of cleaning variable N */
  } /*CHECKSCALAR(shape(A,1)==M)*/
  } /*if (f2py_success) of M*/
  /* End of cleaning variable M */
  if((PyObject *)capi_A_tmp!=A_capi) {
    Py_XDECREF(capi_A_tmp); }
  }  /*if (capi_A_tmp == NULL) ... else of A*/
  /* End of cleaning variable A */
/*end of cleanupfrompyobj*/
  if (capi_buildvalue == NULL) {
/*routdebugfailure*/
  } else {
/*routdebugleave*/
  }
  CFUNCSMESS("Freeing memory.\n");
/*freemem*/
#ifdef F2PY_REPORT_ATEXIT
f2py_stop_clock();
#endif
  return capi_buildvalue;
}
/********************************* end of FOO *********************************/
/*eof body*/

/******************* See f2py2e/f90mod_rules.py: buildhooks *******************/
/*need_f90modhooks*/

/************** See f2py2e/rules.py: module_rules['modulebody'] **************/

/******************* See f2py2e/common_rules.py: buildhooks *******************/

/*need_commonhooks*/

/**************************** See f2py2e/rules.py ****************************/

static char doc_f2py_has_column_major_storage[] = "\
Function has_column_major_storage(obj):\n\
  Return transpose(obj).iscontiguous().\n";
static PyObject *f2py_has_column_major_storage(PyObject *self,PyObject *args) {
  PyObject * obj = NULL;
  if (!PyArg_ParseTuple(args, "O",&obj))
    return NULL;
  return Py_BuildValue("i",(PyArray_Check(obj)? array_has_column_major_storage((PyArrayObject*)(obj)):0));
}

static char doc_f2py_as_column_major_storage[] = "\
Function as_column_major_storage(arr):\n\
  Return array in column major data storage order.\n";
static PyObject *f2py_as_column_major_storage(PyObject *self,PyObject *args) {
  PyObject * obj = NULL;
  PyArrayObject * arr = NULL;
  if (!PyArg_ParseTuple(args, "O",&obj))
    return NULL;
  if (!PyArray_Check(obj)) {
    PyErr_SetString(array_test_error,"expected array object\n");
    return NULL;
  }
  arr = (PyArrayObject*)obj;
  arr = array_from_pyobj(arr->descr->type_num, arr->dimensions, arr->nd,
                         F2PY_INTENT_OUT|F2PY_INTENT_IN, obj);
  if (arr == NULL) {
    if (!PyErr_Occurred())
      PyErr_SetString(array_test_error,
        "failed in converting argument to C/Fortran array");
    return NULL;
  }
  return Py_BuildValue("N",arr);
}

static FortranDataDef f2py_routine_defs[] = {
  {"FOO",-1,{{-1}},0,(char *)F_FUNC(FOO,FOO),(f2py_init_func)f2py_rout_array_test_FOO,doc_f2py_rout_array_test_FOO},

/*eof routine_defs*/
  {NULL}
};

static PyMethodDef f2py_module_methods[] = {

  {"has_column_major_storage",f2py_has_column_major_storage,METH_VARARGS,doc_f2py_has_column_major_storage},
  {"as_column_major_storage",f2py_as_column_major_storage,METH_VARARGS,doc_f2py_as_column_major_storage},
  {NULL,NULL}
};

DL_EXPORT(void) initarray_test(void) {
  int i;
  PyObject *m,*d, *s;
  m = Py_InitModule("array_test", f2py_module_methods);
  PyFortran_Type.ob_type = &PyType_Type;
  import_array();
  if (PyErr_Occurred())
    Py_FatalError("can't initialize module array_test (failed to import _numpy)");
#if !defined(NUMARRAY)
  if (PyImport_ImportModule("Numeric")==NULL) {
    PyErr_Print();
    Py_FatalError("can't initialize module array_test");
  }
#else
  import_libnumarray();
#endif
  d = PyModule_GetDict(m);
  s = PyString_FromString("$Revision: $");
  PyDict_SetItemString(d, "__version__", s);
  s = PyString_FromString("This module 'array_test' is auto-generated with f2py (version:2.43.239_1844).\nFunctions:\n"
"  FOO(A,N=shape(A,0),M=shape(A,1))\n"
".");
  PyDict_SetItemString(d, "__doc__", s);
  array_test_error = PyErr_NewException ("array_test.error", NULL, NULL);
  Py_DECREF(s);
  for(i=0;f2py_routine_defs[i].name!=NULL;i++)
    PyDict_SetItemString(d, f2py_routine_defs[i].name,PyFortranObject_NewAsAttr(&f2py_routine_defs[i]));
/*eof initf90modhooks*/

/*eof initcommonhooks*/

  if (PyErr_Occurred())
    Py_FatalError("can't initialize module array_test");

#ifdef F2PY_REPORT_ATEXIT
  on_exit(f2py_report_on_exit,(void*)"array_test");
#endif

}
#ifdef __cplusplus
}
#endif
