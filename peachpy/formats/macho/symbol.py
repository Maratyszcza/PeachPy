# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class SymbolVisibility(IntEnum):
    external = 0x01
    private_external = 0x10


class SymbolType(IntEnum):
    undefined = 0x00
    prebound_undefined = 0x0C
    absolute = 0x02
    section_relative = 0x0E
    indirect = 0x0A


class SymbolDescription(IntEnum):
    undefined_lazy = 0x00
    undefined_non_lazy = 0x01
    defined = 0x02
    private_defined = 0x03
    private_undefined_lazy = 0x05
    private_undefined_non_lazy = 0x04


class SymbolFlags(IntEnum):
    referenced_dynamically = 0x10
    no_dead_strip = 0x20
    weak_reference = 0x40
    weak_definition = 0x80


class Symbol:
    def __init__(self, abi):
        self.abi = abi
        self.size = {4: 12, 8: 16}[abi.pointer_size]
        self.string_index = None
        self.visibility = 0
        self.type = None
        self.section_index = None
        self.description = 0
        self.flags = 0
        self.value = None

    @property
    def as_bytearray(self):
        import peachpy.encoder
        encoder = peachpy.encoder.Encoder(self.abi.endianness)

        if self.abi.pointer_size == 4:
            return encoder.uint32(self.string_index) + \
                encoder.uint8(self.type | self.visibility) + \
                encoder.uint8(self.section_index) + \
                encoder.uint16(self.description | self.flags) + \
                encoder.uint32(self.value)
        else:
            return encoder.uint32(self.string_index) + \
                encoder.uint8(self.type | self.visibility) + \
                encoder.uint8(self.section_index) + \
                encoder.uint16(self.description | self.flags) + \
                encoder.uint64(self.value)
