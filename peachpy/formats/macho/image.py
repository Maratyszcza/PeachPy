# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Image:
    def __init__(self, abi):
        from peachpy.formats.macho.file import SegmentCommand, SymbolTableCommand
        from peachpy.formats.macho.section import StringTable, TextSection, ConstSection
        self.abi = abi
        self.segment_command = SegmentCommand(abi)
        self.segment_command.section_count = 0
        self.sections = list()
        text_section = TextSection(abi)
        self.bind_section(text_section)
        const_section = ConstSection(abi)
        self.bind_section(const_section)
        self.symbol_table_command = SymbolTableCommand(abi)
        self.symbols = list()
        self.string_table = StringTable()

    def bind_section(self, section):
        self.sections.append(section)
        section.index = len(self.sections)
        self.segment_command.section_count += 1
        self.segment_command.size += section.header.size
        return section.index

    @property
    def text_section(self):
        return self.sections[0]

    @property
    def const_section(self):
        return self.sections[1]

    @property
    def as_bytearray(self):
        from peachpy.formats.macho.file import MachHeader

        mach_header = MachHeader(self.abi)
        mach_header.command_size = self.segment_command.size + self.symbol_table_command.size
        mach_header.command_count = 2
        data = mach_header.as_bytearray

        # Update section offsets
        data_offset = mach_header.size + \
                      self.segment_command.size + \
                      self.symbol_table_command.size
        self.segment_command.offset = data_offset
        for section in self.sections:
            if data_offset % self.abi.pointer_size != 0:
                padding_length = self.abi.pointer_size - data_offset % self.abi.pointer_size
                data_offset += padding_length
            section.header.offset = data_offset
            data_offset += section.header.content_size

        self.symbol_table_command.symbol_count = len(self.symbols)
        if len(self.symbols):
            if data_offset % self.abi.pointer_size != 0:
                padding_length = self.abi.pointer_size - data_offset % self.abi.pointer_size
                data_offset += padding_length
            self.symbol_table_command.symbol_offset = data_offset
            data_offset += sum([symbol.size for symbol in self.symbols])

        self.symbol_table_command.string_size = self.string_table.size
        if self.string_table.size:
            self.symbol_table_command.string_offset = data_offset

        # Write commands
        data += self.segment_command.as_bytearray
        for section in self.sections:
            data += section.header.as_bytearray
        data += self.symbol_table_command.as_bytearray

        # Write section content
        for section in self.sections:
            if len(data) % self.abi.pointer_size != 0:
                padding_length = self.abi.pointer_size - len(data) % self.abi.pointer_size
                data += bytearray(padding_length)
            data += section.content

        # Write symbols
        if len(self.symbols):
            if len(data) % self.abi.pointer_size != 0:
                padding_length = self.abi.pointer_size - len(data) % self.abi.pointer_size
                data += bytearray(padding_length)
            for symbol in self.symbols:
                data += symbol.as_bytearray

        # Write string table
        data += self.string_table.as_bytearray

        return data
