# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class FileType(IntEnum):
    # No file type
    null = 0
    # Relocatable file
    object = 1
    # Executable file
    executable = 2
    # Fixed VM shared library (?)
    fixed_vm_library = 3
    # Core dump file
    core_dump = 4
    # Preloaded executable file
    preloaded_executable = 5
    # Dynamically bound shared library
    dynamic_library = 6
    # Dynamic linker (dyld)
    dynamic_linker = 7
    # Dynamically bound bundle file
    dynamic_bundle = 8
    # Shared library stub for build-time linking (no section content)
    dynamic_library_stub = 9
    # Companion file with debug sections only
    debug_symbols = 10
    # Kernel-mode driver
    kext_bundle = 11


class MemoryProtection(IntEnum):
    read = 0x01
    write = 0x02
    execute = 0x04
    default = 0x07


class CpuType(IntEnum):
    x86 = 0x00000007
    x86_64 = 0x01000007
    arm = 0x0000000C
    arm64 = 0x0100000C
    ppc = 0x00000012
    ppc64 = 0x01000012

    abi64 = 0x01000000


class PPCCpuSubType(IntEnum):
    all = 0
    # PowerPC G3
    powerpc750 = 9
    # PowerPC G4
    powerpc7400 = 10
    # PowerPC G4+
    powerpc7450 = 11
    # PowerPC G5
    powerpc970 = 100


class X86CpuSubType(IntEnum):
    all = 3


class ARMCpuSubType(IntEnum):
    all = 0
    # ARM 1176
    v6 = 6
    # ARM Cortex-A8
    v7 = 9
    # Cortex-A9 (ARMv7 + MP extension + NEON-HP, de-facto useless, removed from Clang)
    v7f = 10
    # Swift (ARMv7 + MP extension + VFPv4/NEONv2 + DIV)
    v7s = 11
    # Marvell Kirkwood (ARMv7 + XScale extension + WMMXv2 + Armada extension, no NEON)
    v7k = 12
    # Cyclone
    v8 = 13


class ARM64CpuSubType(IntEnum):
    all = 0
    # Cyclone
    v8 = 1


class MachHeader:
    def __init__(self, abi):
        import peachpy.x86_64
        import peachpy.arm

        self.abi = abi
        self.size = {4: 28, 8: 32}[abi.pointer_size]
        if abi == peachpy.x86_64.abi.system_v_x86_64_abi:
            # 64-bit
            self.magic = 0xFEEDFACF
            self.cpu_type = CpuType.x86_64
            self.cpu_subtype = X86CpuSubType.all
        else:
            raise ValueError("Unsupported ABI: %s" % str(abi))
        self.file_type = FileType.object
        self.command_count = 0
        self.command_size = 0
        self.flags = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder

        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        bytes = encoder.uint32(self.magic) + \
                encoder.uint32(self.cpu_type) + \
                encoder.uint32(self.cpu_subtype) + \
                encoder.uint32(self.file_type) + \
                encoder.uint32(self.command_count) + \
                encoder.uint32(self.command_size) + \
                encoder.uint32(self.flags)
        if self.abi.pointer_size == 8:
            bytes += bytearray(4)
        return bytes


class LoadCommand(object):
    def __init__(self, abi, id, size):
        super(LoadCommand, self).__init__()
        self.abi = abi
        self.id = id
        self.size = size

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        return encoder.uint32(self.id) + encoder.uint32(self.size)


class SymbolTableCommand(LoadCommand):
    def __init__(self, abi):
        super(SymbolTableCommand, self).__init__(abi, id=0x2, size=24)
        self.symbol_offset = None
        self.symbol_count = 0
        self.string_offset = None
        self.string_size = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        return encoder.uint32(self.id) + \
            encoder.uint32(self.size) + \
            encoder.uint32(self.symbol_offset or 0) + \
            encoder.uint32(self.symbol_count) + \
            encoder.uint32(self.string_offset or 0) + \
            encoder.uint32(self.string_size)


class SegmentCommand(LoadCommand):
    def __init__(self, abi):
        super(SegmentCommand, self).__init__(abi,
                                             id={4: 0x1, 8: 0x19}[abi.pointer_size],
                                             size={4: 56, 8: 72}[abi.pointer_size])
        self.name = None
        self.address = None
        self.memory_size = 0
        self.offset = None
        self.file_size = 0
        self.section_count = 0
        self.flags = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        if self.abi.pointer_size == 4:
            return encoder.uint32(self.id) + \
                   encoder.uint32(self.size) + \
                   encoder.fixed_string(self.name, 16) + \
                   encoder.uint32(self.address or 0) + \
                   encoder.uint32(self.memory_size) + \
                   encoder.uint32(self.offset) + \
                   encoder.uint32(self.file_size) + \
                   encoder.uint32(MemoryProtection.default) + \
                   encoder.uint32(MemoryProtection.default) + \
                   encoder.uint32(self.section_count) + \
                   encoder.uint32(self.flags)
        else:
            return encoder.uint32(self.id) + \
                   encoder.uint32(self.size) + \
                   encoder.fixed_string(self.name, 16) + \
                   encoder.uint64(self.address or 0) + \
                   encoder.uint64(self.memory_size) + \
                   encoder.uint64(self.offset) + \
                   encoder.uint64(self.file_size) + \
                   encoder.uint32(MemoryProtection.default) + \
                   encoder.uint32(MemoryProtection.default) + \
                   encoder.uint32(self.section_count) + \
                   encoder.uint32(self.flags)


