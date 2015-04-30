# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.formats.elf.file import ElfClass

class SymbolBinding:
    Local = 0
    Global = 1
    Weak = 2


class SymbolType:
    # No type specified (e.g. an absolute symbol)
    Unspecified = 0
    # Data object
    DataObject = 1
    # Function entry point
    Function = 2
    # Symbol associated with a section
    Section = 3
    # Source file associated with the object file
    File = 4


class Symbol:
    def __init__(self, abi):
        self.abi = abi

        # Index into the object's string table
        self.name_index = None
        # Value of the symbol
        self.value = None
        # Size of the data object (0 if size is unknown or meaningless)
        self.content_size = 0
        # Binding attribute
        self.binding = 0
        # Type attribute
        self.type = 0
        # Index of the relevant section in the section header table
        self.section_index = None

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)
        if self.abi.elf_class == ElfClass.Class32:
            return encoder.uint32(self.name_index) + \
                encoder.uint32(self.value) + \
                encoder.uint32(self.content_size) + \
                encoder.uint8((self.binding << 4) | (self.type & 0xF)) + \
                encoder.uint8(0) + \
                encoder.uint16(self.section_index)
        else:
            return encoder.uint32(self.name_index) + \
                encoder.uint8((self.binding << 4) | (self.type & 0xF)) + \
                encoder.uint8(0) + \
                encoder.uint16(self.section_index) + \
                encoder.uint64(self.value) + \
                encoder.uint64(self.content_size)
