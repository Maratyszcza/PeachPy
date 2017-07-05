# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


import six


class Register(object):
    """A base class for all encodable registers (rip is not encodable)"""
    _mask_size_map = {
        0x1: 1,
        0x2: 1,
        0x3: 2,
        0x7: 4,
        0xF: 8,
        0x10: 8,
        0x40: 8,
        0x100: 16,
        0x300: 32,
        0x700: 64
    }
    size = None

    def __init__(self, mask, virtual_id=None, physical_id=None):
        super(Register, self).__init__()
        from peachpy.util import is_int
        assert is_int(mask), \
            "Mask must be an integer"
        assert mask in Register._mask_size_map, \
            "Unknown mask value: %X" % mask
        self.mask = int(mask)
        assert virtual_id is not None or physical_id is not None, \
            "Virtual or physical ID must be specified"
        assert virtual_id is None or is_int(virtual_id) and virtual_id > 0,\
            "Virtual ID must be a positive integer"
        assert physical_id is None or is_int(physical_id) and physical_id >= 0,\
            "Physical ID must be a non-negative integer"
        self.virtual_id = None if virtual_id is None else int(virtual_id)
        self.physical_id = None if physical_id is None else int(physical_id)

    def __eq__(self, other):
        return isinstance(other, Register) and self.mask == other.mask and self._internal_id == other._internal_id

    def __ne__(self, other):
        return not isinstance(other, Register) or self.mask != other.mask or self._internal_id != other._internal_id

    def __lt__(self, other):
        return isinstance(other, Register) and (self.mask, -self._internal_id) < (other.mask, -other._internal_id)

    def __le__(self, other):
        return isinstance(other, Register) and (self.mask, -self._internal_id) <= (other.mask, -other._internal_id)

    def __hash__(self):
        h = hash(self.mask)
        if self.physical_id is not None:
            return hash(self.physical_id) ^ h
        else:
            return hash(self.virtual_id) ^ h

    def __repr__(self):
        return str(self)

    @property
    def _internal_id(self):
        if self.is_virtual:
            return -self.virtual_id
        else:
            return self.physical_id

    @staticmethod
    def _reconstruct(internal_id, mask):
        registers = set()
        if internal_id >= 0:
            # Physical register
            if mask & 0x400 != 0:
                mask &= ~0x700
                registers.add(ZMMRegister(physical_id=internal_id))
            elif mask & 0x200 != 0:
                mask &= ~0x300
                registers.add(YMMRegister(physical_id=internal_id))
            elif mask & 0x100 != 0:
                mask &= ~0x100
                registers.add(XMMRegister(physical_id=internal_id))
            if mask & 0x10 != 0:
                mask &= ~0x10
                registers.add(MMXRegister(physical_id=internal_id))
            if mask & 0x8 != 0:
                mask &= ~0xF
                registers.add(GeneralPurposeRegister64(physical_id=internal_id))
            elif mask & 0x4 != 0:
                mask &= ~0x7
                registers.add(GeneralPurposeRegister32(physical_id=internal_id))
            elif mask & 0x2 != 0:
                mask &= ~0x3
                registers.add(GeneralPurposeRegister16(physical_id=internal_id))
            elif mask & 0x1 != 0:
                mask &= ~0x1
                registers.add(GeneralPurposeRegister8(physical_id=internal_id))
            assert mask == 0, "Unknown register mask component: %X" % mask
        else:
            # Virtual register
            # Physical register
            if mask & 0x400 != 0:
                mask &= ~0x700
                registers.add(ZMMRegister(virtual_id=-internal_id))
            elif mask & 0x200 != 0:
                mask &= ~0x300
                registers.add(YMMRegister(virtual_id=-internal_id))
            elif mask & 0x100 != 0:
                mask &= ~0x100
                registers.add(XMMRegister(virtual_id=-internal_id))
            if mask & 0x10 != 0:
                mask &= ~0x10
                registers.add(MMXRegister(virtual_id=-internal_id))
            if mask & 0x40 != 0:
                mask &= ~0x40
                registers.add(KRegister(virtual_id=-internal_id))
            if mask & 0x8 != 0:
                mask &= ~0xF
                registers.add(GeneralPurposeRegister64(virtual_id=-internal_id))
            elif mask & 0x4 != 0:
                mask &= ~0x7
                registers.add(GeneralPurposeRegister32(virtual_id=-internal_id))
            elif mask & 0x2 != 0:
                mask &= ~0x3
                registers.add(GeneralPurposeRegister16(virtual_id=-internal_id))
            elif mask & 0x1 != 0:
                mask &= ~0x1
                registers.add(GeneralPurposeRegister8(virtual_id=-internal_id))
            assert mask == 0, "Unknown register mask component: %X" % mask
        return registers

    @staticmethod
    def _reconstruct_multiple(reg_dict):
        reg_set = set()
        for (reg_id, reg_mask) in six.iteritems(reg_dict):
            reg_set.update(Register._reconstruct(reg_id, reg_mask))
        return reg_set

    @property
    def kind(self):
        if self.mask & GeneralPurposeRegister64._mask != 0:
            return GeneralPurposeRegister._kind
        elif self.mask & MMXRegister._mask != 0:
            return MMXRegister._kind
        elif self.mask & XMMRegister._mask != 0:
            return XMMRegister._kind
        elif self.mask & KRegister._mask != 0:
            return KRegister._kind
        else:
            assert False, "Unknown register mask: %X" % self.mask

    @property
    def is_virtual(self):
        """Indicated if a register is virtual, i.e. not bounded to a physical register"""
        return self.physical_id is None

    @property
    def lcode(self):
        """Returns the bits 0-2 of register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        if self.mask == GeneralPurposeRegister8._high_mask:
            assert self.physical_id & ~0x3 == 0, \
                "Only ah, bh, ch, dh can be the high 8-bit registers"
            return 0x4 | self.physical_id
        else:
            return self.physical_id & 0x7

    @property
    def hcode(self):
        """Returns the bit 3 of register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return (self.physical_id >> 3) & 1

    @property
    def ecode(self):
        """Returns the bit 4 of register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return (self.physical_id >> 4) & 1

    @property
    def hlcode(self):
        """Returns the bits 0-3 of register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        assert self.mask != GeneralPurposeRegister8._high_mask, \
            "ah/bh/ch/dh registers never use 4-bit encoding"
        return self.physical_id & 0xF

    @property
    def ehcode(self):
        """Returns the bits 3-4 of register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return (self.physical_id >> 3) & 0b11


class GeneralPurposeRegister(Register):
    """A base class for general-purpose registers"""
    _go_physical_id_map = {0x0: 'AX',  0x1: 'CX',  0x2: 'DX',  0x3: 'BX',
                           0x4: 'SP',  0x5: 'BP',  0x6: 'SI',  0x7: 'DI',
                           0x8: 'R8',  0x9: 'R9',  0xA: 'R10', 0xB: 'R11',
                           0xC: 'R12', 0xD: 'R13', 0xE: 'R14', 0xF: 'R15'}
    _kind = 1

    def __init__(self, mask, virtual_id=None, physical_id=None):
        super(GeneralPurposeRegister, self).__init__(mask, virtual_id, physical_id)

    @property
    def as_low_byte(self):
        return GeneralPurposeRegister8(self.physical_id, self.virtual_id)

    @property
    def as_word(self):
        return GeneralPurposeRegister16(self.physical_id, self.virtual_id)

    @property
    def as_dword(self):
        return GeneralPurposeRegister32(self.physical_id, self.virtual_id)

    @property
    def as_qword(self):
        return GeneralPurposeRegister64(self.physical_id, self.virtual_id)

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            assert not self.is_virtual, \
                "Go assembler does not support virtual registers"
            return GeneralPurposeRegister._go_physical_id_map[self.physical_id]
        elif assembly_format == "gas":
            return "%" + str(self)
        else:
            return str(self)


class GeneralPurposeRegister64(GeneralPurposeRegister):
    """64-bit general-purpose register"""
    size = 8

    _physical_id_map = {0x0: 'rax', 0x1: 'rcx', 0x2: 'rdx', 0x3: 'rbx',
                        0x4: 'rsp', 0x5: 'rbp', 0x6: 'rsi', 0x7: 'rdi',
                        0x8: 'r8',  0x9: 'r9',  0xA: 'r10', 0xB: 'r11',
                        0xC: 'r12', 0xD: 'r13', 0xE: 'r14', 0xF: 'r15'}
    _mask = 0xF

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(GeneralPurposeRegister64, self).__init__(GeneralPurposeRegister64._mask,
                                                           active_function._allocate_general_purpose_register_id())
        else:
            super(GeneralPurposeRegister64, self).__init__(GeneralPurposeRegister64._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "gp64-vreg<%d>" % self.virtual_id
        else:
            return GeneralPurposeRegister64._physical_id_map[self.physical_id]

    def __add__(self, offset):
        from peachpy.x86_64.operand import MemoryAddress
        return MemoryAddress(self) + offset

    def __sub__(self, offset):
        from peachpy.x86_64.operand import MemoryAddress
        return MemoryAddress(self) - offset

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)

rax = GeneralPurposeRegister64(0)
rcx = GeneralPurposeRegister64(1)
rdx = GeneralPurposeRegister64(2)
rbx = GeneralPurposeRegister64(3)
rsp = GeneralPurposeRegister64(4)
rbp = GeneralPurposeRegister64(5)
rsi = GeneralPurposeRegister64(6)
rdi = GeneralPurposeRegister64(7)
r8 = GeneralPurposeRegister64(8)
r9 = GeneralPurposeRegister64(9)
r10 = GeneralPurposeRegister64(10)
r11 = GeneralPurposeRegister64(11)
r12 = GeneralPurposeRegister64(12)
r13 = GeneralPurposeRegister64(13)
r14 = GeneralPurposeRegister64(14)
r15 = GeneralPurposeRegister64(15)


class GeneralPurposeRegister32(GeneralPurposeRegister):
    """32-bit general-purpose register"""
    size = 4

    _physical_id_map = {0x0: 'eax',  0x1: 'ecx',  0x2: 'edx',  0x3: 'ebx',
                        0x4: 'esp',  0x5: 'ebp',  0x6: 'esi',  0x7: 'edi',
                        0x8: 'r8d',  0x9: 'r9d',  0xA: 'r10d', 0xB: 'r11d',
                        0xC: 'r12d', 0xD: 'r13d', 0xE: 'r14d', 0xF: 'r15d'}
    _mask = 0x7

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(GeneralPurposeRegister32, self).__init__(GeneralPurposeRegister32._mask,
                                                           active_function._allocate_general_purpose_register_id())
        else:
            super(GeneralPurposeRegister32, self).__init__(GeneralPurposeRegister32._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "gp32-vreg<%d>" % self.virtual_id
        else:
            return GeneralPurposeRegister32._physical_id_map[self.physical_id]

    def __add__(self, offset):
        from peachpy.x86_64.operand import MemoryAddress
        return MemoryAddress(self) + offset

    def __sub__(self, offset):
        from peachpy.x86_64.operand import MemoryAddress
        return MemoryAddress(self) - offset

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)


eax = GeneralPurposeRegister32(0)
ecx = GeneralPurposeRegister32(1)
edx = GeneralPurposeRegister32(2)
ebx = GeneralPurposeRegister32(3)
esp = GeneralPurposeRegister32(4)
ebp = GeneralPurposeRegister32(5)
esi = GeneralPurposeRegister32(6)
edi = GeneralPurposeRegister32(7)
r8d = GeneralPurposeRegister32(8)
r9d = GeneralPurposeRegister32(9)
r10d = GeneralPurposeRegister32(10)
r11d = GeneralPurposeRegister32(11)
r12d = GeneralPurposeRegister32(12)
r13d = GeneralPurposeRegister32(13)
r14d = GeneralPurposeRegister32(14)
r15d = GeneralPurposeRegister32(15)


class GeneralPurposeRegister16(GeneralPurposeRegister):
    """16-bit general-purpose register"""
    size = 2

    _physical_id_map = {0x0: 'ax',   0x1: 'cx',   0x2: 'dx',   0x3: 'bx',
                        0x4: 'sp',   0x5: 'bp',   0x6: 'si',   0x7: 'di',
                        0x8: 'r8w',  0x9: 'r9w',  0xA: 'r10w', 0xB: 'r11w',
                        0xC: 'r12w', 0xD: 'r13w', 0xE: 'r14w', 0xF: 'r15w'}
    _mask = 0x3

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(GeneralPurposeRegister16, self).__init__(GeneralPurposeRegister16._mask,
                                                           active_function._allocate_general_purpose_register_id())
        else:
            super(GeneralPurposeRegister16, self).__init__(GeneralPurposeRegister16._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "gp16-vreg<%d>" % self.virtual_id
        else:
            return GeneralPurposeRegister16._physical_id_map[self.physical_id]


ax = GeneralPurposeRegister16(0)
cx = GeneralPurposeRegister16(1)
dx = GeneralPurposeRegister16(2)
bx = GeneralPurposeRegister16(3)
sp = GeneralPurposeRegister16(4)
bp = GeneralPurposeRegister16(5)
si = GeneralPurposeRegister16(6)
di = GeneralPurposeRegister16(7)
r8w = GeneralPurposeRegister16(8)
r9w = GeneralPurposeRegister16(9)
r10w = GeneralPurposeRegister16(10)
r11w = GeneralPurposeRegister16(11)
r12w = GeneralPurposeRegister16(12)
r13w = GeneralPurposeRegister16(13)
r14w = GeneralPurposeRegister16(14)
r15w = GeneralPurposeRegister16(15)


class GeneralPurposeRegister8(GeneralPurposeRegister):
    """8-bit general-purpose register"""
    size = 1

    _physical_id_map = {(0x0, 0x1): 'al',   (0x1, 0x1): 'cl',   (0x2, 0x1): 'dl',   (0x3, 0x1): 'bl',
                        (0x0, 0x2): 'ah',   (0x1, 0x2): 'ch',   (0x2, 0x2): 'dh',   (0x3, 0x2): 'bh',
                        (0x4, 0x1): 'spl',  (0x5, 0x1): 'bpl',  (0x6, 0x1): 'sil',  (0x7, 0x1): 'dil',
                        (0x8, 0x1): 'r8b',  (0x9, 0x1): 'r9b',  (0xA, 0x1): 'r10b', (0xB, 0x1): 'r11b',
                        (0xC, 0x1): 'r12b', (0xD, 0x1): 'r13b', (0xE, 0x1): 'r14b', (0xF, 0x1): 'r15b'}
    _go_physical_id_map = {(0x0, 0x1): 'AX',   (0x1, 0x1): 'CX',   (0x2, 0x1): 'DX',   (0x3, 0x1): 'BX',
                           (0x0, 0x2): 'AH',   (0x1, 0x2): 'CH',   (0x2, 0x2): 'DH',   (0x3, 0x2): 'BH',
                           (0x4, 0x1): 'SP',  (0x5, 0x1): 'BP',  (0x6, 0x1): 'SI',  (0x7, 0x1): 'DI',
                           (0x8, 0x1): 'R8',  (0x9, 0x1): 'R9',  (0xA, 0x1): 'R10', (0xB, 0x1): 'R11',
                           (0xC, 0x1): 'R12', (0xD, 0x1): 'R13', (0xE, 0x1): 'R14', (0xF, 0x1): 'R15'}
    _mask = 0x1
    _high_mask = 0x2

    def __init__(self, physical_id=None, virtual_id=None, is_high=False):
        mask = GeneralPurposeRegister8._high_mask if is_high else GeneralPurposeRegister8._mask
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(GeneralPurposeRegister8, self).__init__(mask, active_function._allocate_general_purpose_register_id())
        else:
            super(GeneralPurposeRegister8, self).__init__(mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "gp8-vreg<%d>" % self.virtual_id
        else:
            return GeneralPurposeRegister8._physical_id_map[(self.physical_id, self.mask)]

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            assert not self.is_virtual, \
                "Go assembler does not support virtual registers"
            return GeneralPurposeRegister8._go_physical_id_map[(self.physical_id, self.mask)]
        else:
            return super(GeneralPurposeRegister8, self).format(assembly_format)


al = GeneralPurposeRegister8(0)
cl = GeneralPurposeRegister8(1)
dl = GeneralPurposeRegister8(2)
bl = GeneralPurposeRegister8(3)
ah = GeneralPurposeRegister8(0, is_high=True)
ch = GeneralPurposeRegister8(1, is_high=True)
dh = GeneralPurposeRegister8(2, is_high=True)
bh = GeneralPurposeRegister8(3, is_high=True)
spl = GeneralPurposeRegister8(4)
bpl = GeneralPurposeRegister8(5)
sil = GeneralPurposeRegister8(6)
dil = GeneralPurposeRegister8(7)
r8b = GeneralPurposeRegister8(8)
r9b = GeneralPurposeRegister8(9)
r10b = GeneralPurposeRegister8(10)
r11b = GeneralPurposeRegister8(11)
r12b = GeneralPurposeRegister8(12)
r13b = GeneralPurposeRegister8(13)
r14b = GeneralPurposeRegister8(14)
r15b = GeneralPurposeRegister8(15)


class MMXRegister(Register):
    """64-bit MMX technology register"""
    size = 8

    _physical_id_map = {n: "mm" + str(n) for n in range(8)}
    _go_physical_id_map = {n: "M" + str(n) for n in range(8)}
    _kind = 2
    _mask = 0x10

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(MMXRegister, self).__init__(MMXRegister._mask,
                                              active_function._allocate_mmx_register_id())
        else:
            super(MMXRegister, self).__init__(MMXRegister._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "mm-vreg<%d>" % self.virtual_id
        else:
            return MMXRegister._physical_id_map[self.physical_id]

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            assert not self.is_virtual, \
                "Go assembler does not support virtual registers"
            return MMXRegister._go_physical_id_map[self.physical_id]
        elif assembly_format == "gas":
            return "%" + str(self)
        else:
            return str(self)


mm0 = MMXRegister(0)
mm1 = MMXRegister(1)
mm2 = MMXRegister(2)
mm3 = MMXRegister(3)
mm4 = MMXRegister(4)
mm5 = MMXRegister(5)
mm6 = MMXRegister(6)
mm7 = MMXRegister(7)


class XMMRegister(Register):
    """128-bit xmm (SSE) register"""
    size = 16

    _physical_id_map = {n: "xmm" + str(n) for n in range(32)}
    _go_physical_id_map = {n: "X" + str(n) for n in range(16)}
    _kind = 3
    _mask = 0x100

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(XMMRegister, self).__init__(XMMRegister._mask,
                                              active_function._allocate_xmm_register_id())
        else:
            super(XMMRegister, self).__init__(XMMRegister._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "xmm-vreg<%d>" % self.virtual_id
        else:
            return XMMRegister._physical_id_map[self.physical_id]

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            assert not self.is_virtual, \
                "Go assembler does not support virtual registers"
            return XMMRegister._go_physical_id_map[self.physical_id]
        elif assembly_format == "gas":
            return "%" + str(self)
        else:
            return str(self)

    @property
    def as_xmm(self):
        return XMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_ymm(self):
        return YMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_zmm(self):
        return ZMMRegister(self.physical_id, self.virtual_id)

    @property
    def code(self):
        """Returns 5-bit encoding of the register"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return self.physical_id

    @property
    def kcode(self):
        """Returns encoding of mask register"""
        return 0

    @property
    def zcode(self):
        """Returns encoding of zeroing/merging flag of mask register"""
        return 0

    def __call__(self, mask):
        if not isinstance(mask, (KRegister, RegisterMask)):
            raise SyntaxError("xmm(mask) syntax requires mask to be a KRegister or KRegister.z")
        return MaskedRegister(self, mask)

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)


xmm0 = XMMRegister(0)
xmm1 = XMMRegister(1)
xmm2 = XMMRegister(2)
xmm3 = XMMRegister(3)
xmm4 = XMMRegister(4)
xmm5 = XMMRegister(5)
xmm6 = XMMRegister(6)
xmm7 = XMMRegister(7)
xmm8 = XMMRegister(8)
xmm9 = XMMRegister(9)
xmm10 = XMMRegister(10)
xmm11 = XMMRegister(11)
xmm12 = XMMRegister(12)
xmm13 = XMMRegister(13)
xmm14 = XMMRegister(14)
xmm15 = XMMRegister(15)
xmm16 = XMMRegister(16)
xmm17 = XMMRegister(17)
xmm18 = XMMRegister(18)
xmm19 = XMMRegister(19)
xmm20 = XMMRegister(20)
xmm21 = XMMRegister(21)
xmm22 = XMMRegister(22)
xmm23 = XMMRegister(23)
xmm24 = XMMRegister(24)
xmm25 = XMMRegister(25)
xmm26 = XMMRegister(26)
xmm27 = XMMRegister(27)
xmm28 = XMMRegister(28)
xmm29 = XMMRegister(29)
xmm30 = XMMRegister(30)
xmm31 = XMMRegister(31)


class YMMRegister(Register):
    """256-bit ymm (AVX) register"""
    size = 32

    _physical_id_map = {n: "ymm" + str(n) for n in range(32)}
    _kind = 3
    _mask = 0x300

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(YMMRegister, self).__init__(YMMRegister._mask,
                                              active_function._allocate_xmm_register_id())
        else:
            super(YMMRegister, self).__init__(YMMRegister._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "ymm-vreg<%d>" % self.virtual_id
        else:
            return YMMRegister._physical_id_map[self.physical_id]

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            assert not self.is_virtual, \
                "Go assembler does not support virtual registers"
            return XMMRegister._go_physical_id_map[self.physical_id]
        elif assembly_format == "gas":
            return "%" + str(self)
        else:
            return str(self)

    @property
    def as_xmm(self):
        return XMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_ymm(self):
        return YMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_zmm(self):
        return ZMMRegister(self.physical_id, self.virtual_id)

    @property
    def code(self):
        """Returns 5-bit encoding of the register"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return self.physical_id

    @property
    def kcode(self):
        """Returns encoding of mask register"""
        return 0

    @property
    def zcode(self):
        """Returns encoding of zeroing/merging flag of mask register"""
        return 0

    def __call__(self, mask):
        if not isinstance(mask, (KRegister, RegisterMask)):
            raise SyntaxError("ymm(mask) syntax requires mask to be a KRegister or KRegister.z")
        return MaskedRegister(self, mask)

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)


ymm0 = YMMRegister(0)
ymm1 = YMMRegister(1)
ymm2 = YMMRegister(2)
ymm3 = YMMRegister(3)
ymm4 = YMMRegister(4)
ymm5 = YMMRegister(5)
ymm6 = YMMRegister(6)
ymm7 = YMMRegister(7)
ymm8 = YMMRegister(8)
ymm9 = YMMRegister(9)
ymm10 = YMMRegister(10)
ymm11 = YMMRegister(11)
ymm12 = YMMRegister(12)
ymm13 = YMMRegister(13)
ymm14 = YMMRegister(14)
ymm15 = YMMRegister(15)
ymm16 = YMMRegister(16)
ymm17 = YMMRegister(17)
ymm18 = YMMRegister(18)
ymm19 = YMMRegister(19)
ymm20 = YMMRegister(20)
ymm21 = YMMRegister(21)
ymm22 = YMMRegister(22)
ymm23 = YMMRegister(23)
ymm24 = YMMRegister(24)
ymm25 = YMMRegister(25)
ymm26 = YMMRegister(26)
ymm27 = YMMRegister(27)
ymm28 = YMMRegister(28)
ymm29 = YMMRegister(29)
ymm30 = YMMRegister(30)
ymm31 = YMMRegister(31)


class ZMMRegister(Register):
    """512-bit zmm (AVX-512) register"""
    size = 64

    _physical_id_map = {n: "zmm" + str(n) for n in range(32)}
    _kind = 3
    _mask = 0x700

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(ZMMRegister, self).__init__(ZMMRegister._mask,
                                              active_function._allocate_xmm_register_id())
        else:
            super(ZMMRegister, self).__init__(ZMMRegister._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "zmm-vreg<%d>" % self.virtual_id
        else:
            return ZMMRegister._physical_id_map[self.physical_id]

    @property
    def as_xmm(self):
        return XMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_ymm(self):
        return YMMRegister(self.physical_id, self.virtual_id)

    @property
    def as_zmm(self):
        return ZMMRegister(self.physical_id, self.virtual_id)

    @property
    def code(self):
        """Returns 5-bit encoding of the register"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return self.physical_id

    @property
    def kcode(self):
        """Returns encoding of mask register"""
        return 0

    @property
    def zcode(self):
        """Returns encoding of zeroing/merging flag of mask register"""
        return 0

    def __call__(self, mask):
        if not isinstance(mask, (KRegister, RegisterMask)):
            raise SyntaxError("zmm(mask) syntax requires mask to be a KRegister or KRegister.z")
        return MaskedRegister(self, mask)

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)


zmm0 = ZMMRegister(0)
zmm1 = ZMMRegister(1)
zmm2 = ZMMRegister(2)
zmm3 = ZMMRegister(3)
zmm4 = ZMMRegister(4)
zmm5 = ZMMRegister(5)
zmm6 = ZMMRegister(6)
zmm7 = ZMMRegister(7)
zmm8 = ZMMRegister(8)
zmm9 = ZMMRegister(9)
zmm10 = ZMMRegister(10)
zmm11 = ZMMRegister(11)
zmm12 = ZMMRegister(12)
zmm13 = ZMMRegister(13)
zmm14 = ZMMRegister(14)
zmm15 = ZMMRegister(15)
zmm16 = ZMMRegister(16)
zmm17 = ZMMRegister(17)
zmm18 = ZMMRegister(18)
zmm19 = ZMMRegister(19)
zmm20 = ZMMRegister(20)
zmm21 = ZMMRegister(21)
zmm22 = ZMMRegister(22)
zmm23 = ZMMRegister(23)
zmm24 = ZMMRegister(24)
zmm25 = ZMMRegister(25)
zmm26 = ZMMRegister(26)
zmm27 = ZMMRegister(27)
zmm28 = ZMMRegister(28)
zmm29 = ZMMRegister(29)
zmm30 = ZMMRegister(30)
zmm31 = ZMMRegister(31)


class KRegister(Register):
    """AVX-512 mask register"""
    size = 8

    _physical_id_map = {n: "k" + str(n) for n in range(8)}
    _kind = 4
    _mask = 0x40

    def __init__(self, physical_id=None, virtual_id=None):
        if virtual_id is None and physical_id is None:
            from peachpy.common.function import active_function
            super(KRegister, self).__init__(KRegister._mask,
                                               active_function._allocate_mask_register_id())
        else:
            super(KRegister, self).__init__(KRegister._mask, virtual_id, physical_id)

    def __str__(self):
        if self.is_virtual:
            return "k-vreg<%d>" % self.virtual_id
        else:
            return KRegister._physical_id_map[self.physical_id]

    @property
    def z(self):
        return RegisterMask(self, is_zeroing=True)

    @property
    def kcode(self):
        """Returns the register encoding"""
        assert self.physical_id is not None, \
            "The method returns encoding detail for a physical register"
        return self.physical_id

    @property
    def zcode(self):
        """Returns encoding of the merge/zero flags"""
        return 0

    def __call__(self, mask):
        if not isinstance(mask, KRegister):
            raise SyntaxError("k(mask) syntax requires mask to be a KRegister")
        return MaskedRegister(self, mask)


class RegisterMask:
    def __init__(self, mask_register, is_zeroing=False):
        self.mask_register = mask_register
        self.is_zeroing = is_zeroing

    @property
    def kcode(self):
        """Returns encoding of the mask register"""
        return self.mask_register.kcode

    @property
    def zcode(self):
        """Returns encoding of the merge/zero flags"""
        return int(self.is_zeroing)


k0 = KRegister(0)
k1 = KRegister(1)
k2 = KRegister(2)
k3 = KRegister(3)
k4 = KRegister(4)
k5 = KRegister(5)
k6 = KRegister(6)
k7 = KRegister(7)


class MaskedRegister:
    def __init__(self, register, mask):
        assert isinstance(register, (XMMRegister, YMMRegister, ZMMRegister, KRegister))
        assert isinstance(mask, (KRegister, RegisterMask))
        self.register = register
        if isinstance(mask, KRegister):
            self.mask = RegisterMask(mask)
        else:
            self.mask = mask

    @property
    def code(self):
        """Returns the 5-bit register encoding"""
        return self.register.code

    @property
    def lcode(self):
        """Returns the bits 0-2 of register encoding"""
        return self.register.lcode

    @property
    def hcode(self):
        """Returns the bit 3 of register encoding"""
        return self.register.hcode

    @property
    def ecode(self):
        """Returns the bit 4 of register encoding"""
        return self.register.ecode

    @property
    def hlcode(self):
        """Returns the bits 0-3 of register encoding"""
        return self.register.hlcode

    @property
    def ehcode(self):
        """Returns the bits 3-4 of register encoding"""
        return self.register.ehcode

    @property
    def kcode(self):
        """Returns encoding of mask register"""
        return self.mask.kcode

    @property
    def zcode(self):
        """Returns encoding of zeroing/merging flag of mask register"""
        return self.mask.zcode

    def __mul__(self, scale):
        from peachpy.x86_64.operand import MemoryAddress
        from peachpy.util import is_int
        if not is_int(scale):
            raise TypeError("Register can be scaled only by an integer number")
        if int(scale) not in {1, 2, 4, 8}:
            raise ValueError("Invalid scale value (%d): only scaling by 1, 2, 4, or 8 is supported" % scale)
        return MemoryAddress(index=self, scale=scale)


class RIPRegister:
    def __init__(self):
        pass

    def __str__(self):
        return "rip"

    def __add__(self, offset):
        from peachpy.x86_64.operand import RIPRelativeOffset
        return RIPRelativeOffset(offset)

    def __sub__(self, offset):
        from peachpy.x86_64.operand import RIPRelativeOffset
        return RIPRelativeOffset(-offset)


rip = RIPRegister()
