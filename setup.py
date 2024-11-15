import io
from distutils.core import setup
from distutils.extension import Extension

pypikchr_ext: Extension = Extension(
    name="pypikchr.util.pikchr",
    sources=["src/c/pypikchr.c", "src/c/pikchr.c"],
    include_dirs=["include"],
    language="stdc",
)

version_fptr: io.TextIOWrapper
version: str
with open("src/pypikchr/__init__.py", "r") as version_fptr:
    version = version_fptr.readlines()[-1].split("=")[1].strip().split('"')[1]

setup(
    name="pypikchr",
    version=version,
    description="Small Python wrapper for pikchr markup language.",
    ext_modules=[pypikchr_ext],
    include_package_data=True,
    packages=["pypikchr", "pypikchr.diagram", "pypikchr.util"],
    package_dir={"":"src"},
    platforms="any",
)
