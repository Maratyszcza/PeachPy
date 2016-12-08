# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy import *
from peachpy.x86_64 import *

x = Argument(ptr(const_float_))
y = Argument(ptr(const_float_))
length = Argument(size_t)

with Function("DotProduct", (x, y, length), float_, target=uarch.default + isa.fma3) as function:
    reg_x = GeneralPurposeRegister64()
    reg_y = GeneralPurposeRegister64()
    reg_length = GeneralPurposeRegister64()

    LOAD.ARGUMENT(reg_x, x)
    LOAD.ARGUMENT(reg_y, y)
    LOAD.ARGUMENT(reg_length, length)

    vector_loop = Loop()
    scalar_loop = Loop()

    unroll_factor = 6
    ymm_accs = [YMMRegister() for _ in range(unroll_factor)]

    for ymm_acc in ymm_accs:
        xmm_acc = ymm_acc.as_xmm
        VXORPS(xmm_acc, xmm_acc, xmm_acc)

    SUB(reg_length, 8*unroll_factor)
    JB(vector_loop.end)
    with vector_loop:
        ymm_xs = [YMMRegister() for _ in range(unroll_factor)]

        for (i, ymm_x) in enumerate(ymm_xs):
            VMOVUPS(ymm_x, [reg_x + 32*i])

        for (i, (ymm_acc, ymm_x)) in enumerate(zip(ymm_accs, ymm_xs)):
            VFMADD132PS(ymm_acc, ymm_x, [reg_y + 32*i])

        ADD(reg_x, 32*unroll_factor)
        ADD(reg_y, 32*unroll_factor)

        SUB(reg_length, 8*unroll_factor)
        JAE(vector_loop.begin)

    # Reduction of multiple YMM registers into into YMM register
    VADDPS(ymm_accs[0], ymm_accs[0], ymm_accs[1])
    VADDPS(ymm_accs[2], ymm_accs[2], ymm_accs[3])
    VADDPS(ymm_accs[4], ymm_accs[4], ymm_accs[5])

    VADDPS(ymm_accs[0], ymm_accs[0], ymm_accs[2])
    VADDPS(ymm_accs[0], ymm_accs[0], ymm_accs[4])

    ymm_acc = ymm_accs[0]
    xmm_acc = ymm_acc.as_xmm

    xmm_scalar_acc = XMMRegister()
    VXORPS(xmm_scalar_acc, xmm_scalar_acc, xmm_scalar_acc)

    ADD(reg_length, 8*unroll_factor)
    JZ(scalar_loop.end)

    with scalar_loop:
        xmm_scalar_x = XMMRegister()
        VMOVSS(xmm_scalar_x, [reg_x])
        VFMADD132SS(xmm_scalar_acc, xmm_scalar_x, [reg_y])

        ADD(reg_x, 4)
        ADD(reg_y, 4)

        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    # Add remainder
    VADDPS(ymm_acc, ymm_acc, xmm_scalar_acc.as_ymm)

    xmm_temp = XMMRegister()
    VEXTRACTF128(xmm_temp, ymm_acc, 1)
    VADDPS(xmm_acc, xmm_acc, xmm_temp)
    VHADDPS(xmm_acc, xmm_acc, xmm_acc)
    VHADDPS(xmm_acc, xmm_acc, xmm_acc)

    RETURN(xmm_acc)

