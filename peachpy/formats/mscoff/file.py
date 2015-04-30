# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class MachineType:
    # Machine-independent
    Unknown = 0
    # IA32 (x86)
    X86 = 0x14C
    # x86-64 (AMD64, Intel64, x64)
    X86_64 = 0x8664
    # IA64 (Itanium)
    IA64 = 0x200
    # ARM
    ARM = 0x1C0
    # ARMv7 (Thumb mode only)
    ARMNT = 0x1C4
    # ARMv8 AArch64
    ARM64 = 0xAA64
    # EFI bytecode
    EBC = 0xEBC


class FileHeader:
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
        self.characteristics = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)
        return encoder.uint16le(self.abi.mscoff_machine_type) + \
            encoder.uint16le(self.section_count) + \
            encoder.uint32le(self.timestamp or 0) + \
            encoder.uint32le(self.symbol_table_offset or 0) + \
            encoder.uint32le(self.symbol_count) + \
            encoder.uint16le(0) + \
            encoder.uint16le(self.characteristics)


