# This file is part of PeachPy package and is licensed under the Simplified BSD license.
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
        self.commands_count = 0
        self.commands_size = 0
        self.flags = 0

    @staticmethod
    def get_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.pointer_size in [4, 8]

        return {4: 24, 8: 32}[abi.pointer_size]

    def encode(self, encoder):
        bytes = encoder.uint32(self.magic) + \
            encoder.uint32(self.cpu_type) + \
            encoder.uint32(self.cpu_subtype) + \
            encoder.uint32(self.file_type) + \
            encoder.uint32(self.commands_count) + \
            encoder.uint32(self.commands_size) + \
            encoder.uint32(self.flags)
        if self.abi.pointer_size == 8:
            bytes += bytearray(4)
        return bytes
