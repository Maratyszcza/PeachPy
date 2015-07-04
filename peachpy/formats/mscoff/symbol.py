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


class SymbolEntry:
    size = 18

    def __init__(self):
        # Either short string (<= 8 bytes) or offset into the string table
        self.name = None
        # Value of the symbol. Interpretation depends on section_index and storage_class
        self.value = None
        # Index (1-based) of the relevant section in the section table
        self.section_index = None
        # Symbol type. Microsoft tools use only 0x20 (function) or 0x0 (not a function)
        self.symbol_type = None
        # Storage class
        self.storage_class = None
        # Number of auxiliary symbol table following the symbol entry.
        self.auxiliary_entries = 0

    @property
    def as_bytearray(self):
        from peachpy.encoder import Encoder
        from peachpy.util import is_int
        if is_int(self.name):
            entry = Encoder.uint32le(0) + Encoder.uint32le(self.name)
        else:
            entry = Encoder.fixed_string(self.name, 8)
        return entry + \
            Encoder.uint32le(self.value) + \
            Encoder.uint16le(self.section_index) + \
            Encoder.uint16le(self.symbol_type) + \
            Encoder.uint8(self.storage_class) + \
            Encoder.uint8(self.auxiliary_entries)
