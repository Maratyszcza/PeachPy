[![License](//img.shields.io/badge/license-BSD-brightgreen.png?style=flat)](https://github.com/Maratyszcza/PeachPy/blob/master/license.md)

# Portable Efficient Assembly Code-generator in Higher-level Python (PeachPy)

PeachPy is a Python framework for writing high-performance assembly kernels. PeachPy is developed to simplify writing optimized assembly kernels while preserving all optimization opportunities of traditional assembly. Some PeachPy features:

  - Universal assembly syntax for Windows, Unix, and Golang assembly
  - Automatic register allocation
  - Automatic adaption of function to different calling conventions and ABIs (e.g. functions for Microsoft x64 ABI and System V x86-64 ABI can be generated from the same source)
  - Tracking of instruction extensions used in the function.
  - Multiplexing of multiple instruction streams (helpful for software pipelining)

## Getting started

```bash
pip install opcodes
python setup.py generate
export PYTHONPATH="$PWD:$PYTHONPATH"
```
