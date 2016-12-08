# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


def optional_rex(r, rm, force_rex=False):
    assert r in {0, 1}, "REX.R must be 0 or 1"
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    from peachpy.x86_64.registers import Register
    assert isinstance(rm, (Register, MemoryAddress, RIPRelativeOffset)), \
        "rm is expected to be a register or a memory address"
    b = 0
    x = 0
    if isinstance(rm, Register):
        b = rm.hcode
    elif isinstance(rm, MemoryAddress):
        if rm.base is not None:
            b = rm.base.hcode
        if rm.index is not None:
            x = rm.index.hcode
    # If REX.R, REX.X, and REX.B are all zeroes, REX prefix can be omitted
    if (r | x | b) == 0 and not force_rex:
        return bytearray()
    else:
        return bytearray([0x40 | (r << 2) | (x << 1) | b])


def rex(w, r, rm):
    assert w in {0, 1}, "REX.W must be 0 or 1"
    assert r in {0, 1}, "REX.R must be 0 or 1"
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    assert isinstance(rm, (MemoryAddress, RIPRelativeOffset)), \
        "rm is expected to be a memory address"
    b = 0
    x = 0
    if isinstance(rm, MemoryAddress):
        if rm.base is not None:
            b = rm.base.hcode
        if rm.index is not None:
            x = rm.index.hcode
    return bytearray([0x40 | (w << 3) | (r << 2) | (x << 1) | b])


def vex2(lpp, r, rm, vvvv=0, force_vex3=False):
    #                          2-byte VEX prefix:
    # Requires: VEX.W = 0, VEX.mmmmm = 0b00001 and VEX.B = VEX.X = 0
    #         +----------------+
    # Byte 0: | Bits 0-7: 0xC5 |
    #         +----------------+
    #
    #         +-----------+----------------+----------+--------------+
    # Byte 1: | Bit 7: ~R | Bits 3-6 ~vvvv | Bit 2: L | Bits 0-1: pp |
    #         +-----------+----------------+----------+--------------+
    #
    #
    #                          3-byte VEX prefix:
    #         +----------------+
    # Byte 0: | Bits 0-7: 0xC4 |
    #         +----------------+
    #
    #         +-----------+-----------+-----------+-------------------+
    # Byte 1: | Bit 7: ~R | Bit 6: ~X | Bit 5: ~B | Bits 0-4: 0b00001 |
    #         +-----------+-----------+-----------+-------------------+
    #
    #         +----------+-----------------+----------+--------------+
    # Byte 2: | Bit 7: 0 | Bits 3-6: ~vvvv | Bit 2: L | Bits 0-1: pp |
    #         +----------+-----------------+----------+--------------+
    assert lpp & ~0b111 == 0, "VEX.Lpp must be a 3-bit mask"
    assert r & ~0b1 == 0, "VEX.R must be a single-bit mask"
    assert vvvv & ~0b1111 == 0, "VEX.vvvv must be a 4-bit mask"
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    from peachpy.x86_64.registers import Register
    assert rm is None or isinstance(rm, (Register, MemoryAddress, RIPRelativeOffset)), \
        "rm is expected to be a register, a memory address, a rip-relative offset, or None"
    b = 0
    x = 0
    if rm is not None:
        if isinstance(rm, Register):
            b = rm.hcode
        elif isinstance(rm, MemoryAddress):
            if rm.base is not None:
                b = rm.base.hcode
            if rm.index is not None:
                x = rm.index.hcode
    # If VEX.B and VEX.X are zeroes, 2-byte VEX prefix can be used
    if (x | b) == 0 and not force_vex3:
        return bytearray([0xC5, 0xF8 ^ (r << 7) ^ (vvvv << 3) ^ lpp])
    else:
        return bytearray([0xC4, 0xE1 ^ (r << 7) ^ (x << 6) ^ (b << 5), 0x78 ^ (vvvv << 3) ^ lpp])


def vex3(escape, mmmmm, w____lpp, r, rm, vvvv=0):
    #                         3-byte VEX/XOP prefix
    #         +-----------------------------------+
    # Byte 0: | Bits 0-7: 0xC4 (VEX) / 0x8F (XOP) |
    #         +-----------------------------------+
    #
    #         +-----------+-----------+-----------+-----------------+
    # Byte 1: | Bit 7: ~R | Bit 6: ~X | Bit 5: ~B | Bits 0-4: mmmmm |
    #         +-----------+-----------+-----------+-----------------+
    #
    #         +----------+-----------------+----------+--------------+
    # Byte 2: | Bit 7: W | Bits 3-6: ~vvvv | Bit 2: L | Bits 0-1: pp |
    #         +----------+-----------------+----------+--------------+
    assert escape in {0xC4, 0x8F}, "escape must be a 3-byte VEX (0xC4) or XOP (0x8F) prefix"
    assert w____lpp & ~0b10000111 == 0, "VEX.W____Lpp is expected to have no bits set except 0, 1, 2 and 7"
    assert mmmmm & ~0b11111 == 0, "VEX.m-mmmm is expected to be a 5-bit mask"
    assert r & ~0b1 == 0, "VEX.R must be a single-bit mask"
    assert vvvv & ~0b1111 == 0, "VEX.vvvv must be a 4-bit mask"
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    assert isinstance(rm, (MemoryAddress, RIPRelativeOffset)), \
        "rm is expected to be a memory address or a rip-relative offset"
    b = 0
    x = 0
    if isinstance(rm, MemoryAddress):
        if rm.base is not None:
            b = rm.base.hcode
        if rm.index is not None:
            x = rm.index.hcode
    return bytearray([escape, 0xE0 ^ (r << 7) ^ (x << 6) ^ (b << 5) ^ mmmmm, 0x78 ^ (vvvv << 3) ^ w____lpp])


def evex(mm, w____1pp, ll, rr, rm, Vvvvv=0, aaa=0, z=0, b=0):
    assert mm & ~0b11 == 0, "EVEX.mm must be a 2-bit mask"
    assert w____1pp & ~0b10000011 == 0b100, "EVEX.W____1pp is expected to have no bits set except 0, 1, 2, and 7"
    assert ll & ~0b11 == 0, "EVEX.L'L must be a 2-bit mask"
    assert rr & ~0b11 == 0, "EVEX.R'R must be a 2-bit mask"
    assert Vvvvv & ~0b11111 == 0, "EVEX.v'vvvv must be a 5-bit mask"
    assert aaa & ~0b111 == 0, "EVEX.aaa must be a 3-bit mask"
    assert z & ~0b1 == 0, "EVEX.z must be a single-bit mask"
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    from peachpy.x86_64.registers import Register, XMMRegister, YMMRegister, ZMMRegister
    assert rm is None or isinstance(rm, (Register, MemoryAddress, RIPRelativeOffset)), \
        "rm is expected to be a register, a memory address, or None"
    r_, r = rr >> 1, rr & 1
    v_, vvvv = Vvvvv >> 4, Vvvvv & 0b1111
    b_ = 0
    x = 0
    if rm is not None:
        if isinstance(rm, Register):
            b_ = rm.hcode
            x = rm.ecode
        elif isinstance(rm, MemoryAddress):
            if rm.base is not None:
                b_ = rm.base.hcode
            if rm.index is not None:
                x = rm.index.hcode
                if isinstance(rm.index, (XMMRegister, YMMRegister, ZMMRegister)):
                    v_ = rm.index.ecode
    p0 = (r << 7) | (x << 6) | (b_ << 5) | (r_ << 4) | mm
    p1 = w____1pp | (vvvv << 3)
    p2 = (z << 7) | (ll << 5) | (b << 4) | (v_ << 3) | aaa
    # p0: invert RXBR' (bits 4-7)
    # p1: invert vvvv (bits 3-6)
    # p2: invert V' (bit 3)
    return bytearray([0x62, p0 ^ 0xF0, p1 ^ 0x78, p2 ^ 0x08])


def modrm_sib_disp(reg, rm, force_sib=False, min_disp=0, disp8xN=None):
    from peachpy.x86_64.operand import MemoryAddress, RIPRelativeOffset
    from peachpy.x86_64.registers import rsp, rbp, r13
    from peachpy.util import is_int, is_sint8, ilog2

    assert is_int(reg) and 0 <= reg <= 7, \
        "Constant reg value expected, got " + str(reg)
    assert isinstance(rm, (MemoryAddress, RIPRelativeOffset))

    if disp8xN is None:
        disp8xN = 1
    assert disp8xN in [1, 2, 4, 8, 16, 32, 64]

    #                    ModR/M byte
    # +----------------+---------------+--------------+
    # | Bits 6-7: mode | Bits 3-5: reg | Bits 0-2: rm |
    # +----------------+---------------+--------------+
    #
    #                         SIB byte
    # +-----------------+-----------------+----------------+
    # | Bits 6-7: scale | Bits 3-5: index | Bits 0-2: base |
    # +-----------------+-----------------+----------------+
    if isinstance(rm, MemoryAddress):
        # TODO: support global addresses, including rip-relative addresses
        assert rm.base is not None or rm.index is not None, \
            "Global addressing is not yet supported"
        if not force_sib and rm.index is None and rm.base.lcode != 0b100:
            # No SIB byte
            if rm.displacement == 0 and rm.base != rbp and rm.base != r13 and min_disp <= 0:
                # ModRM.mode = 0 (no displacement)

                assert rm.base.lcode != 0b100, \
                    "rsp/r12 are not encodable as a base register (interpreted as SIB indicator)"
                assert rm.base.lcode != 0b101, \
                    "rbp/r13 is not encodable as a base register (interpreted as disp32 address)"
                return bytearray([(reg << 3) | rm.base.lcode])
            elif (rm.displacement % disp8xN == 0) and is_sint8(rm.displacement // disp8xN) and min_disp <= 1:
                # ModRM.mode = 1 (8-bit displacement)

                assert rm.base.lcode != 0b100, \
                    "rsp/r12 are not encodable as a base register (interpreted as SIB indicator)"
                return bytearray([0x40 | (reg << 3) | rm.base.lcode, (rm.displacement // disp8xN) & 0xFF])
            else:
                # ModRM.mode == 2 (32-bit displacement)

                assert rm.base.lcode != 0b100, \
                    "rsp/r12 are not encodable as a base register (interpreted as SIB indicator)"
                return bytearray([0x80 | (reg << 3) | rm.base.lcode,
                                 rm.displacement & 0xFF, (rm.displacement >> 8) & 0xFF,
                                 (rm.displacement >> 16) & 0xFF, (rm.displacement >> 24) & 0xFF])
        else:
            # All encodings below use ModRM.rm = 4 (0b100) to indicate the presence of SIB

            assert rsp != rm.index, "rsp is not encodable as an index register (interpreted as no index)"
            # Index = 4 (0b100) denotes no-index encoding
            index = 0x4 if rm.index is None else rm.index.lcode
            scale = 0 if rm.scale is None else ilog2(rm.scale)
            if rm.base is None:
                # SIB.base = 5 (0b101) and ModRM.mode = 0 indicates no-base encoding with disp32

                return bytearray([(reg << 3) | 0x4, (scale << 6) | (index << 3) | 0x5,
                                 rm.displacement & 0xFF, (rm.displacement >> 8) & 0xFF,
                                 (rm.displacement >> 16) & 0xFF, (rm.displacement >> 24) & 0xFF])
            else:
                if rm.displacement == 0 and rm.base.lcode != 0b101 and min_disp <= 0:
                    # ModRM.mode == 0 (no displacement)

                    assert rm.base.lcode != 0b101, \
                        "rbp/r13 is not encodable as a base register (interpreted as disp32 address)"
                    return bytearray([(reg << 3) | 0x4, (scale << 6) | (index << 3) | rm.base.lcode])
                elif (rm.displacement % disp8xN == 0) and is_sint8(rm.displacement // disp8xN) and min_disp <= 1:
                    # ModRM.mode == 1 (8-bit displacement)

                    return bytearray([(reg << 3) | 0x44, (scale << 6) | (index << 3) | rm.base.lcode,
                                      (rm.displacement // disp8xN) & 0xFF])
                else:
                    # ModRM.mode == 2 (32-bit displacement)

                    return bytearray([(reg << 3) | 0x84, (scale << 6) | (index << 3) | rm.base.lcode,
                                     rm.displacement & 0xFF, (rm.displacement >> 8) & 0xFF,
                                     (rm.displacement >> 16) & 0xFF, (rm.displacement >> 24) & 0xFF])
    elif isinstance(rm, RIPRelativeOffset):
        # ModRM.mode == 0 and ModeRM.rm == 5 (0b101) indicates (rip + disp32) addressing
        return bytearray([0b00000101 | (reg << 3),
                          rm.offset & 0xFF, (rm.offset >> 8) & 0xFF,
                          (rm.offset >> 16) & 0xFF, (rm.offset >> 24) & 0xFF])


def nop(length):
    assert 1 <= length <= 15
    # Note: the generated NOPs must be allowed by NaCl validator, see
    # https://src.chromium.org/viewvc/native_client/trunk/src/native_client/src/trusted/validator_ragel/instruction_definitions/general_purpose_instructions.def
    # https://src.chromium.org/viewvc/native_client/trunk/src/native_client/src/trusted/validator_ragel/instruction_definitions/nops.def
    return {
        1: bytearray([0x90]),
        2: bytearray([0x40, 0x90]),
        3: bytearray([0x0F, 0x1F, 0x00]),
        4: bytearray([0x0F, 0x1F, 0x40, 0x00]),
        5: bytearray([0x0F, 0x1F, 0x44, 0x00, 0x00]),
        6: bytearray([0x66, 0x0F, 0x1F, 0x44, 0x00, 0x00]),
        7: bytearray([0x0F, 0x1F, 0x80, 0x00, 0x00, 0x00, 0x00]),
        8: bytearray([0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        9: bytearray([0x66, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        10: bytearray([0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        11: bytearray([0x66, 0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        12: bytearray([0x66, 0x66, 0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        13: bytearray([0x66, 0x66, 0x66, 0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        14: bytearray([0x66, 0x66, 0x66, 0x66, 0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00]),
        15: bytearray([0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x2E, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00])
    }[length]


class Flags:
    AccumulatorOp0 = 0x01
    AccumulatorOp1 = 0x02
    Rel8Label = 0x04
    Rel32Label = 0x08
    ModRMSIBDisp = 0x10
    OptionalREX = 0x20
    VEX2 = 0x40


class Options:
    Disp8 = 0x01
    Disp32 = 0x02
    SIB = 0x04
    REX = 0x08
    VEX3 = 0x10