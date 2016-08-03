import unittest
from peachpy.x86_64 import *


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
