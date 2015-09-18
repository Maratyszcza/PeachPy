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


class Float64(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Constant.float64(0.0).data,                    (0x0000000000000000,))
        self.assertEqual(Constant.float64(1.0).data,                    (0x3FF0000000000000,))
        self.assertEqual(Constant.float64(0.5).data,                    (0x3FE0000000000000,))
        self.assertEqual(Constant.float64(0.75).data,                   (0x3FE8000000000000,))
        self.assertEqual(Constant.float64(2.0).data,                    (0x4000000000000000,))
        self.assertEqual(Constant.float64(float("inf")).data,           (0x7FF0000000000000,))
        self.assertEqual(Constant.float64(-0.0).data,                   (0x8000000000000000,))
        self.assertEqual(Constant.float64(-1.0).data,                   (0xBFF0000000000000,))
        self.assertEqual(Constant.float64(-0.5).data,                   (0xBFE0000000000000,))
        self.assertEqual(Constant.float64(-0.75).data,                  (0xBFE8000000000000,))
        self.assertEqual(Constant.float64(-2.0).data,                   (0xC000000000000000,))
        self.assertEqual(Constant.float64(-float("inf")).data,          (0xFFF0000000000000,))
        self.assertEqual(Constant.float64("0x1.6A09E667F3BCDp+0").data, (0x3FF6A09E667F3BCD,))
        self.assertEqual(Constant.float64("0x1.BB67AE8584CAAp+0").data, (0x3FFBB67AE8584CAA,))
        self.assertEqual(Constant.float64("0x1.921fb54442d18p+1").data, (0x400921FB54442D18,))
        self.assertEqual(Constant.float64("0x1.5bf0a8b145769p+1").data, (0x4005BF0A8B145769,))


class Float32(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Constant.float32(0.0).data,             (0x00000000,))
        self.assertEqual(Constant.float32(1.0).data,             (0x3F800000,))
        self.assertEqual(Constant.float32(0.5).data,             (0x3F000000,))
        self.assertEqual(Constant.float32(0.75).data,            (0x3F400000,))
        self.assertEqual(Constant.float32(2.0).data,             (0x40000000,))
        self.assertEqual(Constant.float32(float("inf")).data,    (0x7F800000,))
        self.assertEqual(Constant.float32(-0.0).data,            (0x80000000,))
        self.assertEqual(Constant.float32(-1.0).data,            (0xBF800000,))
        self.assertEqual(Constant.float32(-0.5).data,            (0xBF000000,))
        self.assertEqual(Constant.float32(-0.75).data,           (0xBF400000,))
        self.assertEqual(Constant.float32(-2.0).data,            (0xC0000000,))
        self.assertEqual(Constant.float32(-float("inf")).data,   (0xFF800000,))
        self.assertEqual(Constant.float32("0x1.6A09E6p+0").data, (0x3FB504F3,))
        self.assertEqual(Constant.float32("0x1.BB67AEp+0").data, (0x3FDDB3D7,))
        self.assertEqual(Constant.float32("0x1.921FB6p+1").data, (0x40490FDB,))
        self.assertEqual(Constant.float32("0x1.5BF0A8p+1").data, (0x402DF854,))
