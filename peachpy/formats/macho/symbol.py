# This file is part of PeachPy package and is licensed under the Simplified BSD license.
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
    def __init__(self, name, type, section, value=None):
        self.name = name
        self.visibility = 0
        self.type = type
        self.section = section
        self.description = 0
        self.flags = 0
        self.value = value

    @staticmethod
    def get_entry_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.pointer_size in [4, 8]

        return {4: 12, 8: 16}[abi.pointer_size]

    def encode(self, encoder, name_index_map, section_index_map, section_address_map):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert self.name in name_index_map
        assert self.section is None or self.section in section_index_map

        name_index = name_index_map[self.name]
        section_index = 0
        if self.section is not None:
            section_index = section_index_map[self.section]
        if encoder.bitness == 32:
            return encoder.uint32(name_index) + \
                encoder.uint8(self.type | self.visibility) + \
                encoder.uint8(section_index) + \
                encoder.uint16(self.description | self.flags) + \
                encoder.uint32(self.value)
        else:
            return encoder.uint32(name_index) + \
                encoder.uint8(self.type | self.visibility) + \
                encoder.uint8(section_index) + \
                encoder.uint16(self.description | self.flags) + \
                encoder.uint64(self.value + section_address_map[self.section])


class RelocationType(IntEnum):
    x86_64_unsigned = 0
    x86_64_signed = 1
    # CALL or JMP instruction with 32-bit displacement.
    x86_64_branch = 2
    # Load (MOVQ) of a 64-bit Global Offset Table entry
    x86_64_got_load = 3
    x86_64_got = 4
    x86_64_subtractor = 5
    # Signed 32-bit displacement with a -1 addend
    x86_64_signed_minus_1 = 6
    # Signed 32-bit displacement with a -2 addend
    x86_64_signed_minus_2 = 7
    # Signed 32-bit displacement with a -4 addend
    x86_64_signed_minus_4 = 8

    arm_vanilla = 0
    arm_pair = 1
    arm_sectdiff = 2
    arm_local_sectdiff = 3
    arm_pb_la_ptr = 4
    arm_br_24 = 5
    arm_half = 6
    arm_half_sectdiff = 7

    arm64_unsigned = 0
    arm64_subtractor = 1
    arm64_branch26 = 2
    arm64_page21 = 3
    arm64_pageoff12 = 4
    arm64_got_load_page21 = 5
    arm64_got_load_pageoff12 = 6
    arm64_pointer_to_got = 7
    arm64_tlvp_load_page21 = 8
    arm64_tlvp_load_pageoff12 = 9
    arm64_reloc_addend = 10


class Relocation:
    size = 8

    def __init__(self, type, offset, size, symbol, is_pc_relative=False):
        from peachpy.util import is_sint32
        assert is_sint32(offset)
        assert offset >= 0
        assert size in [1, 2, 4, 8]
        from peachpy.formats.macho.section import Section
        assert symbol is None or isinstance(symbol, (Section, Symbol))

        self.type = type
        self.offset = offset
        self.size = size
        self.symbol = symbol
        self.is_pc_relative = is_pc_relative

    def encode(self, encoder, section_index_map, symbol_index_map):
        from peachpy.formats.macho.section import Section
        from peachpy.util import ilog2

        symbol = 0
        if isinstance(self.symbol, Symbol):
            # Set "external" bit (bit 27) if referencing an external symbol
            symbol = symbol_index_map[self.symbol] | 0x8000000
        elif isinstance(self.symbol, Section):
            symbol = section_index_map[self.symbol]
        if self.is_pc_relative:
            # Set "pc_relative" bit (bit 24) if the relocation is relative to the program counter
            symbol |= 0x1000000
        log2_size = ilog2(self.size)
        symbol |= log2_size << 25
        symbol |= self.type << 28

        return encoder.uint32(self.offset) + encoder.uint32(symbol)
