import unittest
from test import equal_codes
from peachpy import *
from peachpy.x86_64 import *


class Empty(unittest.TestCase):
    def runTest(self):

        with Function("empty", tuple()) as function:
            RETURN()

        code = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_code = """
// func empty()
TEXT \xc2\xB7empty(SB),4,$0
    RET
"""
        assert equal_codes(code, ref_code), "Unexpected Golang code:\n" + code


class ReturnIntegerArgument(unittest.TestCase):
    def runTest(self):

        n_arg = Argument(uint32_t)

        with Function("return_int_arg", (n_arg,), uint32_t) as function:
            n = ebx
            LOAD.ARGUMENT(n, n_arg)

            STORE.RESULT(n)
            RETURN()

        code = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_code = """
// func return_int_arg(n uint32) uint32
TEXT \xc2\xB7return_int_arg(SB),4,$0-8
    MOVL n+0(FP), BX
    MOVL BX, ret+4(FP)
    RET
"""
        assert equal_codes(code, ref_code), "Unexpected Golang code:\n" + code


class ComputeIntegerSum(unittest.TestCase):
    def runTest(self):

        x_arg = Argument(uint32_t)
        y_arg = Argument(uint32_t)

        with Function("integer_sum", (x_arg, y_arg), uint32_t) as function:
            x = ecx
            LOAD.ARGUMENT(x, x_arg)
            y = r8d
            LOAD.ARGUMENT(y, y_arg)

            ADD(x, y)

            STORE.RESULT(x)
            RETURN()

        code = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_code = """
// func integer_sum(x uint32, y uint32) uint32
TEXT \xc2\xB7integer_sum(SB),4,$0-12
    MOVL x+0(FP), CX
    MOVL y+4(FP), R8
    ADDL R8, CX
    MOVL CX, ret+8(FP)
    RET
"""
        assert equal_codes(code, ref_code), "Unexpected Golang code:\n" + code
