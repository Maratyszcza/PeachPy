# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.x86_64 import *
from peachpy import *

a = Argument(ptr(const_float_))
b = Argument(ptr(const_float_))
c = Argument(ptr(float_))

with Function("matmul", (a, b, c)) as function:
    reg_a = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_a, a)

    reg_b = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_b, b)

    reg_c = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_c, c)

    xmm_Brow0 = XMMRegister()
    MOVUPS(xmm_Brow0, [reg_b + 0])

    xmm_Brow1 = XMMRegister()
    MOVUPS(xmm_Brow1, [reg_b + 16])

    xmm_Brow2 = XMMRegister()
    MOVUPS(xmm_Brow2, [reg_b + 32])

    xmm_Brow3 = XMMRegister()
    MOVUPS(xmm_Brow3, [reg_b + 48])

    for k in range(4):
        xmm_Ak0 = XMMRegister()
        MOVSS(xmm_Ak0, [reg_a + k * 16])
        SHUFPS(xmm_Ak0, xmm_Ak0, 0x00)
        MULPS(xmm_Ak0, xmm_Brow0)

        xmm_Ak1 = XMMRegister()
        MOVSS(xmm_Ak1, [reg_a + k * 16 + 4])
        SHUFPS(xmm_Ak1, xmm_Ak1, 0x00)
        MULPS(xmm_Ak1, xmm_Brow1)
        ADDPS(xmm_Ak0, xmm_Ak1)

        xmm_Ak2 = XMMRegister()
        MOVSS(xmm_Ak2, [reg_a + k * 16 + 8])
        SHUFPS(xmm_Ak2, xmm_Ak2, 0x00)
        MULPS(xmm_Ak2, xmm_Brow2)

        xmm_Ak3 = XMMRegister()
        MOVSS(xmm_Ak3, [reg_a + k * 16 + 12])
        SHUFPS(xmm_Ak3, xmm_Ak3, 0x00)
        MULPS(xmm_Ak3, xmm_Brow3)
        ADDPS(xmm_Ak2, xmm_Ak3)

        ADDPS(xmm_Ak0, xmm_Ak2)
        MOVUPS([reg_c + k * 16], xmm_Ak0)

    RETURN()
