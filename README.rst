.. image:: https://github.com/Maratyszcza/PeachPy/blob/master/logo.png
  :alt: PeachPy logo
  :align: center

===========================================================================
Portable Efficient Assembly Code-generator in Higher-level Python (PeachPy)
===========================================================================

.. image:: https://img.shields.io/github/license/Maratyszcza/PeachPy.svg
  :alt: PeachPy License: Simplified BSD
  :target: https://github.com/Maratyszcza/PeachPy/blob/master/LICENSE.rst

.. image:: https://travis-ci.org/Maratyszcza/PeachPy.svg?branch=master
  :alt: CI Build Status
  :target: https://travis-ci.org/Maratyszcza/PeachPy/

PeachPy is a Python framework for writing high-performance assembly kernels. PeachPy is developed to simplify writing optimized assembly kernels while preserving all optimization opportunities of traditional assembly. Some PeachPy features:

  - Universal assembly syntax for Windows, Unix, and Golang assembly
  - Python-based metaprogramming and code-generation
  - Automatic register allocation
  - Automatic adaption of function to different calling conventions and ABIs (e.g. functions for Microsoft x64 ABI and System V x86-64 ABI can be generated from the same source)
  - Tracking of instruction extensions used in the function.
  - Multiplexing of multiple instruction streams (helpful for software pipelining)

Installation
------------

PeachPy is actively developed, and thus there are presently no stable releases. We recommend that you use the `master` version:

.. code-block:: bash

  git clone https://github.com/Maratyszcza/PeachPy.git
  cd PeachPy
  pip install opcodes
  python setup.py generate
  export PYTHONPATH="$PWD:$PYTHONPATH"

Dependencies and Users
----------------------

- Nearly all instruction classes in PeachPy are generated from Opcode
Most of PeachPy is generated from `Opcodes Database <https://github.com/Maratyszcza/Opcodes>`_
- Instruction encodings in PeachPy are validated against `binutils <https://www.gnu.org/software/binutils/>`_ using auto-generated tests
- PeachPy powers `Yeppp! <http://www.yeppp.info>`_ performance library. All optimized kernels in Yeppp! are implemented in PeachPy.
