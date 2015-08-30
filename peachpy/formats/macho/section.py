# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


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


class SectionHeader:
    def __init__(self, abi):
        self.abi = abi
        self.size = {4: 68, 8: 80}[abi.pointer_size]
        self.name = None
        self.segment_name = None
        self.address = None
        self.content_size = 0
        self.offset = None
        self.alignment = 0
        self.relocation_offset = None
        self.relocation_count = 0
        self.type = None
        self.attributes = 0

    @property
    def as_bytearray(self):
        import peachpy.encoder

        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        if self.abi.pointer_size == 4:
            return encoder.fixed_string(self.name, 16) + \
                encoder.fixed_string(self.segment_name, 16) + \
                encoder.uint32(self.address or 0) + \
                encoder.uint32(self.content_size) + \
                encoder.uint32(self.offset) + \
                encoder.uint32(self.alignment) + \
                encoder.uint32(self.relocation_offset or 0) + \
                encoder.uint32(self.relocation_count) + \
                encoder.uint32(self.type | self.attributes) + \
                bytearray(8)
        else:
            return encoder.fixed_string(self.name, 16) + \
                encoder.fixed_string(self.segment_name, 16) + \
                encoder.uint64(self.address or 0) + \
                encoder.uint64(self.content_size) + \
                encoder.uint32(self.offset) + \
                encoder.uint32(self.alignment) + \
                encoder.uint32(self.relocation_offset or 0) + \
                encoder.uint32(self.relocation_count) + \
                encoder.uint32(self.type | self.attributes) + \
                bytearray(12)


class Section(object):
    def __init__(self, abi, segment_name, name):
        self.header = SectionHeader(abi)
        self.header.segment_name = segment_name
        self.header.name = name
        self._content = bytearray()

    @property
    def content(self):
        return self._content


class RegularSection(Section):
    def __init__(self, abi, name, segment_name):
        super(RegularSection, self).__init__(abi, name, segment_name)
        self.header.type = SectionType.regular

    def append(self, bytes):
        self.header.content_size += len(bytes)
        self._content += bytes

    def align(self, alignment):
        import peachpy.util
        ilog2_alignment = peachpy.util.ilog2(alignment)
        self.header.alignment = max(self.header.alignment, ilog2_alignment)
        if self.header.content_size % alignment != 0:
            padding_length = alignment - self.header.content_size % alignment
            self.header.content_size += padding_length
            self._content.append(bytearray(padding_length))


class TextSection(RegularSection):
    def __init__(self, abi):
        super(TextSection, self).__init__(abi, "__TEXT", "__text")
        self.header.attributes = SectionAttributes.only_instructions | SectionAttributes.some_instructions


class ConstSection(RegularSection):
    def __init__(self, abi):
        super(ConstSection, self).__init__(abi, "__TEXT", "__const")


class StringTable:
    def __init__(self):
        self._strings = dict()
        self.size = 0

    def add(self, string):
        import codecs
        if string is None or len(string) == 0:
            return 0
        if string in self._strings:
            return self._strings[string]
        else:
            content_size = self.size
            if content_size == 0:
                content_size = 1
            string_index = content_size
            self._strings[string] = string_index
            bytestring = codecs.encode(string, "utf-8")
            content_size += len(bytestring) + 1
            self.size = content_size
            return string_index

    @property
    def as_bytearray(self):
        import codecs
        if self.size != 0:
            bytestring = b"\x00"
            for string in sorted(self._strings, key=self._strings.get):
                bytestring += codecs.encode(string, "utf8") + b"\x00"
            return bytestring
        else:
            return bytearray()
