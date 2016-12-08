import unittest
from test import equal_codes
from peachpy import *
from peachpy.x86_64 import *


class TestExplicitRegisterInputConflict(unittest.TestCase):
    def runTest(self):
        with Function("explicit_reg_input", (), uint64_t) as function:
            reg_tmp = GeneralPurposeRegister64()
            MOV(reg_tmp, 42)
            MOV([reg_tmp], rax)
            RETURN(reg_tmp)

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func explicit_reg_input() uint64
TEXT \xc2\xB7explicit_reg_input(SB),4,$0-8
   	MOVQ $42, BX
   	MOVQ AX, 0(BX)
   	MOVQ BX, ret+0(FP)
   	RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing


class TestExplicitRegisterConflict2(unittest.TestCase):
    def runTest(self):
        with Function("explicit_reg_input_2", ()) as function:
            g1 = GeneralPurposeRegister64()
            g2 = GeneralPurposeRegister64()
            MOV(g1, 0)
            MOV(g2, 0)
            MOV(rax, 0)
            MOV([g1], 0)
            MOV([g2], 0)
            RET()

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func explicit_reg_input_2()
TEXT \xc2\xB7explicit_reg_input_2(SB),4,$0
        MOVQ $0, BX
        MOVQ $0, CX
        MOVQ $0, AX
        MOVB $0, 0(BX)
        MOVB $0, 0(CX)
        RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing


class TestExplicitRegisterOutputConflict(unittest.TestCase):
    def runTest(self):
        with Function("explicit_reg_output", (), uint64_t) as function:
            reg_tmp = GeneralPurposeRegister64()
            MOV(reg_tmp, 1)
            MOV(rax, 2)
            RETURN(reg_tmp)

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func explicit_reg_output() uint64
TEXT \xc2\xB7explicit_reg_output(SB),4,$0-8
   	MOVQ $1, BX
   	MOVQ $2, AX
   	MOVQ BX, ret+0(FP)
   	RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing


class TestImplicitRegisterConflict(unittest.TestCase):
    def runTest(self):
        with Function("implicit_reg", (), uint64_t) as function:
            reg_tmp = GeneralPurposeRegister64()
            MOV(reg_tmp, 42)
            CPUID()
            RETURN(reg_tmp)

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func implicit_reg() uint64
TEXT \xc2\xB7implicit_reg(SB),4,$0-8
	MOVQ $42, DI
	CPUID
	MOVQ DI, ret+0(FP)
	RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing


class TestIssue65(unittest.TestCase):
    def runTest(self):
        with Function("crash", (), int64_t) as function:
            r = GeneralPurposeRegister64()
            MOV(r, 999)
            RETURN(rax)

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func crash() int64
TEXT \xc2\xB7crash(SB),4,$0-8
	MOVQ $999, BX
	MOVQ AX, ret+0(FP)
	RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing

class TestIssue65SecondComment(unittest.TestCase):
    def runTest(self):
        with Function("crash", (), int64_t) as function:
            r = GeneralPurposeRegister64()
            MOV(r, 1)
            MOV(r, [rax])
            RET()

        listing = function.finalize(abi.goasm_amd64_abi).format("go")
        ref_listing = """
// func crash() int64
TEXT \xc2\xB7crash(SB),4,$0-8
MOVQ $1, BX
MOVQ 0(AX), BX
RET
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing
