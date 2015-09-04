# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
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
