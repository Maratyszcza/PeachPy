#!/usr/bin/env python

from peachpy import __version__
import distutils.log
from distutils.cmd import Command
from distutils.core import setup


def read_text_file(path):
    import os
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


class GenerateInstructions(Command):
    description = "Generate Peach-Py instructions from Opcodes DB"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # package_dir may be None, in that case use the current directory.
        import os
        if self.distribution.package_dir is None:
            src_dir = os.getcwd()
        else:
            src_dir = os.path.abspath(self.distribution.package_dir[""])
        # Run code-generation script
        import opcodes
        self.announce("Generating x86-64 instruction classes from opcodes %s" % opcodes.__version__,
                      level=distutils.log.INFO)
        import codegen.x86_64
        codegen.x86_64.main(src_dir)


setup(
    name="PeachPy",
    version=__version__,
    description="Portable Efficient Assembly Codegen in Higher-level Python",
    author="Marat Dukhan",
    author_email="maratek@gmail.com",
    url="https://github.com/Maratyszcza/PeachPy/",
    packages=["peachpy"],
    keywords=["assembly", "codegen", "x86-64"],
    long_description=read_text_file("readme.rst"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Assembly",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Libraries"
        ],
    cmdclass={
        "generate": GenerateInstructions
    })
