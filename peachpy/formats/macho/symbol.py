# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class SymbolVisibility:
    External = 0x01
    PrivateExternal = 0x10


class SymbolType:
    Undefined = 0x00
    PreboundUndefined = 0x0C
    Absolute = 0x02
    SectionRelative = 0x0E
    Indirect = 0x0A


class SymbolDescription:
    UndefinedLazy = 0x00
    UndefinedNonLazy = 0x01
    Defined = 0x02
    PrivateDefined = 0x03
    PrivateUndefinedLazy = 0x05
    PrivateUndefinedNonLazy = 0x04


class SymbolFlags:
    ReferencedDynamically = 0x10
    NoDeadStrip = 0x20
    WeakReference = 0x40
    WeakDefinition = 0x80


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
