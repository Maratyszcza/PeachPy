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
