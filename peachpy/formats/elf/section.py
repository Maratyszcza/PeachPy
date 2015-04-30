# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import codecs

from peachpy.formats.elf.file import ElfClass


class SectionFlags:
    # Section contains writable data during process execution
    Writable = 0x1
    # Section occupies memory during process execution
    Allocate = 0x2
    # Section contains executable data machine instructions
    Executable = 0x4


class SectionType:
    # Nil section
    Null = 0
    # Program-specific content
    ProgramBits = 1
    # Symbol table
    SymbolTable = 2
    # String table
    StringTable = 3
    # Relocations with explicit addend
    AddendRelocations = 4
    # Hash table for symbols used in dynamic linking
    SymbolHashTable = 5
    # Information for dynamic linking
    DynamicLinkingInfo = 6
    # Free-form note
    Note = 7
    # Program-specific zero-initialized content
    NoBits = 8
    # Relocations without explicit addends
    Relocations = 9
    # Minimal symbol table for dynamic linking
    DynamicSymbolTable = 11


class SectionIndex:
    Absolute = 0xFFF1
    Common = 0xFFF2
    Undefined = 0x0000


class SectionHeader:
    def __init__(self, abi):
        self.size = {ElfClass.Class32: 40, ElfClass.Class64: 64}[abi.elf_class]
        self.abi = abi

        # Section name, specified as the index into the section header string table section.
        self.name_index = None
        # Interpretation of the section content
        self.content_type = None
        # Properties of section content
        self.flags = 0
        # Load address for section data. 0 if section does not need to be loaded.
        self.address = None
        # Offset in the ELF file to the start of section. 0 if section data occupies no space in the file.
        self.offset = None
        # Size of section data in the file.
        self.content_size = 0
        # Section header table index link.
        self.link_index = None
        # Extra information with section type-dependent interpretation.
        self.info = None
        # Section address alignment. Only powers of 2 are allowed. Value 0 or 1 mean no alignment restrictions.
        self.address_alignment = 1
        # Size of fixed-length entries in the section (e.g. string table entries).
        # 0 if section contains no such entries.
        self.entry_size = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)
        if self.abi.elf_class == ElfClass.Class32:
            return encoder.uint32(self.name_index) + \
                encoder.uint32(self.content_type) + \
                encoder.uint32(self.flags) + \
                encoder.uint32(self.address or 0) + \
                encoder.uint32(self.offset or 0) + \
                encoder.uint32(self.content_size) + \
                encoder.uint32(self.link_index) + \
                encoder.uint32(self.info) + \
                encoder.uint32(self.address_alignment) + \
                encoder.uint32(self.entry_size)
        else:
            return encoder.uint32(self.name_index) + \
                encoder.uint32(self.content_type) + \
                encoder.uint64(self.flags) + \
                encoder.uint64(self.address or 0) + \
                encoder.uint64(self.offset or 0) + \
                encoder.uint64(self.content_size) + \
                encoder.uint32(self.link_index or 0) + \
                encoder.uint32(self.info) + \
                encoder.uint64(self.address_alignment) + \
                encoder.uint64(self.entry_size)


class Section(object):
    def __init__(self, abi):
        super(Section, self).__init__()
        self.abi = abi
        self.header = SectionHeader(abi)
        self.index = None
        self._content = bytearray()

    @property
    def content(self):
        return self._content


class ProgramBitsSection(Section):
    def __init__(self, abi, writable=False, executable=False, allocate=False):
        super(ProgramBitsSection, self).__init__(abi)
        self.header.content_type = SectionType.ProgramBits
        self.header.link_index = SectionIndex.Undefined
        self.header.info = 0
        self.header.flags = 0
        if writable:
            self.header.flags |= SectionFlags.Writable
        if executable:
            self.header.flags |= SectionFlags.Executable
        if allocate:
            self.header.flags |= SectionFlags.Allocate
        self.header.content_size = 0

    def append(self, bytes):
        self.header.content_size += len(bytes)
        self._content += bytes


class TextSection(ProgramBitsSection):
    def __init__(self, abi):
        super(TextSection, self).__init__(abi, executable=True, allocate=True)


class DataSection(ProgramBitsSection):
    def __init__(self, abi):
        super(DataSection, self).__init__(abi, writable=True, allocate=True)


class StringSection(Section):
    def __init__(self, abi):
        super(StringSection, self).__init__(abi)
        self.header.content_type = SectionType.StringTable
        self.header.link_index = SectionIndex.Undefined
        self.header.info = 0
        self.header.address_alignment = 0
        self.header.entry_size = 0
        self._strings = dict()

    @property
    def content(self):
        if self.header.content_size != 0:
            bytes = b"\x00"
            for string in sorted(self._strings, key=self._strings.get):
                bytes += codecs.encode(string, "utf8") + b"\x00"
            return bytes
        else:
            return bytearray()

    def add(self, string):
        if string in self._strings:
            return self._strings[string]
        else:
            content_size = self.header.content_size
            if content_size == 0:
                content_size = 1
            string_index = content_size
            self._strings[string] = string_index
            string_bytes = codecs.encode(string, "utf-8")
            content_size += len(string_bytes) + 1
            self.header.content_size = content_size
            return string_index


class SymbolSection(Section):
    def __init__(self, abi):
        super(SymbolSection, self).__init__(abi)
        self.header.entry_size = {ElfClass.Class32: 16, ElfClass.Class64: 24}[abi.elf_class]
        self.header.content_type = SectionType.SymbolTable
        self.header.flags = 0
        self.header.info = 0
        self.header.address_alignment = abi.pointer_size
        self._symbols = []

    @property
    def content(self):
        from peachpy.formats.elf.symbol import SymbolBinding
        data = bytearray()
        # First all local symbols
        for symbol in self._symbols:
            if symbol.binding == SymbolBinding.Local:
                data += symbol.as_bytearray
        # Then all global symbols
        for symbol in self._symbols:
            if symbol.binding != SymbolBinding.Local:
                data += symbol.as_bytearray
        return data

    def add(self, symbol):
        from peachpy.formats.elf.symbol import SymbolBinding
        self.header.content_size += len(symbol.as_bytearray)
        self._symbols.append(symbol)
        if symbol.binding == SymbolBinding.Local:
            self.header.info += 1

    def bind(self):
        from peachpy.formats.elf.symbol import SymbolBinding
        index = 0
        for symbol in self._symbols:
            if symbol.binding == SymbolBinding.Local:
                symbol.index = index
                index += 1
        for symbol in self._symbols:
            if symbol.binding != SymbolBinding.Local:
                symbol.index = index
                index += 1


class NullSection(Section):
    def __init__(self, abi):
        super(NullSection, self).__init__(abi)
        self.header.name_index = 0
        self.header.content_type = SectionType.Null
        self.header.flags = 0
        self.header.address = 0
        self.header.offset = 0
        self.header.content_size = 0
        self.header.link_index = SectionIndex.Undefined
        self.header.info = 0
        self.header.address_alignment = 0
        self.header.entry_size = 0
