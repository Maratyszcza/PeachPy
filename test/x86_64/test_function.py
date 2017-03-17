import unittest
from test import equal_codes
from peachpy import *
from peachpy.x86_64 import *


class Empty(unittest.TestCase):
    def runTest(self):

        with Function("empty", tuple()) as function:
            RETURN()

        code = function.format()
        ref_code = """
void empty()
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class ReturnIntegerArgument(unittest.TestCase):
    def runTest(self):

        n = Argument(uint32_t)

        with Function("return_int_arg", (n,), uint32_t) as function:
            r_n = GeneralPurposeRegister32()
            LOAD.ARGUMENT(r_n, n)

            MOV(eax, r_n)
            RETURN()

        code = function.format()
        ref_code = """
uint32_t return_int_arg(uint32_t n)
    LOAD.ARGUMENT gp32-vreg<1>, uint32_t n
    MOV eax, gp32-vreg<1>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class ReturnFloatArgument(unittest.TestCase):
    def runTest(self):
        x = Argument(float_)

        with Function("return_float_arg", (x,), float_) as function:
            xmm_x = XMMRegister()
            LOAD.ARGUMENT(xmm_x, x)

            MOVSS(xmm0, xmm_x)
            RETURN()

        code = function.format()
        ref_code = """
float return_float_arg(float x)
    LOAD.ARGUMENT xmm-vreg<1>, float x
    MOVSS xmm0, xmm-vreg<1>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class ReturnDoubleArgument(unittest.TestCase):
    def runTest(self):
        x = Argument(double_)

        with Function("return_float_arg", (x,), double_) as function:
            xmm_x = XMMRegister()
            LOAD.ARGUMENT(xmm_x, x)

            MOVSD(xmm0, xmm_x)
            RETURN()

        code = function.format()
        ref_code = """
double return_float_arg(double x)
    LOAD.ARGUMENT xmm-vreg<1>, double x
    MOVSD xmm0, xmm-vreg<1>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class ReturnM128Argument(unittest.TestCase):
    def runTest(self):
        x = Argument(m128)

        with Function("return_m128_arg", (x,), m128) as function:
            xmm_x = XMMRegister()
            LOAD.ARGUMENT(xmm_x, x)

            MOVAPS(xmm0, xmm_x)
            RETURN()

        code = function.format()
        ref_code = """
__m128 return_m128_arg(__m128 x)
    LOAD.ARGUMENT xmm-vreg<1>, __m128 x
    MOVAPS xmm0, xmm-vreg<1>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class ComputeIntegerSum(unittest.TestCase):
    def runTest(self):

        x = Argument(uint32_t)
        y = Argument(uint32_t)

        with Function("integer_sum", (x, y), uint32_t) as function:
            r_x = GeneralPurposeRegister32()
            r_y = GeneralPurposeRegister32()
            LOAD.ARGUMENT(r_x, x)
            LOAD.ARGUMENT(r_y, y)

            ADD(r_x, r_y)
            MOV(eax, r_x)
            RETURN()

        code = function.format()
        ref_code = """
uint32_t integer_sum(uint32_t x, uint32_t y)
    LOAD.ARGUMENT gp32-vreg<1>, uint32_t x
    LOAD.ARGUMENT gp32-vreg<2>, uint32_t y
    ADD gp32-vreg<1>, gp32-vreg<2>
    MOV eax, gp32-vreg<1>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code

class ComputeIntegerSumWithLocalVariable(unittest.TestCase):
    def runTest(self):

        x = Argument(uint32_t)
        y = Argument(uint32_t)

        with Function("integer_sum", (x, y), uint32_t) as function:
            r_x = GeneralPurposeRegister32()
            r_x_temp = GeneralPurposeRegister32()
            r_y = GeneralPurposeRegister32()
            buffer = LocalVariable(4)

            LOAD.ARGUMENT(r_x, x)
            LOAD.ARGUMENT(r_y, y)

            MOV(buffer, r_x)
            MOV(r_x_temp, buffer)

            ADD(r_x_temp, r_y)
            MOV(eax, r_x_temp)
            RETURN()

        code = function.format()
        ref_code = """
uint32_t integer_sum(uint32_t x, uint32_t y)
    LOAD.ARGUMENT gp32-vreg<1>, uint32_t x
    LOAD.ARGUMENT gp32-vreg<3>, uint32_t y
    MOV dword [rsp], gp32-vreg<1>
    MOV gp32-vreg<2>, dword [rsp]
    ADD gp32-vreg<2>, gp32-vreg<3>
    MOV eax, gp32-vreg<2>
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code

class SimpleLoop(unittest.TestCase):
    def runTest(self):
        x = Argument(ptr(const_float_))
        y = Argument(ptr(float_))
        length = Argument(size_t)

        with Function("square", (x, y, length)) as function:
            r_x = GeneralPurposeRegister64()
            r_y = GeneralPurposeRegister64()
            r_length = GeneralPurposeRegister64()
            LOAD.ARGUMENT(r_x, x)
            LOAD.ARGUMENT(r_y, y)
            LOAD.ARGUMENT(r_length, length)

            with Loop() as loop:
                xmm_value = XMMRegister()
                MOVSS(xmm_value, [r_x])
                MULSS(xmm_value, xmm_value)
                MOVSS([r_y], xmm_value)

                SUB(r_length, 1)
                JNZ(loop.begin)

            RETURN()

        code = function.format()
        ref_code = """
void square(const float* x, float* y, size_t length)
    LOAD.ARGUMENT gp64-vreg<1>, const float* x
    LOAD.ARGUMENT gp64-vreg<2>, float* y
    LOAD.ARGUMENT gp64-vreg<3>, size_t length
loop.begin:
    MOVSS xmm-vreg<1>, [gp64-vreg<1>]
    MULSS xmm-vreg<1>, xmm-vreg<1>
    MOVSS [gp64-vreg<2>], xmm-vreg<1>
    SUB gp64-vreg<3>, 1
    JNZ loop.begin
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code

# class SSEArgument(unittest.TestCase):
#     def runTest(self):
#
#         x_arg = Argument(m128d)
#
#         # This optimized kernel will target Intel Nehalem processors. Any instructions which are not
#         # supported on Intel Nehalem (e.g. AVX instructions) will generate an error. If you don't have
#         # a particular target in mind, use "Unknown"
#         with Function("_mm_sqr_pd", (x_arg,), abi=ABI.SystemV, report_generation=False) as add_function:
#             x = SSERegister()
#             LOAD.ARGUMENT(x, x_arg)
#
#             MULPD(x, x)
#             MOVAPD(xmm0, x)
#
#             RETURN()
#
#         print add_function.assembly
