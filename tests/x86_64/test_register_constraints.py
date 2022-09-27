import unittest
from peachpy.x86_64 import *


class SALwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_sal_r32_cl", ()):
            n = GeneralPurposeRegister32()
            SAL(n, cl)
            RETURN()


class SARwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_sar_r32_cl", ()):
            n = GeneralPurposeRegister32()
            SAR(n, cl)
            RETURN()


class SHLwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_shl_r32_cl", ()):
            n = GeneralPurposeRegister32()
            SHL(n, cl)
            RETURN()


class SHRwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_shr_r32_cl", ()):
            n = GeneralPurposeRegister32()
            SHR(n, cl)
            RETURN()


class ROLwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_rol_r32_cl", ()):
            n = GeneralPurposeRegister32()
            ROL(n, cl)
            RETURN()


class RORwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_ror_r32_cl", ()):
            n = GeneralPurposeRegister32()
            ROR(n, cl)
            RETURN()


class RCLwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_rcl_r32_cl", ()):
            n = GeneralPurposeRegister32()
            RCL(n, cl)
            RETURN()


class RCRwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_rcr_r32_cl", ()):
            n = GeneralPurposeRegister32()
            RCR(n, cl)
            RETURN()


class SHLDwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_shld_r32_cl", ()):
            lo = GeneralPurposeRegister32()
            hi = GeneralPurposeRegister32()
            SHLD(lo, hi, cl)
            RETURN()


class SHRDwithCL(unittest.TestCase):
    def runTest(self):
        with Function("test_shrd_r32_cl", ()):
            lo = GeneralPurposeRegister32()
            hi = GeneralPurposeRegister32()
            SHRD(lo, hi, cl)
            RETURN()


class BLENDVPDwithXMM0(unittest.TestCase):
    def runTest(self):
        with Function("test_blendvpd_xmm_xmm_xmm0", (), target=uarch.default + isa.sse4_1):
            x = XMMRegister()
            y = XMMRegister()
            BLENDVPD(x, y, xmm0)
            RETURN()


class BLENDVPSwithXMM0(unittest.TestCase):
    def runTest(self):
        with Function("test_blendvps_xmm_xmm_xmm0", (), target=uarch.default + isa.sse4_1):
            x = XMMRegister()
            y = XMMRegister()
            BLENDVPS(x, y, xmm0)
            RETURN()


class PBLENDVBwithXMM0(unittest.TestCase):
    def runTest(self):
        with Function("test_pblendv_xmm_xmm_xmm0", (), target=uarch.default + isa.sse4_1):
            x = XMMRegister()
            y = XMMRegister()
            PBLENDVB(x, y, xmm0)
            RETURN()


class SHA256RNDS2withXMM0(unittest.TestCase):
    def runTest(self):
        with Function("test_sha256rnds2_xmm_xmm_xmm0", (), target=uarch.default + isa.sha):
            x = XMMRegister()
            y = XMMRegister()
            SHA256RNDS2(x, y, xmm0)
            RETURN()
