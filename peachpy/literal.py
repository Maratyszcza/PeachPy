import six
from peachpy.c.types import Type, \
    int8_t, int16_t, int32_t, int64_t, \
    uint8_t, uint16_t, uint32_t, uint64_t, \
    float_, double_
from peachpy.parse import parse_assigned_variable_name
from peachpy.name import Name


class Constant:
    _supported_sizes = [1, 2, 4, 8, 16, 32, 64]
    _supported_types = [uint8_t, uint16_t, uint32_t, uint64_t,
                        int8_t, int16_t, int32_t, int64_t,
                        float_, double_]

    def __init__(self, size, repeats, data, element_ctype, name):
        assert isinstance(size, six.integer_types), "Constant size must be an integer"
        assert size in Constant._supported_sizes, "Unsupported size %s: the only supported sizes are %s" \
            % (str(size), ", ".join(map(str, sorted(Constant._supported_sizes))))
        assert isinstance(repeats, six.integer_types), "The number of contant repeats must be an integer"
        assert size % repeats == 0, "The number of constant repeats must divide constant size without remainder"
        assert isinstance(element_ctype, Type), "Element type must be an instance of peachpy.c.Type"
        assert element_ctype in Constant._supported_types, "The only supported types are %s" \
            % ", ".join(Constant._supported_types)
        assert isinstance(name, Name)

        self.size = size
        self.repeats = repeats
        self.element_ctype = element_ctype
        self.data = data

        self.name = (name,)

        self.label = None
        self.prefix = None

    def __str__(self):
        format_spec = "%%0%dX" % (self.size / self.repeats * 2)
        return "<" + ", ".join(format_spec % data for data in self.data) + ">"

    def __hash__(self):
        return hash(self.data) ^ hash(self.size) ^ hash(self.repeats)

    def __eq__(self, other):
        return isinstance(other, Constant) and self.data == other.data and self.element_ctype == other.element_ctype

    def encode(self, encoder):
        from peachpy.encoder import Encoder
        assert isinstance(encoder, Encoder)
        encode_function = {
            1: encoder.uint8,
            2: encoder.uint16,
            4: encoder.uint32,
            8: encoder.uint64
        }[self.size / self.repeats]
        return bytearray().join([encode_function(data) for data in self.data])

    @property
    def alignment(self):
        if self.size == 10:
            return 16
        else:
            return self.size

    @property
    def as_hex(self):
        from peachpy.encoder import Encoder, Endianness
        bytestring = self.encode(Encoder(Endianness.Little))
        return "".join("%02X" % byte for byte in bytestring)

    def format(self, assembly_format):
        if assembly_format == "go":
            return "const0x" + self.as_hex + "(SB)"
        else:
            return str(self)

    @staticmethod
    def _uint64xN(name, n, *args):
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
        return Constant(8 * n, n, tuple(args), uint64_t, name)

    @staticmethod
    def _uint32xN(name, n, *args):
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
        return Constant(4 * n, n, tuple(args), uint32_t, name)

    @staticmethod
    def _uint16xN(name, n, *args):
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
                raise ValueError("The number %d is not a 16-bit integer" % number)
            if number < 0:
                args[i] += 0x100000000
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(2 * n, n, tuple(args), uint32_t, name)

    @staticmethod
    def _float64xN(name, n, *args):
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        args = [Constant._parse_float64(arg) for arg in args]
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(8 * n, n, tuple(args), double_, name)

    @staticmethod
    def _float32xN(name, n, *args):
        args = [arg for arg in args if arg is not None]
        if len(args) == 0:
            raise ValueError("At least one constant value must be specified")
        if len(args) != 1 and len(args) != n:
            raise ValueError("Either 1 or %d values must be specified" % n)
        args = [Constant._parse_float32(arg) for arg in args]
        if len(args) == 1:
            args = [args[0]] * n
        return Constant(4 * n, n, tuple(args), double_, name)

    @staticmethod
    def uint64(number, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint64"))

        return Constant._uint64xN(name, 1, number)

    @staticmethod
    def uint64x2(number1, number2=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint64x2"))

        return Constant._uint64xN(name, 2, number1, number2)

    @staticmethod
    def uint64x4(number1, number2=None, number3=None, number4=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint64x4"))

        return Constant._uint64xN(name, 4, number1, number2, number3, number4)

    @staticmethod
    def uint64x8(number1, number2=None, number3=None, number4=None,
                 number5=None, number6=None, number7=None, number8=None,
                 name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint64x8"))

        return Constant._uint64xN(name, 8,
                                  number1, number2, number3, number4, number5, number6, number7, number8)

    @staticmethod
    def uint32(number, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint32"))

        return Constant._uint32xN(name, 1, number)

    @staticmethod
    def uint32x2(number1, number2=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint32x2"))

        return Constant._uint32xN(name, 2, number1, number2)

    @staticmethod
    def uint32x4(number1, number2=None, number3=None, number4=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint32x4"))

        return Constant._uint32xN(name, 4, number1, number2, number3, number4)

    @staticmethod
    def uint32x8(number1, number2=None, number3=None, number4=None,
                 number5=None, number6=None, number7=None, number8=None,
                 name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint32x8"))

        return Constant._uint32xN(name, 8,
                                  number1, number2, number3, number4, number5, number6, number7, number8)

    @staticmethod
    def uint32x16(number1, number2=None, number3=None, number4=None,
                  number5=None, number6=None, number7=None, number8=None,
                  number9=None, number10=None, number11=None, number12=None,
                  number13=None, number14=None, number15=None, number16=None,
                  name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint32x16"))

        return Constant._uint32xN(name, 16,
                                  number1, number2, number3, number4, number5, number6, number7, number8,
                                  number9, number10, number11, number12, number13, number14, number15, number16)

    @staticmethod
    def uint16x8(number1, number2=None, number3=None, number4=None,
                 number5=None, number6=None, number7=None, number8=None,
                 name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint16x8"))

        return Constant._uint16xN(name, 8,
                                  number1, number2, number3, number4, number5, number6, number7, number8)

    @staticmethod
    def uint16x16(number1, number2=None, number3=None, number4=None,
                  number5=None, number6=None, number7=None, number8=None,
                  number9=None, number10=None, number11=None, number12=None,
                  number13=None, number14=None, number15=None, number16=None,
                  name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.uint16x16"))

        return Constant._uint16xN(name, 16,
                                  number1, number2, number3, number4, number5, number6, number7, number8,
                                  number9, number10, number11, number12, number13, number14, number15, number16)

    @staticmethod
    def float64(number, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float64"))

        return Constant._float64xN(name, 1, number)

    @staticmethod
    def float64x2(number1, number2=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float64x2"))

        return Constant._float64xN(name, 2, number1, number2)

    @staticmethod
    def float64x4(number1, number2=None, number3=None, number4=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float64x4"))

        return Constant._float64xN(name, 4, number1, number2, number3, number4)

    @staticmethod
    def float32(number, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float32"))

        return Constant._float32xN(name, 1, number)

    @staticmethod
    def float32x2(number1, number2=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float32x2"))

        return Constant._float32xN(name, 2, number1, number2)

    @staticmethod
    def float32x4(number1, number2=None, number3=None, number4=None, name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float32x4"))

        return Constant._float32xN(name, 4, number1, number2, number3, number4)

    @staticmethod
    def float32x8(number1, number2=None, number3=None, number4=None,
                  number5=None, number6=None, number7=None, number8=None,
                  name=None):
        if name is not None:
            Name.check_name(name)
            name = Name(name=name)
        else:
            import inspect
            name = Name(prename=parse_assigned_variable_name(inspect.stack(), "Constant.float32x8"))

        return Constant._float32xN(name, 8,
                                   number1, number2, number3, number4, number5, number6, number7, number8)

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
