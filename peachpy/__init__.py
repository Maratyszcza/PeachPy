# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
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


class Argument(object):
    """
    Function argument.

    An argument must have a C type and a name.
    """
    def __init__(self, ctype, name=None):
        if not isinstance(ctype, Type):
            raise TypeError("%s is not a C type" % ctype)
        self.ctype = ctype
        if name is None:
            import inspect
            import re

            _, _, _, _, caller_lines, _ = inspect.stack()[1]
            if caller_lines is None:
                raise ValueError("Argument error is not specified and the caller context is not available")
            source_line = caller_lines[0].strip()
            match = re.match("(?:\\w+\\.)*(\\w+)\\s*=\\s*(?:\\w+\\.)*Argument\\(.+\\)", source_line)
            if match:
                name = match.group(1)
                while name.startswith("_"):
                    name = name[1:]
                if name.endswith("argument") or name.endswith("Argument"):
                    name = name[:-len("argument")]
                if name.endswith("arg") or name.endswith("Arg"):
                    name = name[:-len("arg")]
                while name.endswith("_"):
                    name = name[:-1]
                if len(name):
                    self.name = name
                else:
                    raise ValueError("Argument error is not specified and can not be parsed from the code")
        else:
            self.name = name

    def __str__(self):
        return str(self.ctype) + " " + self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Argument) and self.ctype == other.ctype and self.name == other.name

    @property
    def is_floating_point(self):
        return self.ctype.is_floating_point

    @property
    def is_codeunit(self):
        return self.ctype.is_codeunit

    @property
    def is_integer(self):
        return self.ctype.is_integer

    @property
    def is_unsigned_integer(self):
        return self.ctype.is_unsigned_integer

    @property
    def is_signed_integer(self):
        return self.ctype.is_signed_integer

    @property
    def is_size_integer(self):
        return self.ctype.is_size_integer

    @property
    def is_pointer_integer(self):
        return self.ctype.is_pointer_integer

    @property
    def is_pointer(self):
        return self.ctype.is_pointer

    @property
    def is_vector(self):
        return self.ctype.is_vector

    @property
    def is_mask(self):
        return self.ctype.is_mask

    @property
    def size(self):
        return self.ctype.size


class RegisterAllocationError(Exception):
    pass
