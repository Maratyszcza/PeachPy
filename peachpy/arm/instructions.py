# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

class QuasiInstruction(object):
    def __init__(self, name, origin=None):
        super(QuasiInstruction, self).__init__()
        self.name = name
        self.line_number = origin[1][2] if origin else None
        self.source_file = origin[1][1] if origin else None
        self.source_code = origin[1][4][0].strip() if origin else None


class Instruction(QuasiInstruction):
    def __init__(self, name, operands, isa_extensions=None, origin=None):
        import peachpy.x86_64.isa
        super(Instruction, self).__init__(name, origin=origin)
        self.operands = operands
        self.isa_extensions = peachpy.x86_64.isa.Extensions(isa_extensions)
        self.available_registers = set()
        self.live_registers = set()

    def __len__(self):
        return self.size

    def __str__(self):
        return self.name + " " + ", ".join(map(str, self.operands))

    def get_registers_list(self):
        return [register for operand in self.operands for register in operand.get_registers_list()]

    def get_local_variable(self):
        for operand in self.operands:
            if isinstance(operand, Operand) and operand.is_local_variable():
                return operand.variable

    def get_constant(self):
        for operand in self.operands:
            if isinstance(operand, Operand) and operand.is_constant():
                return operand.constant


class Operand(object):
    RegisterType = 1
    RegisterListType = 2
    RegisterLanesType = 3
    RegisterLanesListType = 4
    ShiftedRegisterType = 5
    AddressRegisterType = 6
    ImmediateType = 7
    MemoryType = 8
    ConstantType = 9
    VariableType = 10
    LabelType = 11
    NoneType = 12

    def __init__(self, operand):
        super(Operand, self).__init__()
        import copy
        from peachpy import Constant
        from peachpy.arm.registers import Register, GeneralPurposeRegister, \
            GeneralPurposeRegisterWriteback, ShiftedGeneralPurposeRegister, DRegisterLanes
        from peachpy.arm.function import LocalVariable
        from peachpy.arm.pseudo import Label
        from peachpy.util import is_int

        if isinstance(operand, GeneralPurposeRegisterWriteback):
            self.type = Operand.AddressRegisterType
            self.register = copy.deepcopy(operand.register)
        elif isinstance(operand, Register):
            self.type = Operand.RegisterType
            self.register = copy.deepcopy(operand)
        elif isinstance(operand, DRegisterLanes):
            self.type = Operand.RegisterLanesType
            self.lanes = copy.deepcopy(operand)
        elif isinstance(operand, ShiftedGeneralPurposeRegister):
            self.type = Operand.ShiftedRegisterType
            self.register = copy.deepcopy(operand)
        elif isinstance(operand, tuple):
            if all(isinstance(element, Register) for element in operand):
                if len(set((register.type, register.size) for register in operand)) == 1:
                    self.type = Operand.RegisterListType
                    self.register_list = copy.deepcopy(operand)
                else:
                    raise TypeError('Register in the list {0} have different types'.format(", ".join(operand)))
            elif all(isinstance(element, DRegisterLanes) for element in operand):
                self.type = Operand.RegisterLanesListType
                self.register_list = copy.deepcopy(operand)
            else:
                raise TypeError('Unknown tuple elements {0}'.format(operand))
        elif is_int(operand):
            if -9223372036854775808 <= operand <= 18446744073709551615:
                self.type = Operand.ImmediateType
                self.immediate = operand
            else:
                raise ValueError('The immediate operand {0} is not a 64-bit value'.format(operand))
        elif isinstance(operand, list):
            if len(operand) == 1 and (isinstance(operand[0], GeneralPurposeRegister) or isinstance(operand[0],
                                                                                                   GeneralPurposeRegisterWriteback)):
                self.type = Operand.MemoryType
                self.base = copy.deepcopy(operand[0])
                self.offset = None
            elif len(operand) == 2 and isinstance(operand[0], GeneralPurposeRegister) and (
                isinstance(operand[1], int) or isinstance(operand[1], ShiftedGeneralPurposeRegister)):
                self.type = Operand.MemoryType
                self.base = copy.deepcopy(operand[0])
                self.offset = operand[1]
            else:
                raise ValueError('Memory operand must be a list with only one or two elements')
        elif isinstance(operand, Constant):
            self.type = Operand.ConstantType
            self.constant = operand
            self.size = operand.size * operand.repeats
        elif isinstance(operand, LocalVariable):
            self.type = Operand.VariableType
            self.variable = operand
            self.size = operand.size * 8
        elif isinstance(operand, str):
            self.type = Operand.LabelType
            self.label = operand
        elif isinstance(operand, Label):
            self.type = Operand.LabelType
            self.label = operand.name
        elif operand is None:
            self.type = Operand.NoneType
        else:
            raise TypeError('The operand {0} is not a valid assembly instruction operand'.format(operand))

    def __str__(self):
        if self.is_constant():
            if self.constant.prefix is None:
                return "[rel {0}]".format(self.constant.label)
            else:
                return "[rel {1}.{0}]".format(self.constant.label, self.constant.prefix)
        elif self.is_local_variable():
            return str(self.variable)
        elif self.is_memory_address():
            from peachpy.arm.registers import GeneralPurposeRegisterWriteback
            if self.offset is None:
                if isinstance(self.base, GeneralPurposeRegisterWriteback):
                    return "[" + str(self.base.register) + "]!"
                else:
                    return "[" + str(self.base) + "]"
            else:
                if isinstance(self.base, GeneralPurposeRegisterWriteback):
                    return "[" + str(self.base.register) + ", #" + str(self.offset) + "]!"
                else:
                    if isinstance(self.offset, int):
                        return "[" + str(self.base) + ", #" + str(self.offset) + "]"
                    else:
                        return "[" + str(self.base) + ", " + str(self.offset) + "]"
        elif self.is_register() or self.is_shifted_general_purpose_register():
            return str(self.register)
        elif self.is_register_lanes():
            return str(self.register)
        elif self.is_address_register():
            return str(self.register) + "!"
        elif self.is_register_list() or self.is_register_lanes_list():
            return "{" + ", ".join(map(str, self.register_list)) + "}"
        elif self.is_label():
            return self.label
        elif self.is_immediate():
            return "#" + str(self.immediate)
        elif self.is_none():
            return ""
        else:
            raise TypeError('Unsupported operand type')

    def __eq__(self, other):
        if isinstance(other, Operand) and self.type == other.type:
            if self.is_immediate():
                return self.immediate == other.immediate
            elif self.is_register():
                return self.register == other.register
            elif self.is_memory_address():
                return self.base == other.base and self.offset == other.offset
            elif self.is_label():
                return self.label == other.label
            else:
                return False
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def is_none(self):
        return self.type == Operand.NoneType

    def is_immediate(self):
        return self.type == Operand.ImmediateType

    def is_immediate5(self):
        return self.is_immediate and 0 <= self.immediate <= 31

    def is_modified_immediate12(self):
        def rotate32(x, n):
            return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

        if self.type == Operand.ImmediateType:
            if -2147483648 <= self.immediate <= 4294967295:
                dword = self.immediate & 0xFFFFFFFF
                ndword = (~self.immediate) & 0xFFFFFFFF
                return any(
                    [(rotate32(dword, n) & 0xFFFFFF00) == 0x00000000 or (rotate32(ndword, n) & 0xFFFFFF00) == 0x00000000
                     for n in range(0, 32, 2)])
            else:
                return False
        else:
            return False

    def is_neon_modified_immediate8(self):
        return self.type == Operand.ImmediateType and -128 <= self.immediate <= 255

    def is_neon_modified_immediate16(self):
        if self.type == Operand.ImmediateType and -32768 <= self.immediate <= 65535:
            hword = self.immediate & 0xFFFF
            return (hword & 0xFF00) == 0 or (hword & 0x00FF) == 0
        else:
            return False

    def is_neon_modified_immediate32(self):
        if self.type == Operand.ImmediateType and -2147483648 <= self.immediate <= 4294967295:
            word = self.immediate & 0xFFFFFFFF
            return (word & 0x00FFFFFF) == 0x00000000 or \
                   (word & 0xFF00FFFF) == 0x00000000 or \
                   (word & 0xFFFF00FF) == 0x00000000 or \
                   (word & 0xFFFFFF00) == 0x00000000 or \
                   (word & 0xFF00FFFF) == 0x0000FFFF or \
                   (word & 0xFFFF00FF) == 0x000000FF
        else:
            return False

    def is_neon_modified_immediate64(self):
        if self.type == Operand.ImmediateType and -2147483648 <= self.immediate <= 4294967295:
            dword = self.immediate & 0xFFFFFFFFFFFFFFFF
            byte = dword & 0xFF
            return all([(dword >> n) & 0xFF == byte for n in range(8, 64, 8)])
        else:
            return False

    def is_preindexed_memory_address(self):
        from peachpy.arm.registers import GeneralPurposeRegisterWriteback
        return self.type == Operand.MemoryType and \
            self.offset is not None and \
            isinstance(self.base, GeneralPurposeRegisterWriteback)

    def is_memory_address(self, offset_bits=None, allow_writeback=True):
        from peachpy.arm.registers import GeneralPurposeRegisterWriteback, ShiftedGeneralPurposeRegister
        if self.type == Operand.MemoryType:
            if not allow_writeback and isinstance(self.base, GeneralPurposeRegisterWriteback):
                return False
            else:
                if self.offset is None or offset_bits is None:
                    return True
                elif isinstance(self.offset, ShiftedGeneralPurposeRegister):
                    return True
                else:
                    bound = (1 << offset_bits) - 1
                    return -bound <= self.offset <= bound
        else:
            return False

    def is_writeback_memory_address(self):
        from peachpy.arm.registers import GeneralPurposeRegisterWriteback
        return self.type == Operand.MemoryType and isinstance(self.base, GeneralPurposeRegisterWriteback)

    def is_memory_address_offset8_mod4(self):
        return self.type == Operand.MemoryType and \
            (self.offset is None or -1020 <= self.offset <= 1020 and self.offset % 4 == 0)

    def is_offset8(self):
        return self.type == Operand.ImmediateType and -255 <= self.immediate <= 255

    def is_offset12(self):
        return self.type == Operand.ImmediateType and -4095 <= self.immediate <= 4095

    def is_label(self):
        return self.type == Operand.LabelType

    def is_constant(self):
        return self.type == Operand.ConstantType

    def is_local_variable(self):
        return self.type == Operand.VariableType

    def is_register(self):
        return self.type == Operand.RegisterType

    def is_register_lanes(self):
        return self.type == Operand.RegisterLanesType

    def is_register_list(self):
        return self.is_register() or self.type == Operand.RegisterListType

    def is_register_lanes_list(self):
        return self.type == Operand.RegisterLanesListType

    def is_general_purpose_register(self):
        from peachpy.arm.registers import GeneralPurposeRegister
        return self.type == Operand.RegisterType and \
            isinstance(self.register, GeneralPurposeRegister)

    def is_shifted_general_purpose_register(self):
        from peachpy.arm.registers import ShiftedGeneralPurposeRegister
        return self.is_general_purpose_register() or self.type == Operand.ShiftedRegisterType and \
            isinstance(self.register, ShiftedGeneralPurposeRegister)

    def is_general_purpose_register_list(self):
        from peachpy.arm.registers import GeneralPurposeRegister
        return self.is_general_purpose_register() or self.type == Operand.RegisterListType and \
            isinstance(self.register_list[0], GeneralPurposeRegister)

    def is_address_register(self):
        return self.is_general_purpose_register() or self.type == Operand.AddressRegisterType

    def is_wmmx_register(self):
        from peachpy.arm.registers import WMMXRegister
        return self.type == Operand.RegisterType and isinstance(self.register, WMMXRegister)

    def is_s_register(self):
        from peachpy.arm.registers import SRegister
        return self.type == Operand.RegisterType and isinstance(self.register, SRegister)

    def is_s_register_list(self):
        from peachpy.arm.registers import SRegister
        return self.is_s_register() or \
               self.type == Operand.RegisterListType and isinstance(self.register_list[0], SRegister)

    def is_d_register(self):
        from peachpy.arm.registers import DRegister
        return self.type == Operand.RegisterType and isinstance(self.register, DRegister)

    def is_d_register_list(self):
        from peachpy.arm.registers import DRegister
        return self.is_d_register() or \
               self.type == Operand.RegisterListType and isinstance(self.register_list[0], DRegister)

    def is_q_register(self):
        from peachpy.arm.registers import QRegister
        return self.type == Operand.RegisterType and isinstance(self.register, QRegister)

    def is_vldst1_register_list(self):
        from peachpy.arm.registers import DRegister
        return self.is_d_register() or \
            self.type == Operand.RegisterListType and \
            isinstance(self.register_list[0], DRegister) and \
            len(self.register_list) <= 4

    def is_vldst1_register_lanes_list(self):
        from peachpy.arm.registers import DRegisterLanes
        return self.type == Operand.RegisterLanesType and \
               isinstance(self.register, DRegisterLanes) or \
               self.type == Operand.RegisterLanesListType and \
               all(isinstance(register, DRegisterLanes) for register in self.register_list)

    def is_general_purpose_memory_address(self):
        return self.type == Operand.MemoryType and -4095 <= self.offset <= 4095

    def get_registers_list(self):
        from peachpy.arm.registers import sp, GeneralPurposeRegisterWriteback, ShiftedGeneralPurposeRegister
        if self.is_address_register() or self.is_register() or self.is_register_lanes():
            return [self.register]
        elif self.is_shifted_general_purpose_register():
            return [self.register.register]
        elif self.is_constant():
            return list()
        elif self.is_local_variable():
            return [sp]
        elif self.is_register_list():
            return list(self.register_list)
        elif self.is_register_lanes_list():
            return [register_lanes.register for register_lanes in self.register_list]
        elif self.is_memory_address():
            if isinstance(self.base, GeneralPurposeRegisterWriteback):
                return [self.base.register]
            else:
                if isinstance(self.offset, ShiftedGeneralPurposeRegister):
                    return [self.base, self.offset.register]
                else:
                    return [self.base]
        else:
            return list()

    def get_writeback_registers_list(self):
        if self.is_memory_address():
            from peachpy.arm.registers import GeneralPurposeRegisterWriteback
            if isinstance(self.base, GeneralPurposeRegisterWriteback):
                return [self.base.register]
            else:
                return [self.base]
        else:
            return list()


