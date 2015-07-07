# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

__version_info__ = (0, 2, 0)
__version__ = '.'.join(map(str, __version_info__))

from peachpy.stream import InstructionStream


class Type:
    def __init__(self, base, size=None, is_const=False,
                 is_floating_point=False, is_signed_integer=False, is_unsigned_integer=False,
                 is_pointer_integer=False, is_size_integer=False, is_vector=False, is_mask=False,
                 is_char=False, is_wchar=False, is_bool=False,
                 is_short=False, is_int=False, is_long=False, is_longlong=False,
                 header=None):
        self.size = size
        self.is_const = is_const
        self.is_floating_point = is_floating_point
        self.is_signed_integer = is_signed_integer
        self.is_unsigned_integer = is_unsigned_integer
        self.is_pointer_integer = is_pointer_integer
        self.is_size_integer = is_size_integer
        self.is_vector = is_vector
        self.is_mask = is_mask
        self.is_short = is_short
        self.is_char = is_char
        self.is_wchar = is_wchar
        self.is_bool = is_bool
        self.is_int = is_int
        self.is_long = is_long
        self.is_longlong = is_longlong
        self.header = header
        if base is None or isinstance(base, Type):
            self.base = base
            self.name = None
            self.is_pointer = True
        elif isinstance(base, str):
            self.base = None
            self.name = base
            self.is_pointer = False
        else:
            raise TypeError("%s must be either a type name or a type" % base)

    def __str__(self):
        text = str(self.base) + "*" if self.is_pointer else self.name
        if self.is_const:
            text += " const"
        return text

    def __hash__(self):
        if self.is_pointer:
            h = hash(self.base)
            return (h >> 5) | ((h & 0x07FFFFFF) << 27)
        else:
            h = hash(self.size)
            if self.is_floating_point:
                h ^= 0x00000003
            if self.is_signed_integer:
                h ^= 0x0000000C
            if self.is_unsigned_integer:
                h ^= 0x00000030
            if self.is_pointer_integer:
                h ^= 0x000000C0
            if self.is_size_integer:
                h ^= 0x00000300
            if self.is_vector:
                h ^= 0x00000C00
            if self.is_mask:
                h ^= 0x00003000
            if self.is_short:
                h ^= 0x0000C000
            if self.is_char:
                h ^= 0x00030000
            if self.is_wchar:
                h ^= 0x000C0000
            if self.is_bool:
                h ^= 0x00300000
            if self.is_int:
                h ^= 0x00C00000
            if self.is_long:
                h ^= 0x03000000
            if self.is_longlong:
                h ^= 0x0C000000
            return h

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        elif self.is_pointer:
            return other.is_pointer and self.base == other.base
        else:
            if self.name == other.name:
                return True
            else:
                return self.size == other.size and \
                    self.is_floating_point == other.is_floating_point and \
                    self.is_signed_integer == other.is_signed_integer and \
                    self.is_unsigned_integer == other.is_unsigned_integer and \
                    self.is_pointer_integer == other.is_pointer_integer and \
                    self.is_size_integer == other.is_size_integer and \
                    self.is_vector == other.is_vector and \
                    self.is_mask == other.is_mask and \
                    self.is_short == other.is_short and \
                    self.is_char == other.is_char and \
                    self.is_wchar == other.is_wchar and \
                    self.is_bool == other.is_bool and \
                    self.is_int == other.is_int and \
                    self.is_long == other.is_long and \
                    self.is_longlong == other.is_longlong

    def __ne__(self, other):
        return not self == other

    def get_size(self, abi):
        if self.size is None:
            if self.is_pointer or self.is_pointer_integer:
                return abi.pointer_size
            elif self.is_size_integer:
                return abi.index_size
            elif self.is_short:
                return abi.short_size
            elif self.is_int:
                return abi.int_size
            elif self.is_long:
                return abi.long_size
            elif self.is_longlong:
                return abi.longlong_size
            elif self.is_wchar:
                return abi.wchar_size
            elif self.is_bool:
                return abi.bool_size
            else:
                assert False
        else:
            return self.size

    @property
    def is_integer(self):
        return self.is_unsigned_integer or self.is_signed_integer

    @property
    def is_codeunit(self):
        return self.is_char or self.is_wchar

    @property
    def primitive_type(self):
        t = self
        while t.is_pointer:
            t = t.base
        return t

    @property
    def as_ctypes_type(self):
        import ctypes
        if self.is_pointer:
            if self.base is None:
                return ctypes.c_void_p
            else:
                return ctypes.POINTER(self.base.as_ctypes_type)
        else:
            types_map = {
                uint8_t: ctypes.c_uint8,
                uint16_t: ctypes.c_uint16,
                uint32_t: ctypes.c_uint32,
                uint64_t: ctypes.c_uint64,
                int8_t: ctypes.c_int8,
                int16_t: ctypes.c_int16,
                int32_t: ctypes.c_int32,
                int64_t: ctypes.c_int64,
                size_t: ctypes.c_size_t,
                ptrdiff_t: ctypes.c_ssize_t, # Not exactly the same, but seems to match on all supported platforms
                char: ctypes.c_char,
                signed_char: ctypes.c_byte,
                unsigned_char: ctypes.c_ubyte,
                signed_short: ctypes.c_short,
                unsigned_short: ctypes.c_ushort,
                signed_int: ctypes.c_int,
                unsigned_int: ctypes.c_uint,
                signed_long: ctypes.c_long,
                unsigned_long: ctypes.c_ulong,
                signed_long_long: ctypes.c_longlong,
                unsigned_long_long: ctypes.c_ulonglong,
                float_: ctypes.c_float,
                double_: ctypes.c_double
            }
            ctype = types_map.get(self)
            if ctype is None:
                raise ValueError("Type %s has no analog in ctypes module" % str(self))
            return ctype


# Fixed-width C types
uint8_t = Type("uint8_t", size=1, is_unsigned_integer=True, header="stdint.h")
uint16_t = Type("uint16_t", size=2, is_unsigned_integer=True, header="stdint.h")
uint32_t = Type("uint32_t", size=4, is_unsigned_integer=True, header="stdint.h")
uint64_t = Type("uint64_t", size=8, is_unsigned_integer=True, header="stdint.h")
uintptr_t = Type("uintptr_t", is_unsigned_integer=True, is_pointer_integer=True, header="stdint.h")
int8_t = Type("int8_t", size=1, is_signed_integer=True, header="stdint.h")
int16_t = Type("int16_t", size=2, is_signed_integer=True, header="stdint.h")
int32_t = Type("int32_t", size=4, is_signed_integer=True, header="stdint.h")
int64_t = Type("int64_t", size=8, is_signed_integer=True, header="stdint.h")
intptr_t = Type("intptr_t", is_signed_integer=True, is_pointer_integer=True, header="stdint.h")
size_t = Type("size_t", is_unsigned_integer=True, is_size_integer=True, header="stddef.h")
ptrdiff_t = Type("ptrdiff_t", is_signed_integer=True, is_size_integer=True, header="stddef.h")
Float16 = Type("_Float16", is_floating_point=True, size=2)
Float32 = Type("_Float32", is_floating_point=True, size=4)
Float64 = Type("_Float64", is_floating_point=True, size=8)

const_uint8_t = Type("uint8_t", size=1, is_const=True, is_unsigned_integer=True, header="stdint.h")
const_uint16_t = Type("uint16_t", size=2, is_const=True, is_unsigned_integer=True, header="stdint.h")
const_uint32_t = Type("uint32_t", size=4, is_const=True, is_unsigned_integer=True, header="stdint.h")
const_uint64_t = Type("uint64_t", size=8, is_const=True, is_unsigned_integer=True, header="stdint.h")
const_uintptr_t = Type("uintptr_t", is_const=True, is_unsigned_integer=True, is_pointer_integer=True, header="stdint.h")
const_int8_t = Type("int8_t", size=1, is_const=True, is_signed_integer=True, header="stdint.h")
const_int16_t = Type("int16_t", size=2, is_const=True, is_signed_integer=True, header="stdint.h")
const_int32_t = Type("int32_t", size=4, is_const=True, is_signed_integer=True, header="stdint.h")
const_int64_t = Type("int64_t", size=8, is_const=True, is_signed_integer=True, header="stdint.h")
const_intptr_t = Type("intptr_t", is_const=True, is_signed_integer=True, is_pointer_integer=True, header="stdint.h")
const_size_t = Type("size_t", is_const=True, is_unsigned_integer=True, is_size_integer=True, header="stddef.h")
const_ptrdiff_t = Type("ptrdiff_t", is_const=True, is_signed_integer=True, is_size_integer=True, header="stddef.h")
const_Float16 = Type("_Float16", is_const=True, is_floating_point=True, size=2)
const_Float32 = Type("_Float32", is_const=True, is_floating_point=True, size=4)
const_Float64 = Type("_Float64", is_const=True, is_floating_point=True, size=8)


# Yeppp! types
Yep8u = Type("Yep8u", size=1, is_unsigned_integer=True, header="yepTypes.h")
Yep16u = Type("Yep16u", size=2, is_unsigned_integer=True, header="yepTypes.h")
Yep32u = Type("Yep32u", size=4, is_unsigned_integer=True, header="yepTypes.h")
Yep64u = Type("Yep64u", size=8, is_unsigned_integer=True, header="yepTypes.h")
Yep8s = Type("Yep8s", size=1, is_signed_integer=True, header="yepTypes.h")
Yep16s = Type("Yep16s", size=2, is_signed_integer=True, header="yepTypes.h")
Yep32s = Type("Yep32s", size=4, is_signed_integer=True, header="yepTypes.h")
Yep64s = Type("Yep64s", size=8, is_signed_integer=True, header="yepTypes.h")
Yep16f = Type("Yep16f", size=2, is_floating_point=True, header="yepTypes.h")
Yep32f = Type("Yep32f", size=4, is_floating_point=True, header="yepTypes.h")
Yep64f = Type("Yep64f", size=8, is_floating_point=True, header="yepTypes.h")
YepSize = Type("YepSize", is_unsigned_integer=True, is_size_integer=True, header="yepTypes.h")

const_Yep8u = Type("Yep8u", size=1, is_const=True, is_unsigned_integer=True, header="yepTypes.h")
const_Yep16u = Type("Yep16u", size=2, is_const=True, is_unsigned_integer=True, header="yepTypes.h")
const_Yep32u = Type("Yep32u", size=4, is_const=True, is_unsigned_integer=True, header="yepTypes.h")
const_Yep64u = Type("Yep64u", size=8, is_const=True, is_unsigned_integer=True, header="yepTypes.h")
const_Yep8s = Type("Yep8s", size=1, is_const=True, is_signed_integer=True, header="yepTypes.h")
const_Yep16s = Type("Yep16s", size=2, is_const=True, is_signed_integer=True, header="yepTypes.h")
const_Yep32s = Type("Yep32s", size=4, is_const=True, is_signed_integer=True, header="yepTypes.h")
const_Yep64s = Type("Yep64s", size=8, is_const=True, is_signed_integer=True, header="yepTypes.h")
const_Yep16f = Type("Yep16f", size=2, is_const=True, is_floating_point=True, header="yepTypes.h")
const_Yep32f = Type("Yep32f", size=4, is_const=True, is_floating_point=True, header="yepTypes.h")
const_Yep64f = Type("Yep64f", size=8, is_const=True, is_floating_point=True, header="yepTypes.h")
const_YepSize = Type("YepSize", is_const=True, is_unsigned_integer=True, is_size_integer=True, header="yepTypes.h")


# Basic C types
char = Type("char", size=1, is_char=True)
wchar_t = Type("wchar_t", is_wchar=True)
signed_char = Type("signed char", size=1, is_signed_integer=True)
unsigned_char = Type("unsigned char", size=1, is_unsigned_integer=True)
signed_short = Type("short", is_signed_integer=True, is_short=True)
unsigned_short = Type("unsigned short", is_unsigned_integer=True, is_short=True)
signed_int = Type("int", is_signed_integer=True, is_int=True)
unsigned_int = Type("unsigned int", is_unsigned_integer=True, is_int=True)
signed_long = Type("long", is_signed_integer=True, is_long=True)
unsigned_long = Type("unsigned long", is_unsigned_integer=True, is_long=True)
signed_long_long = Type("long long", is_signed_integer=True, is_longlong=True)
unsigned_long_long = Type("unsigned long long", is_unsigned_integer=True, is_longlong=True)
float_ = Type("float", is_floating_point=True, size=4)
double_ = Type("double", is_floating_point=True, size=8)

const_char = Type("char", size=1, is_const=True, is_char=True)
const_wchar_t = Type("wchar_t", is_const=True, is_wchar=True)
const_signed_char = Type("signed char", size=1, is_const=True, is_signed_integer=True)
const_unsigned_char = Type("unsigned char", size=1, is_const=True, is_unsigned_integer=True)
const_signed_short = Type("short", is_const=True, is_signed_integer=True, is_short=True)
const_unsigned_short = Type("unsigned short", is_const=True, is_unsigned_integer=True, is_short=True)
const_signed_int = Type("int", is_const=True, is_signed_integer=True, is_int=True)
const_unsigned_int = Type("unsigned int", is_const=True, is_unsigned_integer=True, is_int=True)
const_signed_long = Type("long", is_const=True, is_signed_integer=True, is_long=True)
const_unsigned_long = Type("unsigned long", is_const=True, is_unsigned_integer=True, is_long=True)
const_signed_long_long = Type("long long", is_const=True, is_signed_integer=True, is_longlong=True)
const_unsigned_long_long = Type("unsigned long long", is_const=True, is_unsigned_integer=True, is_longlong=True)
const_float_ = Type("float", is_const=True, is_floating_point=True, size=4)
const_double_ = Type("double", is_const=True, is_floating_point=True, size=8)


def ptr(t=None):
    if t is None or isinstance(t, Type):
        return Type(base=t)
    else:
        raise TypeError("%s must be a type, e.g. uint32_t, size_t, or Yep64f" % type)


def const_ptr(t=None):
    if t is None or isinstance(t, Type):
        return Type(base=t, is_const=True)
    else:
        raise TypeError("%s must be a type, e.g. uint32_t, size_t, or Yep64f" % type)


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


class ConstantBucket(object):
    supported_capacity = [1, 2, 4, 8, 16, 32, 64, 128]

    def __init__(self, capacity):
        super(ConstantBucket, self).__init__()
        if isinstance(capacity, int):
            if capacity in ConstantBucket.supported_capacity:
                self.capacity = capacity
            else:
                raise ValueError("Capacity value {0} is not among the supports capacities ({1})".format(
                    capacity, ConstantBucket.supported_capacity))
        else:
            raise TypeError("Constant capacity {0} must be an integer".format(capacity))
        self.size = 0
        self.constants = list()

    def add(self, constant):
        if isinstance(constant, Constant):
            if constant.get_alignment() > self.get_capacity() * 8:
                raise ValueError("Constants alignment exceeds constant bucket alignment")
            elif (self.size * 8) % constant.get_alignment() != 0:
                raise ValueError("Constant alignment is not compatible with the internal constant bucket alignment")
            elif self.size + constant.size * constant.repeats / 8 > self.capacity:
                raise ValueError("Constant bucket is overflowed")
            else:
                self.constants.append(constant)
                self.size += constant.size * constant.repeats / 8
        else:
            raise TypeError("Only Constant objects can be added to a constant bucket")

    def get_capacity(self):
        return self.capacity

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def empty(self):
        constants = self.constants
        self.constants = list()
        return constants


class Constant(object):
    supported_sizes = [8, 16, 32, 64, 128, 256]
    supported_types = ['uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256',
                       'sint8', 'sint16', 'sint32', 'sint64', 'sint128', 'sint256',
                       'int8', 'int16', 'int32', 'int64', 'int128', 'int256',
                       'float16', 'float32', 'float64', 'float80', 'float128']

    def __init__(self, size, repeats, data, basic_type):
        super(Constant, self).__init__()
        if isinstance(size, int):
            if size in Constant.supported_sizes:
                self.size = size
            else:
                raise ValueError("Constant size {0} is not among the supported sizes ({1})"
                                 .format(size, ", ".join(map(str, Constant.supported_sizes))))
        else:
            raise TypeError("Constant size {0} must be an integer".format(size))
        if isinstance(repeats, int):
            if size in Constant.supported_sizes:
                self.repeats = repeats
            else:
                raise ValueError(
                    "The number of constant repeats {0} is not among the supported repeat numbers ({1})"
                    .format(repeats, ", ".join(map(str, Constant.supported_sizes))))
        else:
            raise TypeError("The number of constant repeats {0} must be an integer".format(repeats))
        if isinstance(basic_type, str):
            if basic_type in Constant.supported_types:
                self.basic_type = basic_type
        else:
            raise TypeError("The basic type {0} of a constant must be an integer".format(basic_type))
        self.data = data
        self.label = None
        self.prefix = None

    def __str__(self):
        text = hex(self.data)
        if text.endswith("L"):
            text = text[:-1]
        if text.startswith("0x"):
            text = text[2:]
        if len(text) < self.size * 2:
            text = "0" * (self.size / 4 - len(text)) + text
        if self.size == 8:
            return "0x" + text.upper()
        elif self.size == 16:
            return "0x" + text.upper()
        elif self.size == 32:
            return "0x" + text.upper()
        elif self.size == 64:
            return "0x" + text.upper()
        elif self.size == 128:
            return "0x" + text[0:16].upper() + ", 0x" + text[16:32].upper()

    def __hash__(self):
        return hash(self.data) ^ hash(self.size) ^ hash(self.repeats)

    def __eq__(self, other):
        if isinstance(other, Constant):
            if self.size == other.size and self.repeats == other.repeats:
                return self.data == other.data
            else:
                return False
        else:
            return False

    def get_alignment(self):
        if self.size == 80:
            return 128
        else:
            return self.size * self.repeats

    @staticmethod
    def is_int64(number):
        if isinstance(number, int) or isinstance(number, long):
            return -9223372036854775808 <= number <= 18446744073709551615
        else:
            return False

    @staticmethod
    def as_uint64(number):
        assert Constant.is_int64(number)
        if 0 <= number <= 18446744073709551615:
            return long(number)
        else:
            return long(number + 18446744073709551616)

    @staticmethod
    def is_int32(number):
        if isinstance(number, int) or isinstance(number, long):
            return -2147483648 <= number <= 4294967295
        else:
            return False

    @staticmethod
    def as_uint32(number):
        assert Constant.is_int32(number)
        if 0 <= number <= 4294967295:
            return long(number)
        else:
            return long(number + 4294967296)

    @staticmethod
    def is_int16(number):
        if isinstance(number, int) or isinstance(number, long):
            return -32768 <= number <= 65535
        else:
            return False

    @staticmethod
    def as_uint16(number):
        assert Constant.is_int16(number)
        if 0 <= number <= 65535:
            return long(number)
        else:
            return long(number + 65536)

    @staticmethod
    def is_int8(number):
        if isinstance(number, int) or isinstance(number, long):
            return -128 <= number <= 255
        else:
            return False

    @staticmethod
    def as_uint8(number):
        assert Constant.is_int8(number)
        if 0 <= number <= 255:
            return long(number)
        else:
            return long(number + 256)

    @staticmethod
    def uint64(number):
        if isinstance(number, int) or isinstance(number, long):
            if Constant.is_int64(number):
                return Constant(64, 1, Constant.as_uint64(number + 18446744073709551616))
            else:
                raise ValueError("The number {0} is not a 64-bit integer".format(number))
        else:
            raise TypeError("The number used to construct a 64-bit unsigned integer constant must be an integer")

    @staticmethod
    def uint64x2(number1, number2=None):
        if Constant.is_int64(number1):
            number1 = Constant.as_uint64(number1)
        else:
            raise ValueError("The number {0} is not a 64-bit integer".format(number1))
        if number2 is None:
            number2 = number1
        elif Constant.is_int64(number2):
            number2 = Constant.as_uint64(number2)
        else:
            raise ValueError("The number {0} is not a 64-bit integer".format(number2))
        if number1 == number2:
            return Constant(64, 2, number1, 'uint64')
        else:
            return Constant(128, 1, (number1 << 64) + number2, 'uint64')

    @staticmethod
    def uint64x4(number1, number2=None, number3=None, number4=None):
        if isinstance(number1, int) or isinstance(number1, long):
            if Constant.is_int64(number1):
                number1 = Constant.as_uint64(number1)
            else:
                raise ValueError("The number {0} is not a 64-bit integer".format(number1))
        else:
            raise TypeError("The number used to construct a 64-bit unsigned integer constant must be an integer")
        if number2 is None or number3 is None or number4 is None:
            if number2 is None and number3 is None and number4 is None:
                number2 = number1
                number3 = number1
                number4 = number1
            else:
                raise ValueError("Either one or four values must be supplied")
        elif Constant.is_int64(number2) and Constant.is_int64(number3) and Constant.is_int64(number4):
            number2 = Constant.as_uint64(number2)
            number3 = Constant.as_uint64(number3)
            number4 = Constant.as_uint64(number4)
        else:
            raise ValueError(
                "The one of the numbers ({0}, {1}, {2}) is not a 64-bit integer".format(number2, number3, number4))
        if number1 == number2 == number3 == number4:
            return Constant(64, 4, number1, 'uint64')
        elif number1 == number3 and number2 == number4:
            return Constant(128, 2, (number1 << 64) + number2, 'uint64')
        else:
            return Constant(256, 1, (number1 << 192) + (number2 << 128) + (number3 << 64) + number4, 'uint64')

    @staticmethod
    def uint32x4(number1, number2=None, number3=None, number4=None):
        if Constant.is_int32(number1):
            number1 = Constant.as_uint32(number1)
        else:
            raise ValueError("The number {0} is not a 32-bit integer".format(number1))
        if number2 is None or number3 is None or number4 is None:
            if number2 is None and number3 is None and number4 is None:
                number2 = number1
                number3 = number1
                number4 = number1
            else:
                raise ValueError("Either one or four values must be supplied")
        elif Constant.is_int32(number2) and Constant.is_int32(number3) and Constant.is_int32(number4):
            number2 = Constant.as_uint32(number2)
            number3 = Constant.as_uint32(number3)
            number4 = Constant.as_uint32(number4)
        else:
            raise ValueError("The one of the numbers ({0}, {1}, {2}) is not a 32-bit integer"
                             .format(number2, number3, number4))
        if number1 == number2 == number3 == number4:
            return Constant(32, 4, number1, 'uint32')
        elif number1 == number3 and number2 == number4:
            return Constant(64, 2, (number1 << 32) + number2, 'uint32')
        else:
            return Constant(128, 1, (number1 << 96) + (number2 << 64) + (number3 << 32) + number4, 'uint32')

    @staticmethod
    def uint32x8(number1, number2=None, number3=None, number4=None,
                 number5=None, number6=None, number7=None, number8=None):
        if Constant.is_int32(number1):
            number1 = Constant.as_uint32(number1)
        else:
            raise ValueError("The number {0} is not a 32-bit integer".format(number1))
        numbers = [number2, number3, number4, number5, number6, number7, number8]
        if any(number is None for number in numbers):
            if all(number is None for number in numbers):
                number2 = number1
                number3 = number1
                number4 = number1
                number5 = number1
                number6 = number1
                number7 = number1
                number8 = number1
            else:
                raise ValueError("Either one or eight values must be supplied")
        elif all(Constant.is_int32(number) for number in numbers):
            number2 = Constant.as_uint32(number2)
            number3 = Constant.as_uint32(number3)
            number4 = Constant.as_uint32(number4)
            number5 = Constant.as_uint32(number5)
            number6 = Constant.as_uint32(number6)
            number7 = Constant.as_uint32(number7)
            number8 = Constant.as_uint32(number8)
        else:
            raise ValueError(
                "The one of the numbers ({0}, {1}, {2}) is not a 32-bit integer".format(number2, number3, number4))
        if number1 == number2 == number3 == number4 == number5 == number6 == number7 == number8:
            return Constant(32, 8, number1, 'uint32')
        elif number1 == number3 == number5 == number7 and number2 == number4 == number6 == number8:
            return Constant(64, 4, (number1 << 32) + number2, 'uint32')
        elif number1 == number5 and number2 == number6 and number3 == number7 and number4 == number8:
            return Constant(128, 2, (number1 << 96) + (number2 << 64) + (number3 << 32) + number4, 'uint32')
        else:
            return Constant(256, 1,
                (number1 << 224) + (number2 << 192) + (number3 << 160) + (number4 << 128) +
                (number5 << 96) + (number6 << 64) + (number7 << 32) + number8,
                'uint32')

    @staticmethod
    def uint8x16(number1, number2=None, number3=None, number4=None,
                 number5=None, number6=None, number7=None, number8=None,
                 number9=None, number10=None, number11=None, number12=None,
                 number13=None, number14=None, number15=None, number16=None):
        if Constant.is_int8(number1):
            number1 = Constant.as_uint8(number1)
        else:
            raise ValueError("The number {0} is not an 8-bit integer".format(number1))
        numbers = [number2, number3, number4, number5, number6, number7, number8,
                   number9, number10, number11, number12, number13, number14, number15, number16]
        if any(number is None for number in numbers):
            if all(number is None for number in numbers):
                number2 = number1
                number3 = number1
                number4 = number1
                number5 = number1
                number6 = number1
                number7 = number1
                number8 = number1
                number9 = number1
                number10 = number1
                number11 = number1
                number12 = number1
                number13 = number1
                number14 = number1
                number15 = number1
                number16 = number1
            else:
                raise ValueError("Either one or sixteen values must be supplied")
        elif all(Constant.is_int8(number) for number in numbers):
            number2 = Constant.as_uint8(number2)
            number3 = Constant.as_uint8(number3)
            number4 = Constant.as_uint8(number4)
            number5 = Constant.as_uint8(number5)
            number6 = Constant.as_uint8(number6)
            number7 = Constant.as_uint8(number7)
            number8 = Constant.as_uint8(number8)
            number9 = Constant.as_uint8(number9)
            number10 = Constant.as_uint8(number10)
            number11 = Constant.as_uint8(number11)
            number12 = Constant.as_uint8(number12)
            number13 = Constant.as_uint8(number13)
            number14 = Constant.as_uint8(number14)
            number15 = Constant.as_uint8(number15)
            number16 = Constant.as_uint8(number16)
        else:
            raise ValueError("The one of the numbers ({0}, {1}, {2}) is not a 8-bit integer".format(number2, number3, number4))
        if number1 == number2 == number3 == number4 == number5 == number6 == number7 == number8 == \
                number9 == number10 == number11 == number12 == number13 == number14 == number15 == number16:
            return Constant(8, 16, number1, 'uint8')
        elif number1 == number2 == number3 == number4 == number5 == number6 == number7 == number8 and \
                number9 == number10 == number11 == number12 == number13 == number14 == number15 == number16:
            return Constant(16, 8, (number1 << 8) + number2, 'uint8')
        elif number1 == number3 == number5 == number7 and number2 == number4 == number6 == number8 and \
                number9 == number10 == number11 == number12 and number13 == number14 == number15 == number16:
            return Constant(32, 4, (number1 << 24) + (number2 << 16) + (number3 << 8) + number4, 'uint8')
        elif number1 == number5 and number2 == number6 and number3 == number7 and number4 == number8 and \
                number9 == number10 and number11 == number12 and number13 == number14 and number15 == number16:
            return Constant(64, 2,
                (number1 << 56) + (number2 << 48) + (number3 << 40) + (number4 << 32) +
                (number5 << 24) + (number6 << 16) + (number7 << 8) + number8,
                'uint8')
        else:
            return Constant(128, 1,
                (number1 << 120) + (number2 << 112) + (number3 << 104) + (number4 << 96) +
                (number5 << 88) + (number6 << 80) + (number7 << 72) + (number8 << 64) +
                (number9 << 56) + (number10 << 48) + (number11 << 40) + (number12 << 32) +
                (number13 << 24) + (number14 << 16) + (number15 << 8) + number16,
                'uint8')

    @staticmethod
    def uint32(number):
        if isinstance(number, int) or isinstance(number, long):
            if 0 <= number <= 4294967295:
                return Constant(32, 1, long(number), 'uint32')
            elif -2147483648 <= number < 0:
                return Constant(32, 1, long(number + 4294967296), 'uint32')
            else:
                raise ValueError("The number {0} is not a 32-bit integer".format(number))
        else:
            raise TypeError("The number used to construct a 32-bit unsigned integer constant must be an integer")

    @staticmethod
    def uint16(number):
        if isinstance(number, int) or isinstance(number, long):
            if 0 <= number <= 65535:
                return Constant(16, 1, long(number), 'uint16')
            elif -32768 <= number < 0:
                return Constant(16, 1, long(number + 65536), 'uint16')
            else:
                raise ValueError("The number {0} is not a 16-bit integer".format(number))
        else:
            raise TypeError("The number used to construct a 16-bit unsigned integer constant must be an integer")

    @staticmethod
    def uint8(number):
        if isinstance(number, int) or isinstance(number, long):
            if 0 <= number <= 255:
                return Constant(8, 1, long(number), 'uint8')
            elif -128 <= number < 0:
                return Constant(8, 1, long(number + 256), 'uint8')
            else:
                raise ValueError("The number {0} is not an 8-bit integer".format(number))
        else:
            raise TypeError("The number used to construct an 8-bit unsigned integer constant must be an integer")

    @staticmethod
    def float64(number):
        return Constant(64, 1, Constant.parse_float64(number), 'float64')

    @staticmethod
    def float64x2(number1, number2=None):
        number1 = Constant.parse_float64(number1)
        if number2 is None:
            number2 = number1
        else:
            number2 = Constant.parse_float64(number2)
        if number1 == number2:
            return Constant(64, 2, number1, 'float64')
        else:
            return Constant(128, 1, (number1 << 64) + number2, 'float64')

    @staticmethod
    def float64x4(number1, number2=None, number3=None, number4=None):
        number1 = Constant.parse_float64(number1)
        if number2 is None or number3 is None or number4 is None:
            if number3 is None and number4 is None:
                number2 = number1
                number3 = number1
                number4 = number1
            else:
                raise ValueError("Either one or four values must be supplied")
        else:
            number2 = Constant.parse_float64(number2)
            number3 = Constant.parse_float64(number3)
            number4 = Constant.parse_float64(number4)
        if number1 == number2 == number3 == number4:
            return Constant(64, 4, number1, 'float64')
        elif number1 == number3 and number2 == number4:
            return Constant(128, 2, (number1 << 64) + number2, 'float64')
        else:
            return Constant(256, 1, (number1 << 192) + (number2 << 128) + (number3 << 64) + number4, 'float64')

    @staticmethod
    def parse_float64(number):
        if isinstance(number, float):
            number = float.hex(number)
        elif isinstance(number, str):
            if number == "inf" or number == "+inf":
                return 0x7FF0000000000000
            elif number == "-inf":
                return 0xFFF0000000000000
            elif number == "nan":
                return 0x7FF8000000000000
            else:
                # Validity check
                float.hex(float.fromhex(number))
        else:
            raise TypeError('Unsupported constant type {0} for constant {1}'.format(type(number), number))
        is_negative = number.startswith("-")
        point_position = number.index('.')
        exp_position = number.rindex('p')
        number_prefix = number[int(is_negative):point_position]
        assert number_prefix == '0x0' or number_prefix == '0x1'
        mantissa = number[point_position + 1:exp_position]
        if number_prefix == '0x0' and int(mantissa) == 0:
            # Zero
            return long(is_negative) << 63
        else:
            exponent = number[exp_position + 1:]
            mantissa_bits = len(mantissa) * 4
            if mantissa_bits == 52:
                mantissa = long(mantissa, 16)
            elif mantissa_bits < 52:
                mantissa = long(mantissa, 16) << (52 - mantissa_bits)
            else:
                mantissa = long(mantissa, 16) >> (mantissa_bits - 52)
            exponent = int(exponent)
            if exponent <= -1023:
                # Denormals
                mantissa = (mantissa + (1 << 52)) >> -(exponent + 1022)
                exponent = -1023
            elif exponent > 1023:
                # Infinity
                mantissa = 0
                exponent = 1023
            return mantissa + (long(exponent + 1023) << 52) + (long(is_negative) << 63)


class RegisterAllocationError(Exception):
    pass
