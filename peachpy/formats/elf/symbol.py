# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import IntEnum


class SymbolBinding(IntEnum):
    local = 0
    global_ = 1
    weak = 2


class SymbolType:
    # No type specified (e.g. an absolute symbol)
    unspecified = 0
    # Data object
    data_object = 1
    # Function entry point
    function = 2
    # Symbol associated with a section
    section = 3
    # Source file associated with the object file
    file = 4


class Symbol:
    def __init__(self):
        # Symbol name
        self.name = None
        # Value of the symbol (typically offset from the section)
        self.value = None
        # Size of the data object (0 if size is unknown or meaningless)
        self.size = 0
        # Binding attribute
        self.binding = 0
        # Type attribute
        self.type = 0
        # The relevant section in the section header table
        self.section = None

    @staticmethod
    def get_entry_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.elf_bitness in [32, 64]

        return {32: 16, 64: 24}[abi.elf_bitness]

    def encode(self, encoder, name_index_map, section_index_map):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert encoder.bitness in [32, 64]
        assert self.name in name_index_map
        from peachpy.formats.elf.section import SectionIndex
        assert self.section is None or isinstance(self.section, SectionIndex) or self.section in section_index_map

        name_index = name_index_map[self.name]
        section_index = SectionIndex.absolute
        if self.section is not None:
            if isinstance(self.section, SectionIndex):
                section_index = self.section
            else:
                section_index = section_index_map[self.section]
        if encoder.bitness == 32:
            return encoder.uint32(name_index) + \
                encoder.uint32(self.value) + \
                encoder.uint32(self.size) + \
                encoder.uint8((self.binding << 4) | (self.type & 0xF)) + \
                encoder.uint8(0) + \
                encoder.uint16(section_index)
        else:
            return encoder.uint32(name_index) + \
                encoder.uint8((self.binding << 4) | (self.type & 0xF)) + \
                encoder.uint8(0) + \
                encoder.uint16(section_index) + \
                encoder.uint64(self.value) + \
                encoder.uint64(self.size)


class RelocationType(IntEnum):
    x86_32 = 1
    x86_pc32 = 2
    x86_got32 = 3
    x86_plt32 = 4
    x86_copy = 5
    x86_glob_dat = 6
    x86_jmp_slot = 7
    x86_relative = 8
    x86_gotoff = 9
    x86_gotpc = 10

    x86_64_64 = 1
    x86_64_pc32 = 2
    x86_64_got32 = 3
    x86_64_plt32 = 4
    x86_64_copy = 5
    x86_64_glob_dat = 6
    x86_64_jump_slot = 7
    x86_64_relative = 8
    x86_64_gotpcrel = 9
    x86_64_32 = 10
    x86_64_32s = 11
    x86_64_16 = 12
    x86_64_pc16 = 13
    x86_64_8 = 14
    x86_64_pc8 = 15
    x86_64_dtpmod64 = 16
    x86_64_dtpoff64 = 17
    x86_64_tpoff64 = 18
    x86_64_tlsgd = 19
    x86_64_tlsld = 20
    x86_64_dtpoff32 = 21
    x86_64_gottpoff = 22
    x86_64_tpoff32 = 23
    x86_64_pc64 = 24
    x86_64_gotoff64 = 25
    x86_64_gotpc32 = 26
    x86_64_got64 = 27
    x86_64_gotpcrel64 = 28
    x86_64_gotpc64 = 29
    x86_64_gotplt64 = 30
    x86_64_pltoff64 = 31
    x86_64_size32 = 32
    x86_64_size64 = 33
    x86_64_gotpc32_tlsdesc = 34
    x86_64_tlsdesc_call = 35
    x86_64_tlsdesc = 36
    x86_64_irelative = 37

    arm_abs32 = 2
    arm_rel32 = 3
    arm_ldr_pc_g0 = 4
    arm_abs16 = 5
    arm_abs12 = 6
    arm_thm_abs5 = 7
    arm_abs8 = 8
    arm_sbrel32 = 9
    arm_thm_call = 10
    arm_thm_pc8 = 11
    arm_brel_adj = 12
    arm_tls_desc = 13
    arm_tls_dtpmod32 = 17
    arm_tls_dtpoff32 = 18
    arm_tls_tpoff32 = 19
    arm_copy = 20
    arm_glob_dat = 21
    arm_jump_slot = 22
    arm_relative = 23
    arm_gotoff32 = 24
    arm_base_prel = 25
    arm_got_brel = 26
    arm_plt32 = 27
    arm_call = 28
    arm_jump24 = 29
    arm_thm_jump24 = 30
    arm_base_abs = 31
    arm_target1 = 38
    arm_v4bx = 40
    arm_target2 = 41
    arm_prel31 = 42
    arm_movw_abs_nc = 43
    arm_movt_abs = 44
    arm_movw_prel_nc = 45
    arm_movt_prel = 46
    arm_thm_movw_abs_nc = 47
    arm_thm_movt_abs = 48
    arm_thm_movw_prel_nc = 49
    arm_thm_movt_prel = 50
    arm_thm_jump19 = 51
    arm_thm_jump6 = 52
    arm_thm_alu_prel_11_0 = 53
    arm_thm_pc12 = 54
    arm_abs32_noi = 55
    arm_rel32_noi = 56
    arm_alu_pc_g0_nc = 57
    arm_alu_pc_g0 = 58
    arm_alu_pc_g1_nc = 59
    arm_alu_pc_g1 = 60
    arm_alu_pc_g2 = 61
    arm_ldr_pc_g1 = 62
    arm_ldr_pc_g2 = 63
    arm_ldrs_pc_g0 = 64
    arm_ldrs_pc_g1 = 65
    arm_ldrs_pc_g2 = 66
    arm_ldc_pc_g0 = 67
    arm_ldc_pc_g1 = 68
    arm_ldc_pc_g2 = 69
    arm_alu_sb_g0_nc = 70
    arm_alu_sb_g0 = 71
    arm_alu_sb_g1_nc = 72
    arm_alu_sb_g1 = 73
    arm_alu_sb_g2 = 74
    arm_ldr_sb_g0 = 75
    arm_ldr_sb_g1 = 76
    arm_ldr_sb_g2 = 77
    arm_ldrs_sb_g0 = 78
    arm_ldrs_sb_g1 = 79
    arm_ldrs_sb_g2 = 80
    arm_ldc_sb_g0 = 81
    arm_ldc_sb_g1 = 82
    arm_ldc_sb_g2 = 83
    arm_movw_brel_nc = 84
    arm_movt_brel = 85
    arm_movw_brel = 86
    arm_thm_movw_brel_nc = 87
    arm_thm_movt_brel = 88
    arm_thm_movw_brel = 89
    arm_tls_gotdesc = 90
    arm_tls_call = 91
    arm_tls_descseq = 92
    arm_thm_tls_call = 93
    arm_plt32_abs = 94
    arm_got_abs = 95
    arm_got_prel = 96
    arm_got_brel12 = 97
    arm_gotoff12 = 98
    arm_gotrelax = 99
    arm_thm_jump11 = 102
    arm_thm_jump8 = 103
    arm_tls_gd32 = 104
    arm_tls_ldm32 = 105
    arm_tls_ldo32 = 106
    arm_tls_ie32 = 107
    arm_tls_le32 = 108
    arm_tls_ldo12 = 109
    arm_tls_le12 = 110
    arm_tls_ie12gp = 111
    arm_thm_tls_descseq16 = 129
    arm_thm_tls_descseq32 = 130
    arm_thm_got_brel12 = 131


class RelocationWithAddend:
    def __init__(self, type, offset, symbol, addend):
        from peachpy.util import is_uint64, is_sint64
        assert isinstance(type, RelocationType)
        assert is_uint64(offset)
        assert isinstance(symbol, Symbol)
        assert is_sint64(addend)

        self.type = type
        self.offset = offset
        self.symbol = symbol
        self.addend = addend

    @staticmethod
    def get_entry_size(abi):
        from peachpy.abi import ABI
        assert isinstance(abi, ABI)
        assert abi.elf_bitness in [32, 64]

        return {32: 12, 64: 24}[abi.elf_bitness]

    def encode(self, encoder, symbol_index_map):
        import peachpy.encoder
        assert isinstance(encoder, peachpy.encoder.Encoder)
        assert encoder.bitness in [32, 64]
        assert self.symbol in symbol_index_map

        symbol_index = symbol_index_map[self.symbol]
        info = (symbol_index << 32) | self.type

        return encoder.unsigned_offset(self.offset) + \
            encoder.unsigned_offset(info) + \
            encoder.signed_offset(self.addend)
