import unittest
from peachpy import *
from peachpy.x86_64 import *

abi_list = [abi.microsoft_x64_abi, abi.system_v_x86_64_abi, abi.linux_x32_abi, abi.native_client_x86_64_abi]


class Return0(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            for return_type in [int8_t, int16_t, int32_t, int64_t, uint8_t, uint16_t, uint32_t, uint64_t]:
                with Function("return_0", tuple(), return_type) as function:
                    RETURN(0)

                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "XOR eax, eax", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnOne(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            for return_type in [int8_t, int16_t, int32_t, int64_t, uint8_t, uint16_t, uint32_t, uint64_t]:
                with Function("return_1", tuple(), return_type) as function:
                    RETURN(1)

                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOV eax, 1", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnMinusOne(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            for return_type in [int8_t, int16_t, int32_t]:
                with Function("return_minus_one", tuple(), return_type) as function:
                    RETURN(-1)

                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOV eax, -1", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            with Function("return_minus_one", tuple(), int64_t) as function:
                RETURN(-1)

            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOV rax, -1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class Return0xFFFFFFFF(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            for return_type in [int64_t, uint64_t]:
                with Function("return_0xFFFFFFFF", tuple(), return_type) as function:
                    RETURN(0xFFFFFFFF)

                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOV eax, 4294967295", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnGeneralPurposeRegister(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            for return_type in [int8_t, int16_t, int32_t]:
                with Function("return_r8_intX", tuple(), return_type) as function:
                    RETURN(dl)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOVSX eax, dl", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            for return_type in [int16_t, int32_t]:
                with Function("return_r16_intX", tuple(), return_type) as function:
                    RETURN(dx)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOVSX eax, dx", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            for return_type in [uint8_t, uint16_t, uint32_t, uint64_t]:
                with Function("return_r8_uintX", tuple(), return_type) as function:
                    RETURN(dl)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOVZX eax, dl", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            for return_type in [uint16_t, uint32_t, uint64_t]:
                with Function("return_r16_uintX", tuple(), return_type) as function:
                    RETURN(dx)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOVZX eax, dx", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            for return_type in [int32_t, uint32_t, uint64_t]:
                with Function("return_r32", tuple(), return_type) as function:
                    RETURN(edx)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOV eax, edx", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            for return_type in [int64_t, uint64_t]:
                with Function("return_r64", tuple(), return_type) as function:
                    RETURN(rdx)
                code = function.finalize(abi).format_code(line_separator=None, indent=False)
                assert code[0] == "MOV rax, rdx", \
                    "Unexpected PeachPy code:\n" + "\n".join(code)

            with Function("return_r8_int64", tuple(), int64_t) as function:
                RETURN(dl)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVSX rax, dl", \
                "Unexpected PeachPy code:\n" + "\n".join(code)

            with Function("return_r16_int64", tuple(), int64_t) as function:
                RETURN(dx)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVSX rax, dx", \
                "Unexpected PeachPy code:\n" + "\n".join(code)

            with Function("return_r32_int64", tuple(), int64_t) as function:
                RETURN(edx)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVSXD rax, edx", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnFloat(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_float", tuple(), float_) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] in ["MOVSS xmm0, xmm1", "MOVAPS xmm0, xmm1"], \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnDouble(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_double", tuple(), double_) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] in ["MOVSD xmm0, xmm1", "MOVAPD xmm0, xmm1"], \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnFloatAVX(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            v = Argument(m256)
            with Function("return_float_avx_arg", (v,), float_) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] in ["VMOVSS xmm0, xmm1", "VMOVAPS xmm0, xmm1"], \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "VZEROUPPER" not in code
            assert "VZEROALL" not in code


class ReturnDoubleAVX(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            v = Argument(m256d)
            with Function("return_double_avx_arg", (v,), double_) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] in ["VMOVSD xmm0, xmm1", "VMOVAPD xmm0, xmm1"], \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "VZEROUPPER" not in code
            assert "VZEROALL" not in code


class ReturnM64(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m64", tuple(), m64) as function:
                RETURN(mm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVQ mm0, mm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "EMMS" not in code
            assert "FEMMS" not in code


class ReturnM128(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m128", tuple(), m128) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVAPS xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnM128D(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m128d", tuple(), m128d) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVAPD xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnM128I(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m128i", tuple(), m128i) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "MOVDQA xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnM128AVX(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            v = Argument(m256)
            with Function("return_m128_avx", (v,), m128) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVAPS xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "VZEROUPPER" not in code
            assert "VZEROALL" not in code


class ReturnM128DAVX(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            v = Argument(m256d)
            with Function("return_m128d_avx", (v,), m128d) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVAPD xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "VZEROUPPER" not in code
            assert "VZEROALL" not in code


class ReturnM128IAVX(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            v = Argument(m256i)
            with Function("return_m128i_avx", (v,), m128i) as function:
                RETURN(xmm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVDQA xmm0, xmm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)
            assert "VZEROUPPER" not in code
            assert "VZEROALL" not in code


class ReturnM256(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m256", tuple(), m256) as function:
                RETURN(ymm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVAPS ymm0, ymm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnM256D(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m256d", tuple(), m256d) as function:
                RETURN(ymm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVAPD ymm0, ymm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)


class ReturnM256I(unittest.TestCase):
    def runTest(self):
        for abi in abi_list:
            with Function("return_m256i", tuple(), m256i) as function:
                RETURN(ymm1)
            code = function.finalize(abi).format_code(line_separator=None, indent=False)
            assert code[0] == "VMOVDQA ymm0, ymm1", \
                "Unexpected PeachPy code:\n" + "\n".join(code)
