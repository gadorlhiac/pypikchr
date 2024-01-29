from libcpp.vector cimport vector
from libc.stdlib cimport malloc, free
from libc.stdint cimport int8_t

import numpy

cdef extern from "pikchr.h":
    char* pikchr(
        char *zText,
        char *zClass,
        unsigned int mFlags,
        int *pnWidth,
        int *pnHeight
    );

def create_pikchr(char[:,::1] in_str, char[:, ::1] svg_class, unsigned int flags, int width, int height):
    pikchr(in_str, svg_class, flags, &width, &height)
