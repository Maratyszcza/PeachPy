# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Image:
    def __init__(self, abi, source=None):
        from peachpy.formats.elf.section import NullSection, StringSection, SymbolSection, SectionIndex
        from peachpy.formats.elf.symbol import Symbol, SymbolBinding, SymbolType
        self.abi = abi
        self.sections = []
        null = NullSection(abi)
        self.bind_section(null)
        shstrtab = StringSection(abi)
        self.bind_section(shstrtab, ".shstrtab")
        strtab = StringSection(abi)
        self.bind_section(strtab, ".strtab")
        symtab = SymbolSection(abi)
        symtab.header.link_index = strtab.index
        symtab.header.info = 0
        self.bind_section(symtab, ".symtab")
        if source:
            source_symbol = Symbol(abi)
            source_symbol.value = 0
            source_symbol.binding = SymbolBinding.Local
            source_symbol.type = SymbolType.File
            source_symbol.name_index = strtab.add(source)
            source_symbol.content_size = 0
            source_symbol.section_index = SectionIndex.Absolute
            symtab.add(source_symbol)

    @property
    def strtab(self):
        return self.sections[2]

    @property
    def symtab(self):
        return self.sections[3]

    def bind_section(self, section, section_name=None):
        section.index = len(self.sections)
        self.sections.append(section)
        if section_name is not None:
            section.header.name_index = self.sections[1].add(section_name)
        return section.index

    @property
    def as_bytearray(self):
        from peachpy.formats.elf.file import FileHeader

        file_header = FileHeader(self.abi)
        file_header.section_header_table_offset = file_header.size
        file_header.section_header_entries_count = len(self.sections)
        file_header.section_name_string_table_index = 1
        data = file_header.as_bytearray

        # Update section offsets
        data_offset = file_header.size + self.sections[0].header.size * len(self.sections)
        for section in self.sections:
            if section.header.address_alignment != 0:
                if data_offset % section.header.address_alignment != 0:
                    padding_length = section.header.address_alignment - data_offset % section.header.address_alignment
                    data_offset += padding_length
            section.header.offset = data_offset
            data_offset += section.header.content_size

        # Write section headers
        for section in self.sections:
            data += section.header.as_bytearray

        # Write section content
        for section in self.sections:
            if section.header.address_alignment != 0:
                if len(data) % section.header.address_alignment != 0:
                    padding_length = section.header.address_alignment - len(data) % section.header.address_alignment
                    padding_data = bytearray([0] * padding_length)
                    data += padding_data
            data += section.content

        return data
