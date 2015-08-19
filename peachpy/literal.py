import six
from peachpy.c.types import Type, \
    int8_t, int16_t, int32_t, int64_t, \
    uint8_t, uint16_t, uint32_t, uint64_t, \
    float_, double_


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
    _supported_sizes = [1, 2, 4, 8, 16, 32, 64]
    _supported_types = [uint8_t, uint16_t, uint32_t, uint64_t,
                        int8_t, int16_t, int32_t, int64_t,
                        float_, double_]

    def __init__(self, size, repeats, data, element_ctype):
        super(Constant, self).__init__()
        assert isinstance(size, six.integer_types), "Constant size must be an integer"
        assert size in Constant._supported_sizes, "Unsupported size %s: the only supported sizes are %s" \
            % (str(size), ", ".join(map(str, sorted(Constant._supported_sizes))))
        assert isinstance(repeats, six.integer_types), "The number of contant repeats must be an integer"
        assert size % repeats == 0, "The number of constant repeats must divide constant size without remainder"
        assert isinstance(element_ctype, Type), "Element type must be an instance of peachpy.c.Type"
        assert element_ctype in Constant._supported_types, "The only supported types are %s" \
            % ", ".join(Constant._supported_types)

        self.size = size
        self.repeats = repeats
        self.element_ctype = element_ctype
        self.data = data

        self.label = None
        self.prefix = None

    def __str__(self):
        return "<" + ", ".join("%016X" % data for data in self.data) + ">"

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

    @property
    def alignment(self):
        if self.size == 10:
            return 16
        else:
            return self.size

    def format(self, assembly_format):
        return str(self)

    @staticmethod
    def _uint64xN(n, *args):
        from peachpy.util import is_int, is_int64
        assert is_int(n)
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        for i, number in enumerate(args):
            if not is_int(number):
                raise TypeError("The value %s is not an integer" % str(number))
            if not is_int64(number):
                raise ValueError("The number %d is not a 64-bit integer" % number)
            if number < 0:
                args[i] += 0x10000000000000000
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(8 * n, n, tuple(args), uint64_t)

    @staticmethod
    def _uint32xN(n, *args):
        from peachpy.util import is_int, is_int32
        assert is_int(n)
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        for i, number in enumerate(args):
            if not is_int(number):
                raise TypeError("The value %s is not an integer" % str(number))
            if not is_int32(number):
                raise ValueError("The number %d is not a 32-bit integer" % number)
            if number < 0:
                args[i] += 0x100000000
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(4 * n, n, tuple(args), uint32_t)

    @staticmethod
    def _float64xN(n, *args):
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        args = [Constant._parse_float64(arg) for arg in args]
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(8 * n, n, tuple(args), double_)

    @staticmethod
    def _float32xN(n, *args):
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        args = [Constant._parse_float32(arg) for arg in args]
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(4 * n, n, tuple(args), double_)

    @staticmethod
    def uint64(number):
        return Constant._uint64xN(1, number)

    @staticmethod
    def uint64x2(number1, number2=None):
        return Constant._uint64xN(2, number1, number2)

    @staticmethod
    def uint64x4(number1, number2=None, number3=None, number4=None):
        return Constant._uint64xN(4, number1, number2, number3, number4)

    @staticmethod
    def uint64x8(*numbers8):
        return Constant._uint64xN(8, *numbers8)

    @staticmethod
    def uint32(number1):
        return Constant._uint32xN(1, number1)

    @staticmethod
    def uint32x2(number1, number2=None):
        return Constant._uint32xN(2, number1, number2)

    @staticmethod
    def uint32x4(number1, number2=None, number3=None, number4=None):
        return Constant._uint32xN(4, number1, number2, number3, number4)

    @staticmethod
    def uint32x8(*numbers8):
        return Constant._uint32xN(8, *numbers8)

    @staticmethod
    def uint32x16(*numbers16):
        return Constant._uint32xN(16, *numbers16)

    @staticmethod
    def float64(number):
        return Constant._float64xN(1, number)

    @staticmethod
    def float64x2(number1, number2=None):
        return Constant._float64xN(2, number1, number2)

    @staticmethod
    def float64x4(number1, number2=None, number3=None, number4=None):
        return Constant._float64xN(4, number1, number2, number3, number4)

    @staticmethod
    def float32(number):
        return Constant._float32xN(1, number)

    @staticmethod
    def float32x2(number1, number2=None):
        return Constant._float32xN(2, number1, number2)

    @staticmethod
    def float32x4(number1, number2=None, number3=None, number4=None):
        return Constant._float32xN(4, number1, number2, number3, number4)

    @staticmethod
    def float32x8(*numbers8):
        return Constant._float32xN(8, *numbers8)

    @staticmethod
    def _convert_to_float32(number):
        import array
        float_array = array.array('f', [number])
        return float_array[0]

    @staticmethod
    def _parse_float32(number):
        if isinstance(number, float):
            number = float.hex(Constant._convert_to_float32(number))
        elif isinstance(number, str):
            # Validity check
            try:
                number = float.hex(Constant._convert_to_float32(float.fromhex(number)))
            except ValueError:
                raise ValueError("The string %s is not a hexadecimal floating-point number" % number)
        else:
            raise TypeError("Unsupported type of constant number %s" % str(number))
        if number == "inf" or number == "+inf":
            return 0x7F800000
        elif number == "-inf":
            return 0xFF800000
        elif number == "nan":
            return 0x7FC00000
        is_negative = number.startswith("-")
        point_position = number.index('.')
        exp_position = number.rindex('p')
        number_prefix = number[int(is_negative):point_position]
        assert number_prefix == '0x0' or number_prefix == '0x1'
        mantissa = number[point_position + 1:exp_position]
        if number_prefix == '0x0' and int(mantissa) == 0:
            # Zero
            return int(is_negative) << 31
        else:
            exponent = number[exp_position + 1:]
            mantissa_bits = len(mantissa) * 4
            if mantissa_bits == 23:
                mantissa = int(mantissa, 16)
            elif mantissa_bits < 23:
                mantissa = int(mantissa, 16) << (23 - mantissa_bits)
            else:
                mantissa = int(mantissa, 16) >> (mantissa_bits - 23)
            exponent = int(exponent)
            if exponent <= -127:
                # Denormals
                mantissa = (mantissa + (1 << 23)) >> -(exponent + 126)
                exponent = -127
            return mantissa + (int(exponent + 127) << 23) + (int(is_negative) << 31)

    @staticmethod
    def _parse_float64(number):
        if isinstance(number, float):
            number = float.hex(number)
        elif isinstance(number, str):
            # Validity check
            try:
                number = float.hex(float.fromhex(number))
            except ValueError:
                raise ValueError("The string %s is not a hexadecimal floating-point number" % number)
        else:
            raise TypeError("Unsupported type of constant number %s" % str(number))
        if number == "inf" or number == "+inf":
            return 0x7FF0000000000000
        if number == "-inf":
            return 0xFFF0000000000000
        if number == "nan":
            return 0x7FF8000000000000
        is_negative = number.startswith("-")
        point_position = number.index('.')
        exp_position = number.rindex('p')
        number_prefix = number[int(is_negative):point_position]
        assert number_prefix == '0x0' or number_prefix == '0x1'
        mantissa = number[point_position + 1:exp_position]
        if number_prefix == '0x0':
            # Zero
            assert int(mantissa) == 0
            return int(is_negative) << 63
        else:
            exponent = number[exp_position + 1:]
            mantissa_bits = len(mantissa) * 4
            if mantissa_bits == 52:
                mantissa = int(mantissa, 16)
            elif mantissa_bits < 52:
                mantissa = int(mantissa, 16) << (52 - mantissa_bits)
            else:
                mantissa = int(mantissa, 16) >> (mantissa_bits - 52)
            exponent = int(exponent)
            if exponent <= -1023:
                # Denormals
                mantissa = (mantissa + (1 << 52)) >> -(exponent + 1022)
                exponent = -1023
            elif exponent > 1023:
                # Infinity
                mantissa = 0
                exponent = 1023
            return mantissa + (int(exponent + 1023) << 52) + (int(is_negative) << 63)
