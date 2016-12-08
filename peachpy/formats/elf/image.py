# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Image:
    def __init__(self, abi, source=None):
        from peachpy.formats.elf.section import null_section, StringSection, SymbolSection, SectionIndex
        from peachpy.formats.elf.symbol import Symbol, SymbolBinding, SymbolType
        self.abi = abi
        self.shstrtab = StringSection(".shstrtab")
        self.strtab = StringSection(".strtab")
        self.symtab = SymbolSection(string_table=self.strtab)
        self.sections = [null_section, self.shstrtab, self.strtab, self.symtab]
        self._section_names = set([self.shstrtab.name, self.strtab.name, self.symtab.name])
        if source:
            source_symbol = Symbol()
            source_symbol.value = 0
            source_symbol.binding = SymbolBinding.local
            source_symbol.type = SymbolType.file
            source_symbol.name = source
            source_symbol.size = 0
            source_symbol.section = SectionIndex.absolute
            self.symtab.add(source_symbol)

    def add_section(self, section):
        from peachpy.formats.elf.section import Section
        if not isinstance(section, Section):
            raise TypeError("%s is not a Section object" % str(section))
        if section.name is not None and section.name in self._section_names:
            raise ValueError("Section %s is already present in the image" % section.name)
        self.sections.append(section)
        self._section_names.add(section.name)

    def find_section(self, section_name):
        for section in self.sections:
            if section.name == section_name:
                return section

    @property
    def as_bytearray(self):
        import six
        from peachpy.formats.elf.file import FileHeader
        from peachpy.formats.elf.section import Section, StringSection, SymbolSection
        from peachpy.util import roundup

        file_header = FileHeader(self.abi)
        file_header.section_header_table_offset = file_header.size
        file_header.section_header_entries_count = len(self.sections)
        file_header.section_name_string_table_index = 1
        data = file_header.as_bytearray

        # Collect strings from sections
        for section in self.sections:
            self.shstrtab.add(section.name)
            if isinstance(section, StringSection):
                pass
            elif isinstance(section, SymbolSection):
                for symbol in six.iterkeys(section.symbol_index_map):
                    self.strtab.add(symbol.name)

        # Layout sections
        data_offset = file_header.size + Section.get_header_size(self.abi) * len(self.sections)
        section_offsets = []
        for section in self.sections:
            if section.alignment != 0:
                data_offset = roundup(data_offset, section.alignment)
            section_offsets.append(data_offset)
            data_offset += section.get_content_size(self.abi)

        from peachpy.encoder import Encoder
        encoder = Encoder(self.abi.endianness, self.abi.elf_bitness)

        section_index_map = {section: index for index, section in enumerate(self.sections)}
        # Write section headers
        for section, offset in zip(self.sections, section_offsets):
            data += section.encode_header(encoder, self.shstrtab._string_index_map, section_index_map, offset)

        # Write section content
        for section in self.sections:
            padding = bytearray(roundup(len(data), section.alignment) - len(data))
            data += padding
            data += section.encode_content(encoder,
                                           self.strtab._string_index_map, section_index_map,
                                           self.symtab.symbol_index_map)

        return data
