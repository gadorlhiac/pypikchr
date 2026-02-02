/*
 * pypikchr - Small Python wrapper for the Pikchr diagramming language.
 *
 * Copyright (C) 2026 Gabriel Dorlhiac gabriel@dorlhiac.com
 *
 * This file is part of pypikchr.
 *
 * pypikchr is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * pypikchr is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with pypikchr. If not, see <https://www.gnu.org/licenses/>.
 */

#include "pikchr.h"

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#ifndef Py_PYTHON_H
  #error "Python headers required"
#endif

#include <stdio.h>

#define MODULE_NAME "pypikchr.util.pikchr"
#define MODULE_DOC "Thin Python wrapper around the pikchr C library."
#define MODULE_PER_INTERPRET_SIZE -1 // Do not support sub-interpreters


static PyObject *PikchrError;
static PyObject *pikchr_create_pikchr(PyObject*, PyObject*);
static void on_free();

static PyMethodDef pikchr_methods[] = {
  {"create_pikchr", pikchr_create_pikchr, METH_VARARGS, "Compile pikchr markdown."},
  {NULL,NULL,0,NULL}
};

static struct PyModuleDef pikchr_module = {
    PyModuleDef_HEAD_INIT,
    MODULE_NAME,
    MODULE_DOC,
    MODULE_PER_INTERPRET_SIZE,
    pikchr_methods,
    NULL, // m_slots
    NULL, // m_traverse
    NULL, // m_clear
#ifdef PYPIKCHR_DEBUG
    on_free
#else
    NULL
#endif
};

PyMODINIT_FUNC PyInit_pikchr(void)
{
  PyObject *m;

  m = PyModule_Create(&pikchr_module);
  if (m == NULL)
    return NULL;

  PikchrError = PyErr_NewException(MODULE_NAME".PikchrException", NULL, NULL);

#if PY_VERSION_HEX < 0x030A0000
  Py_INCREF(PikchrError);
  if (PyModule_AddObject(m, "PikchrException", PikchrError) < 0) {
    Py_DECREF(PikchrError);
    Py_CLEAR(PikchrError);
    Py_DECREF(m);
    return NULL;
  }
#else
  if (PyModule_AddObjectRef(m, "PikchrException", PikchrError) < 0) {
    Py_CLEAR(PikchrError);
    Py_DECREF(m);
    return NULL;
  }
#endif

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

  char *pikchr_svg = pikchr(in_str, svg_class, flags, &width, &height);
  if (!pikchr_svg) {
    PyErr_SetString(PikchrError, "Error in pikchr C call.");
    return NULL;
  }

  PyObject *str = PyUnicode_FromString(pikchr_svg);
  if (!str) {
    PyErr_SetString(PikchrError, "Cannot convert to Python string.");
    return NULL;
  }

  return str;
}

#ifdef PYPIKCHR_DEBUG
static void on_free() {
  printf("Pikchr resources released.\n");
}
#endif
