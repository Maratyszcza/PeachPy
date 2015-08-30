# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class MachineType(IntEnum):
    # Machine-independent
    unknown = 0
    # IA32 (x86)
    x86 = 0x14C
    # x86-64 (AMD64, Intel64, x64)
    x86_64 = 0x8664
    # IA64 (Itanium)
    ia64 = 0x200
    # ARM
    arm = 0x1C0
    # ARMv7 (Thumb mode only)
    armnt = 0x1C4
    # ARMv8 AArch64
    arm64 = 0xAA64
    # EFI bytecode
    efi_bytecode = 0xEBC


class FileHeader:
    size = 20

    def __init__(self, abi):
        import peachpy.formats.elf.section
        import peachpy.abi
        if not isinstance(abi, peachpy.abi.ABI):
            raise TypeError("ABI %s must be represented by an ABI object" % str(abi))
        if not abi.is_mscoff_compatible:
            raise ValueError("ABI %s is not compatible with MS COFF" % str(abi))
        self.abi = abi
        self.section_count = 0
        self.timestamp = None
        self.symbol_table_offset = None
        self.symbol_count = 0
        self.flags = 0

    @property
    def as_bytearray(self):
        from peachpy.encoder import Encoder
        return Encoder.uint16le(self.abi.mscoff_machine_type) + \
            Encoder.uint16le(self.section_count) + \
            Encoder.uint32le(self.timestamp or 0) + \
            Encoder.uint32le(self.symbol_table_offset or 0) + \
            Encoder.uint32le(self.symbol_count) + \
            Encoder.uint16le(0) + \
            Encoder.uint16le(self.flags)


