# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy import *
from peachpy.x86_64 import *

x = Argument(ptr(const_float_))
y = Argument(ptr(const_float_))
z = Argument(ptr(float_))
length = Argument(size_t)

with Function("dot_product", (x, y, z, length), package="main") as function:
    reg_x = rdi
    reg_y = rsi
    reg_z = rdx
    reg_length = rcx

    LOAD.ARGUMENT(reg_x, x)
    LOAD.ARGUMENT(reg_y, y)
    LOAD.ARGUMENT(reg_z, z)
    LOAD.ARGUMENT(reg_length, length)

    vector_loop = Loop()
    scalar_loop = Loop()

    VXORPS(xmm0, xmm0, xmm0)
    SUB(reg_length, 8)
    JB(vector_loop.end)
    with vector_loop:
        VMOVUPS(ymm1, [reg_x])
        VMULPS(ymm1, ymm1, [reg_y])
        VADDPS(ymm0, ymm0, ymm1)
        ADD(reg_x, 32)
        ADD(reg_y, 32)

        SUB(reg_length, 8)
        JNZ(vector_loop.begin)
    ADD(reg_length, 8)
    JZ(scalar_loop.end)
    with scalar_loop:
        VMOVSS(xmm1, [reg_x])
        VMULSS(xmm1, xmm1, [reg_y])
        VADDPS(ymm0, ymm0, xmm1.as_ymm)
        ADD(reg_x, 4)
        ADD(reg_y, 4)

        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)
    VEXTRACTF128(xmm1, ymm0, 1)
    VADDPS(xmm0, xmm0, xmm1)
    VHADDPS(xmm0, xmm0, xmm0)
    VHADDPS(xmm0, xmm0, xmm0)
    VMOVSS([reg_z], xmm0)

    RETURN()

golang_function = function.finalize(abi.golang_amd64_abi)
print(golang_function.format(assembly_format="go"))
with open("dotproduct_amd64.s", "w") as dot_product_asm:
    dot_product_asm.write(golang_function.format(assembly_format="go"))


# sysv_function = function.finalize(abi.system_v_x86_64_abi)
# sysv_bytecode = sysv_function.encode()
# print(sysv_bytecode.format_code())
# sysv_executable = sysv_bytecode.load()
#
# import ctypes
# import array
# x = array.array('f', range(1024))
# y = array.array('f', reversed(range(1024)))
# z = array.array('f', [0])
# ptr_x = ctypes.ARRAY(ctypes.c_float, len(x)).from_buffer(x)
# ptr_y = ctypes.ARRAY(ctypes.c_float, len(y)).from_buffer(y)
# ptr_z = ctypes.c_float.from_buffer(z)
# sysv_executable(ptr_x, ptr_y, ptr_z, 1024)
# print(z[0])

# nacl_function = function.finalize(abi.native_client_x86_64_abi)
# nacl_bytecode = nacl_function.encode()
#
# from peachpy.elf.image import Image
# from peachpy.elf.section import TextSection
# from peachpy.elf.symbol import Symbol, SymbolBinding, SymbolType
#
# image = Image(abi.native_client_x86_64_abi, __file__)
#
# text = TextSection(abi.native_client_x86_64_abi)
# text.append(nacl_bytecode.as_bytearray)
# image.bind_section(text, ".text")
#
# # Add symbols
# f = Symbol(abi.native_client_x86_64_abi)
# f.name_index = image.strtab.add("dot_product")
# f.value = 0
# f.content_size = len(nacl_bytecode.as_bytearray)
# f.section_index = text.index
# f.binding = SymbolBinding.Global
# f.type = SymbolType.Function
# image.symtab.add(f)
#
# image.symtab.bind()
#
# with open("dot_product.o", "wb") as dot_product_obj:
#     dot_product_obj.write(image.as_bytearray)
