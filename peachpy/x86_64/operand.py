# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


def check_operand(operand):
    """Validates operand object as an instruction operand and converts it to a standard form"""

    from peachpy.x86_64.registers import Register
    from peachpy.x86_64.pseudo import Label
    from peachpy.x86_64.function import LocalVariable
    from peachpy.literal import Constant
    from peachpy import Argument
    from peachpy.util import is_int, is_int64
    if isinstance(operand, (Register, Constant, MemoryOperand, LocalVariable, Argument, RIPRelativeOffset, Label)):
        return operand
    elif is_int(operand):
        if not is_int64(operand):
            raise ValueError("The immediate operand %d is not representable as a 64-bit value")
        return operand
    elif isinstance(operand, list):
        if len(operand) != 1:
            raise ValueError("Memory operands must be represented by a list with only one element")
        return MemoryOperand(operand[0])
    else:
        raise TypeError("Unsupported operand: %s" % str(operand))


def get_operand_registers(operand):
    """Returns a set of registers that comprise the operand"""

    from peachpy.x86_64.registers import Register
    if isinstance(operand, Register):
        return {operand}
    elif isinstance(operand, MemoryOperand):
        registers = set()
        if operand.address.base is not None:
            registers.add(operand.address.base)
        if operand.address.index is not None:
            registers.add(operand.address.index)
        return registers
    else:
        return set()


def format_operand(operand, assembly_format):
    assert assembly_format in {"peachpy", "gnu", "nasm", "go"}, \
        "Supported assembly formats are 'peachpy', 'gnu', 'nasm', 'go'"

    immediate_prefix_map = {
        "peachpy": "",
        "gnu": "$",
        "nasm": "",
        "go": "$"
    }

    from peachpy.util import is_int64
    if is_int64(operand):
        return immediate_prefix_map[assembly_format] + str(operand)
    else:
        return operand.format(assembly_format)


def format_operand_type(operand):
    """Returns string representation of the operand type in assembly language"""
    from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32, GeneralPurposeRegister16,\
        GeneralPurposeRegister8, MMXRegister, XMMRegister, YMMRegister,\
        al, ax, eax, rax, cl, xmm0
    from peachpy.x86_64.pseudo import Label
    from peachpy.util import is_int64, is_int32, is_int16, is_int8
    if is_int8(operand):
        return "imm8"
    elif is_int16(operand):
        return "imm16"
    elif is_int32(operand):
        return "imm32"
    elif is_int64(operand):
        return "imm64"
    elif al == operand:
        return "al"
    elif ax == operand:
        return "ax"
    elif eax == operand:
        return "eax"
    elif rax == operand:
        return "rax"
    elif cl == operand:
        return "cl"
    elif xmm0 == operand:
        return "xmm0"
    elif isinstance(operand, GeneralPurposeRegister64):
        return "r64"
    elif isinstance(operand, GeneralPurposeRegister32):
        return "r32"
    elif isinstance(operand, GeneralPurposeRegister16):
        return "r16"
    elif isinstance(operand, GeneralPurposeRegister8):
        return "r8"
    elif isinstance(operand, MMXRegister):
        return "mm"
    elif isinstance(operand, XMMRegister):
        return "xmm"
    elif isinstance(operand, YMMRegister):
        return "ymm"
    elif isinstance(operand, MemoryOperand):
        if operand.size is None:
            return "m"
        else:
            return "m" + str(operand.size)
    elif isinstance(operand, Label):
        return "rel"
    else:
        return operand.__class__.__name__


class MemoryAddress:
    """An address expression involving a register, e.g. rax - 10, r8d * 4."""

    def __init__(self, base=None, index=None, scale=None, displacement=0):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32
        from peachpy.util import is_int, is_sint32

        # Check individual arguments
        if base is not None and not isinstance(base, (GeneralPurposeRegister32, GeneralPurposeRegister64)):
            raise TypeError("Base register must be a 32- or 64-bit general-purpose register")
        if index is not None and not isinstance(index, (GeneralPurposeRegister32, GeneralPurposeRegister64)):
            raise TypeError("Index register must be a 32- or 64-bit general-purpose register")
        if scale is not None and not is_int(scale):
            raise TypeError("Scale must be an integer")
        if scale is not None and int(scale) not in {1, 2, 4, 8}:
            raise TypeError("Scale must be 1, 2, 4, or 8")
        if not is_sint32(displacement):
            raise ValueError("Displacement value (%s) is not representable as a signed 32-bit integer" % str(displacement))

        # Check relations of arguments
        if scale is not None and index is None or scale is None and index is not None:
            raise ValueError("Either both of neither of scale and index must be defined")
        if base is not None and index is not None and base.size != index.size:
            raise TypeError("Base (%s) and index (%s) registers have different size" % (str(base), str(index)))
        if index is None and base is None:
            raise ValueError("Either base or index * scale must be specified")

        self.base = base
        self.index = index
        self.scale = None if scale is None else int(scale)
        self.displacement = int(displacement)

    def __add__(self, addend):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32
        from peachpy.util import is_int, is_sint32
        if is_int(addend):
            if not is_sint32(addend):
                raise ValueError("The addend value (%d) is not representable as a signed 32-bit integer" % addend)
            return MemoryAddress(self.base, self.index, self.scale, self.displacement + addend)
        elif isinstance(addend, (GeneralPurposeRegister64, GeneralPurposeRegister32)):
            if self.base is not None:
                raise TypeError("Can not add a general-purpose register to a memory operand with existing base")
            if self.index.size != addend.size:
                raise TypeError("Index (%s) and addend (%s) registers have different size" %
                                (str(self.index), str(addend)))
            return MemoryAddress(addend, self.index, self.scale, self.displacement)
        elif isinstance(addend, MemoryAddress):
            if self.base is not None and addend.base is not None:
                raise ValueError("Can not add memory address: both address expressions use base registers")
            if self.index is not None and addend.index is not None:
                raise ValueError("Can not add memory address: both address expressions use index registers")
            sum_base = self.base if self.base is not None else addend.base
            (sum_index, sum_scale) = (self.index, self.scale) \
                if self.index is not None else (addend.index, addend.scale)
            return MemoryAddress(sum_base, sum_index, sum_scale, self.displacement + addend.displacement)
        else:
            raise TypeError("Can not add %s: unsupported addend type" % str(addend))

    def __sub__(self, minuend):
        from peachpy.util import is_int, is_sint32
        if is_int(minuend):
            if not is_sint32(-minuend):
                raise ValueError("The addend value (%d) is not representable as a signed 32-bit integer" % minuend)
            return MemoryAddress(self.base, self.index, self.scale, self.displacement - minuend)
        else:
            raise TypeError("Can not add %s: unsupported addend type" % str(minuend))

    def __str__(self):
        parts = []
        if self.base is not None:
            parts.append(str(self.base))
        if self.index is not None:
            parts.append(str(self.index) + "*" + str(self.scale))
        if self.displacement >= 0:
            if self.displacement > 0:
                parts.append(str(self.displacement))
            return " + ".join(parts)
        else:
            return " + ".join(parts) + " - " + str(-self.displacement)

    def __repr__(self):
        return str(self)


class MemoryOperand:
    def __init__(self, address, size=None):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32
        assert isinstance(address, (GeneralPurposeRegister64, GeneralPurposeRegister32, MemoryAddress)),\
            "Only MemoryAddress, and 32- or 64-bit general-purpose registers may be specified as an address"
        from peachpy.util import is_int
        assert size is None or is_int(size) and \
            int(size) in SizeSpecification._size_name_map, \
            "Unsupported size: %d" % size
        if isinstance(address, MemoryAddress):
            self.address = address
        else:
            # Convert general-purpose register to memory address expression
            self.address = MemoryAddress(address)
        self.size = size

    def __str__(self):
        if self.size is None:
            return "[" + str(self.address) + "]"
        else:
            return SizeSpecification._size_name_map[self.size] + " [" + str(self.address) + "]"

    def __repr__(self):
        return str(self)

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gnu", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gnu', 'nasm', 'go'"

        if assembly_format == "go":
            text = str(self.address.displacement)
            if self.address.base is not None:
                text += "(" + self.address.base.format(assembly_format) + ")"
            if self.address.index is not None:
                text += "(%s*%d)" % (self.address.index.format(assembly_format), str(self.address.scale))
            return text
        elif assembly_format == "gnu":
            return "%" + str(self)
        else:
            return str(self)


class SizeSpecification:
    _size_name_map = {
        1: "byte",
        2: "word",
        4: "dword",
        8: "qword",
        10: "tword",
        16: "oword",
        32: "hword",
        64: "zword"
    }

    def __init__(self, size):
        from peachpy.util import is_int
        assert is_int(size) and int(size) in SizeSpecification._size_name_map, \
            "Unsupported size: %d" % size
        self.size = size

    def __str__(self):
        return SizeSpecification._size_name_map[self.size]

    def __getitem__(self, address):
        return MemoryOperand(address, self.size)


class RIPRelativeOffset:
    def __init__(self, offset):
        import peachpy.util
        if not peachpy.util.is_sint32(offset):
            raise ValueError("RIP-relative offset must be a 32-bit signed integer")
        self.offset = offset

    def __add__(self, extra_offset):
        return RIPRelativeOffset(self.offset + extra_offset)

    def __sub__(self, extra_offset):
        return RIPRelativeOffset(self.offset - extra_offset)


def is_al(operand):
    from peachpy.x86_64.registers import GeneralPurposeRegister8, al
    return isinstance(operand, GeneralPurposeRegister8) and (operand.is_virtual or operand == al)


def is_cl(operand):
    from peachpy.x86_64.registers import GeneralPurposeRegister8, cl
    return isinstance(operand, GeneralPurposeRegister8) and (operand.is_virtual or operand == cl)


def is_ax(operand):
    from peachpy.x86_64.registers import GeneralPurposeRegister16, ax
    return isinstance(operand, GeneralPurposeRegister16) and (operand.is_virtual or operand == ax)


def is_eax(operand):
    from peachpy.x86_64.registers import GeneralPurposeRegister32, eax
    return isinstance(operand, GeneralPurposeRegister32) and (operand.is_virtual or operand == eax)


def is_rax(operand):
    from peachpy.x86_64.registers import GeneralPurposeRegister64, rax
    return isinstance(operand, GeneralPurposeRegister64) and (operand.is_virtual or operand == rax)


def is_xmm0(operand):
    from peachpy.x86_64.registers import XMMRegister, xmm0
    return isinstance(operand, XMMRegister) and (operand.is_virtual or operand == xmm0)


def is_r8(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister8)


def is_r8rex(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister8) and \
        operand.physical_id >= 4


def is_r8h(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister8) and \
        operand.mask == peachpy.x86_64.registers.GeneralPurposeRegister8._high_mask


def is_r16(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister16)


def is_r32(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister32)


def is_r64(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.GeneralPurposeRegister64)


def is_mm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.MMXRegister)


def is_xmm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.XMMRegister)


def is_ymm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.YMMRegister)


def is_m(operand):
    if not isinstance(operand, MemoryOperand):
        return False
    from peachpy.x86_64.registers import GeneralPurposeRegister
    return operand.address.index is None or isinstance(operand.address.index, GeneralPurposeRegister)


def is_vmx(operand):
    from peachpy.x86_64.registers import XMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, XMMRegister)


def is_vmy(operand):
    from peachpy.x86_64.registers import YMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, YMMRegister)


def is_m8(operand, strict=False):
    return is_m(operand) and (operand.size is None and not strict or operand.size == 1)


def is_m16(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 2) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 2


def is_m32(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 4) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 4


def is_m64(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 8) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 8


def is_m80(operand, strict=False):
    return is_m(operand) and (operand.size is None and not strict or operand.size == 10)


def is_m128(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 16) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 16


def is_m256(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 32) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 32


def is_vm32x(operand, strict=False):
    return is_vmx(operand) and (operand.size is None and not strict or operand.size == 4)


def is_vm64x(operand, strict=False):
    return is_vmx(operand) and (operand.size is None and not strict or operand.size == 8)


def is_vm32y(operand, strict=False):
    return is_vmy(operand) and (operand.size is None and not strict or operand.size == 4)


def is_vm64y(operand, strict=False):
    return is_vmy(operand) and (operand.size is None and not strict or operand.size == 8)


def is_imm(operand):
    import peachpy.util
    return peachpy.util.is_int(operand)


def is_imm4(operand):
    import peachpy.util
    return peachpy.util.is_int(operand) and 0 <= operand <= 15


def is_imm8(operand, ext_size=None):
    import peachpy.util
    if ext_size is None:
        return peachpy.util.is_int8(operand)
    else:
        sup = 2**(8*ext_size)
        return peachpy.util.is_int(operand) and \
            (-128 <= operand <= 127 or sup - 128 <= operand < sup)


def is_imm16(operand, ext_size=None):
    import peachpy.util
    if ext_size is None:
        return peachpy.util.is_int16(operand)
    else:
        sup = 2**(8*ext_size)
        return peachpy.util.is_int(operand) and \
            (-32768 <= operand <= 32767 or sup - 32768 <= operand < sup)


def is_imm32(operand, ext_size=None):
    import peachpy.util
    if ext_size is None:
        return peachpy.util.is_int32(operand)
    else:
        sup = 2**(8*ext_size)
        return peachpy.util.is_int(operand) and \
            (-2147483648 <= operand <= 2147483647 or sup - 2147483648 <= operand < sup)


def is_imm64(operand):
    import peachpy.util
    return peachpy.util.is_int64(operand)


def is_rel8(operand):
    from peachpy.util import is_sint8
    return isinstance(operand, RIPRelativeOffset) and is_sint8(operand.offset)


def is_rel32(operand):
    from peachpy.util import is_sint32
    return isinstance(operand, RIPRelativeOffset) and is_sint32(operand.offset)


def is_label(operand):
    import peachpy.x86_64.pseudo
    return isinstance(operand, peachpy.x86_64.pseudo.Label)


byte = SizeSpecification(1)
word = SizeSpecification(2)
dword = SizeSpecification(4)
qword = SizeSpecification(8)
tword = SizeSpecification(10)
oword = SizeSpecification(16)
hword = SizeSpecification(32)
yword = SizeSpecification(32)
zword = SizeSpecification(64)
