# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


def check_operand(operand):
    """Validates operand object as an instruction operand and converts it to a standard form"""

    from peachpy.x86_64.registers import Register, MaskedRegister
    from peachpy.x86_64.pseudo import Label
    from peachpy.x86_64.function import LocalVariable
    from peachpy.literal import Constant
    from peachpy import Argument
    from peachpy.util import is_int, is_int64
    from copy import copy, deepcopy
    if isinstance(operand, Register):
        return copy(operand)
    elif isinstance(operand, (MaskedRegister, MemoryOperand)):
        return deepcopy(operand)
    elif isinstance(operand, (Argument, RIPRelativeOffset, Label)):
        return operand
    elif is_int(operand):
        if not is_int64(operand):
            raise ValueError("The immediate operand %d is not representable as a 64-bit value")
        return operand
    elif isinstance(operand, list):
        if len(operand) != 1:
            raise ValueError("Memory operands must be represented by a list with only one element")
        return MemoryOperand(operand[0])
    elif isinstance(operand, Constant):
        from copy import copy, deepcopy
        operand = copy(operand)
        import peachpy.common.function
        if peachpy.common.function.active_function:
            operand.name = deepcopy(operand.name, peachpy.common.function.active_function._names_memo)
        return MemoryOperand(operand)
    elif isinstance(operand, LocalVariable):
        return MemoryOperand(operand)
    elif isinstance(operand, set):
        if len(operand) != 1:
            raise ValueError("Rounding control & suppress-all-errors operands must be represented by a set "
                             "with only one element")
        return next(iter(operand))
    else:
        raise TypeError("Unsupported operand: %s" % str(operand))


def get_operand_registers(operand):
    """Returns a set of registers that comprise the operand"""

    from peachpy.x86_64.registers import Register, MaskedRegister
    if isinstance(operand, Register):
        return [operand]
    elif isinstance(operand, MaskedRegister):
        return [operand.register, operand.mask.mask_register]
    elif isinstance(operand, MemoryOperand) and isinstance(operand.address, MemoryAddress):
        registers = list()
        if operand.address.base is not None:
            registers.append(operand.address.base)
        if operand.address.index is not None:
            registers.append(operand.address.index)
        return registers
    else:
        return list()


def format_operand(operand, assembly_format):
    assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
        "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

    immediate_prefix_map = {
        "peachpy": "",
        "gas": "$",
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
        GeneralPurposeRegister8, MMXRegister, XMMRegister, YMMRegister, ZMMRegister, MaskedRegister, \
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
    elif isinstance(operand, ZMMRegister):
        return "zmm"
    elif isinstance(operand, MaskedRegister):
        if operand.mask.is_zeroing:
            return format_operand_type(operand.register) + "{k}{z}"
        else:
            return format_operand_type(operand.register) + "{k}"
    elif isinstance(operand, MemoryOperand):
        if operand.size is None:
            return "m"
        else:
            if operand.mask is None:
                return "m" + str(operand.size * 8)
            elif operand.mask.is_zeroing:
                return "m" + str(operand.size * 8) + "{k}{z}"
            else:
                return "m" + str(operand.size * 8) + "{k}"
    elif isinstance(operand, RoundingControl):
        return "{er}"
    elif isinstance(operand, SuppressAllExceptions):
        return "{sae}"
    elif isinstance(operand, Label):
        return "rel"
    else:
        return operand.__class__.__name__


class MemoryAddress:
    """An address expression involving a register, e.g. rax - 10, r8d * 4."""

    def __init__(self, base=None, index=None, scale=None, displacement=0):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, \
            XMMRegister, YMMRegister, ZMMRegister, MaskedRegister
        from peachpy.util import is_int, is_sint32

        # Check individual arguments
        if base is not None and not isinstance(base, GeneralPurposeRegister64):
            raise TypeError("Base register must be a 64-bit general-purpose register")
        if index is not None and \
            not isinstance(index, (GeneralPurposeRegister64, XMMRegister, YMMRegister, ZMMRegister)) and not \
            (isinstance(index, MaskedRegister) and
                isinstance(index.register, (XMMRegister, YMMRegister, ZMMRegister)) and
                not index.mask.is_zeroing):
            raise TypeError("Index register must be a 64-bit general-purpose register or an XMM/YMM/ZMM register")
        if scale is not None and not is_int(scale):
            raise TypeError("Scale must be an integer")
        if scale is not None and int(scale) not in {1, 2, 4, 8}:
            raise TypeError("Scale must be 1, 2, 4, or 8")
        if not is_sint32(displacement):
            raise ValueError("Displacement value (%s) is not representable as a signed 32-bit integer" %
                             str(displacement))

        # Check relations of arguments
        if scale is not None and index is None or scale is None and index is not None:
            raise ValueError("Either both of neither of scale and index must be defined")
        if index is None and base is None:
            raise ValueError("Either base or index * scale must be specified")

        self.base = base
        self.index = index
        self.scale = None if scale is None else int(scale)
        self.displacement = int(displacement)

    def __add__(self, addend):
        from peachpy.x86_64.registers import GeneralPurposeRegister64
        from peachpy.util import is_int, is_sint32
        if is_int(addend):
            if not is_sint32(addend):
                raise ValueError("The addend value (%d) is not representable as a signed 32-bit integer" % addend)
            return MemoryAddress(self.base, self.index, self.scale, self.displacement + addend)
        elif isinstance(addend, GeneralPurposeRegister64):
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
    def __init__(self, address, size=None, mask=None, broadcast=None):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, \
            XMMRegister, YMMRegister, ZMMRegister, MaskedRegister
        from peachpy.x86_64.function import LocalVariable
        from peachpy.literal import Constant
        assert isinstance(address, (GeneralPurposeRegister64, XMMRegister, YMMRegister, ZMMRegister,
                                    MemoryAddress, Constant, LocalVariable)) or \
            isinstance(address, MaskedRegister) and \
            isinstance(address.register, (XMMRegister, YMMRegister, ZMMRegister)) and \
            not address.mask.is_zeroing, \
            "Only MemoryAddress, 64-bit general-purpose registers, XMM/YMM/ZMM registers, " \
            "and merge-masked XMM/YMM/ZMM registers may be specified as an address"
        from peachpy.util import is_int
        assert size is None or is_int(size) and int(size) in SizeSpecification._size_name_map, \
            "Unsupported size: %d" % size

        self.symbol = None
        self.size = size
        self.mask = mask
        self.broadcast = broadcast

        if isinstance(address, MemoryAddress):
            if isinstance(address.index, MaskedRegister):
                self.address = MemoryAddress(address.base, address.index.register, address.scale, address.displacement)
                assert mask is None, "Mask argument can't be used when address index is a masked XMM/YMM/ZMM register"
                self.mask = address.index.mask
            else:
                self.address = address
        elif isinstance(address, MaskedRegister):
            self.address = MemoryAddress(index=address.register, scale=1)
            assert mask is None, "Mask argument can't be used when address is a masked XMM/YMM/ZMM register"
            self.mask = address.mask
        elif isinstance(address, Constant):
            self.address = RIPRelativeOffset(0)
            self.symbol = address
            self.size = address.size
        elif isinstance(address, LocalVariable):
            from peachpy.x86_64.registers import rsp
            self.address = MemoryAddress(rsp, displacement=address.offset)
            self.symbol = address
            self.size = address.size
        else:
            # Convert register to memory address expression
            self.address = MemoryAddress(address)

    def __str__(self):
        if self.size is None:
            return "[" + str(self.address) + "]"
        else:
            return SizeSpecification._size_name_map[self.size] + " [" + str(self.address) + "]"

    def __repr__(self):
        return str(self)

    def __call__(self, mask):
        from peachpy.x86_64.registers import KRegister, RegisterMask
        if not isinstance(mask, (KRegister, RegisterMask)):
            raise SyntaxError("zmm(mask) syntax requires mask to be a KRegister or KRegister.z")
        if self.broadcast:
            raise ValueError("mask can not be applied to memory operands with broadcasting")
        if isinstance(mask, KRegister):
            mask = RegisterMask(mask)
        return MemoryOperand(self.address, self.size, mask)

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            text = str(self.address.displacement)
            if self.address.base is not None:
                text += "(" + self.address.base.format(assembly_format) + ")"
            if self.address.index is not None:
                text += "(%s*%d)" % (self.address.index.format(assembly_format), self.address.scale)
            return text
        elif assembly_format == "gas":
            if isinstance(self.address, RIPRelativeOffset):
                return str(self.address.offset) + "(%%rip)"
            else:
                base = self.address.base
                if self.address.index is None:
                    return "{displacement}({base})".format(
                        displacement=self.address.displacement,
                        base=base.format(assembly_format))
                else:
                    return "{displacement}({base},{index},{scale})".format(
                        displacement=self.address.displacement,
                        base="" if base is None else base.format(assembly_format),
                        index=self.address.index,
                        scale=self.address.scale)
        else:
            return str(self)

    @property
    def bcode(self):
        return int(self.broadcast is not None)

    @property
    def kcode(self):
        if self.mask is None:
            return 0
        else:
            return self.mask.kcode

    @property
    def zcode(self):
        if self.mask is None:
            return 0
        else:
            return self.mask.zcode


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

    @property
    def to2(self):
        if self.size not in [4, 8]:
            raise ValueError("{1to2} broadcasting is only supported for dword and qword memory locations")
        return BroadcastSpecification(self.size, 2)

    @property
    def to4(self):
        if self.size not in [4, 8]:
            raise ValueError("{1to4} broadcasting is only supported for dword and qword memory locations")
        return BroadcastSpecification(self.size, 4)

    @property
    def to8(self):
        if self.size not in [4, 8]:
            raise ValueError("{1to8} broadcasting is only supported for dword and qword memory locations")
        return BroadcastSpecification(self.size, 8)

    @property
    def to16(self):
        if self.size != 4:
            raise ValueError("{1to16} broadcasting is only supported for dword memory locations")
        return BroadcastSpecification(self.size, 16)


class BroadcastSpecification:
    def __init__(self, size, broadcast):
        assert size in [4, 8]
        assert broadcast in [2, 4, 8, 16]
        assert size * broadcast in [16, 32, 64]
        self.size = size
        self.broadcast = broadcast

    def __str__(self):
        return SizeSpecification._size_name_map[self.size] + "{1to%d}" % self.broadcast

    def __getitem__(self, address):
        return MemoryOperand(address, self.size, broadcast=self.broadcast)


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
    return isinstance(operand, peachpy.x86_64.registers.XMMRegister) and \
           (operand.physical_id is None or operand.physical_id < 16)


def is_evex_xmm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.XMMRegister)


def is_xmmk(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.XMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.XMMRegister) and \
        not operand.mask.is_zeroing


def is_xmmkz(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.XMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.XMMRegister)


def is_ymm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.YMMRegister) and \
           (operand.physical_id is None or operand.physical_id < 16)


def is_evex_ymm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.YMMRegister)


def is_ymmk(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.YMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.YMMRegister) and \
        not operand.mask.is_zeroing


def is_ymmkz(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.YMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.YMMRegister)


def is_zmm(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.ZMMRegister)


def is_zmmk(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.ZMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.ZMMRegister) and \
        not operand.mask.is_zeroing


def is_zmmkz(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.ZMMRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.ZMMRegister)


def is_k(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.KRegister)


def is_kk(operand):
    import peachpy.x86_64.registers
    return isinstance(operand, peachpy.x86_64.registers.KRegister) or \
        isinstance(operand, peachpy.x86_64.registers.MaskedRegister) and \
        isinstance(operand.register, peachpy.x86_64.registers.KRegister) and \
        not operand.mask.is_zeroing


def is_m(operand):
    if not isinstance(operand, MemoryOperand) or operand.mask is not None or operand.broadcast is not None:
        return False
    # Check that the operand does not use vector index
    from peachpy.x86_64.registers import GeneralPurposeRegister
    return isinstance(operand.address, RIPRelativeOffset) or \
        operand.address.index is None or isinstance(operand.address.index, GeneralPurposeRegister)


def is_mk(operand):
    if not isinstance(operand, MemoryOperand) or operand.broadcast is not None:
        return False
    # Check that the no zero-masking applied to the operand
    if operand.mask is not None and operand.mask.is_zeroing:
        return False
    # Check that the operand does not use vector index
    from peachpy.x86_64.registers import GeneralPurposeRegister
    return operand.address.index is None or isinstance(operand.address.index, GeneralPurposeRegister)


def is_mkz(operand):
    if not isinstance(operand, MemoryOperand) or operand.broadcast is not None:
        return False
    # Check that the operand does not use vector index
    from peachpy.x86_64.registers import GeneralPurposeRegister
    return operand.address.index is None or isinstance(operand.address.index, GeneralPurposeRegister)


def is_vmx(operand):
    from peachpy.x86_64.registers import XMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, XMMRegister) and \
        (operand.address.index is None or operand.address.index.physical_id < 16) and \
        operand.mask is None


def is_evex_vmx(operand):
    from peachpy.x86_64.registers import XMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, XMMRegister) and \
        operand.mask is None


def is_vmxk(operand):
    from peachpy.x86_64.registers import XMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, XMMRegister)


def is_vmy(operand):
    from peachpy.x86_64.registers import YMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, YMMRegister) and \
        (operand.address.index is None or operand.address.index.physical_id < 16) and \
        operand.mask is None


def is_evex_vmy(operand):
    from peachpy.x86_64.registers import YMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, YMMRegister) and \
        operand.mask is None


def is_vmyk(operand):
    from peachpy.x86_64.registers import YMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, YMMRegister)


def is_vmz(operand):
    from peachpy.x86_64.registers import ZMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, ZMMRegister) and \
        operand.mask is None


def is_vmzk(operand):
    from peachpy.x86_64.registers import ZMMRegister
    return isinstance(operand, MemoryOperand) and isinstance(operand.address.index, ZMMRegister)


def is_m8(operand, strict=False):
    return is_m(operand) and (operand.size is None and not strict or operand.size == 1)


def is_m16(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 2) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 2


def is_m16kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 2)


def is_m32(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 4) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 4


def is_m32k(operand):
    return is_mk(operand) and (operand.size is None or operand.size == 4)


def is_m32kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 4)


def is_m64(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 8) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 8


def is_m64k(operand):
    return is_mk(operand) and (operand.size is None or operand.size == 8)


def is_m64kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 8)


def is_m80(operand, strict=False):
    return is_m(operand) and (operand.size is None and not strict or operand.size == 10)


def is_m128(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 16) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 16


def is_m128kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 16)


def is_m256(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 32) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 32


def is_m256kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 32)


def is_m512(operand, strict=False):
    import peachpy.literal
    return is_m(operand) and (operand.size is None and not strict or operand.size == 64) or \
        isinstance(operand, peachpy.literal.Constant) and operand.size == 64


def is_m512kz(operand):
    return is_mkz(operand) and (operand.size is None or operand.size == 64)


def is_m64_m32bcst(operand):
    return is_m64(operand) or isinstance(operand, MemoryOperand) and operand.size == 4 and operand.broadcast == 2


def is_m128_m32bcst(operand):
    return is_m128(operand) or isinstance(operand, MemoryOperand) and operand.size == 4 and operand.broadcast == 4


def is_m256_m32bcst(operand):
    return is_m256(operand) or isinstance(operand, MemoryOperand) and operand.size == 4 and operand.broadcast == 8


def is_m512_m32bcst(operand):
    return is_m512(operand) or isinstance(operand, MemoryOperand) and operand.size == 4 and operand.broadcast == 16


def is_m128_m64bcst(operand):
    return is_m128(operand) or isinstance(operand, MemoryOperand) and operand.size == 8 and operand.broadcast == 2


def is_m256_m64bcst(operand):
    return is_m256(operand) or isinstance(operand, MemoryOperand) and operand.size == 8 and operand.broadcast == 4


def is_m512_m64bcst(operand):
    return is_m512(operand) or isinstance(operand, MemoryOperand) and operand.size == 8 and operand.broadcast == 8


def is_m32bcst(operand):
    return False


def is_m64bcst(operand):
    return False


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


def is_er(operand):
    return isinstance(operand, RoundingControl)


def is_sae(operand):
    return isinstance(operand, SuppressAllExceptions)


byte = SizeSpecification(1)
word = SizeSpecification(2)
dword = SizeSpecification(4)
qword = SizeSpecification(8)
tword = SizeSpecification(10)
oword = SizeSpecification(16)
hword = SizeSpecification(32)
yword = SizeSpecification(32)
zword = SizeSpecification(64)


class RoundingControl:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, RoundingControl) and other.name == self.name and other.code == self.code

    def __ne__(self, other):
        return not isinstance(other, RoundingControl) or other.name != self.name or other.code != self.code

    def __str__(self):
        return "{" + self.name + "}"


class SuppressAllExceptions:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, SuppressAllExceptions) and other.name == self.name

    def __ne__(self, other):
        return not isinstance(other, SuppressAllExceptions) or other.name != self.name

    def __str__(self):
        return "{" + self.name + "}"


rn_sae = RoundingControl("rn-sae", 0b00)
rz_sae = RoundingControl("rz-sae", 0b11)
ru_sae = RoundingControl("ru-sae", 0b10)
rd_sae = RoundingControl("rd-sae", 0b01)
sae = SuppressAllExceptions("sae")
