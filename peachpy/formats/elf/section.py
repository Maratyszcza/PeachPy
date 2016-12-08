# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class SectionFlags(IntEnum):
    # Section contains writable data during process execution
    writable = 0x1
    # Section occupies memory during process execution
    allocate = 0x2
    # Section contains executable data machine instructions
    executable = 0x4


class SectionType(IntEnum):
    # Nil section
    null = 0
    # Program-specific content
    program_bits = 1
    # Symbol table
    symbol_table = 2
    # String table
    string_table = 3
    # Relocations with explicit addend
    relocations_with_addend = 4
    # Hash table for symbols used in dynamic linking
    symbol_hash_table = 5
    # Information for dynamic linking
    dynamic_linking_info = 6
    # Free-form note
    note = 7
    # Program-specific zero-initialized content
    no_bits = 8
    # Relocations without explicit addends
    relocations = 9
    # Minimal symbol table for dynamic linking
    dynamic_symbol_table = 11


class SectionIndex(IntEnum):
    absolute = 0xFFF1
    common = 0xFFF2
    undefined = 0x0000


class Section(object):
    def __init__(self, name, type, allocate=False, writable=False, executable=False):
        # Section name
        self.name = name
        # Type of the section content
        self._type = SectionType.null
        self.type = type  # Check the type object in property setter
        # Properties of section content
        self.flags = 0
        if allocate:
            self.flags |= SectionFlags.allocate
        if writable:
            self.flags |= SectionFlags.writable
        if executable:
            self.flags |= SectionFlags.executable
        # Section address alignment. Only powers of 2 are allowed. Value 0 or 1 mean no alignment restrictions.
        self._alignment = 1

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if not isinstance(type, SectionType):
            raise TypeError("Section type %s is not a SectionType enum" % str(type))
        self._type = type

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, alignment):
        from peachpy.util import is_uint32
        if not is_uint32(alignment):
            raise TypeError("Section alignment %s is not representable as a 32-bit unsigned integer" % str(alignment))
        if alignment & (alignment - 1) != 0:
            raise ValueError("Section alignment %d is not a power of 2" % alignment)
        if alignment == 0:
            alignment = 1
        self._alignment = alignment

    @staticmethod
    def get_header_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.elf_bitness in [32, 64]

        return {32: 40, 64: 64}[abi.elf_bitness]

    def get_content_size(self, abi):
        return 0

    def encode_header(self, encoder, name_index_map, section_index_map, offset,
                      address=None, link_section=None, info=None,
                      content_size=0, entry_size=0):
        import peachpy.encoder
        from peachpy.util import is_uint64, is_uint32
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert isinstance(name_index_map, dict)
        assert section_index_map is None or isinstance(section_index_map, dict)
        assert offset is None or is_uint64(offset)
        assert address is None or is_uint64(address)
        assert link_section is None or isinstance(link_section, Section)
        assert info is None or is_uint64(info)
        assert is_uint64(content_size)
        assert is_uint32(entry_size)

        assert encoder.bitness in [32, 64]
        if encoder.bitness == 32:
            assert offset is None or is_uint32(offset)
            assert address is None or is_uint32(address)
        assert self.name is None or self.name in name_index_map
        assert section_index_map is not None or link_section is None

        name_index = name_index_map.get(self.name, 0)
        if address is None:
            address = 0
        if offset is None:
            offset = 0
        link = 0
        if link_section is not None:
            link = section_index_map[link_section]
        if info is None:
            info = 0
        return encoder.uint32(name_index) + \
            encoder.uint32(self.type) + \
            encoder.unsigned_offset(self.flags) + \
            encoder.unsigned_offset(address) + \
            encoder.unsigned_offset(offset) + \
            encoder.unsigned_offset(content_size) + \
            encoder.uint32(link) + \
            encoder.uint32(info) + \
            encoder.unsigned_offset(self.alignment) + \
            encoder.unsigned_offset(entry_size)

    def encode_content(self, encoder, name_index_map, section_index_map, symbol_index_map):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert isinstance(name_index_map, dict)
        assert section_index_map is None or isinstance(section_index_map, dict)
        assert symbol_index_map is None or isinstance(symbol_index_map, dict)

        assert encoder.bitness in [32, 64]

        return bytearray()


null_section = Section(None, SectionType.null)


class ProgramBitsSection(Section):
    def __init__(self, name, allocate=True, writable=False, executable=False):
        super(ProgramBitsSection, self).__init__(name, SectionType.program_bits, allocate, writable, executable)
        self.content = bytearray()

    def get_content_size(self, abi):
        return len(self.content)

    def encode_header(self, encoder, name_index_map, section_index_map, offset, address=None):
        return super(ProgramBitsSection, self).encode_header(encoder, name_index_map, section_index_map, offset,
                                                             address=address, content_size=len(self.content))

    def encode_content(self, encoder, name_index_map, section_index_map, symbol_index_map):
        super(ProgramBitsSection, self).encode_content(encoder, name_index_map, section_index_map, symbol_index_map)
        return self.content


class TextSection(ProgramBitsSection):
    def __init__(self, name=".text"):
        super(TextSection, self).__init__(name, executable=True)


class DataSection(ProgramBitsSection):
    def __init__(self, name=".data"):
        super(DataSection, self).__init__(name, writable=True)


class ReadOnlyDataSection(ProgramBitsSection):
    def __init__(self, name=".rodata"):
        super(ReadOnlyDataSection, self).__init__(name)


class StringSection(Section):
    def __init__(self, name=".strtab"):
        super(StringSection, self).__init__(name, SectionType.string_table)
        self._string_index_map = dict()
        self.content_size = 0

    def add(self, string):
        if not string:
            return 0
        elif string in self._string_index_map:
            return self._string_index_map[string]
        else:
            import codecs

            if self.content_size == 0:
                self.content_size = 1
            string_index = self.content_size
            self._string_index_map[string] = string_index
            string_bytes = codecs.encode(string, "utf-8")
            self.content_size += len(string_bytes) + 1
            return string_index

    def get_content_size(self, abi):
        return self.content_size

    def encode_header(self, encoder, name_index_map, section_index_map, offset):
        return super(StringSection, self).encode_header(encoder, name_index_map, section_index_map, offset,
                                                        content_size=self.content_size)

    def encode_content(self, encoder, name_index_map, section_index_map, symbol_index_map):
        super(StringSection, self).encode_content(encoder, name_index_map, section_index_map, symbol_index_map)
        if self.content_size != 0:
            import codecs

            bytes = b"\x00"
            for string in sorted(self._string_index_map, key=self._string_index_map.get):
                bytes += codecs.encode(string, "utf8") + b"\x00"
            return bytes
        else:
            return bytearray()


class SymbolSection(Section):
    def __init__(self, name=".symtab", string_table=None):
        super(SymbolSection, self).__init__(name, SectionType.symbol_table)
        self._symbols_set = set()
        self._local_symbols = list()
        self._nonlocal_symbols = list()
        self._string_table = string_table

    @property
    def symbol_index_map(self):
        symbol_index_map = {symbol: index for index, symbol in enumerate(self._local_symbols)}
        local_symbols_count = len(self._local_symbols)
        symbol_index_map.update(
            {symbol: local_symbols_count + index for index, symbol in enumerate(self._nonlocal_symbols)})
        return symbol_index_map

    def add(self, symbol):
        from peachpy.formats.elf.symbol import Symbol, SymbolBinding
        assert isinstance(symbol, Symbol)

        if symbol in self._symbols_set:
            raise ValueError("Symbol %s is already present in the section %s" % (str(symbol), self.name))
        self._symbols_set.add(symbol)
        if symbol.binding == SymbolBinding.local:
            self._local_symbols.append(symbol)
        else:
            self._nonlocal_symbols.append(symbol)

    def get_content_size(self, abi):
        from peachpy.formats.elf.symbol import Symbol
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.elf_bitness in [32, 64]

        entry_size = Symbol.get_entry_size(abi)
        return entry_size * (len(self._local_symbols) + len(self._nonlocal_symbols))

    def encode_header(self, encoder, name_index_map, section_index_map, offset):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert encoder.bitness in [32, 64]

        entry_size = {32: 16, 64: 24}[encoder.bitness]
        symbols_count = len(self._local_symbols) + len(self._nonlocal_symbols)
        return super(SymbolSection, self).encode_header(encoder, name_index_map, section_index_map, offset,
                                                        link_section=self._string_table,
                                                        info=len(self._local_symbols),
                                                        content_size=symbols_count * entry_size,
                                                        entry_size=entry_size)

    def encode_content(self, encoder, name_index_map, section_index_map, symbol_index_map):
        super(SymbolSection, self).encode_content(encoder, name_index_map, section_index_map, symbol_index_map)

        # Local symbols must be encoded before non-local symbols. Thus, need to separate the two classes
        content = bytearray()

        # Step 1: encode local symbols
        for symbol in self._local_symbols:
            content += symbol.encode(encoder, name_index_map, section_index_map)
        # Step 2: encode non-local symbols
        for symbol in self._nonlocal_symbols:
            content += symbol.encode(encoder, name_index_map, section_index_map)

        return content


class RelocationsWithAddendSection(Section):
    def __init__(self, reference_section, symbol_table):
        super(RelocationsWithAddendSection, self).__init__(".rela" + reference_section.name,
                                                           SectionType.relocations_with_addend)
        self.reference_section = reference_section
        self.symbol_table = symbol_table

        self.relocations = list()

    def add(self, relocation):
        from peachpy.formats.elf.symbol import RelocationWithAddend
        assert isinstance(relocation, RelocationWithAddend)

        self.relocations.append(relocation)

    def get_content_size(self, abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.elf_bitness in [32, 64]

        entry_size = {32: 12, 64: 24}[abi.elf_bitness]
        return entry_size * len(self.relocations)

    def encode_header(self, encoder, name_index_map, section_index_map, offset):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert encoder.bitness in [32, 64]

        entry_size = {32: 16, 64: 24}[encoder.bitness]
        relocations_count = len(self.relocations)
        reference_section_index = section_index_map[self.reference_section]
        return super(RelocationsWithAddendSection, self).\
            encode_header(encoder, name_index_map, section_index_map, offset,
                          link_section=self.symbol_table,
                          info=reference_section_index,
                          content_size=relocations_count * entry_size,
                          entry_size=entry_size)

    def encode_content(self, encoder, name_index_map, section_index_map, symbol_index_map):
        super(RelocationsWithAddendSection, self).\
            encode_content(encoder, name_index_map, section_index_map, symbol_index_map)

        content = bytearray()
        for relocation in self.relocations:
            content += relocation.encode(encoder, symbol_index_map)

        return content
