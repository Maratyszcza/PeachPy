# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class MemoryProtection(IntEnum):
    read = 0x01
    write = 0x02
    execute = 0x04
    default = 0x07


class Segment:
    def __init__(self, name):
        self.name = name
        self.sections = list()
        self.flags = 0

    def add_section(self, section):
        assert isinstance(section, Section)
        assert section.segment_name == self.name

        self.sections.append(section)

    def get_command_size(self, abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.pointer_size in [4, 8]

        return {4: 56, 8: 72}[abi.pointer_size] + \
            sum(section.get_command_size(abi) for section in self.sections)

    def encode_command(self, encoder, section_offset_map, section_address_map, section_relocations_map):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)

        offset = section_offset_map[self.sections[0]]
        memory_size = section_address_map[self.sections[-1]] + self.sections[-1].content_size
        file_size = sum(section.content_size for section in self.sections)

        address = 0
        if self.sections:
            address = section_address_map[self.sections[0]]
        # TODO: combine the two cases
        if encoder.bitness == 32:
            command_id = 0x1
            command_size = 56 + len(self.sections) * 68
            command = encoder.uint32(command_id) + \
                encoder.uint32(command_size) + \
                encoder.fixed_string(self.name, 16) + \
                encoder.uint32(address) + \
                encoder.uint32(memory_size) + \
                encoder.uint32(offset) + \
                encoder.uint32(file_size) + \
                encoder.uint32(MemoryProtection.default) + \
                encoder.uint32(MemoryProtection.default) + \
                encoder.uint32(len(self.sections)) + \
                encoder.uint32(self.flags)
        else:
            command_id = 0x19
            command_size = 72 + len(self.sections) * 80
            command = encoder.uint32(command_id) + \
                encoder.uint32(command_size) + \
                encoder.fixed_string(self.name, 16) + \
                encoder.uint64(address) + \
                encoder.uint64(memory_size) + \
                encoder.uint64(offset) + \
                encoder.uint64(file_size) + \
                encoder.uint32(MemoryProtection.default) + \
                encoder.uint32(MemoryProtection.default) + \
                encoder.uint32(len(self.sections)) + \
                encoder.uint32(self.flags)
        for section in self.sections:
            command += section.encode_command(encoder,
                                              section_offset_map[section],
                                              section_address_map[section],
                                              section_relocations_map.get(section))
        from peachpy.x86_64.abi import system_v_x86_64_abi
        return command


class SectionIndex(IntEnum):
    no_section = 0


class SectionType(IntEnum):
    regular = 0x00
    zero_fill = 0x01
    gb_zero_fill = 0x0C
    cstring_literals = 0x02
    four_byte_literals = 0x03
    eight_byte_literals = 0x04
    sixteen_byte_literals = 0x0E
    literal_pointers = 0x05
    non_lazy_symbol_pointers = 0x06
    lazy_symbol_pointers = 0x07
    symbol_stubs = 0x08
    module_init_function_pointers = 0x09
    module_terminate_function_pointers = 0x0A
    coalesced_symbols = 0x0B
    interposing = 0x0D
    dtrace_object_format = 0x0F
    lazy_dylib_symbol_pointers = 0x10
    thread_local_regular = 0x11
    thread_local_zero_fill = 0x12
    thread_local_variable_descriptors = 0x13
    thread_local_variable_pointers = 0x14
    thread_local_function_pointers = 0x15


class SectionAttributes(IntEnum):
    only_instructions = 0x80000000
    coalesced_symbols = 0x40000000
    strip_static_symbols = 0x20000000
    no_dead_stripping = 0x10000000
    live_support = 0x08000000
    self_modifying_code = 0x04000000
    debug = 0x02000000
    some_instructions = 0x00000400
    external_relocations = 0x00000200
    local_relocations = 0x00000100


class Section(object):
    def __init__(self, type, segment_name, section_name):
        self.type = type
        self.segment_name = segment_name
        self.section_name = section_name
        self.attributes = 0
        self._alignment = 1
        self.relocations = []
        self.content = bytearray()

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

    @property
    def log2_alignment(self):
        from peachpy.util import ilog2
        return ilog2(self._alignment)

    @property
    def relocations_count(self):
        return len(self.relocations)

    @property
    def content_size(self):
        return len(self.content)

    @staticmethod
    def get_command_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.pointer_size in [4, 8]

        return {4: 68, 8: 80}[abi.pointer_size]

    def encode_command(self, encoder, offset, address, relocations_offset):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)

        if len(self.relocations) == 0:
            relocations_offset = 0
        if encoder.bitness == 32:
            return encoder.fixed_string(self.section_name, 16) + \
                encoder.fixed_string(self.segment_name, 16) + \
                encoder.uint32(address) + \
                encoder.uint32(self.content_size) + \
                encoder.uint32(offset) + \
                encoder.uint32(self.log2_alignment) + \
                encoder.uint32(relocations_offset) + \
                encoder.uint32(self.relocations_count) + \
                encoder.uint32(self.type | self.attributes) + \
                bytearray(8)
        else:
            return encoder.fixed_string(self.section_name, 16) + \
                encoder.fixed_string(self.segment_name, 16) + \
                encoder.uint64(address) + \
                encoder.uint64(self.content_size) + \
                encoder.uint32(offset) + \
                encoder.uint32(self.log2_alignment) + \
                encoder.uint32(relocations_offset) + \
                encoder.uint32(self.relocations_count) + \
                encoder.uint32(self.type | self.attributes) + \
                bytearray(12)


class RegularSection(Section):
    def __init__(self, segment_name, section_name):
        super(RegularSection, self).__init__(SectionType.regular, segment_name, section_name)

    def align(self, alignment):
        import peachpy.util
        ilog2_alignment = peachpy.util.ilog2(alignment)
        self.alignment = max(self.alignment, ilog2_alignment)
        if len(self.content) % alignment != 0:
            padding_length = alignment - len(self.content) % alignment
            self.content += bytearray(padding_length)


class TextSection(RegularSection):
    def __init__(self):
        super(TextSection, self).__init__("__TEXT", "__text")
        self.attributes = SectionAttributes.only_instructions | SectionAttributes.some_instructions


class ConstSection(RegularSection):
    def __init__(self):
        super(ConstSection, self).__init__("__TEXT", "__const")


class SymbolTable:
    command_size = 24

    def __init__(self, string_table):
        assert isinstance(string_table, StringTable)

        self.symbols = list()
        self.string_table = string_table

    def add_symbol(self, symbol):
        from peachpy.formats.macho.symbol import Symbol
        assert isinstance(symbol, Symbol)

        self.symbols.append(symbol)
        self.string_table.add(symbol.name)

    def encode_command(self, encoder, symbol_offset_map, string_offset):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)

        command_id = 0x2
        symbols_offset = 0
        if self.symbols:
            symbols_offset = symbol_offset_map[self.symbols[0]]
        return encoder.uint32(command_id) + \
            encoder.uint32(SymbolTable.command_size) + \
            encoder.uint32(symbols_offset) + \
            encoder.uint32(len(self.symbols)) + \
            encoder.uint32(string_offset) + \
            encoder.uint32(self.string_table.size)


class StringTable:
    def __init__(self):
        self.string_index_map = dict()
        self.size = 0

    def add(self, string):
        import codecs
        if string is None or len(string) == 0:
            return 0
        if string in self.string_index_map:
            return self.string_index_map[string]
        else:
            content_size = self.size
            if content_size == 0:
                content_size = 1
            string_index = content_size
            self.string_index_map[string] = string_index
            bytestring = codecs.encode(string, "utf-8")
            content_size += len(bytestring) + 1
            self.size = content_size

    def encode(self):
        import codecs
        if self.size != 0:
            bytestring = b"\x00"
            for string in sorted(self.string_index_map, key=self.string_index_map.get):
                bytestring += codecs.encode(string, "utf8") + b"\x00"
            return bytestring
        else:
            return bytearray()
