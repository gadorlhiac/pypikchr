from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

pypikchr = Extension(
    name="pypikchr",
    sources=["pypikchr.pyx", "pikchr.c"],
    language="stdc",
    #include_dirs=[],
)
#pypikchr.c = {"embedsignature": True}
setup(ext_modules=cythonize(pypikchr))
