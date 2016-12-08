# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy import Constant, ConstantBucket, RegisterAllocationError
import peachpy.codegen
import peachpy.c
import string
import inspect
import time

active_function = None
active_stream = None


