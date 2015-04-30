# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class FileType:
    # No file type
    Null = 0
    # Relocatable file
    Object = 1
    # Executable file
    Executable = 2
    # Fixed VM shared library (?)
    FixedVMLibrary = 3
    # Core dump file
    CoreDump = 4
    # Preloaded executable file
    PreloadedExecutable = 5
    # Dynamically bound shared library
    DynamicLibrary = 6
    # Dynamic linker (dyld)
    DynamicLinker = 7
    # Dynamically bound bundle file
    DynamicBundle = 8
    # Shared library stub for build-time linking (no section content)
    DynamicLibraryStub = 9
    # Companion file with debug sections only
    DebugSymbols = 10
    # Kernel-mode driver
    KExtBundle = 11


class MemoryProtection:
    Read = 0x01
    Write = 0x02
    Execute = 0x04
    Default = 0x07


class CpuType:
    X86 = 0x00000007
    X86_64 = 0x01000007
    ARM = 0x0000000C
    ARM64 = 0x0100000C
    PPC = 0x00000012
    PPC64 = 0x01000012

    ABI64 = 0x01000000


class PPCCpuSubType:
    All = 0
    # PowerPC G3
    PowerPC750 = 9
    # PowerPC G4
    PowerPC7400 = 10
    # PowerPC G4+
    PowerPC7450 = 11
    # PowerPC G5
    PowerPC970 = 100


class X86CpuSubType:
    All = 3


class ARMCpuSubType:
    All = 0
    # ARM 1176
    V6 = 6
    # ARM Cortex-A8
    V7 = 9
    # Cortex-A9 (ARMv7 + MP extension + NEON-HP, de-facto useless, removed from Clang)
    V7F = 10
    # Swift (ARMv7 + MP extension + VFPv4/NEONv2 + DIV)
    V7S = 11
    # Marvell Kirkwood (ARMv7 + XScale extension + WMMXv2 + Armada extension, no NEON)
    V7K = 12
    # Cyclone
    V8 = 13


class ARM64CpuSubType:
    All = 0
    # Cyclone
    V8 = 1


class MachHeader:
    def __init__(self, abi):
        import peachpy.x86_64
        import peachpy.arm

        self.abi = abi
        self.size = {4: 28, 8: 32}[abi.pointer_size]
        if abi == peachpy.x86_64.abi.system_v_x86_64_abi:
            # 64-bit
            self.magic = 0xFEEDFACF
            self.cpu_type = CpuType.X86_64
            self.cpu_subtype = X86CpuSubType.All
        else:
            raise ValueError("Unsupported ABI: %s" % str(abi))
        self.file_type = FileType.Object
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
                   encoder.uint32(MemoryProtection.Default) + \
                   encoder.uint32(MemoryProtection.Default) + \
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
                   encoder.uint32(MemoryProtection.Default) + \
                   encoder.uint32(MemoryProtection.Default) + \
                   encoder.uint32(self.section_count) + \
                   encoder.uint32(self.flags)


