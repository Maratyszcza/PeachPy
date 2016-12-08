# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


import six


class Register(object):
    GPType = 1
    WMMXType = 2
    VFPType = 3

    def __init__(self):
        super(Register, self).__init__()
        self.number = None
        self.size = None

    def __lt__(self, other):
        return self.number < other.number

    def __le__(self, other):
        return self.number <= other.number

    def __eq__(self, other):
        return isinstance(other, Register) and self.number == other.number

    def __ne__(self, other):
        return not isinstance(other, Register) or self.number != other.number

    def __gt__(self, other):
        return self.number > other.number

    def __ge__(self, other):
        return self.number >= other.number

    def __contains__(self, register):
        if self.id == register.id:
            register_mask = register.get_mask()
            return (self.mask & register_mask) == register_mask
        else:
            return False

    def __hash__(self):
        return self.number

    @property
    def id(self):
        return self.number >> 12

    @property
    def mask(self):
        return self.number & 0xFFF

    @property
    def bitboard(self):
        assert not self.is_virtual
        if isinstance(self, GeneralPurposeRegister) or isinstance(self, WMMXRegister) or isinstance(self, SRegister):
            return 0x1 << self.get_physical_number()
        elif isinstance(self, DRegister):
            return 0x3 << (self.get_physical_number() * 2)
        elif isinstance(self, QRegister):
            return 0xF << (self.get_physical_number() * 4)

    @staticmethod
    def from_parts(id, mask, expand=False):
        if mask == 0x001:
            # General-purpose register
            return GeneralPurposeRegister((id << 12) | mask)
        elif mask == 0x002:
            # WMMX register
            return WMMXRegister((id << 12) | 0x002)
        elif (mask & ~0x7F0) == 0x000:
            # VFP or NEON register
            if (mask & 0x7F0) == 0x0F0:
                return QRegister((id << 12) | mask)
            elif ((mask & 0x7F0) == 0x030) or ((mask & 0x7F0) == 0x0C0) or ((mask & 0x7F0) == 0x300):
                return DRegister((id << 12) | mask)
            elif (mask & (mask - 1)) == 0:
                return SRegister((id << 12) | mask)
            else:
                if expand and ((mask & ~0x0F0) == 0):
                    return QRegister((id << 12) | 0x0F0)
                else:
                    raise ValueError("Invalid register mask %s" % hex(mask))
        else:
            raise ValueError("Invalid register mask %s" % hex(mask))

    @staticmethod
    def from_bitboard(bitboard, regtype):
        if regtype == Register.GPType:
            return {0x0001: r0,
                    0x0002: r1,
                    0x0004: r2,
                    0x0008: r3,
                    0x0010: r4,
                    0x0020: r5,
                    0x0040: r6,
                    0x0080: r7,
                    0x0100: r8,
                    0x0200: r9,
                    0x0400: r10,
                    0x0800: r11,
                    0x1000: r12,
                    0x2000: sp,
                    0x4000: lr,
                    0x8000: pc}[bitboard]
        elif regtype == Register.WMMXType:
            return {0x0001: wr0,
                    0x0002: wr1,
                    0x0004: wr2,
                    0x0008: wr3,
                    0x0010: wr4,
                    0x0020: wr5,
                    0x0040: wr6,
                    0x0080: wr7,
                    0x0100: wr8,
                    0x0200: wr9,
                    0x0400: wr10,
                    0x0800: wr11,
                    0x1000: wr12,
                    0x2000: wr13,
                    0x4000: wr14,
                    0x8000: wr15}[bitboard]
        elif regtype == Register.VFPType:
            return {0x00000001: s0,
                    0x00000002: s1,
                    0x00000004: s2,
                    0x00000008: s3,
                    0x00000010: s4,
                    0x00000020: s5,
                    0x00000040: s6,
                    0x00000080: s7,
                    0x00000100: s8,
                    0x00000200: s9,
                    0x00000400: s10,
                    0x00000800: s11,
                    0x00001000: s12,
                    0x00002000: s13,
                    0x00004000: s14,
                    0x00008000: s15,
                    0x00010000: s16,
                    0x00020000: s17,
                    0x00040000: s18,
                    0x00080000: s19,
                    0x00100000: s20,
                    0x00200000: s21,
                    0x00400000: s22,
                    0x00800000: s23,
                    0x01000000: s24,
                    0x02000000: s25,
                    0x04000000: s26,
                    0x08000000: s27,
                    0x10000000: s28,
                    0x20000000: s29,
                    0x40000000: s30,
                    0x80000000: s31,
                    0x0000000000000003: d0,
                    0x000000000000000C: d1,
                    0x0000000000000030: d2,
                    0x00000000000000C0: d3,
                    0x0000000000000300: d4,
                    0x0000000000000C00: d5,
                    0x0000000000003000: d6,
                    0x000000000000C000: d7,
                    0x0000000000030000: d8,
                    0x00000000000C0000: d9,
                    0x0000000000300000: d10,
                    0x0000000000C00000: d11,
                    0x0000000003000000: d12,
                    0x000000000C000000: d13,
                    0x0000000030000000: d14,
                    0x00000000C0000000: d15,
                    0x0000000300000000: d16,
                    0x0000000C00000000: d17,
                    0x0000003000000000: d18,
                    0x000000C000000000: d19,
                    0x0000030000000000: d20,
                    0x00000C0000000000: d21,
                    0x0000300000000000: d22,
                    0x0000C00000000000: d23,
                    0x0003000000000000: d24,
                    0x000C000000000000: d25,
                    0x0030000000000000: d26,
                    0x00C0000000000000: d27,
                    0x0300000000000000: d28,
                    0x0C00000000000000: d29,
                    0x3000000000000000: d30,
                    0xC000000000000000: d31,
                    0x000000000000000F: q0,
                    0x00000000000000F0: q1,
                    0x0000000000000F00: q2,
                    0x000000000000F000: q3,
                    0x00000000000F0000: q4,
                    0x0000000000F00000: q5,
                    0x000000000F000000: q6,
                    0x00000000F0000000: q7,
                    0x0000000F00000000: q8,
                    0x000000F000000000: q9,
                    0x00000F0000000000: q10,
                    0x0000F00000000000: q11,
                    0x000F000000000000: q12,
                    0x00F0000000000000: q13,
                    0x0F00000000000000: q14,
                    0xF000000000000000: q15}[bitboard]

    def extend_bitboard(self, bitboard):
        physical_register = Register.from_bitboard(bitboard, self.type)
        if isinstance(self, SRegister) and self.parent and self.parent.parent:
            physical_register = physical_register.get_parent().get_parent()
        elif (isinstance(self, SRegister) or isinstance(self, DRegister)) and self.parent:
            physical_register = physical_register.get_parent()
        return physical_register.get_bitboard()

    @property
    def is_virtual(self):
        return self.number >= 0x40000

    def bind(self, register):
        assert self.is_virtual
        assert not register.is_virtual
        if isinstance(register, GeneralPurposeRegister) or isinstance(register, WMMXRegister):
            self.number = (self.number & 0xFFF) | (register.id << 12)
        elif isinstance(register, SRegister):
            self.number = register.number
        elif isinstance(register, DRegister):
            if isinstance(self, DRegister):
                self.number = register.number
            elif isinstance(self, SRegister):
                if register.mask == 0x030 and self.mask == 0x100:
                    self.number = (register.id << 12) | 0x010
                elif register.mask == 0x030 and self.mask == 0x200:
                    self.number = (register.id << 12) | 0x020
                elif register.mask == 0x0C0 and self.mask == 0x100:
                    self.number = (register.id << 12) | 0x040
                elif register.mask == 0x0C0 and self.mask == 0x200:
                    self.number = (register.id << 12) | 0x080
                else:
                    assert False
            else:
                assert False
        elif isinstance(register, QRegister):
            if isinstance(self, QRegister):
                self.number = register.number
            elif isinstance(self, DRegister):
                self.number = (register.id << 12) | self.mask
            elif isinstance(self, SRegister):
                self.number = (register.id << 12) | self.mask
            else:
                assert False
        assert not self.is_virtual


class GeneralPurposeRegister(Register):
    _name_to_number_map = {'r0': 0x20001,
                           'r1': 0x21001,
                           'r2': 0x22001,
                           'r3': 0x23001,
                           'r4': 0x24001,
                           'r5': 0x25001,
                           'r6': 0x26001,
                           'r7': 0x27001,
                           'r8': 0x28001,
                           'r9': 0x29001,
                           'r10': 0x2A001,
                           'r11': 0x2B001,
                           'r12': 0x2C001,
                           'sp': 0x2D001,
                           'lr': 0x2E001,
                           'pc': 0x2F001}

    _number_to_name_map = {0x20001: 'r0',
                           0x21001: 'r1',
                           0x22001: 'r2',
                           0x23001: 'r3',
                           0x24001: 'r4',
                           0x25001: 'r5',
                           0x26001: 'r6',
                           0x27001: 'r7',
                           0x28001: 'r8',
                           0x29001: 'r9',
                           0x2A001: 'r10',
                           0x2B001: 'r11',
                           0x2C001: 'r12',
                           0x2D001: 'sp',
                           0x2E001: 'lr',
                           0x2F001: 'pc'}

    def __init__(self, id=None):
        super(GeneralPurposeRegister, self).__init__()
        if id is None:
            from peachpy.arm.function import active_function
            self.number = active_function.allocate_general_purpose_register()
            self.type = Register.GPType
            self.size = 4
        elif isinstance(id, int):
            self.number = id
            self.type = Register.GPType
            self.size = 4
        elif isinstance(id, str):
            if id in GeneralPurposeRegister._name_to_number_map:
                self.number = GeneralPurposeRegister._name_to_number_map[id]
                self.type = Register.GPType
                self.size = 4
            else:
                raise ValueError('Unknown register name: {0}'.format(id))
        elif isinstance(id, GeneralPurposeRegister):
            self.number = id.number
            self.type = id.type
            self.size = id.size
        else:
            raise TypeError('Invalid register id')

    def get_physical_number(self):
        return {0x20001: 0,
                0x21001: 1,
                0x22001: 2,
                0x23001: 3,
                0x24001: 4,
                0x25001: 5,
                0x26001: 6,
                0x27001: 7,
                0x28001: 8,
                0x29001: 9,
                0x2A001: 10,
                0x2B001: 11,
                0x2C001: 12,
                0x2D001: 13,
                0x2E001: 14,
                0x2F001: 15}[self.number]

    @staticmethod
    def is_compatible_bitboard(bitboard):
        return bitboard in {0x0001, 0x0002, 0x0004, 0x0008,
                            0x0010, 0x0020, 0x0040, 0x0080,
                            0x0100, 0x0200, 0x0400, 0x0800,
                            0x1000, 0x2000, 0x4000, 0x8000}

    def __str__(self):
        if self.is_virtual:
            return 'gp-vreg<{0}>'.format((self.number - 0x40000) >> 12)
        else:
            return GeneralPurposeRegister._number_to_name_map[self.number]

    def __neg__(self):
        return NegatedGeneralPurposeRegister(self)

    def wb(self):
        return GeneralPurposeRegisterWriteback(self)

    def LSL(self, shift):
        return ShiftedGeneralPurposeRegister(self, "LSL", shift)

    def LSR(self, shift):
        return ShiftedGeneralPurposeRegister(self, "LSR", shift)

    def ASR(self, shift):
        return ShiftedGeneralPurposeRegister(self, "ASR", shift)

    def ROR(self, shift):
        return ShiftedGeneralPurposeRegister(self, "ROR", shift)

    def RRX(self):
        return ShiftedGeneralPurposeRegister(self, "RRX")


r0 = GeneralPurposeRegister('r0')
r1 = GeneralPurposeRegister('r1')
r2 = GeneralPurposeRegister('r2')
r3 = GeneralPurposeRegister('r3')
r4 = GeneralPurposeRegister('r4')
r5 = GeneralPurposeRegister('r5')
r6 = GeneralPurposeRegister('r6')
r7 = GeneralPurposeRegister('r7')
r8 = GeneralPurposeRegister('r8')
r9 = GeneralPurposeRegister('r9')
r10 = GeneralPurposeRegister('r10')
r11 = GeneralPurposeRegister('r11')
r12 = GeneralPurposeRegister('r12')
sp = GeneralPurposeRegister('sp')
lr = GeneralPurposeRegister('lr')
pc = GeneralPurposeRegister('pc')


class GeneralPurposeRegisterWriteback(GeneralPurposeRegister):
    def __init__(self, register):
        if isinstance(register, GeneralPurposeRegister):
            super(GeneralPurposeRegisterWriteback, self).__init__(register)
            self.register = register
        else:
            raise TypeError('Register parameter is not an instance of GeneralPurposeRegister')

    def __str__(self):
        return str(self.register) + "!"


class NegatedGeneralPurposeRegister:
    def __init__(self, register):
        if isinstance(register, GeneralPurposeRegister):
            self.register = register
        else:
            raise TypeError('Register parameter is not an instance of GeneralPurposeRegister')

    def __str__(self):
        return "-" + str(self.register)


class ShiftedGeneralPurposeRegister:
    def __init__(self, register, kind, shift=None):
        if isinstance(register, GeneralPurposeRegister):
            self.register = register
            if kind in {'LSR', 'ASR'}:
                if 1 <= shift <= 32:
                    self.shift = int(shift)
                    self.type = kind
                else:
                    raise ValueError("Shift is beyond the allowed range (1 to 32)")
            elif kind in {'LSL', 'ROR'}:
                if 1 <= shift <= 31:
                    self.shift = int(shift)
                    self.type = kind
                else:
                    raise ValueError("Shift is beyond the allowed range (1 to 31)")
            elif kind == 'RRX':
                if shift is None:
                    self.shift = shift
                    self.type = kind
                else:
                    raise ValueError("Shift parameter is not allowed for RRX modificator")
            else:
                raise ValueError("Illegal shift kind %s" % kind)
        else:
            raise TypeError("Register parameter must be a general-purpose register")

    def __str__(self):
        if self.type != 'RRX':
            return str(self.register) + ", " + self.type + " #" + str(self.shift)
        else:
            return str(self.register) + ", " + self.type


class WMMXRegister(Register):
    _name_to_number_map = {'wr0': 0x10002,
                           'wr1': 0x11002,
                           'wr2': 0x12002,
                           'wr3': 0x13002,
                           'wr4': 0x14002,
                           'wr5': 0x15002,
                           'wr6': 0x16002,
                           'wr7': 0x17002,
                           'wr8': 0x18002,
                           'wr9': 0x19002,
                           'wr10': 0x1A002,
                           'wr11': 0x1B002,
                           'wr12': 0x1C002,
                           'wr13': 0x1D002,
                           'wr14': 0x1E002,
                           'wr15': 0x1F002}

    _number_to_name_map = {0x10002: 'wr0',
                           0x11002: 'wr1',
                           0x12002: 'wr2',
                           0x13002: 'wr3',
                           0x14002: 'wr4',
                           0x15002: 'wr5',
                           0x16002: 'wr6',
                           0x17002: 'wr7',
                           0x18002: 'wr8',
                           0x19002: 'wr9',
                           0x1A002: 'wr10',
                           0x1B002: 'wr11',
                           0x1C002: 'wr12',
                           0x1D002: 'wr13',
                           0x1E002: 'wr14',
                           0x1F002: 'wr15'}

    def __init__(self, id=None):
        super(WMMXRegister, self).__init__()
        if id is None:
            from peachpy.arm.function import active_function
            self.number = active_function.allocate_wmmx_register()
            self.regtype = Register.WMMXType
            self.size = 8
        elif isinstance(id, int):
            self.number = id
            self.regtype = Register.WMMXType
            self.size = 8
        elif isinstance(id, str):
            if id in WMMXRegister._name_to_number_map:
                self.number = WMMXRegister._name_to_number_map[id]
                self.regtype = Register.WMMXType
                self.size = 8
            else:
                raise ValueError('Unknown register name: {0}'.format(id))
        elif isinstance(id, WMMXRegister):
            self.number = id.number
            self.regtype = id.regtype
            self.size = id.size
        else:
            raise TypeError(
                'Register id is neither a name of an architectural mmx register, nor an id of a virtual register')

    @staticmethod
    def is_compatible_bitboard(bitboard):
        return bitboard in {0x0001, 0x0002, 0x0004, 0x0008,
                            0x0010, 0x0020, 0x0040, 0x0080,
                            0x0100, 0x0200, 0x0400, 0x0800,
                            0x1000, 0x2000, 0x4000, 0x8000}

    def __str__(self):
        if self.is_virtual:
            return 'wmmx-vreg<{0}>'.format((self.number - 0x40000) >> 12)
        else:
            return WMMXRegister._number_to_name_map[self.number]


wr0 = WMMXRegister('wr0')
wr1 = WMMXRegister('wr1')
wr2 = WMMXRegister('wr2')
wr3 = WMMXRegister('wr3')
wr4 = WMMXRegister('wr4')
wr5 = WMMXRegister('wr5')
wr6 = WMMXRegister('wr6')
wr7 = WMMXRegister('wr7')
wr8 = WMMXRegister('wr8')
wr9 = WMMXRegister('wr9')
wr10 = WMMXRegister('wr10')
wr11 = WMMXRegister('wr11')
wr12 = WMMXRegister('wr12')
wr13 = WMMXRegister('wr13')
wr14 = WMMXRegister('wr14')
wr15 = WMMXRegister('wr15')


class SRegister(Register):
    _name_to_number_map = {'s0': 0x00010,
                           's1': 0x00020,
                           's2': 0x00040,
                           's3': 0x00080,
                           's4': 0x01010,
                           's5': 0x01020,
                           's6': 0x01040,
                           's7': 0x01080,
                           's8': 0x02010,
                           's9': 0x02020,
                           's10': 0x02040,
                           's11': 0x02080,
                           's12': 0x03010,
                           's13': 0x03020,
                           's14': 0x03040,
                           's15': 0x03080,
                           's16': 0x04010,
                           's17': 0x04020,
                           's18': 0x04040,
                           's19': 0x04080,
                           's20': 0x05010,
                           's21': 0x05020,
                           's22': 0x05040,
                           's23': 0x05080,
                           's24': 0x06010,
                           's25': 0x06020,
                           's26': 0x06040,
                           's27': 0x06080,
                           's28': 0x07010,
                           's29': 0x07020,
                           's30': 0x07040,
                           's31': 0x07080}

    _number_to_name_map = {0x00010: 's0',
                           0x00020: 's1',
                           0x00040: 's2',
                           0x00080: 's3',
                           0x01010: 's4',
                           0x01020: 's5',
                           0x01040: 's6',
                           0x01080: 's7',
                           0x02010: 's8',
                           0x02020: 's9',
                           0x02040: 's10',
                           0x02080: 's11',
                           0x03010: 's12',
                           0x03020: 's13',
                           0x03040: 's14',
                           0x03080: 's15',
                           0x04010: 's16',
                           0x04020: 's17',
                           0x04040: 's18',
                           0x04080: 's19',
                           0x05010: 's20',
                           0x05020: 's21',
                           0x05040: 's22',
                           0x05080: 's23',
                           0x06010: 's24',
                           0x06020: 's25',
                           0x06040: 's26',
                           0x06080: 's27',
                           0x07010: 's28',
                           0x07020: 's29',
                           0x07040: 's30',
                           0x07080: 's31'}

    def __init__(self, id=None):
        super(SRegister, self).__init__()
        if id is None:
            from peachpy.arm.function import active_function
            self.number = active_function.allocate_s_register()
            self.type = Register.VFPType
            self.size = 4
        elif isinstance(id, int):
            self.number = id
            self.type = Register.VFPType
            self.size = 4
        elif isinstance(id, str):
            if id in SRegister._name_to_number_map:
                self.number = SRegister._name_to_number_map[id]
                self.type = Register.VFPType
                self.size = 4
            else:
                raise ValueError('Unknown register name: {0}'.format(id))
        elif isinstance(id, SRegister):
            self.number = id.number
            self.type = id.type
            self.size = id.size
        else:
            raise TypeError(
                'Register id is neither a name of an architectural S register, nor an id of a virtual register')

    def get_physical_number(self):
        assert not self.is_virtual
        return {0x00010: 0,
                0x00020: 1,
                0x00040: 2,
                0x00080: 3,
                0x01010: 4,
                0x01020: 5,
                0x01040: 6,
                0x01080: 7,
                0x02010: 8,
                0x02020: 9,
                0x02040: 10,
                0x02080: 11,
                0x03010: 12,
                0x03020: 13,
                0x03040: 14,
                0x03080: 15,
                0x04010: 16,
                0x04020: 17,
                0x04040: 18,
                0x04080: 19,
                0x05010: 20,
                0x05020: 21,
                0x05040: 22,
                0x05080: 23,
                0x06010: 24,
                0x06020: 25,
                0x06040: 26,
                0x06080: 27,
                0x07010: 28,
                0x07020: 29,
                0x07040: 30,
                0x07080: 31}[self.number]

    def is_compatible_bitboard(self, bitboard):
        if self.mask == 0x400:
            return bitboard in {0x00000001, 0x00000002, 0x00000004, 0x00000008,
                                0x00000010, 0x00000020, 0x00000040, 0x00000080,
                                0x00000100, 0x00000200, 0x00000400, 0x00000800,
                                0x00001000, 0x00002000, 0x00004000, 0x00008000,
                                0x00010000, 0x00020000, 0x00040000, 0x00080000,
                                0x00100000, 0x00200000, 0x00400000, 0x00800000,
                                0x01000000, 0x02000000, 0x04000000, 0x08000000,
                                0x10000000, 0x20000000, 0x40000000, 0x80000000}
        elif self.mask == 0x200:
            return bitboard in {0x00000002, 0x00000008,
                                0x00000020, 0x00000080,
                                0x00000200, 0x00000800,
                                0x00002000, 0x00008000,
                                0x00020000, 0x00080000,
                                0x00200000, 0x00800000,
                                0x02000000, 0x08000000,
                                0x20000000, 0x80000000}
        elif self.mask == 0x100:
            return bitboard in {0x00000001, 0x00000004,
                                0x00000010, 0x00000040,
                                0x00000100, 0x00000400,
                                0x00001000, 0x00004000,
                                0x00010000, 0x00040000,
                                0x00100000, 0x00400000,
                                0x01000000, 0x04000000,
                                0x10000000, 0x40000000}
        elif self.mask == 0x080:
            return bitboard in {0x00000008, 0x00000080, 0x00000800, 0x00008000,
                                0x00080000, 0x00800000, 0x08000000, 0x80000000}
        elif self.mask == 0x040:
            return bitboard in {0x00000004, 0x00000040, 0x00000400, 0x00004000,
                                0x00040000, 0x00400000, 0x04000000, 0x40000000}
        elif self.mask == 0x020:
            return bitboard in {0x00000002, 0x00000020, 0x00000200, 0x00002000,
                                0x00020000, 0x00200000, 0x02000000, 0x20000000}
        elif self.mask == 0x010:
            return bitboard in {0x00000001, 0x00000010, 0x00000100, 0x00001000,
                                0x00010000, 0x00100000, 0x01000000, 0x10000000}
        else:
            assert False

    def __str__(self):
        if self.is_virtual:
            return 's-vreg<{0}>'.format((self.number - 0x40000) >> 12)
        else:
            return SRegister._number_to_name_map[self.number]

    @property
    def parent(self):
        mask = self.mask
        parent_mask = {0x400: None,
                       0x200: 0x300,
                       0x100: 0x300,
                       0x080: 0x0C0,
                       0x040: 0x0C0,
                       0x020: 0x030,
                       0x010: 0x030}[mask]
        if parent_mask:
            return DRegister(self.number | parent_mask)


s0 = SRegister('s0')
s1 = SRegister('s1')
s2 = SRegister('s2')
s3 = SRegister('s3')
s4 = SRegister('s4')
s5 = SRegister('s5')
s6 = SRegister('s6')
s7 = SRegister('s7')
s8 = SRegister('s8')
s9 = SRegister('s9')
s10 = SRegister('s10')
s11 = SRegister('s11')
s12 = SRegister('s12')
s13 = SRegister('s13')
s14 = SRegister('s14')
s15 = SRegister('s15')
s16 = SRegister('s16')
s17 = SRegister('s17')
s18 = SRegister('s18')
s19 = SRegister('s19')
s20 = SRegister('s20')
s21 = SRegister('s21')
s22 = SRegister('s22')
s23 = SRegister('s23')
s24 = SRegister('s24')
s25 = SRegister('s25')
s26 = SRegister('s26')
s27 = SRegister('s27')
s28 = SRegister('s28')
s29 = SRegister('s29')
s30 = SRegister('s30')
s31 = SRegister('s31')


class DRegister(Register):
    _name_to_number_map = {'d0': 0x00030,
                           'd1': 0x000C0,
                           'd2': 0x01030,
                           'd3': 0x010C0,
                           'd4': 0x02030,
                           'd5': 0x020C0,
                           'd6': 0x03030,
                           'd7': 0x030C0,
                           'd8': 0x04030,
                           'd9': 0x040C0,
                           'd10': 0x05030,
                           'd11': 0x050C0,
                           'd12': 0x06030,
                           'd13': 0x060C0,
                           'd14': 0x07030,
                           'd15': 0x070C0,
                           'd16': 0x08030,
                           'd17': 0x080C0,
                           'd18': 0x09030,
                           'd19': 0x090C0,
                           'd20': 0x0A030,
                           'd21': 0x0A0C0,
                           'd22': 0x0B030,
                           'd23': 0x0B0C0,
                           'd24': 0x0C030,
                           'd25': 0x0C0C0,
                           'd26': 0x0D030,
                           'd27': 0x0D0C0,
                           'd28': 0x0E030,
                           'd29': 0x0E0C0,
                           'd30': 0x0F030,
                           'd31': 0x0F0C0}

    _number_to_name_map = {0x00030: 'd0',
                           0x000C0: 'd1',
                           0x01030: 'd2',
                           0x010C0: 'd3',
                           0x02030: 'd4',
                           0x020C0: 'd5',
                           0x03030: 'd6',
                           0x030C0: 'd7',
                           0x04030: 'd8',
                           0x040C0: 'd9',
                           0x05030: 'd10',
                           0x050C0: 'd11',
                           0x06030: 'd12',
                           0x060C0: 'd13',
                           0x07030: 'd14',
                           0x070C0: 'd15',
                           0x08030: 'd16',
                           0x080C0: 'd17',
                           0x09030: 'd18',
                           0x090C0: 'd19',
                           0x0A030: 'd20',
                           0x0A0C0: 'd21',
                           0x0B030: 'd22',
                           0x0B0C0: 'd23',
                           0x0C030: 'd24',
                           0x0C0C0: 'd25',
                           0x0D030: 'd26',
                           0x0D0C0: 'd27',
                           0x0E030: 'd28',
                           0x0E0C0: 'd29',
                           0x0F030: 'd30',
                           0x0F0C0: 'd31'}

    def __init__(self, id=None):
        super(DRegister, self).__init__()
        if id is None:
            from peachpy.arm.function import active_function
            self.number = active_function.allocate_d_register()
            self.type = Register.VFPType
            self.size = 8
        elif isinstance(id, int):
            self.number = id
            self.type = Register.VFPType
            self.size = 8
        elif isinstance(id, str):
            if id in DRegister._name_to_number_map:
                self.number = DRegister._name_to_number_map[id]
                self.type = Register.VFPType
                self.size = 8
            else:
                raise ValueError('Unknown register name: {0}'.format(id))
        elif isinstance(id, DRegister):
            self.number = id.number
            self.type = id.type
            self.size = id.size
        else:
            raise TypeError(
                'Register id is neither a name of an architectural D register, nor an id of a virtual register')

    def get_physical_number(self):
        assert not self.is_virtual
        return {0x00030: 0,
                0x000C0: 1,
                0x01030: 2,
                0x010C0: 3,
                0x02030: 4,
                0x020C0: 5,
                0x03030: 6,
                0x030C0: 7,
                0x04030: 8,
                0x040C0: 9,
                0x05030: 10,
                0x050C0: 11,
                0x06030: 12,
                0x060C0: 13,
                0x07030: 14,
                0x070C0: 15,
                0x08030: 16,
                0x080C0: 17,
                0x09030: 18,
                0x090C0: 19,
                0x0A030: 20,
                0x0A0C0: 21,
                0x0B030: 22,
                0x0B0C0: 23,
                0x0C030: 24,
                0x0C0C0: 25,
                0x0D030: 26,
                0x0D0C0: 27,
                0x0E030: 28,
                0x0E0C0: 29,
                0x0F030: 30,
                0x0F0C0: 31}[self.number]

    @property
    def is_extended(self):
        return self.number >= 0x08000

    def is_compatible_bitboard(self, bitboard):
        if self.mask == 0x300:
            return bitboard in {0x0000000000000003, 0x000000000000000C,
                                0x0000000000000030, 0x00000000000000C0,
                                0x0000000000000300, 0x0000000000000C00,
                                0x0000000000003000, 0x000000000000C000,
                                0x0000000000030000, 0x00000000000C0000,
                                0x0000000000300000, 0x0000000000C00000,
                                0x0000000003000000, 0x000000000C000000,
                                0x0000000030000000, 0x00000000C0000000,
                                0x0000000300000000, 0x0000000C00000000,
                                0x0000003000000000, 0x000000C000000000,
                                0x0000030000000000, 0x00000C0000000000,
                                0x0000300000000000, 0x0000C00000000000,
                                0x0003000000000000, 0x000C000000000000,
                                0x0030000000000000, 0x00C0000000000000,
                                0x0300000000000000, 0x0C00000000000000,
                                0x3000000000000000, 0xC000000000000000}
        elif self.mask == 0x0C0:
            return bitboard in {0x000000000000000C,
                                0x00000000000000C0,
                                0x0000000000000C00,
                                0x000000000000C000,
                                0x00000000000C0000,
                                0x0000000000C00000,
                                0x000000000C000000,
                                0x00000000C0000000,
                                0x0000000C00000000,
                                0x000000C000000000,
                                0x00000C0000000000,
                                0x0000C00000000000,
                                0x000C000000000000,
                                0x00C0000000000000,
                                0x0C00000000000000,
                                0xC000000000000000}
        elif self.mask == 0x030:
            return bitboard in {0x0000000000000003,
                                0x0000000000000030,
                                0x0000000000000300,
                                0x0000000000003000,
                                0x0000000000030000,
                                0x0000000000300000,
                                0x0000000003000000,
                                0x0000000030000000,
                                0x0000000300000000,
                                0x0000003000000000,
                                0x0000030000000000,
                                0x0000300000000000,
                                0x0003000000000000,
                                0x0030000000000000,
                                0x0300000000000000,
                                0x3000000000000000}
        else:
            assert False

    def __str__(self):
        if self.is_virtual:
            return 'd-vreg<{0}>'.format((self.number - 0x40000) >> 12)
        else:
            return DRegister._number_to_name_map[self.number]

    def __getitem__(self, key):
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step is None:
            return DRegisterLanes(self)
        else:
            raise ValueError("Illegal subscript value %s" % key)

    @property
    def parent(self):
        if self.mask != 0x300:
            return QRegister(self.number | 0x0F0)

    @property
    def low_part(self):
        if (self.number & ~0xFFF) == 0x300:
            return SRegister((self.number & ~0xFFF) | 0x100)
        elif (self.number & ~0xFFF) == 0x0C0:
            return SRegister((self.number & ~0xFFF) | 0x040)
        else:
            return SRegister((self.number & ~0xFFF) | 0x010)

    @property
    def high_part(self):
        if (self.number & ~0xFFF) == 0x300:
            return SRegister((self.number & ~0xFFF) | 0x200)
        elif (self.number & ~0xFFF) == 0x0C0:
            return SRegister((self.number & ~0xFFF) | 0x080)
        else:
            return SRegister((self.number & ~0xFFF) | 0x020)


d0 = DRegister('d0')
d1 = DRegister('d1')
d2 = DRegister('d2')
d3 = DRegister('d3')
d4 = DRegister('d4')
d5 = DRegister('d5')
d6 = DRegister('d6')
d7 = DRegister('d7')
d8 = DRegister('d8')
d9 = DRegister('d9')
d10 = DRegister('d10')
d11 = DRegister('d11')
d12 = DRegister('d12')
d13 = DRegister('d13')
d14 = DRegister('d14')
d15 = DRegister('d15')
d16 = DRegister('d16')
d17 = DRegister('d17')
d18 = DRegister('d18')
d19 = DRegister('d19')
d20 = DRegister('d20')
d21 = DRegister('d21')
d22 = DRegister('d22')
d23 = DRegister('d23')
d24 = DRegister('d24')
d25 = DRegister('d25')
d26 = DRegister('d26')
d27 = DRegister('d27')
d28 = DRegister('d28')
d29 = DRegister('d29')
d30 = DRegister('d30')
d31 = DRegister('d31')


class DRegisterLanes:
    def __init__(self, register):
        if isinstance(register, DRegister):
            self.register = register
        else:
            raise TypeError('Register parameter is not an instance of DRegister')

    def __str__(self):
        return str(self.register) + "[]"


class QRegister(Register):
    name_to_number_map = {'q0': 0x000F0,
                          'q1': 0x010F0,
                          'q2': 0x020F0,
                          'q3': 0x030F0,
                          'q4': 0x040F0,
                          'q5': 0x050F0,
                          'q6': 0x060F0,
                          'q7': 0x070F0,
                          'q8': 0x080F0,
                          'q9': 0x090F0,
                          'q10': 0x0A0F0,
                          'q11': 0x0B0F0,
                          'q12': 0x0C0F0,
                          'q13': 0x0D0F0,
                          'q14': 0x0E0F0,
                          'q15': 0x0F0F0}

    number_to_name_map = {0x000F0: 'q0',
                          0x010F0: 'q1',
                          0x020F0: 'q2',
                          0x030F0: 'q3',
                          0x040F0: 'q4',
                          0x050F0: 'q5',
                          0x060F0: 'q6',
                          0x070F0: 'q7',
                          0x080F0: 'q8',
                          0x090F0: 'q9',
                          0x0A0F0: 'q10',
                          0x0B0F0: 'q11',
                          0x0C0F0: 'q12',
                          0x0D0F0: 'q13',
                          0x0E0F0: 'q14',
                          0x0F0F0: 'q15'}

    def __init__(self, id=None):
        super(QRegister, self).__init__()
        if id is None:
            from peachpy.arm.function import active_function
            self.number = active_function.allocate_q_register()
            self.type = Register.VFPType
            self.size = 16
        elif isinstance(id, int):
            self.number = id
            self.type = Register.VFPType
            self.size = 16
        elif isinstance(id, str):
            if id in QRegister.name_to_number_map:
                self.number = QRegister.name_to_number_map[id]
                self.type = Register.VFPType
                self.size = 16
            else:
                raise ValueError('Unknown register name: {0}'.format(id))
        elif isinstance(id, QRegister):
            self.number = id.number
            self.type = id.type
            self.size = id.size
        else:
            raise TypeError(
                'Register id is neither a name of an architectural Q register, nor an id of a virtual register')

    def get_physical_number(self):
        assert not self.is_virtual
        return {0x000F0: 0,
                0x010F0: 1,
                0x020F0: 2,
                0x030F0: 3,
                0x040F0: 4,
                0x050F0: 5,
                0x060F0: 6,
                0x070F0: 7,
                0x080F0: 8,
                0x090F0: 9,
                0x0A0F0: 10,
                0x0B0F0: 11,
                0x0C0F0: 12,
                0x0D0F0: 13,
                0x0E0F0: 14,
                0x0F0F0: 15}[self.number]

    def is_compatible_bitboard(self, bitboard):
        if self.mask == 0x0F0:
            return bitboard in {0x000000000000000F,
                                0x00000000000000F0,
                                0x0000000000000F00,
                                0x000000000000F000,
                                0x00000000000F0000,
                                0x0000000000F00000,
                                0x000000000F000000,
                                0x00000000F0000000,
                                0x0000000F00000000,
                                0x000000F000000000,
                                0x00000F0000000000,
                                0x0000F00000000000,
                                0x000F000000000000,
                                0x00F0000000000000,
                                0x0F00000000000000,
                                0xF000000000000000}
        else:
            assert False

    @property
    def is_extended(self):
        return self.number >= 0x08000

    def __str__(self):
        if self.is_virtual:
            return 'q-vreg<{0}>'.format((self.number - 0x40000) >> 12)
        else:
            return QRegister.number_to_name_map[self.number]

    @property
    def low_part(self):
        return DRegister((self.number & ~0xFFF) | 0x030)

    @property
    def high_part(self):
        return DRegister((self.number & ~0xFFF) | 0x0C0)


q0 = QRegister('q0')
q1 = QRegister('q1')
q2 = QRegister('q2')
q3 = QRegister('q3')
q4 = QRegister('q4')
q5 = QRegister('q5')
q6 = QRegister('q6')
q7 = QRegister('q7')
q8 = QRegister('q8')
q9 = QRegister('q9')
q10 = QRegister('q10')
q11 = QRegister('q11')
q12 = QRegister('q12')
q13 = QRegister('q13')
q14 = QRegister('q14')
q15 = QRegister('q15')


