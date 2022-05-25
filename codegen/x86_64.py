# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
import opcodes
import copy
import six
from opcodes.x86_64 import *
from codegen.code import CodeWriter, CodeBlock
import operator
import json
import os

instruction_set = read_instruction_set()
for instruction in instruction_set:
    extra_instruction_forms = []
    for instruction_form in instruction.forms:
        if any(operand.type in ["{sae}", "{er}"] for operand in instruction_form.operands):
            new_instruction_form = copy.deepcopy(instruction_form)
            new_instruction_form.operands = \
                [operand for operand in new_instruction_form.operands if operand.type not in ["{sae}", "{er}"]]
            new_evex = next(component for component in new_instruction_form.encodings[0].components
                            if isinstance(component, EVEX))
            new_evex.LL = 0b10
            new_evex.b = 0
            extra_instruction_forms.append(new_instruction_form)
            old_evex = next(component for component in instruction_form.encodings[0].components
                            if isinstance(component, EVEX))
            if not isinstance(old_evex.LL, Operand):
                # EVEX.LL didn't encode rounding control.

                # Set LL to 0.
                # This is contrary to Intel spec (319433-023), but this is what binutils does. See discussion at
                # https://software.intel.com/en-us/forums/intel-isa-extensions/topic/562664
                old_evex.LL = 0
            old_evex.b = 1
    instruction.forms.extend(extra_instruction_forms)

instruction_groups = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "x86_64.json")))


def filter_instruction_forms(instruction_forms):
    """Removes the instruction forms that are currently not supported"""

    new_instruction_forms = list()
    for instruction_form in instruction_forms:
        if all([operand.type not in {"r8l", "r16l", "r32l", "moffs32", "moffs64"} for operand in instruction_form.operands]):
            new_instruction_forms.append(instruction_form)
    return new_instruction_forms


def is_avx512_instruction_form(instruction_form):
    """Indicates whether the instruction form belongs to AVX512 extensions"""
    return instruction_form.isa_extensions and instruction_form.isa_extensions[0].name.startswith("AVX512")


def aggregate_instruction_forms(instruction_forms):
    """Hierarhically chains instruction forms

    Combines operand types that differ only by a single operand together
    """

    nested_operand_types = {
        ("1", "imm8"),
        ("3", "imm8"),
        ("rel8", "rel32"),
        ("imm8", "imm16"),
        ("imm8", "imm32"),
        ("imm16", "imm32"),
        ("imm32", "imm64"),
        ("al", "r8"),
        ("ax", "r16"),
        ("eax", "r32"),
        ("rax", "r64")
    }

    def find_single_operand_difference(form, other_form):
        """Checks if two forms differ only by a single operand type and returns the operand number"""
        if form == other_form:
            return None
        if len(form.operands) != len(other_form.operands):
            return None
        different_operand_numbers = \
            list(filter(lambda n: form.operands[n].type != other_form.operands[n].type,
                        range(len(form.operands))))
        if len(different_operand_numbers) == 1:
            return different_operand_numbers[0]
        else:
            return None

    from collections import OrderedDict
    new_instruction_forms = OrderedDict()
    for form in instruction_forms:
        for other_form in instruction_forms:
            n = find_single_operand_difference(form, other_form)
            if n is not None and (form.operands[n].type, other_form.operands[n].type) in nested_operand_types:
                break
        else:
            new_instruction_forms[form] = []

    for form in instruction_forms:
        for other_form in instruction_forms:
            n = find_single_operand_difference(form, other_form)
            if n is not None and (form.operands[n].type, other_form.operands[n].type) in nested_operand_types:
                assert other_form.isa_extensions == form.isa_extensions
                assert other_form.mmx_mode == form.mmx_mode
                assert other_form.xmm_mode == form.xmm_mode
                if other_form in new_instruction_forms:
                    new_instruction_forms[other_form].insert(0, (n, form))
                    break
    return new_instruction_forms


def generate_operand_check(operand_index, operand,
                           ignore_imm_size=True, ext_imm_size=None, lambda_form=False, evex_form=False):
    check_map = {
        "r8": "is_r8(%s)",
        "r16": "is_r16(%s)",
        "r32": "is_r32(%s)",
        "r64": "is_r64(%s)",
        "mm": "is_mm(%s)",
        "xmm": "is_xmm(%s)",
        "xmm{k}": "is_xmmk(%s)",
        "xmm{k}{z}": "is_xmmkz(%s)",
        "ymm": "is_ymm(%s)",
        "ymm{k}": "is_ymmk(%s)",
        "ymm{k}{z}": "is_ymmkz(%s)",
        "zmm": "is_zmm(%s)",
        "zmm{k}": "is_zmmk(%s)",
        "zmm{k}{z}": "is_zmmkz(%s)",
        "k": "is_k(%s)",
        "k{k}": "is_kk(%s)",
        "m": "is_m(%s)",
        "m8": "is_m8(%s)",
        "m16": "is_m16(%s)",
        "m16{k}{z}": "is_m16kz(%s)",
        "m32": "is_m32(%s)",
        "m32{k}": "is_m32k(%s)",
        "m32{k}{z}": "is_m32kz(%s)",
        "m64": "is_m64(%s)",
        "m64{k}": "is_m64k(%s)",
        "m64{k}{z}": "is_m64kz(%s)",
        "m128": "is_m128(%s)",
        "m128{k}{z}": "is_m128kz(%s)",
        "m256": "is_m256(%s)",
        "m256{k}{z}": "is_m256kz(%s)",
        "m512": "is_m512(%s)",
        "m512{k}{z}": "is_m512kz(%s)",
        "m64/m32bcst": "is_m64_m32bcst(%s)",
        "m128/m32bcst": "is_m128_m32bcst(%s)",
        "m256/m32bcst": "is_m256_m32bcst(%s)",
        "m512/m32bcst": "is_m512_m32bcst(%s)",
        "m128/m64bcst": "is_m128_m64bcst(%s)",
        "m256/m64bcst": "is_m256_m64bcst(%s)",
        "m512/m64bcst": "is_m512_m64bcst(%s)",
        "vm32x": "is_vmx(%s)",
        "vm64x": "is_vmx(%s)",
        "vm32x{k}": "is_vmxk(%s)",
        "vm64x{k}": "is_vmxk(%s)",
        "vm32y": "is_vmy(%s)",
        "vm64y": "is_vmy(%s)",
        "vm32y{k}": "is_vmyk(%s)",
        "vm64y{k}": "is_vmyk(%s)",
        "vm32z": "is_vmz(%s)",
        "vm64z": "is_vmz(%s)",
        "vm32z{k}": "is_vmzk(%s)",
        "vm64z{k}": "is_vmzk(%s)",
        "imm": "is_imm(%s)",
        "imm4": "is_imm4(%s)",
        "imm8": "is_imm8(%s)",
        "imm16": "is_imm16(%s)",
        "imm32": "is_imm32(%s)",
        "imm64": "is_imm64(%s)",
        "rel32": "is_rel32(%s)",
        "rel8": "is_rel8(%s)",
        "al": "is_al(%s)",
        "cl": "is_cl(%s)",
        "ax": "is_ax(%s)",
        "eax": "is_eax(%s)",
        "rax": "is_rax(%s)",
        "xmm0": "is_xmm0(%s)",
        "1": "%s == 1",
        "3": "%s == 3",
        "{er}": "is_er(%s)",
        "{sae}": "is_sae(%s)"
    }
    evex_check_map = {
        "xmm": "is_evex_xmm(%s)",
        "ymm": "is_evex_ymm(%s)",
        "vm32x": "is_evex_vmx(%s)",
        "vm64x": "is_evex_vmx(%s)",
        "vm32y": "is_evex_vmy(%s)",
        "vm64y": "is_evex_vmy(%s)",
    }
    imm_check_map = {
        "imm4": "is_imm4(%s, ext_size=%d)",
        "imm8": "is_imm8(%s, ext_size=%d)",
        "imm16": "is_imm16(%s, ext_size=%d)",
        "imm32": "is_imm32(%s, ext_size=%d)",
    }
    imm_map = {
        "imm4": "imm",
        "imm8": "imm",
        "imm16": "imm",
        "imm32": "imm",
        "imm64": "imm"
    }
    optype = operand.type
    assert optype in check_map, "Unknown operand type: " + optype
    operands = "op" if lambda_form else "self.operands"
    if ignore_imm_size:
        optype = imm_map.get(optype, optype)
    if ext_imm_size is not None and optype in imm_check_map:
        return imm_check_map[optype] % (operands + "[" + str(operand_index) + "]", ext_imm_size)
    elif evex_form and optype in evex_check_map:
        return evex_check_map[optype] % (operands + "[" + str(operand_index) + "]")
    else:
        return check_map[optype] % (operands + "[" + str(operand_index) + "]")


def generate_isa_extensions(extensions):
    assert len(extensions) == 1
    extension_map = {
        "MMX+": "MMXPlus"
    }
    extension = extensions[0]
    return "Extension.%s" % extension_map.get(extension, extension)


class Flags:
    AccumulatorOp0 = 0x01
    AccumulatorOp1 = 0x02
    Rel8Label = 0x04
    Rel32Label = 0x08
    ModRMSIBDisp = 0x10
    OptionalREX = 0x20
    VEX2 = 0x40
    EVEX = 0x80


def generate_encoding_lambda(encoding, operands, use_off_argument=False):
    byte_sequence = []
    parts = []
    flags = 0
    disp8xN = None

    def generate_bytes(byte_sequence):
        if byte_sequence:
            parts.append("bytearray([%s])" % ", ".join(byte_sequence))
        return []

    for component in encoding.components:
        if isinstance(component, Prefix):
            prefix = "0x%02X" % component.byte
            byte_sequence.append(prefix)
        elif isinstance(component, REX):
            component.set_ignored()
            if component.is_mandatory:
                if isinstance(component.X, Operand):
                    assert component.X == component.B and component.X.is_memory, \
                        "REX.X must refers to the same memory operand as REX.B. " \
                        "Register operands must have constant REX.X"
                    byte_sequence = generate_bytes(byte_sequence)

                    rex_args = [str(component.W)]
                    if isinstance(component.R, Operand):
                        rex_args.append("op[%d].hcode" % operands.index(component.R))
                    else:
                        rex_args.append(str(component.R))
                    rex_args.append("op[%d].address" % operands.index(component.X))
                    rex = "rex(%s)" % ", ".join(rex_args)
                    parts.append(rex)
                else:
                    assert not isinstance(component.B, Operand) or component.B.is_register, \
                        "Memory operands must have non-constant REX.B"
                    assert component.X in {0, 1}

                    rex_byte = 0x40 | (component.W << 3)
                    rex_parts = []
                    if isinstance(component.R, Operand):
                        rex_parts.append("op[%d].hcode << 2" % operands.index(component.R))
                    else:
                        rex_byte |= component.R << 2
                    if isinstance(component.B, Operand):
                        rex_parts.append("op[%d].hcode" % operands.index(component.B))
                    else:
                        rex_byte |= component.B
                    rex_byte |= component.X << 1
                    rex = " | ".join(["0x%02X" % rex_byte] + rex_parts)
                    byte_sequence.append(rex)
            else:
                assert component.W == 0, "Instructions with REX.W == 1 must mandate REX prefix"
                byte_sequence = generate_bytes(byte_sequence)

                rex_args = []
                if isinstance(component.R, Operand):
                    rex_args.append("op[%d].hcode" % operands.index(component.R))
                else:
                    rex_args.append(str(component.R))
                if isinstance(component.X, Operand):
                    assert component.X == component.B and component.X.is_memory, \
                        "REX.X must refers to the same memory operand as REX.B. " \
                        "Register operands must have constant REX.X"

                    rex_args.append("op[%d].address" % operands.index(component.X))
                else:
                    assert not isinstance(component.B, Operand) or component.B.is_register, \
                        "Memory operands must have non-constant REX.B"

                    rex_args.append("op[%d]" % operands.index(component.B))
                r8_operands = [i for (i, op) in enumerate(operands) if op.type == "r8"]
                force_rex_conditions = ["rex"]
                for r8_operand in r8_operands:
                    force_rex_conditions.append("is_r8rex(op[%d])" % r8_operand)
                rex_args.append(" or ".join(force_rex_conditions))
                rex = "optional_rex(%s)" % ", ".join(rex_args)
                flags |= Flags.OptionalREX
                parts.append(rex)
        elif isinstance(component, VEX):
            component.set_ignored()
            if component.type == "VEX" and component.mmmmm == 0b00001 and component.W == 0:
                if component.R == 1 and component.X == 1 and component.B == 1:
                    # VZEROUPPER and VZEROALL instructions are VEX-encoded and have no arguments
                    byte_sequence.append("0xC5")
                    byte_sequence.append("0x%02X" % (0xF8 | component.L << 2 | component.pp))
                else:
                    byte_sequence = generate_bytes(byte_sequence)

                    vex_args = [str(component.L << 2 | component.pp)]

                    if isinstance(component.R, Operand):
                        vex_args.append("op[%d].hcode" % operands.index(component.R))
                    else:
                        assert component.R == 0
                        vex_args.append("0")

                    if isinstance(component.X, Operand):
                        assert component.X == component.B and component.X.is_memory, \
                            "VEX.X must refers to the same memory operand as VEX.B. " \
                            "Register operands must have constant VEX.X"

                        vex_args.append("op[%d].address" % operands.index(component.X))
                    else:
                        assert not isinstance(component.B, Operand) or component.B.is_register, \
                            "Memory operands must have non-constant VEX.B"

                        if isinstance(component.B, Operand):
                            vex_args.append("op[%d]" % operands.index(component.B))
                        else:
                            assert component.B == 0
                            vex_args.append("None")

                    if isinstance(component.vvvv, Operand):
                        vex_args.append("op[%d].hlcode" % operands.index(component.vvvv))
                    else:
                        assert component.vvvv == 0b0000
                        vex_args.append("0")

                    vex_args.append("vex3")

                    vex = "vex2(%s)" % ", ".join(vex_args)
                    flags |= Flags.VEX2
                    parts.append(vex)
            else:
                if isinstance(component.X, Operand):
                    assert component.X == component.B and component.X.is_memory, \
                        "VEX.X must refers to the same memory operand as VEX.B. " \
                        "Register operands must have constant VEX.X"

                    byte_sequence = generate_bytes(byte_sequence)

                    vex_args = [{"VEX": "0xC4", "XOP": "0x8F"}[component.type],
                                bin(component.mmmmm),
                                "0x%02X" % (component.W << 7 | component.L << 2 | component.pp)]

                    if isinstance(component.R, Operand):
                        vex_args.append("op[%d].hcode" % operands.index(component.R))
                    else:
                        assert component.R == 0
                        vex_args.append("0")

                    vex_args.append("op[%d].address" % operands.index(component.X))

                    if isinstance(component.vvvv, Operand):
                        vex_args.append("op[%d].hlcode" % operands.index(component.vvvv))
                    else:
                        assert component.vvvv == 0b0000

                    vex = "vex3(%s)" % ", ".join(vex_args)
                    parts.append(vex)
                else:
                    assert isinstance(component.B, Operand) and component.B.is_register or component.B == 0, \
                        "Memory operands must have non-constant VEX.B"

                    byte_sequence.append({"VEX": "0xC4", "XOP": "0x8F"}[component.type])

                    vex_byte1 = "0x%02X" % (0xE0 | component.mmmmm)
                    if isinstance(component.R, Operand):
                        vex_byte1 += " ^ (op[%d].hcode << 7)" % operands.index(component.R)
                    else:
                        assert component.R == 0

                    if isinstance(component.B, Operand):
                        vex_byte1 += " ^ (op[%d].hcode << 5)" % operands.index(component.B)
                    else:
                        assert component.B == 0

                    byte_sequence.append(vex_byte1)

                    if isinstance(component.vvvv, Operand):
                        byte_sequence.append("0x%02X ^ (op[%d].hlcode << 3)" %
                                             (0x78 | (component.W << 7) | (component.L << 2) | component.pp,
                                             operands.index(component.vvvv)))
                    else:
                        assert component.vvvv == 0b0000
                        byte_sequence.append("0x%02X" % (0x78 | (component.W << 7) | (component.L << 2) | component.pp))

        elif isinstance(component, EVEX):
            disp8xN = component.disp8xN
            component.set_ignored()
            if component.X.is_memory:
                assert component.X is component.B
                evex_args = ["0b" + format(component.mm, "02b"), "0x%02X" % (component.W << 7 | component.pp | 0b100)]
                if isinstance(component.LL, Operand):
                    evex_args.append("op[%d].code" % operands.index(component.LL))
                else:
                    evex_args.append("0b" + format(component.LL, "02b"))
                if isinstance(component.RR, Operand):
                    evex_args.append("op[%d].ehcode" % operands.index(component.RR))
                else:
                    evex_args.append(str(component.RR))
                evex_args.append("op[%d].address" % operands.index(component.X))
                if component.vvvv != 0:
                    assert component.vvvv is component.V
                    # Component.V | Compnent.vvvv encode the operand
                    evex_args.append("op[%d].code" % operands.index(component.vvvv))
                else:
                    assert component.V == 0 or isinstance(component.V, Operand) and component.V.is_memory
                if component.aaa != 0:
                    evex_args.append("aaa=op[%d].kcode" % operands.index(component.aaa))
                if component.z != 0:
                    evex_args.append("z=op[%d].zcode" % operands.index(component.z))
                if isinstance(component.b, Operand):
                    evex_args.append("b=op[%d].bcode" % operands.index(component.b))
                elif component.b != 0:
                    evex_args.append("b=" + str(component.b))
                evex = "evex(%s)" % ", ".join(evex_args)
                flags |= Flags.EVEX
                parts.append(evex)
            else:
                byte_sequence.append("0x62")
                if isinstance(component.RR, Operand):
                    byte_sequence.append("((op[%d].hcode << 7) | (op[%d].ehcode << 5) | (op[%d].ecode << 4)) ^ %d" %
                                         (operands.index(component.RR), operands.index(component.B),
                                          operands.index(component.RR), 0xF0 | component.mm))
                else:
                    r = component.RR & 1
                    r_ = (component.RR >> 1) & 1
                    byte = (component.mm | (r << 7) | (r_ << 4)) ^ 0xF0
                    if byte == 0:
                        byte_sequence.append("op[%d].ehcode << 5" % operands.index(component.B))
                    else:
                        byte_sequence.append("(op[%d].ehcode << 5) ^ 0x%02X" % (operands.index(component.B), byte))
                if isinstance(component.vvvv, Operand):
                    byte_sequence.append("0x%02X ^ (op[%d].hlcode << 3)" %
                                         (component.W << 7 | component.pp | 0b01111100, operands.index(component.vvvv)))
                else:
                    assert component.vvvv == 0
                    byte_sequence.append("0x%02X" % (component.W << 7 | component.pp | 0b01111100))
                byte = component.b << 4
                byte_parts = []
                if isinstance(component.z, Operand):
                    byte_parts.append("(op[%d].zcode << 7)" % operands.index(component.z))
                else:
                    byte |= component.z << 7
                if isinstance(component.LL, Operand):
                    byte_parts.append("(op[%d].code << 5)" % operands.index(component.LL))
                else:
                    byte |= component.LL << 5
                if isinstance(component.V, Operand):
                    byte_parts.append("(op[%d].ecode << 3 ^ 0x8)" % operands.index(component.V))
                else:
                    byte |= (component.V ^ 1) << 3
                if isinstance(component.aaa, Operand):
                    byte_parts.append("op[%d].kcode" % operands.index(component.aaa))
                else:
                    assert component.aaa == 0
                byte_parts.append("0x%02X" % byte)
                byte_sequence.append(" | ".join(byte_parts))
        elif isinstance(component, Opcode):
            opcode = "0x%02X" % component.byte
            if component.addend:
                opcode += " | op[%d].lcode" % operands.index(component.addend)
            byte_sequence.append(opcode)
        elif isinstance(component, ModRM):
            if isinstance(component.mode, Operand):
                assert component.mode == component.rm and component.rm.is_memory, \
                    "Mod R/M:mode must refer to the same memory operand as Mod R/M:rm. " \
                    "Register operands must have Mod R/M:mode == 0b11"
                byte_sequence = generate_bytes(byte_sequence)

                if isinstance(component.reg, Operand):
                    modrm_reg = "op[%d].lcode" % operands.index(component.reg)
                else:
                    modrm_reg = str(component.reg)
                modrm_rm = "op[%d].address" % operands.index(component.rm)

                if disp8xN is None:
                    modrm = "modrm_sib_disp(%s, %s, sib, min_disp)" % (modrm_reg, modrm_rm)
                else:
                    modrm = "modrm_sib_disp(%s, %s, sib, min_disp, disp8xN=%d)" % (modrm_reg, modrm_rm, disp8xN)
                flags |= Flags.ModRMSIBDisp
                parts.append(modrm)
            else:
                assert component.mode == 0b11 and component.rm.is_register, \
                    "Register operands must have Mod R/M:mode == 0b11. " \
                    "For memory operands Mod R/M:mode must refer to an operand object"
                modrm_byte = component.mode << 6
                modrm_parts = []
                if isinstance(component.reg, Operand):
                    modrm_parts.append("op[%d].lcode << 3" % operands.index(component.reg))
                elif component.reg:
                    modrm_byte |= component.reg << 3
                modrm_parts.append("op[%d].lcode" % operands.index(component.rm))
                modrm = " | ".join(["0x%02X" % modrm_byte] + modrm_parts)
                byte_sequence.append(modrm)
        elif isinstance(component, Immediate):
            assert component.size in {1, 2, 4, 8}
            if component.size == 1:
                if isinstance(component.value, Operand):
                    ib = "op[%d] & 0xFF" % operands.index(component.value)
                else:
                    ib = "0x%02X" % component.value
                byte_sequence.append(ib)
            elif component.size == 2:
                assert isinstance(component.value, Operand)
                iw = ["op[%d] & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 8) & 0xFF" % operands.index(component.value)]
                byte_sequence.extend(iw)
            elif component.size == 4:
                assert isinstance(component.value, Operand)
                id = ["op[%d] & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 8) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 16) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 24) & 0xFF" % operands.index(component.value)]
                byte_sequence.extend(id)
            elif component.size == 8:
                assert isinstance(component.value, Operand)
                iq = ["op[%d] & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 8) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 16) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 24) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 32) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 40) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 48) & 0xFF" % operands.index(component.value),
                      "(op[%d] >> 56) & 0xFF" % operands.index(component.value)]
                byte_sequence.extend(iq)
        elif isinstance(component, RegisterByte):
            ibr = "op[%d].hlcode << 4" % operands.index(component.register)
            if component.payload is not None:
                assert isinstance(component.payload, Operand)
                ibr += " | op[%d] & 0xF" % operands.index(component.payload)
            byte_sequence.append(ibr)
        elif isinstance(component, CodeOffset):
            assert component.size in {1, 4}
            if component.size == 1:
                if use_off_argument:
                    byte_sequence.append("off & 0xFF")
                else:
                    byte_sequence.append("op[%d].offset & 0xFF" % operands.index(component.value))
            elif component.size == 4:
                if use_off_argument:
                    byte_sequence.extend([
                        "off & 0xFF", "(off >> 8) & 0xFF", "(off >> 16) & 0xFF", "(off >> 24) & 0xFF"
                    ])

                else:
                    byte_sequence.extend([
                        "op[%d].offset & 0xFF" % operands.index(component.value),
                        "(op[%d].offset >> 8) & 0xFF" % operands.index(component.value),
                        "(op[%d].offset >> 16) & 0xFF" % operands.index(component.value),
                        "(op[%d].offset >> 24) & 0xFF" % operands.index(component.value)
                    ])
        else:
            print("UNKNOWN: " + component.__class__.__name__)
            return ""
    generate_bytes(byte_sequence)
    if use_off_argument:
        return flags, "lambda off: " + " + ".join(parts)
    else:
        lambda_args = ["op"]
        if flags & Flags.OptionalREX:
            lambda_args.append("rex=False")
        if flags & Flags.VEX2:
            lambda_args.append("vex3=False")
        if flags & Flags.ModRMSIBDisp:
            lambda_args.append("sib=False")
            lambda_args.append("min_disp=0")
        return flags, "lambda %s: %s" % (", ".join(lambda_args), " + ".join(parts))


def get_in_regs(instruction_form):
    """Returns a list indicating which operands might contain input registers for this instruction form"""
    return tuple([bool(o.is_input and o.is_variable or o.is_output and o.is_memory) for o in instruction_form.operands])


def get_out_regs(instruction_form):
    """Returns a list indicating which operands might contain output registers for this instruction form"""
    return tuple([bool(o.is_output and o.is_register) for o in instruction_form.operands])


def get_out_operands(instruction_form):
    """Returns a list indicating which operands are written by this instruction form"""
    return tuple(map(operator.attrgetter("is_output"), instruction_form.operands))


def get_isa_extensions(instruction_form):
    """Returns a hashable immutable set with names of ISA extensions required for this instructions form"""
    return frozenset(map(operator.attrgetter("name"), instruction_form.isa_extensions))


def go_name_init(code, instruction_form):
    """Generates initialization code for go_name property"""
    if instruction_form.go_name:
        code.line("self.go_name = \"%s\"" % instruction_form.go_name)


def gas_name_init(code, instruction_form):
    """Generates initialization code for gas_name property"""
    if instruction_form.gas_name != instruction_form.name.lower():
        code.line("self._gas_name = \"%s\"" % instruction_form.gas_name)


def implicit_regs_init(code, instruction_form):
    """Generates initialization code for _implicit_in_regs and _implicit_out_regs properties"""
    name_reg_map = {
        "al":  (0, 0x1),
        "ax":  (0, 0x3),
        "eax": (0, 0x7),
        "rax": (0, 0xF),
        "cl":  (1, 0x1),
        "ecx": (1, 0x7),
        "rcx": (1, 0xF),
        "dx":  (2, 0x3),
        "edx": (2, 0x7),
        "rdx": (2, 0xF),
        "ebx": (3, 0x7),
        "rbx": (3, 0xF),
        "rsi": (6, 0xF),
        "rdi": (7, 0xF),
        "r11": (11, 0xF),
        "xmm0": (0, 0x100)}
    implicit_in_regs = dict()
    for in_reg_name in instruction_form.implicit_inputs:
        (in_reg_id, in_reg_mask) = name_reg_map[in_reg_name]
        implicit_in_regs[in_reg_id] = \
            implicit_in_regs.get(in_reg_id, 0) | in_reg_mask
    implicit_out_regs = dict()
    for out_reg_name in instruction_form.implicit_outputs:
        (out_reg_id, out_reg_mask) = name_reg_map[out_reg_name]
        implicit_out_regs[out_reg_id] = \
            implicit_out_regs.get(out_reg_id, 0) | out_reg_mask
    if implicit_in_regs:
        code.line("self._implicit_in_regs = " + str(dict(sorted(implicit_in_regs.items()))))
    if implicit_out_regs:
        code.line("self._implicit_out_regs = " + str(dict(sorted(implicit_out_regs.items()))))


def in_regs_init(code, instruction_form):
    """Generates initialization code for in_regs tuple"""
    # Record which operands may contain input registers
    if instruction_form.operands:
        in_regs = get_in_regs(instruction_form)
        code.line("self.in_regs = " + str(in_regs))


def out_regs_init(code, instruction_form):
    """Generates initialization code for out_regs tuple"""
    # Record which operands may contain output registers
    if instruction_form.operands:
        out_regs = get_out_regs(instruction_form)
        code.line("self.out_regs = " + str(out_regs))


def out_operands_init(code, instruction_form):
    """Generates initialization code for out_operands tuple"""
    if instruction_form.operands:
        out_operands = get_out_operands(instruction_form)
        code.line("self.out_operands = " + str(out_operands))


def mmx_mode_init(code, instruction_form):
    """Generates initialization code for mmx_mode attribute"""
    if instruction_form.mmx_mode:
        mmx_mode_map = {"MMX": True, "FPU": False}
        code.line("self.mmx_mode = " + str(mmx_mode_map[instruction_form.mmx_mode]))


def xmm_mode_init(code, instruction_form):
    """Generates initialization code for avx_mode attribute"""
    if instruction_form.xmm_mode:
        avx_mode_map = {"SSE": False, "AVX": True}
        code.line("self.avx_mode = " + str(avx_mode_map[instruction_form.xmm_mode]))


def isa_extensions_init(code, instruction_form):
    """Generates initialization code for isa_extensions attribute"""

    if instruction_form.isa_extensions:
        isa_extensions_map = {
            "MMX+": "mmx_plus",
            "3dnow!": "three_d_now",
            "3dnow!+": "three_d_now_plus",
            "3dnow! Prefetch": "three_d_now_prefetch",
            "SSE4.1": "sse4_1",
            "SSE4.2": "sse4_2"
        }
        isa_extensions = ["peachpy.x86_64.isa." + isa_extensions_map.get(extension.name, extension.name.lower())
                          for extension in instruction_form.isa_extensions]
        code.line("self.isa_extensions = frozenset([%s])" %
                  ", ".join(isa_extensions))


def instruction_branch_label_form_init(code, instruction_form, instruction_subforms,
                                       write_gas_name=True, write_in_regs=True):
    """Generates initialization code for a label operand form of a branch instruction"""

    if write_gas_name:
        gas_name_init(code, instruction_form)

    for form in ([instruction_form] + list(map(operator.itemgetter(1), instruction_subforms))):
        encoding_lambdas = list(map(lambda e: generate_encoding_lambda(e, form.operands, use_off_argument=True),
                                    form.encodings))
        assert len(encoding_lambdas) == 1, \
            "Branch label instructions are expected to have only one encoding for each operand type"
        flags, encoding_lambda = encoding_lambdas[0]
        assert form.operands[0].type in {"rel8", "rel32"}, \
            "Branch label operand type expected to be rel8 or rel32"
        flags |= {"rel8": Flags.Rel8Label, "rel32": Flags.Rel32Label}[form.operands[0].type]
        code.line("self.encodings.append((0x%02X, %s))" % (flags, encoding_lambda))

    implicit_regs_init(code, instruction_form)

    if write_in_regs:
        in_regs_init(code, instruction_form)


def instruction_form_init(code, instruction_form, instruction_subforms,
                          write_go_name=True, write_gas_name=True,
                          write_in_regs=True, write_out_regs=True, write_out_operands=True,
                          write_mmx_mode=True, write_xmm_mode=True,
                          write_isa_extensions=True):
    """Generates initialization code for a particular instruction form"""
    immediate_operands = [(i, op) for (i, op) in enumerate(instruction_form.operands) if op.is_immediate]
    for (i, operand) in immediate_operands:
        code.line("if not %s:" % generate_operand_check(i, operand,
                                                        ignore_imm_size=False, ext_imm_size=operand.extended_size))
        code.indent_line("raise ValueError(\"Argument #%d can not be encoded as %s\")" % (i, operand.type))

    if write_go_name:
        go_name_init(code, instruction_form)
    if write_gas_name:
        gas_name_init(code, instruction_form)

    for (operand_number, instruction_subform) in instruction_subforms:
        operand_check = generate_operand_check(operand_number, instruction_subform.operands[operand_number],
                                               ignore_imm_size=False,
                                               ext_imm_size=instruction_subform.operands[operand_number].extended_size)
        code.line("if %s:" % operand_check)
        with CodeBlock():
            # Record lambda functions that encode the instruction subform
            encoding_lambdas = map(lambda e: generate_encoding_lambda(e, instruction_subform.operands),
                                   instruction_subform.encodings)
            flags = 0
            if instruction_subform.operands[operand_number].is_variable:
                assert instruction_subform.operands[operand_number].type in {"al", "ax", "eax", "rax"}, \
                    "Expect a special accumulator form, got: " + str(instruction_subform.operands[operand_number])
                assert operand_number in {0, 1}, \
                    "Expect that the accumulator is either the first or the second operand"
                flags |= {0: Flags.AccumulatorOp0, 1: Flags.AccumulatorOp1}[operand_number]
            for encoding_flags, encoding_lambda in encoding_lambdas:
                code.line("self.encodings.append((0x%02X, %s))" % (flags | encoding_flags, encoding_lambda))

    # Record lambda functions that encode the most generic instruction form
    encodings = map(lambda e: generate_encoding_lambda(e, instruction_form.operands), instruction_form.encodings)
    for (flags, encoding_lambda) in encodings:
        code.line("self.encodings.append((0x%02X, %s))" % (flags, encoding_lambda))

    implicit_regs_init(code, instruction_form)

    if write_in_regs:
        in_regs_init(code, instruction_form)
    if write_out_regs:
        out_regs_init(code, instruction_form)

    if write_out_operands:
        out_operands_init(code, instruction_form)

    if write_mmx_mode:
        mmx_mode_init(code, instruction_form)

    if write_xmm_mode:
        xmm_mode_init(code, instruction_form)

    if write_isa_extensions:
        isa_extensions_init(code, instruction_form)

    if instruction_form.cancelling_inputs:
        code.line("self._cancelling_inputs = " + str(instruction_form.cancelling_inputs))


def reduce_operand_types(operand_types_list):
    """Combines operand types that differ only by a single operand together"""

    nested_operand_types = {
        ("1", "imm8"),
        ("3", "imm8"),
        ("imm8", "imm16"),
        ("imm8", "imm32"),
        ("imm16", "imm32"),
        ("imm32", "imm64"),
        ("al", "r8"),
        ("ax", "r16"),
        ("eax", "r32"),
        ("rax", "r64")
    }

    # Remove operands combination which differ only by one operand and there
    # is a more general instruction form for this operand, e.g.
    #    ADD eax, imm32 + ADD r32, imm32 -> ADD r32, imm32
    new_operand_types_list = []
    for (i, operand_types) in enumerate(operand_types_list):
        for (j, other_operand_types) in enumerate(operand_types_list):
            if j == i:
                continue
            if len(operand_types) != len(other_operand_types):
                continue
            different_operand_numbers = \
                list(filter(lambda n: operand_types[n] != other_operand_types[n],
                            range(len(operand_types))))
            if len(different_operand_numbers) == 1:
                operand_number = different_operand_numbers[0]
                if (operand_types[operand_number], other_operand_types[operand_number]) in nested_operand_types:
                    break
        else:
            new_operand_types_list.append(operand_types)
    operand_types_list = new_operand_types_list

    mergeble_operand_types = {
        ("r8", "m8"),
        ("r16", "m16"),
        ("r32", "m32"),
        ("r64", "m64"),
        ("mm", "m32"),
        ("mm", "m64"),
        ("xmm", "m8"),
        ("xmm", "m16"),
        ("xmm", "m32"),
        ("xmm", "m64"),
        ("xmm", "m128"),
        ("ymm", "m8"),
        ("ymm", "m16"),
        ("ymm", "m32"),
        ("ymm", "m64"),
        ("ymm", "m128"),
        ("ymm", "m256"),
        ("zmm", "m512")
    }

    # Indicator of whether this argument list was merged into another argument list
    is_merged = [False] * len(operand_types_list)

    new_operand_types_list = []
    for (i, operand_types) in enumerate(operand_types_list):
        for (j, other_operand_types) in enumerate(operand_types_list):
            if j == i:
                continue
            if len(operand_types) != len(other_operand_types):
                continue
            different_operand_numbers = \
                list(filter(lambda n: operand_types[n] != other_operand_types[n],
                       range(len(operand_types))))
            if len(different_operand_numbers) == 1:
                operand_number = different_operand_numbers[0]
                if (other_operand_types[operand_number], operand_types[operand_number]) in mergeble_operand_types:
                    is_merged[j] = True
                    new_operand_types = list(operand_types)
                    new_operand_types[operand_number] = \
                        other_operand_types[operand_number] + "/" + operand_types[operand_number]
                    new_operand_types_list.append(tuple(new_operand_types))
                    break
        else:
            new_operand_types_list.append(operand_types)

    return [operand_types for (operand_types, remove) in zip(new_operand_types_list, is_merged) if not remove]


def score_isa_extensions(isa_extensions):
    if isa_extensions:
        return max(map(operator.attrgetter("score"), isa_extensions))
    return 0


def supported_forms_comment(code, instruction_forms):
    """Generates document comment that describes supported instruction forms"""
    code.line()

    def format_form_descriptions(name, operand_types_list):
        form_descriptions = []
        for operand_types in operand_types_list:
            if operand_types:
                form_descriptions.append(name + "(" + ", ".join(operand_types) + ")")
            else:
                form_descriptions.append(name + "()")
        return form_descriptions

    def get_operand_types_list(instruction_forms):
        operand_types_list = [list(map(operator.attrgetter("type"), instruction_form.operands))
                              for instruction_form in instruction_forms]
        return reduce_operand_types(operand_types_list)

    def get_isa_extensions(instruction_forms):
        isa_extensions = map(operator.attrgetter("isa_extensions"), instruction_forms)
        isa_extensions = map(lambda ext: sorted(ext, key=operator.attrgetter("score")), isa_extensions)
        return isa_extensions

    form_descriptions = format_form_descriptions(instruction_forms[0].name, get_operand_types_list(instruction_forms))
    padding_length = max(map(len, form_descriptions))

    form_isa_extensions_options = sorted(set(map(tuple, get_isa_extensions(instruction_forms))),
                                         key=lambda isa_tuple: score_isa_extensions(isa_tuple))
    lines = []
    for isa_extensions_option in form_isa_extensions_options:
        isa_description = ""
        if isa_extensions_option:
            isa_description = "[" + " and ".join(map(str, isa_extensions_option)) + "]"
        isa_forms = list(filter(lambda form: tuple(sorted(form.isa_extensions, key=operator.attrgetter("score"))) == isa_extensions_option, instruction_forms))
        for form_description in format_form_descriptions(instruction_forms[0].name, get_operand_types_list(isa_forms)):
            if isa_description:
                padding = " " * (4 + padding_length - len(form_description))
                lines.append("* " + form_description + padding + isa_description)
            else:
                lines.append("* " + form_description)
    for x in sorted(lines):
        code.line(x)


def is_label_branch(instruction_form):
    return len(instruction_form.operands) == 1 and instruction_form.operands[0].type in {"rel8", "rel32"}


def main(package_root="."):
    for group, instruction_names in six.iteritems(instruction_groups):
        with open(os.path.join(package_root, "peachpy", "x86_64", group + ".py"), "w") as out:
            with CodeWriter() as code:
                code.line("# This file is auto-generated by /codegen/x86_64.py")
                code.line("# Instruction data is based on package opcodes %s" % opcodes.__version__)
                code.line()
                code.line("import inspect")
                code.line()
                code.line("import peachpy.stream")
                code.line("import peachpy.x86_64.options")
                code.line("import peachpy.x86_64.isa")
                code.line("from peachpy.util import is_sint8, is_sint32")
                code.line("from peachpy.x86_64.encoding import rex, optional_rex, vex2, vex3, evex, modrm_sib_disp")
                code.line("from peachpy.x86_64.instructions import Instruction, BranchInstruction")
                code.line("from peachpy.x86_64.operand import is_al, is_ax, is_eax, is_rax, is_cl, is_xmm0, is_r8, is_r8rex, is_r16, is_r32, is_r64, \\")
                code.indent_line("is_mm, is_xmm, is_ymm, is_m, is_m8, is_m16, is_m32, is_m64, is_m80, is_m128, is_m256, is_m512, \\")
                code.indent_line("is_evex_xmm, is_xmmk, is_xmmkz, is_evex_ymm, is_ymmk, is_ymmkz, is_zmm, is_zmmk, is_zmmkz, is_k, is_kk, \\")
                code.indent_line("is_m32k, is_m64k, is_m16kz, is_m32kz, is_m64kz, is_m128kz, is_m256kz, is_m512kz, \\")
                code.indent_line("is_m64_m32bcst, is_m128_m32bcst, is_m256_m32bcst, is_m512_m32bcst, \\")
                code.indent_line("is_m128_m64bcst, is_m256_m64bcst, is_m512_m64bcst, \\")
                code.indent_line("is_vmx, is_vmy, is_evex_vmx, is_evex_vmy, is_vmz, is_vmxk, is_vmyk, is_vmzk, \\")
                code.indent_line("is_imm, is_imm4, is_imm8, is_imm16, is_imm32, is_imm64, \\")
                code.indent_line("is_rel8, is_rel32, is_label, is_er, is_sae, check_operand, format_operand_type")
                code.line()
                code.line()
                for name in instruction_names:
                    # Instructions with `name` name
                    name_instructions = list(filter(lambda i: i.name == name, instruction_set))
                    if not name_instructions:
                        print("No forms for instruction: " + name)
                        continue
                    assert len(name_instructions) == 1
                    name_instruction = name_instructions[0]

                    instruction_forms = filter_instruction_forms(name_instruction.forms)
                    if not instruction_forms:
                        print("No forms for instruction: " + name)
                        continue

                    instruction_forms = aggregate_instruction_forms(instruction_forms)

                    base_class = "Instruction"
                    if name in {
                        "JA", "JNA",
                        "JAE", "JNAE",
                        "JB", "JNB",
                        "JBE", "JNBE",
                        "JC", "JNC",
                        "JE", "JNE",
                        "JG", "JNG",
                        "JGE", "JNGE",
                        "JL", "JNL",
                        "JLE", "JNLE",
                        "JO", "JNO",
                        "JP", "JNP",
                        "JS", "JNS",
                        "JZ", "JNZ",
                        "JPE", "JPO",
                        "JECXZ", "JRCXZ",
                        "JMP"
                    }:
                        base_class = "BranchInstruction"
                    code.line("class %s(%s):" % (name, base_class))

                    # Class scope
                    with CodeBlock():
                        # Generate documentation comment for the class
                        code.line("\"\"\"%s\"\"\"" % name_instruction.summary)
                        code.line()

                        # Generate constructor
                        code.line("def __init__(self, *args, **kwargs):")
                        with CodeBlock():
                            code.line("\"\"\"Supported forms:")
                            with CodeBlock():
                                supported_forms_comment(code, list(six.iterkeys(instruction_forms)))
                            code.line("\"\"\"")
                            code.line()

                            code.line("origin = kwargs.get(\"origin\")")
                            code.line("prototype = kwargs.get(\"prototype\")")
                            code.line("if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:")
                            code.indent_line("origin = inspect.stack()")
                            code.line("super(%s, self).__init__(\"%s\", origin=origin, prototype=prototype)" % (name, name))
                            code.line("self.operands = tuple(map(check_operand, args))")
                            operand_count_options = sorted(set([len(instruction_form.operands)
                                                                for instruction_form in six.iterkeys(instruction_forms)]))
                            if len(operand_count_options) == 1:
                                code.line("if len(self.operands) != %d:" % operand_count_options[0])
                                code.indent_line("raise SyntaxError(\"Instruction \\\"%s\\\" requires %d operands\")" % (name, operand_count_options[0]))
                            consider_operand_count = len(operand_count_options) > 1
                            for index, count in enumerate(operand_count_options):
                                if consider_operand_count:
                                    code.line("%s len(self.operands) == %d:" % ("if" if index == 0 else "elif", count))
                                with CodeBlock(consider_operand_count):
                                    # Consider only instruction forms that have exactly `count` operands
                                    count_operand_form_trees = list(filter(lambda form_subforms:
                                                                           len(form_subforms[0].operands) == count,
                                                                           six.iteritems(instruction_forms)))
                                    # Make sure operand forms with simpler ISA are checked first.
                                    # This is needed because AVX instructions can be encoded as AVX-512 instructions.
                                    # Thus, we should first check if operands match AVX specification, and only if that
                                    # fails try to match AVX-512 specification
                                    count_operand_form_trees = sorted(count_operand_form_trees,
                                                                      key=lambda form_subforms: score_isa_extensions(form_subforms[0].isa_extensions))
                                    # The most generic instruction forms
                                    count_operand_forms = list(map(operator.itemgetter(0), count_operand_form_trees))
                                    combine_attrs = len(count_operand_forms) > 1 or is_label_branch(count_operand_forms[0])
                                    # Check how many in_regs combinations exist
                                    in_regs_options = set(map(get_in_regs, count_operand_forms))
                                    common_in_regs = combine_attrs and len(in_regs_options) == 1
                                    # Check how many out_regs combinations exist
                                    out_regs_options = set(map(get_out_regs, count_operand_forms))
                                    common_out_regs = combine_attrs and len(out_regs_options) == 1
                                    # Check how many out_operands combinations exist
                                    out_operands_options = set(map(get_out_operands, count_operand_forms))
                                    common_out_operands = combine_attrs and len(out_operands_options) == 1
                                    # Check how many gas names exist
                                    gas_names = set(map(lambda form: form.gas_name, count_operand_forms))
                                    common_gas_name = combine_attrs and len(gas_names) == 1
                                    # Check how many go names exist
                                    go_names = set(map(lambda form: str(form.go_name), count_operand_forms))
                                    common_go_name = combine_attrs and len(go_names) == 1
                                    # Check how many mmx modes exist
                                    mmx_modes = set(map(operator.attrgetter("mmx_mode"), count_operand_forms))
                                    common_mmx_mode = combine_attrs and len(mmx_modes) == 1
                                    # Check how many xmm modes exist
                                    xmm_modes = set(map(operator.attrgetter("xmm_mode"), count_operand_forms))
                                    common_xmm_mode = combine_attrs and len(xmm_modes) == 1
                                    # Check how many ISA extension options exist
                                    isa_extensions_options = set(map(get_isa_extensions, count_operand_forms))
                                    common_isa_extensions = combine_attrs and len(isa_extensions_options) == 1
                                    if common_go_name:
                                        # Initialize go_name only once for all forms with `count` operands
                                        go_name_init(code, count_operand_forms[0])
                                    if common_gas_name:
                                        # Initialize gas_name only once for all forms with `count` operands
                                        gas_name_init(code, count_operand_forms[0])
                                    if common_in_regs:
                                        # Initialize in_regs only once for all registers with count operands
                                        in_regs_init(code, count_operand_forms[0])
                                    if common_out_regs:
                                        # Initialize out_regs only once for all registers with count operands
                                        out_regs_init(code, count_operand_forms[0])
                                    if common_out_operands:
                                        # Initialize out_operands only once for all registers with count operands
                                        out_operands_init(code, count_operand_forms[0])
                                    if common_mmx_mode:
                                        # Initialize mmx_mode only once for all registers with count operands
                                        mmx_mode_init(code, count_operand_forms[0])
                                    if common_xmm_mode:
                                        # Initialize avx_mode only once for all registers with count operands
                                        xmm_mode_init(code, count_operand_forms[0])
                                    if common_isa_extensions:
                                        # Initialize isa_extensions only once for all forms with `count` operands
                                        isa_extensions_init(code, count_operand_forms[0])
                                    if count > 0:
                                        # Instruction form with one or more operands
                                        for (form_index, (instruction_form, instruction_subforms)) \
                                                in enumerate(count_operand_form_trees):
                                            is_avx512 = is_avx512_instruction_form(instruction_form)
                                            operand_checks = map(
                                                lambda o: generate_operand_check(o[0], o[1], evex_form=is_avx512),
                                                enumerate(instruction_form.operands))
                                            code.line("%s %s:" % ("if" if form_index == 0 else "elif", " and ".join(operand_checks)))
                                            with CodeBlock():
                                                instruction_form_init(code, instruction_form, instruction_subforms,
                                                                      not common_go_name, not common_gas_name,
                                                                      not common_in_regs, not common_out_regs,
                                                                      not common_out_operands,
                                                                      not common_mmx_mode, not common_xmm_mode,
                                                                      not common_isa_extensions)
                                            # For branch instructions with rel32 operand additionally generate label form
                                            if is_label_branch(instruction_form):
                                                code.line("elif is_label(self.operands[0]):")
                                                with CodeBlock():
                                                    instruction_branch_label_form_init(code,
                                                        instruction_form, instruction_subforms,
                                                        not common_gas_name, not common_in_regs)
                                        code.line("else:")
                                        with CodeBlock():
                                            code.line("raise SyntaxError(\"Invalid operand types: " + name + " \" + \", \".join(map(format_operand_type, self.operands)))")
                                    else:
                                        # Instruction form with no operands
                                        instruction_form_init(code, count_operand_forms[0], count_operand_form_trees[0][1],
                                                              not common_go_name, not common_gas_name,
                                                              not common_in_regs, not common_out_regs,
                                                              not common_out_operands,
                                                              not common_mmx_mode, not common_xmm_mode,
                                                              not common_isa_extensions)
                            if consider_operand_count:
                                code.line("else:")
                                code.indent_line("raise SyntaxError(\"Invalid number of operands for instruction \\\"" + name + "\\\"\")")
                            code.line("if peachpy.stream.active_stream is not None:")
                            code.line("peachpy.stream.active_stream.add_instruction(self)", indent=1)
                            code.line()
                            code.line()

            print(str(code), file=out)


if __name__ == "__main__":
    main()
