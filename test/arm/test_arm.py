import unittest
from peachpy import *
from peachpy.arm import *


class TestARM(unittest.TestCase):
    def runTest(self):

        # Implement function void add_1(const uint32_t *src, uint32_t *dst, size_t length)
        source_arg = Argument(ptr(const_uint32_t))
        destination_arg = Argument(ptr(uint32_t))
        length_arg = Argument(size_t)

        # This optimized kernel will target Intel Nehalem processors. Any instructions which are not
        # supported on Intel Nehalem (e.g. AVX instructions) will generate an error. If you don't have
        # a particular target in mind, use "Unknown"
        with Function("add_1", (source_arg, destination_arg, length_arg), abi=ABI.GnuEABIHF, report_generation=False) as add_function:
            # Load arguments into registers

            (source, destination, length) = LOAD.ARGUMENTS()

            # Main processing loop. Length must be a multiple of 4.
            with Loop() as loop:
                x = GeneralPurposeRegister()
                LDR(x, [source], 4)

                # Add 1 to x
                ADD(x, x, 1)

                STR(x, [destination], 4)

                SUBS(length, 4)
                BNE(loop.begin)

            RETURN()

        print add_function.assembly
