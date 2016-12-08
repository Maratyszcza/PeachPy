# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Image:
    def __init__(self, abi):
        from peachpy.formats.macho.section import Segment, TextSection, ConstSection, StringTable, SymbolTable

        self.abi = abi
        self.segments = list()

        self.text_segment = Segment("__TEXT")
        self.add_segment(self.text_segment)

        self.text_section = TextSection()
        self.text_segment.add_section(self.text_section)

        self.const_section = ConstSection()
        self.text_segment.add_section(self.const_section)

        self.string_table = StringTable()
        self.symbol_table = SymbolTable(self.string_table)

    def add_segment(self, segment):
        from peachpy.formats.macho.section import Segment
        assert isinstance(segment, Segment)

        self.segments.append(segment)

    def encode(self):
        from peachpy.formats.macho.file import MachHeader
        from peachpy.formats.macho.symbol import Relocation
        from peachpy.util import roundup
        from peachpy.encoder import Encoder

        bitness = {4: 32, 8: 64}[self.abi.pointer_size]
        encoder = Encoder(self.abi.endianness, bitness)

        mach_header = MachHeader(self.abi)
        mach_header.commands_size = self.symbol_table.command_size
        mach_header.commands_count = 1
        for segment in self.segments:
            mach_header.commands_size += segment.get_command_size(self.abi)
            mach_header.commands_count += 1

        symbol_offset_map = dict()
        section_offset_map = dict()
        section_address_map = dict()
        section_relocations_map = dict()

        # Layout the commands
        data_offset = mach_header.get_size(self.abi)
        for segment in self.segments:
            data_offset += segment.get_command_size(self.abi)
        data_offset += self.symbol_table.command_size

        # Layout section data
        data_address = 0
        for segment in self.segments:
            for section in segment.sections:
                data_offset = roundup(data_offset, section.alignment)
                data_address = roundup(data_address, section.alignment)
                section_offset_map[section] = data_offset
                section_address_map[section] = data_address
                data_offset += section.content_size
                data_address += section.content_size
        data_offset = roundup(data_offset, self.abi.pointer_size)

        # Layout the relocations
        for segment in self.segments:
            for section in segment.sections:
                if section.relocations:
                    section_relocations_map[section] = data_offset
                    data_offset += Relocation.size * len(section.relocations)

        # Layout the symbols
        for symbol in self.symbol_table.symbols:
            symbol_offset_map[symbol] = data_offset
            data_offset += symbol.get_entry_size(self.abi)

        # Layout the strings
        string_table_offset = data_offset

        # Create map: section->index
        section_index = 1
        section_index_map = dict()
        for segment in self.segments:
            for section in segment.sections:
                section_index_map[section] = section_index
                section_index += 1

        # Create map: symbol->index
        symbol_index_map = {symbol: index for index, symbol in enumerate(self.symbol_table.symbols)}

        # Write Mach-O header
        data = mach_header.encode(encoder)

        # Write commands
        for segment in self.segments:
            data += segment.encode_command(encoder, section_offset_map, section_address_map, section_relocations_map)
        data += self.symbol_table.encode_command(encoder, symbol_offset_map, string_table_offset)

        # Write section data
        for segment in self.segments:
            for section in segment.sections:
                padding = bytearray(roundup(len(data), section.alignment) - len(data))
                data += padding + section.content
        padding = bytearray(roundup(len(data), self.abi.pointer_size) - len(data))
        data += padding

        # Write relocations
        for segment in self.segments:
            for section in segment.sections:
                for relocation in section.relocations:
                    data += relocation.encode(encoder, section_index_map, symbol_index_map)

        # Write symbols
        for symbol in self.symbol_table.symbols:
            data += symbol.encode(encoder, self.string_table.string_index_map, section_index_map, section_address_map)

        # Write string table
        data += self.string_table.encode()

        return data
