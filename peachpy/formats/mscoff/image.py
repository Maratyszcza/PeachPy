# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Image:
    def __init__(self, abi, source=None):
        from peachpy.formats.mscoff.section import StringTable
        self.abi = abi
        self.sections = []
        self.symbols = []
        self.string_table = StringTable()

    def add_section(self, section, name):
        from peachpy.formats.mscoff.section import Section
        assert isinstance(section, Section)

        section.index = len(self.sections)
        self.sections.append(section)

        import codecs
        name_bytestring = codecs.encode(name, "utf8")
        if len(name_bytestring) > 8:
            section.header.name = self.string_table.add(name_bytestring)
        else:
            section.header.name = name

        return section.index

    def add_symbol(self, symbol, name):
        from peachpy.formats.mscoff.symbol import SymbolEntry
        assert isinstance(symbol, SymbolEntry)

        import codecs
        name_bytestring = codecs.encode(name, "utf8")
        if len(name_bytestring) > 8:
            symbol.name = self.string_table.add(name_bytestring)
        else:
            symbol.name = name
        self.symbols.append(symbol)

    @property
    def as_bytearray(self):
        from peachpy.formats.mscoff.file import FileHeader
        from peachpy.formats.mscoff.section import SectionHeader
        import operator

        file_header = FileHeader(self.abi)
        file_header.section_count = len(self.sections)
        file_header.symbol_count = len(self.symbols)
        file_header.symbol_table_offset = FileHeader.size + len(self.sections) * SectionHeader.size

        # Update section offsets
        data_offset = FileHeader.size + len(self.sections) * SectionHeader.size
        file_header.symbol_table_offset = data_offset

        data = file_header.as_bytearray

        # Update section offsets
        data_offset = file_header.symbol_table_offset + \
            sum(map(operator.attrgetter("size"), self.symbols)) + \
            self.string_table.size
        for section in self.sections:
            if section.header.alignment != 0:
                if data_offset % section.header.alignment != 0:
                    padding_length = section.header.alignment - data_offset % section.header.alignment
                    data_offset += padding_length
            section.header.content_offset = data_offset
            data_offset += section.header.content_size

        # Write section headers
        for section in self.sections:
            data += section.header.as_bytearray

        # Write symbol table and string table (immediately follows symbols table)
        for symbol in self.symbols:
            data += symbol.as_bytearray
        data += self.string_table.as_bytearray

        # Write section content
        for section in self.sections:
            if section.header.alignment != 0:
                if len(data) % section.header.alignment != 0:
                    padding_length = section.header.alignment - len(data) % section.header.alignment
                    padding_data = bytearray([0] * padding_length)
                    data += padding_data
            data += section.content

        return data
