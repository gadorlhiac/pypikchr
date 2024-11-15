#include "pikchr.h"

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#ifndef Py_PYTHON_H
  #error "Python headers required"
#endif

#define MODULE_NAME "pypikchr.util.pikchr"
#define MODULE_DOC "Thin Python wrapper around the pikchr C library."
#define MODULE_PER_INTERPRET_SIZE -1


static PyObject *PikchrError;
static PyObject *pikchr_create_pikchr(PyObject*, PyObject*);

static PyMethodDef pikchr_methods[] = {
  {"create_pikchr", pikchr_create_pikchr, METH_VARARGS, "Compile pikchr markdown."},
  {NULL,NULL,0,NULL}
};

static struct PyModuleDef pikchr_module = {
  PyModuleDef_HEAD_INIT,
  MODULE_NAME,
  MODULE_DOC,
  MODULE_PER_INTERPRET_SIZE,
  pikchr_methods
};

PyMODINIT_FUNC PyInit_pikchr(void) {
  PyObject *m;

  m = PyModule_Create(&pikchr_module);
  if (m == NULL)
    return NULL;

  PikchrError = PyErr_NewException(MODULE_NAME".PikchrException", NULL, NULL);
  if (PyModule_AddObjectRef(m, "PikchrException", PikchrError) < 0) {
    Py_CLEAR(PikchrError);
    Py_DECREF(m);
    return NULL;
  }

  return m;
}

static PyObject *pikchr_create_pikchr(PyObject *self, PyObject *args)
{
  const char *in_str;
  const char *svg_class;
  unsigned flags;
  int width;
  int height;

  if (!PyArg_ParseTuple(args, "ssIii", &in_str, &svg_class, &flags, &width, &height)) {
    PyErr_SetString(PyExc_RuntimeError, "Invalid arguments");
    return NULL;
  }

  char *pikchr_md = pikchr(in_str, svg_class, flags, &width, &height);
  if (!pikchr_md) {
    PyErr_SetString(PikchrError, "Error in pikchr C call.");
    return NULL;
  }

  PyObject *str = PyUnicode_FromString(pikchr_md);
  if (!str) {
    PyErr_SetString(PikchrError, "Cannot convert to Python string.");
    return NULL;
  }

  return str;
}
