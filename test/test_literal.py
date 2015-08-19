import unittest
from peachpy import *


class UInt32(unittest.TestCase):
    def runTest(self):
        Constant.uint32(-2147483648)
        Constant.uint32(0)
        Constant.uint32(2147483647)
        Constant.uint32(2147483648)
        Constant.uint32(4294967295)


class UInt32x2(unittest.TestCase):
    def runTest(self):
        Constant.uint32x2(1)
        Constant.uint32x2(-1, 2)


class UInt32x4(unittest.TestCase):
    def runTest(self):
        Constant.uint32x4(1)
        Constant.uint32x4(-1, 2, -3, 4)


class UInt32x8(unittest.TestCase):
    def runTest(self):
        Constant.uint32x8(1)
        Constant.uint32x8(-1, 2, -3, 4, -5, 6, -7, 8)


class UInt32x16(unittest.TestCase):
    def runTest(self):
        Constant.uint32x16(1)
        Constant.uint32x16(-1, 2, -3, 4, -5, 6, -7, 8, -9, 10, -11, 12, -13, 14, -15, 16)


class UInt64(unittest.TestCase):
    def runTest(self):
        Constant.uint64(-9223372036854775808)
        Constant.uint64(0)
        Constant.uint64(9223372036854775807)
        Constant.uint64(9223372036854775808)
        Constant.uint64(18446744073709551615)


class UInt64x2(unittest.TestCase):
    def runTest(self):
        Constant.uint64x2(1)
        Constant.uint64x2(-1, 2)


class UInt64x4(unittest.TestCase):
    def runTest(self):
        Constant.uint64x4(1)
        Constant.uint64x4(-1, 2, -3, 4)


class UInt64x8(unittest.TestCase):
    def runTest(self):
        Constant.uint64x8(1)
        Constant.uint64x8(-1, 2, -3, 4, -5, 6, -7, 8)
