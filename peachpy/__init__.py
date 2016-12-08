# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

__version_info__ = (0, 2, 0)
__version__ = '.'.join(map(str, __version_info__))

from peachpy.stream import InstructionStream
from peachpy.c.types import Type, \
    uint8_t, uint16_t, uint32_t, uint64_t, uintptr_t, \
    int8_t, int16_t, int32_t, int64_t, intptr_t, \
    size_t, ptrdiff_t, \
    Float16, Float32, Float64, \
    const_uint8_t, const_uint16_t, const_uint32_t, const_uint64_t, const_uintptr_t, \
    const_int8_t, const_int16_t, const_int32_t, const_int64_t, const_intptr_t, \
    const_size_t, const_ptrdiff_t, \
    const_Float16, const_Float32, const_Float64, \
    Yep8u, Yep16u, Yep32u, Yep64u, \
    Yep8s, Yep16s, Yep32s, Yep64s, \
    Yep16f, Yep32f, Yep64f, YepSize, \
    const_Yep8u, const_Yep16u, const_Yep32u, const_Yep64u, \
    const_Yep8s, const_Yep16s, const_Yep32s, const_Yep64s, \
    const_Yep16f, const_Yep32f, const_Yep64f, \
    const_YepSize, \
    char, wchar_t, \
    signed_char, unsigned_char, \
    signed_short, unsigned_short, \
    signed_int, unsigned_int, \
    signed_long, unsigned_long, \
    signed_long_long, unsigned_long_long, \
    float_, double_, \
    const_char, const_wchar_t, \
    const_signed_char, const_unsigned_char, \
    const_signed_short, const_unsigned_short, \
    const_signed_int, const_unsigned_int, \
    const_signed_long, const_unsigned_long, \
    const_signed_long_long, const_unsigned_long_long, \
    const_float_, const_double_, \
    ptr, const_ptr
from peachpy.literal import Constant
from peachpy.function import Argument


class RegisterAllocationError(Exception):
    pass
