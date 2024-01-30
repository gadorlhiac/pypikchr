#distutils: language=c
#distutils: source=pypikchr.c
#cython: language_level=3

cdef extern from "pikchr.h":
    char* pikchr(
        char *zText,
        char *zClass,
        unsigned int mFlags,
        int *pnWidth,
        int *pnHeight
    );

def create_pikchr(char* in_str, char* svg_class, unsigned int flags, int width, int height):
    pikchr(in_str, svg_class, flags, &width, &height)
