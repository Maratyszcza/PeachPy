import unittest
from test import equal_codes
from peachpy import *
from peachpy.x86_64 import *


class LoadAsm(unittest.TestCase):
    def runTest(self):

        x = Argument(int32_t)
        y = Argument(float_)

        with Function("Multiply", (x, y), double_) as asm_multiply:
            reg_x = GeneralPurposeRegister32()
            LOAD.ARGUMENT(reg_x, x)

            xmm_y = XMMRegister()
            LOAD.ARGUMENT(xmm_y, y)

            xmm_x = XMMRegister()
            CVTSI2SD(xmm_x, reg_x)
            CVTSS2SD(xmm_y, xmm_y)

            MULSD(xmm_x, xmm_y)

            RETURN(xmm_x)

        py_multiply = asm_multiply.finalize(abi.detect()).encode().load()
        assert py_multiply(2, 2.0) == 4.0
        assert py_multiply(2, 3.0) == 6.0

