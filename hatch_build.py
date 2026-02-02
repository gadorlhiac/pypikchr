import os
import sys
from setuptools import Extension, Distribution
from setuptools.command.build_ext import build_ext

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data) -> None:
        if self.target_name != "wheel":
            return

        build_data["pure_python"] = False
        build_data["infer_tag"] = True

        # Paths are relative to project root
        extension: Extension = Extension(
            name="pypikchr.util.pikchr",
            sources=["src/c/pypikchr.c", "src/c/pikchr.c"],
            include_dirs=["include"],
        )

        # Build the extension
        dist: Distribution = Distribution(
            {"name": "pypikchr", "ext_modules": [extension]}
        )
        cmd = build_ext(dist)
        cmd.ensure_finalized()
        cmd.run()

        # Builds to cmd.build_lib -> add into build_data
        build_lib: str = os.path.abspath(cmd.build_lib)
        root: str
        dirs: list[str]
        files: list[str]
        for root, dirs, files in os.walk(build_lib):
            for filename in files:
                if filename.endswith((".so", ".pyd")):
                    full_path: str = os.path.join(root, filename)
                    rel_path: str = os.path.relpath(full_path, build_lib)
                    build_data["force_include"][full_path] = rel_path

        # Can optionally install tests, but map them under the pypikchr package
        # to avoid collisions if this is chosen
        if os.environ.get("PYPIKCHR_INSTALL_TESTS") == "1":
            tests_dir: str = os.path.abspath("tests")
            if os.path.isdir(tests_dir):
                for root, dirs, files in os.walk(tests_dir):
                    for filename in files:
                        full_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(full_path, os.path.dirname(tests_dir))
                        target_path: str = os.path.join("pypikchr", rel_path)
                        build_data["force_include"][full_path] = target_path
