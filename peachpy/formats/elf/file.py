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
    # Shared object file
    dynamic_shared_object = 3
    # Core dump file
    core_dump = 4


class MachineType(IntEnum):
    # Not specified
    unspecified = 0
    # SPARC
    sparc = 2
    # IA32 (x86)
    x86 = 3
    # MIPS
    mips = 8
    # 32-bit subset of SPARC V9
    sparc32plus = 18
    # IBM POWER and PowerPC
    ppc = 20
    # IBM PowerPC 64
    ppc64 = 21
    # ARM
    arm = 40
    # SPARC V9 (64-bit)
    sparc64 = 43
    # IA64 (Itanium)
    ia64 = 50
    # x86-64 (AMD64, Intel64, x64)
    x86_64 = 62
    # Intel Knights Ferry
    l1om = 180
    # Intel Knights Corner
    k1om = 181
    # ARMv8 AArch64
    arm64 = 183
    # ATI/AMD GPU code (for any GPU arch)
    cal = 125
    # nVidia CUDA GPU code (for any GPU arch)
    cuda = 190
    # HSAIL code (32-bit ELF)
    hsail32 = 0xAF5A
    # HSAIL code (64-bit ELF)
    hsail64 = 0xAF5B


class FormatVersion(IntEnum):
    # Invalid version
    invalid = 0
    # Current version
    current = 1


class ElfClass(IntEnum):
    # Invalid class
    invalid = 0
    # 32-bit ELF
    class32 = 1
    # 64-bit ELF
    class64 = 2


class DataEncoding(IntEnum):
    # Invalid data encoding
    invalid = 0
    # Least significant byte first (Little-Endian)
    little_endian = 1
    # Most significant byte first (Big-Endian)
    big_endian = 2


class OSABI(IntEnum):
    # No extensions or unspecified
    none = 0
    # GNU Linux
    gnu = 3
    # FreeBSD
    freebsd = 9
    # ATI/AMD GPU ABI
    cal = 100


class FileIdentification:
    def __init__(self, abi):
        self.abi = abi
        self.file_version = FormatVersion.current

    @property
    def as_bytearray(self):
        identification = bytearray(16)
        identification[0] = 0x7F
        identification[1] = ord('E')
        identification[2] = ord('L')
        identification[3] = ord('F')
        identification[4] = self.abi.elf_class
        identification[5] = self.abi.elf_data_encoding
        identification[6] = self.file_version
        return identification


class FileHeader:
    def __init__(self, abi):
        import peachpy.formats.elf.section
        import peachpy.abi
        if not isinstance(abi, peachpy.abi.ABI):
            raise TypeError("ABI %s must be represented by an ABI object" % str(abi))
        if not abi.is_elf_compatible:
            raise ValueError("ABI %s is not compatible with ELF" % str(abi))
        self.abi = abi

        self.identification = FileIdentification(self.abi)
        if self.abi.elf_class == ElfClass.class32:
            # Size of ELF32 file header, in bytes
            self.file_header_size = 52
            # Size of program header, in bytes. All program headers have the same size.
            self.program_header_entry_size = 32
            # Size of a section header, in bytes. All sections have the same size.
            self.section_header_entry_size = 40
        else:
            # Size of ELF64 file header, in bytes
            self.file_header_size = 64
            # Size of program header, in bytes. All program headers have the same size.
            self.program_header_entry_size = 56
            # Size of a section header, in bytes. All sections have the same size.
            self.section_header_entry_size = 64

        self.size = self.file_header_size
        self.file_type = FileType.object
        self.file_version = FormatVersion.current
        self.entry_address = None
        self.program_header_table_offset = None
        self.section_header_table_offset = None
        self.flags = 0
        # Number of program headers in the program header table.
        self.program_header_entries_count = 0
        # Number of section headers in the section header table.
        self.section_header_entries_count = 0
        # Index of the section header for a section which contains section name string table.
        # Usually this section is called ".shstrtab"
        self.section_name_string_table_index = peachpy.formats.elf.section.SectionIndex.undefined

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness, self.abi.elf_bitness)

        return self.identification.as_bytearray + \
            encoder.uint16(self.file_type) + \
            encoder.uint16(self.abi.elf_machine_type) + \
            encoder.uint32(self.file_version) + \
            encoder.unsigned_offset(self.entry_address or 0) + \
            encoder.unsigned_offset(self.program_header_table_offset or 0) + \
            encoder.unsigned_offset(self.section_header_table_offset or 0) + \
            encoder.uint32(self.flags) + \
            encoder.uint16(self.file_header_size) + \
            encoder.uint16(self.program_header_entry_size) + \
            encoder.uint16(self.program_header_entries_count) + \
            encoder.uint16(self.section_header_entry_size) + \
            encoder.uint16(self.section_header_entries_count) + \
            encoder.uint16(self.section_name_string_table_index)
