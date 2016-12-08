# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


from enum import IntEnum


class StorageClass(IntEnum):
    """
    External symbol. If section number is undefined (0), value specifies symbol size. Otherwise value specifies offset
    within section.
    """
    external = 2

    """Static symbol. value specifies offset within section. value of 0 means that symbol represents section name."""
    static = 3

    """A function .bf (beginning of function), .ef (end of function) or .lf (lines in function record) """
    function = 101
    """Source-file symbol record. Followed by auxiliary records that name the file"""
    file = 103


class SymbolType(IntEnum):
    non_function = 0
    function = 0x20


class Symbol:
    entry_size = 18

    def __init__(self):
        # Name of the symbol
        self.name = None
        # Value of the symbol. Interpretation depends on section_index and storage_class
        self.value = None
        # Relevant section
        self.section = None
        # Symbol type. Microsoft tools use only 0x20 (function) or 0x0 (not a function)
        self.symbol_type = None
        # Storage class
        self.storage_class = None

    def encode_entry(self, encoder, name_index_map, section_index_map):
        from peachpy.encoder import Encoder
        assert isinstance(encoder, Encoder)

        try:
            name_8_bytes = encoder.fixed_string(self.name, 8)
        except ValueError:
            name_index = name_index_map[self.name]
            name_8_bytes = encoder.uint32(0) + encoder.uint32(name_index)
        section_index = section_index_map[self.section]
        auxiliary_entries = 0
        return name_8_bytes + \
            encoder.uint32(self.value) + \
            encoder.uint16(section_index) + \
            encoder.uint16(self.symbol_type) + \
            encoder.uint8(self.storage_class) + \
            encoder.uint8(auxiliary_entries)


class RelocationType(IntEnum):
    # Relocation is ignored
    absolute = 0

    # 32-bit address
    x86_address32 = 6
    # 32-bit offset relative to image base
    x86_imagebase_offset32 = 7
    # 16-bit section index
    x86_section_index = 10
    # 32-bit offset relative to the section
    x86_section_offset32 = 11
    # CLR token
    x86_clr_token = 12
    # Unsigned 7-bit offset relative to the section
    x86_section_offset7 = 13
    # 32-bit offset relative to the end of relocation
    x86_relocation_offset32 = 14

    # 64-bit address
    x86_64_address64 = 1
    # 32-bit address
    x86_64_address32 = 2
    # 32-bit offset relative to image base
    x86_64_imagebase_offset32 = 3
    # 32-bit offset relative to the end of relocation
    x86_64_relocation_offset32 = 4
    # 32-bit offset relative to the end of relocation + 1 byte
    x86_64_relocation_plus_1_offset32 = 5
    # 32-bit offset relative to the end of relocation + 2 bytes
    x86_64_relocation_plus_2_offset32 = 6
    # 32-bit offset relative to the end of relocation + 3 bytes
    x86_64_relocation_plus_3_offset32 = 7
    # 32-bit offset relative to the end of relocation + 4 bytes
    x86_64_relocation_plus_4_offset32 = 8
    # 32-bit offset relative to the end of relocation + 5 bytes
    x86_64_relocation_plus_5_offset32 = 9
    # 16-bit section index
    x86_64_section_index = 10
    # 32-bit offset relative to the section
    x86_64_section_offset32 = 11
    # Unsigned 7-bit offset relative to the section
    x86_64_section_offset7 = 12
    # CLR token
    x86_64_clr_token = 13


class Relocation:
    entry_size = 10

    def __init__(self, type, offset, symbol):
        from peachpy.util import is_int, is_uint32
        if not isinstance(type, RelocationType):
            raise TypeError("Relocation type %s is not in RelocationType enumeration" % str(type))
        if not is_int(offset):
            raise TypeError("Offset %s is not an integer" % str(offset))
        if not is_uint32(offset):
            raise ValueError("Offset %d can not be represented as a 32-bit unsigned integer" % offset)
        if not isinstance(symbol, Symbol):
            raise TypeError("Symbol %s is not an instance of Symbol type" % str(symbol))

        self.type = type
        self.offset = offset
        self.symbol = symbol

    def encode_entry(self, encoder, symbol_index_map, section_address=0):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert self.symbol in symbol_index_map

        symbol_index = symbol_index_map[self.symbol]
        return encoder.uint32(section_address + self.offset) + \
            encoder.uint32(symbol_index) + \
            encoder.uint16(self.type)
