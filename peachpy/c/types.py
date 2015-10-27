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
        if self.is_pointer:
            if self.base is None:
                text = "void*"
            else:
                text = str(self.base) + "*"
            if self.is_const:
                text += " const"
        else:
            text = self.name
            if self.is_const:
                text = "const " + text
        return text

    def __hash__(self):
        if self.is_pointer:
            h = hash(self.base)
            return (h >> 5) | ((h & 0x07FFFFFF) << 27)
        else:
            h = 0
            if self.is_fixed_size:
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
                h ^= hash(self.name)
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
                if self.is_vector and other.is_vector:
                    return self.name == other.name
                else:
                    # If both types have size, check it. If any doesn't have type, ignore size altogether.
                    # This is important because the size of ABI-specific types (size_t, etc) is updated after binding
                    # to ABI and it is important to ensure that e.g. size_t == size_t after ABI binding too
                    if self.size is not None and other.size is not None and self.size != other.size:
                        return False
                    else:
                        return self.is_floating_point == other.is_floating_point and \
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
    def is_fixed_size(self):
        return not (self.is_pointer or self.is_size_integer or self.is_wchar or self.is_bool or
                    self.is_short or self.is_int or self.is_long or self.is_longlong)

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
                # Not exactly the same, but seems to match on all supported platforms
                ptrdiff_t: ctypes.c_ssize_t,
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

