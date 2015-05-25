.. image:: https://github.com/Maratyszcza/PeachPy/blob/master/logo.png
  :alt: PeachPy logo
  :align: center

===========================================================================
Portable Efficient Assembly Code-generator in Higher-level Python (PeachPy)
===========================================================================

.. image:: https://img.shields.io/badge/License-BSD-brightgreen.svg
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
  - Multiplexing of multiple instruction streams (helpful for software pipelining).
  - Compatible with Python 2, Python 3 and PyPy.

Installation
------------

PeachPy is actively developed, and thus there are presently no stable releases. We recommend that you use the `master` version:

.. code-block:: bash

  git clone https://github.com/Maratyszcza/PeachPy.git
  cd PeachPy
  pip install -r requirements
  python setup.py generate
  export PYTHONPATH="$PWD:$PYTHONPATH"

Using PeachPy as a command-line tool
------------------------------------

.. code-block:: python
  
  # This two lines are not needed for PeachPy, but will help you get autocompletion in good code editors
  from peachpy import *
  from peachpy.x86_64 import *

  # Lets write a function float DotProduct(const float* x, const float* y)
  
  # If you want maximum cross-platform compatibility, argument must have names
  x = Argument(ptr(const_float_), name="x")
  # If name is not specified, it is auto-detected
  y = Argument(ptr(const_float_))

  # Everything inside the `with` statement is goes to function body
  with Function("DotProduct", (x, y), float_):
    # Request two 64-bit general-purpose register. No need to specify exact names.
    reg_x, reg_y = GeneralPurposeRegister64(), GeneralPurposeRegister64()

    # This is a cross-platform way to load arguments. PeachPy will map it to something proper later.
    LOAD.ARGUMENT(reg_x, x)
    LOAD.ARGUMENT(reg_y, y)

    # Also request a virtual 128-bit SIMD register...
    xmm_x = XMMRegister()
    # ...and fill it with data
    MOVAPS(xmm_x, [reg_x])
    # It is fine to mix virtual and physical (xmm0-xmm15) registers in the same code
    MOVAPS(xmm2, [reg_y])

    # Execute dot product instruction, put result into xmm_x
    DPPS(xmm_x, xmm2, 0xF1)

    # This is a cross-platform way to return results. PeachPy will take care of ABI specifics.
    RETURN(xmm_x)

Now you can compile this code into a binary object file that you can link into a program...

.. code-block:: bash

  # Use Mach-O format with SysV ABI for OS X
  python -m peachpy.x86_64 -mabi=sysv -mcpu=default -mimage-format=mach-o -o example.o example.py
  # Use ELF format with SysV ABI for Linux x86-64
  python -m peachpy.x86_64 -mabi=sysv -mcpu=default -mimage-format=elf -o example.o example.py
  # Use ELF format with x32 ABI for Linux x32 (x86-64 with 32-bit pointer)
  python -m peachpy.x86_64 -mabi=sysv -mcpu=default -mimage-format=elf -o example.o example.py
  # Code-generation for Windows (MS COFF) and Native Client x86-64 SFI doesn't work yet, but we'll get there

What else? You can convert the program to Plan 9 assembly for use with Go programming language:

.. code-block:: bash

  # Use Golang ABI with -S flag to generate assembly for Golang x86-64 targets
  python -m peachpy.x86_64 -mabi=golang -mcpu=default -S -o example_amd64.s example.py
  # Use Golang-p32 ABI with -S flag to generate assembly for Golang x86-64 targets with 32-bit pointers
  python -m peachpy.x86_64 -mabi=golang-p32 -mcpu=default -S -o example_amd64p32.s example.py

Using PeachPy as a Python module
--------------------------------

PeachPy links assembly and Python: it represents assembly instructions and syntax as Python classes, functions, and objects.
But it also works the other way around: PeachPy can represent your assembly functions as callable Python functions!

.. code-block:: python

  # This example works in Linux and OS X

  from peachpy import *
  from peachpy.x86_64 import *

  x = Argument(int32_t)
  y = Argument(int32_t)

  with Function("DotProduct", (x, y), int32_t) as asm_function:
      reg_x = GeneralPurposeRegister32()
      reg_y = GeneralPurposeRegister32()

      LOAD.ARGUMENT(reg_x, x)
      LOAD.ARGUMENT(reg_y, y)

      ADD(reg_x, reg_y)

      RETURN(reg_x)

  python_function = asm_function.finalize(abi.system_v_x86_64_abi).encode().load()

  print(python_function(2, 2)) # -> prints "4"

Dependencies and Users
----------------------

- Nearly all instruction classes in PeachPy are generated from `Opcodes Database <https://github.com/Maratyszcza/Opcodes>`_

- Instruction encodings in PeachPy are validated against `binutils <https://www.gnu.org/software/binutils/>`_ using auto-generated tests

- PeachPy powers `Yeppp! <http://www.yeppp.info>`_ performance library. All optimized kernels in Yeppp! are implemented in PeachPy.
