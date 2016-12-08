# This file is part of PeachPy package and is licensed under the Simplified BSD license.
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


class Image:
    file_header_size = 20

    def __init__(self, abi, source=None):
        from peachpy.formats.mscoff.section import StringTable
        self.abi = abi
        self.sections = list()
        self.symbols = list()
        self.string_table = StringTable()

    def add_section(self, section):
        from peachpy.formats.mscoff.section import Section
        assert isinstance(section, Section)

        self.sections.append(section)

    def add_symbol(self, symbol):
        from peachpy.formats.mscoff.symbol import Symbol
        assert isinstance(symbol, Symbol)

        self.symbols.append(symbol)

    def encode(self):
        from peachpy.encoder import Encoder
        encoder = Encoder(self.abi.endianness)

        # Collect names that need to be encoded in the string table
        import codecs
        for section in self.sections:
            if len(codecs.encode(section.name, "utf8")) > 8:
                self.string_table.add(section.name)
        for symbol in self.symbols:
            if len(codecs.encode(symbol.name, "utf8")) > 8:
                self.string_table.add(symbol.name)

        # Layout sections offsets
        from peachpy.formats.mscoff.section import Section

        section_offset_map = dict()
        symbol_table_offset = Image.file_header_size + len(self.sections) * Section.header_size
        data_offset = symbol_table_offset + self.string_table.size
        for symbol in self.symbols:
            data_offset += symbol.entry_size
        for section in self.sections:
            section_offset_map[section] = data_offset
            data_offset += section.content_size

        # Layout section relocations
        from peachpy.formats.mscoff.symbol import Relocation

        section_relocations_map = dict()
        for section in self.sections:
            if section.relocations:
                section_relocations_map[section] = data_offset
                data_offset += Relocation.entry_size * len(section.relocations)

        section_index_map = {section: index + 1 for index, section in enumerate(self.sections)}
        symbol_index_map = {symbol: index for index, symbol in enumerate(self.symbols)}

        # Write file header
        timestamp = 0
        file_flags = 0
        data = encoder.uint16(self.abi.mscoff_machine_type) + \
            encoder.uint16(len(self.sections)) + \
            encoder.uint32(timestamp) + \
            encoder.uint32(symbol_table_offset) + \
            encoder.uint32(len(self.symbols)) + \
            encoder.uint16(0) + \
            encoder.uint16(file_flags)

        # Write section headers
        for section in self.sections:
            data += section.encode_header(encoder, self.string_table._strings,
                                          section_offset_map[section],
                                          section_relocations_map.get(section))

        # Write symbol table and string table (immediately follows symbols table)
        for symbol in self.symbols:
            data += symbol.encode_entry(encoder, self.string_table._strings, section_index_map)
        data += self.string_table.encode()

        # Write section content
        for section in self.sections:
            data += section.content

        # Write section relocations
        for section in self.sections:
            for relocation in section.relocations:
                data += relocation.encode_entry(encoder, symbol_index_map)

        return data
