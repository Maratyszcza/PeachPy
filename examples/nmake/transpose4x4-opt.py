# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.x86_64 import *
from peachpy import *

matrix = Argument(ptr(float_))

with Function("transpose4x4_opt", (matrix,)):
    reg_matrix = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_matrix, matrix)

    xmm_rows = [XMMRegister() for _ in range(4)]
    for i, xmm_row in enumerate(xmm_rows):
        MOVUPS(xmm_row, [reg_matrix + i * XMMRegister.size])

    xmm_temps = [XMMRegister() for _ in range(2)]
    # xmm_temps[0] = ( m00, m01, m02, m03 )
    MOVAPS(xmm_temps[0], xmm_rows[0])
    # xmm_temps[1] = ( m20, m21, m22, m23 )
    MOVAPS(xmm_temps[1], xmm_rows[2])

    # xmm_rows[0] = ( m00, m10, m01, m11 )
    UNPCKLPS(xmm_rows[0], xmm_rows[1])
    # xmm_rows[2] = ( m20, m30, m21, m31 )
    UNPCKLPS(xmm_rows[2], xmm_rows[3])

    # xmm_rows[1] = ( m02, m12, m03, m13 )
    UNPCKHPS(xmm_temps[0], xmm_rows[1])
    xmm_rows[1] = xmm_temps[0]

    # xmm_rows[3] = ( m22, m32, m23, m33 )
    UNPCKHPS(xmm_temps[1], xmm_rows[3])
    xmm_rows[3] = xmm_temps[1]

    xmm_temps = [XMMRegister() for _ in range(2)]
    # xmm_temps[0] = ( m00, m10, m01, m11 )
    MOVAPS(xmm_temps[0], xmm_rows[0])
    # xmm_temps[1] = ( m02, m12, m03, m13 )
    MOVAPS(xmm_temps[1], xmm_rows[1])

    # xmm_rows[0] = ( m00, m10, m20, m30 )
    MOVLHPS(xmm_rows[0], xmm_rows[2])
    MOVUPS([reg_matrix], xmm_rows[0])

    # xmm_rows[2] = ( m01, m11, m21, m31 )
    MOVHLPS(xmm_rows[2], xmm_temps[0])
    MOVUPS([reg_matrix + 16], xmm_rows[2])

    # xmm_rows[1] = ( m02, m12, m22, m32 )
    MOVLHPS(xmm_rows[1], xmm_rows[3])
    MOVUPS([reg_matrix + 32], xmm_rows[1])

    # xmm_rows[3] = ( m03, m13, m23, m33 )
    MOVHLPS(xmm_rows[3], xmm_temps[1])
    MOVUPS([reg_matrix + 48], xmm_rows[3])

    RETURN()
