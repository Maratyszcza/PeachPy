import unittest
from peachpy import *
from peachpy.x86_64 import *


class EndOfInstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32(42)
        constant.address = 0
        instruction = ADD(ecx, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


class EndOfREXInstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint64(42)
        constant.address = 0
        instruction = ADD(rcx, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


class EndOfVEX2InstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.float32x4(1.0, 2.0, 3.0, 4.0)
        constant.address = 0
        instruction = VADDPS(xmm0, xmm1, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


class EndOfVEX3InstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32x4(1, 2, 3, 4)
        constant.address = 0
        instruction = VPADDD(xmm0, xmm1, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


class EndOfXOPInstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32x4(1, 2, 3, 4)
        constant.address = 0
        instruction = VPHADDDQ(xmm0, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


@unittest.skip
class EndOfEVEXInstructionRelocation(unittest.TestCase):
    def runTest(self):
        constant = Constant.float32x4(1.0, 2.0, 3.0, 4.0)
        constant.address = 0
        instruction = VADDPS(xmm0(k1), xmm1, constant)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 4


class RelocationBeforeImm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32(42)
        constant.address = 0
        instruction = CMP(constant, 42)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


class RelocationBeforeREXImm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint64(42)
        constant.address = 0
        instruction = CMP(constant, 42)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


class RelocationBeforeVEX2Imm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.float32x4(1.0, 2.0, 3.0, 4.0)
        constant.address = 0
        instruction = VSHUFPS(xmm0, xmm1, constant, 0xAA)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


class RelocationBeforeVEX3Imm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32x4(1, 2, 3, 4)
        constant.address = 0
        instruction = VPALIGNR(xmm0, xmm1, constant, 6)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


class RelocationBeforeXOPImm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32x4(1, 2, 3, 4)
        constant.address = 0
        instruction = VPCOMUD(xmm0, xmm1, constant, 0)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


@unittest.skip
class RelocationBeforeEVEXImm8(unittest.TestCase):
    def runTest(self):
        constant = Constant.float32x8(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
        constant.address = 0
        instruction = VALIGND(ymm0, ymm1, constant, 2)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 5


class RelocationBeforeImm32(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint32(42)
        constant.address = 0
        instruction = TEST(constant, 0x12345678)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 8


class RelocationBeforeREXImm32(unittest.TestCase):
    def runTest(self):
        constant = Constant.uint64(42)
        constant.address = 0
        instruction = TEST(constant, 0x12345678)
        instruction.bytecode = instruction.encode()
        relocation = instruction.relocation
        assert relocation.offset == len(instruction.bytecode) - 8
