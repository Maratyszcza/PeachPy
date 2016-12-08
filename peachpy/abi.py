# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Endianness:
    Big, Little = "Big-Endian", "Little-Endian"


class ABI(object):
    def __init__(self, name, endianness,
                 bool_size, wchar_size, short_size, int_size, long_size, longlong_size,
                 pointer_size, index_size,
                 stack_alignment, red_zone,
                 callee_save_registers, argument_registers, volatile_registers, restricted_registers=[],
                 elf_class=None, elf_data_encoding=None, elf_machine_type=None,
                 mscoff_machine_type=None):
        super(ABI, self).__init__()
        self.name = name
        self.endianness = endianness
        self.bool_size = bool_size
        self.wchar_size = wchar_size
        self.short_size = short_size
        self.int_size = int_size
        self.long_size = long_size
        self.longlong_size = longlong_size
        self.pointer_size = pointer_size
        self.index_size = index_size
        self.stack_alignment = stack_alignment
        self.red_zone = red_zone
        self.callee_save_registers = callee_save_registers
        self.argument_registers = argument_registers
        self.volatile_registers = volatile_registers
        self.restricted_registers = restricted_registers
        self.elf_class = elf_class
        self.elf_data_encoding = elf_data_encoding
        self.elf_machine_type = elf_machine_type
        self.mscoff_machine_type = mscoff_machine_type

    def __eq__(self, other):
        return isinstance(other, ABI) and self.name == other.name

    def __ne__(self, other):
        return not isinstance(other, ABI) or self.name != other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def is_elf_compatible(self):
        return self.elf_class is not None and self.elf_data_encoding is not None and self.elf_machine_type is not None

    @property
    def is_mscoff_compatible(self):
        return self.mscoff_machine_type is not None

    @property
    def is_macho_compatible(self):
        return False

    @property
    def elf_bitness(self):
        if self.elf_class is not None:
            from peachpy.formats.elf.file import ElfClass
            return {ElfClass.class32: 32, ElfClass.class64: 64}[self.elf_class]
