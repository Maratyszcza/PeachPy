# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Instruction(object):
    def __init__(self, name, origin=None, prototype=None):
        super(Instruction, self).__init__()
        self.name = name

        self.line_number = None
        self.source_file = None
        self.source_code = None
        if origin is not None:
            self.line_number = origin[1][2]
            self.source_file = origin[1][1]
            self.source_code = origin[1][4][0].strip()
        elif prototype is not None:
            self.line_number = prototype.line_number
            self.source_file = prototype.source_file
            self.source_code = prototype.source_code

        self.operands = ()
        self._implicit_in_regs = dict()
        self._implicit_out_regs = dict()
        self.in_regs = ()
        self.out_regs = ()
        self.out_operands = ()
        self.encodings = []

        self.bytecode = None

        self._gas_name = None
        self.go_name = None
        self.isa_extensions = frozenset()
        self.mmx_mode = None
        self.avx_mode = None
        self._cancelling_inputs = False
        if prototype is None:
            self._available_registers = dict()
            self._live_registers = dict()
            self._indent_level = 0
        else:
            self._available_registers = prototype._available_registers.copy()
            self._live_registers = prototype._available_registers.copy()
            self._indent_level = prototype._indent_level

    def __str__(self):
        if self.operands:
            return str(self.name) + " " + ", ".join(map(str, self.operands))
        else:
            return str(self.name)

    @property
    def gas_name(self):
        if self._gas_name is None:
            return self.name.lower()
        else:
            return self._gas_name

    def format(self, assembly_format, indent=False, line_number=None):
        from peachpy.x86_64.operand import format_operand
        text = "\t" * self._indent_level if indent else ""
        if assembly_format == "peachpy":
            return text + str(self)
        elif assembly_format == "nasm":
            return text + str(self)
        elif assembly_format == "gas":
            if self.operands:
                from peachpy.x86_64.pseudo import Label
                if line_number is not None and len(self.operands) == 1 and isinstance(self.operands[0], Label) and self.operands[0].line_number is not None:
                    label = self.operands[0]
                    return "{indent}{mnemonic} {label_line}{direction} # {label_name}".format(
                        indent=text,
                        mnemonic=self.gas_name,
                        label_line=self.operands[0].line_number,
                        label_name=str(self.operands[0]),
                        direction="b" if self.operands[0].line_number < line_number else "f")
                else:
                    return text + self.gas_name + " " + ", ".join(format_operand(op, assembly_format) for op in reversed(self.operands))
            else:
                return text + self.gas_name
        elif assembly_format == "go":
            if self.go_name:
                from peachpy.util import is_int
                if self.name == "CMP" and is_int(self.operands[1]):
                    # CMP instruction with an immediate operand has operands in normal (non-reversed) order
                    return text + str(self.go_name) + " " + \
                           ", ".join(format_operand(op, assembly_format) for op in self.operands)
                elif self.operands:
                    return text + str(self.go_name) + " " + \
                           ", ".join(format_operand(op, assembly_format) for op in reversed(self.operands))
                else:
                    return text + str(self.go_name)
            else:
                return text + "; ".join(map(lambda b: "BYTE $0x%02X" % b, self.encode())) + " // " + str(self)

    def format_encoding(self, indent):
        if self.bytecode:
            text = "\t" * self._indent_level if indent else ""
            return text + "# " + " ".join("%02X" % byte for byte in self.bytecode)

    @property
    def registers(self):
        from peachpy.x86_64.operand import get_operand_registers
        registers = set()
        for operand in self.operands:
            registers.update(get_operand_registers(operand))
        return registers

    @property
    def register_objects(self):
        from peachpy.x86_64.operand import get_operand_registers
        return sum(map(get_operand_registers, self.operands), [])

    @property
    def available_registers(self):
        from peachpy.x86_64.registers import Register
        return Register._reconstruct_multiple(self._available_registers)

    @property
    def live_registers(self):
        from peachpy.x86_64.registers import Register
        return Register._reconstruct_multiple(self._live_registers)

    @property
    def input_registers(self):
        from peachpy.x86_64.registers import Register
        return Register._reconstruct_multiple(self.input_registers_masks)

    @property
    def input_registers_masks(self):
        from peachpy.x86_64.operand import get_operand_registers
        if self._cancelling_inputs:
            from peachpy.x86_64.registers import Register
            input_operands = [operand for (is_input_reg, operand) in zip(self.in_regs, self.operands) if is_input_reg]
            assert len(input_operands) == 2, "Instruction forms with cancelling inputs must have two inputs"
            assert all(map(lambda op: isinstance(op, Register), input_operands)), \
                "Both inputs of instruction form with cancelling inputs must be registers"
            if input_operands[0] == input_operands[1]:
                return dict()
            else:
                return {reg._internal_id: reg.mask for reg in input_operands}
        else:
            registers_masks = self._implicit_in_regs.copy()
            for (has_input_registers, operand) in zip(self.in_regs, self.operands):
                if has_input_registers:
                    for register in get_operand_registers(operand):
                        register_id = register._internal_id
                        registers_masks[register_id] = \
                            registers_masks.get(register_id, 0) | register.mask
            return registers_masks

    @property
    def output_registers(self):
        from peachpy.x86_64.registers import Register
        return Register._reconstruct_multiple(self.output_registers_masks)

    @property
    def output_registers_masks(self):
        from peachpy.x86_64.operand import get_operand_registers
        from peachpy.x86_64.registers import GeneralPurposeRegister32, GeneralPurposeRegister64, \
            XMMRegister, YMMRegister
        registers_masks = self._implicit_out_regs.copy()
        for (is_output_register, operand) in zip(self.out_regs, self.operands):
            if is_output_register:
                for register in get_operand_registers(operand):
                    register_id = register._internal_id
                    register_mask = register.mask
                    if register_mask == GeneralPurposeRegister32._mask:
                        register_mask = GeneralPurposeRegister64._mask
                    elif bool(self.avx_mode) and register_mask == XMMRegister._mask:
                        register_mask = YMMRegister._mask
                    registers_masks[register_id] = \
                        registers_masks.get(register_id, 0) | register_mask
        return registers_masks

    @property
    def constant(self):
        from peachpy.x86_64.operand import MemoryOperand
        from peachpy.literal import Constant
        return next(iter(operand.symbol for operand in self.operands if
                    isinstance(operand, MemoryOperand) and isinstance(operand.symbol, Constant)), None)

    @property
    def local_variable(self):
        from peachpy.x86_64.operand import MemoryOperand
        from peachpy.x86_64.function import LocalVariable
        return next(iter(operand.symbol for operand in self.operands if
                    isinstance(operand, MemoryOperand) and isinstance(operand.symbol, LocalVariable)), None)

    @property
    def memory_address(self):
        from peachpy.x86_64.operand import MemoryOperand
        memory_operands = [operand for operand in self.operands if isinstance(operand, MemoryOperand)]
        if memory_operands:
            assert len(memory_operands) == 1, \
                "x86-64 instructions can not have more than 1 explicit memory operand"
            return memory_operands[0].address

    def encode(self):
        encodings = self._filter_encodings()
        if encodings:
            bytecodes = [encoding(self.operands) for (_, encoding) in encodings]
            return min(bytecodes, key=len)
        else:
            return bytearray()

    def encode_options(self):
        if self.encodings:
            bytecodes = [encoding(self.operands) for (_, encoding) in self._filter_encodings()]
            min_length = min(map(len, bytecodes))
            return filter(lambda b: len(b) == min_length, bytecodes)
        else:
            return bytearray()

    def encode_length_options(self):
        from peachpy.x86_64.encoding import Flags, Options
        length_encoding_map = {}
        encode_options = []
        for (flags, encode) in self._filter_encodings():
            options = 0
            baseline = encode(self.operands)
            if flags & Flags.ModRMSIBDisp != 0:
                if len(encode(self.operands, sib=True)) != len(baseline):
                    options |= Options.SIB
                if len(encode(self.operands, min_disp=1)) != len(baseline):
                    options |= Options.Disp8
                if len(encode(self.operands, min_disp=4)) != len(baseline):
                    options |= Options.Disp32
            if flags & Flags.OptionalREX != 0:
                if len(encode(self.operands, rex=True)) != len(baseline):
                    options |= Options.REX
            if flags & Flags.VEX2 != 0:
                if len(encode(self.operands, vex3=True)) != len(baseline):
                    options |= Options.VEX3
            length_encoding_map.setdefault(len(baseline), baseline)
            encode_options.append((options, encode))
        # Try disp8/disp32 options as they never involve any decoding overhead
        for (options, encode) in encode_options:
            if options & Options.Disp8:
                bytecode = encode(self.operands, min_disp=1)
                length_encoding_map.setdefault(len(bytecode), bytecode)
            if options & Options.Disp32:
                bytecode = encode(self.operands, min_disp=4)
                length_encoding_map.setdefault(len(bytecode), bytecode)
        # Try to use SIB byte as well (may cause spilling into multiple uops)
        for (options, encode) in encode_options:
            if options & Options.SIB:
                bytecode = encode(self.operands, sib=True)
                length_encoding_map.setdefault(len(bytecode), bytecode)
                # Or try to combine SIB with disp8/disp32
                if options & Options.Disp8:
                    bytecode = encode(self.operands, min_disp=1)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
                if options & Options.Disp32:
                    bytecode = encode(self.operands, min_disp=4)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
        # Try to use VEX3
        for (options, encode) in encode_options:
            if options & Options.VEX3:
                bytecode = encode(self.operands, vex3=True)
                length_encoding_map.setdefault(len(bytecode), bytecode)
                # Combinations of VEX3 with disp8/disp32
                if options & Options.Disp8:
                    bytecode = encode(self.operands, vex3=True, min_disp=1)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
                if options & Options.Disp32:
                    bytecode = encode(self.operands, vex3=True, min_disp=4)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
        # Try to use VEX3 + SIB
        for (options, encode) in encode_options:
            if options & Options.VEX3 and options & Options.SIB:
                bytecode = encode(self.operands, vex3=True, sib=True)
                length_encoding_map.setdefault(len(bytecode), bytecode)
                # Combinations of VEX3, SIB, disp8/disp32
                if options & Options.Disp8:
                    bytecode = encode(self.operands, vex3=True, sib=True, min_disp=1)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
                if options & Options.Disp32:
                    bytecode = encode(self.operands, vex3=True, sib=True, min_disp=4)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
        # Try to use REX
        for (options, encode) in encode_options:
            if options & Options.REX:
                bytecode = encode(self.operands, rex=True)
                length_encoding_map.setdefault(len(bytecode), bytecode)
                # Combinations of REX with disp8/disp32
                if options & Options.Disp8:
                    bytecode = encode(self.operands, rex=True, min_disp=1)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
                if options & Options.Disp32:
                    bytecode = encode(self.operands, rex=True, min_disp=4)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
        # Try to use REX + SIB
        for (options, encode) in encode_options:
            if options & Options.REX and options & Options.SIB:
                bytecode = encode(self.operands, rex=True, sib=True)
                length_encoding_map.setdefault(len(bytecode), bytecode)
                # Combinations of REX, SIB, disp8/disp32
                if options & Options.Disp8:
                    bytecode = encode(self.operands, rex=True, sib=True, min_disp=1)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
                if options & Options.Disp32:
                    bytecode = encode(self.operands, rex=True, sib=True, min_disp=4)
                    length_encoding_map.setdefault(len(bytecode), bytecode)
        return length_encoding_map

    def _filter_encodings(self):
        encodings = []
        from peachpy.x86_64.encoding import Flags
        for (flags, encoding) in self.encodings:
            if flags & Flags.AccumulatorOp0 != 0:
                if self.operands[0].physical_id == 0:
                    encodings.append((flags, encoding))
            elif flags & Flags.AccumulatorOp1 != 0:
                if self.operands[1].physical_id == 0:
                    encodings.append((flags, encoding))
            else:
                encodings.append((flags, encoding))
        return encodings

    @property
    def relocation(self):
        """Returns relocation corresponding to encoding of this instruction of None if no relocation needed.
        Relocation offset and type variables are initialized, symbol variable needs to be initialized by the caller.
        Relocation offset specifies offset relative to the start of instruction encoding.
        """

        from peachpy.x86_64.meta import Relocation, RelocationType
        if self.bytecode:
            from peachpy.literal import Constant
            if self.constant is not None:
                # Mini-disassembler for instruction encoding.
                # Possible encoding sequences:
                #   | [66, F2, or F3 prefix] | [REX] | [66, F2, or F3 prefix] | ...
                #     ... [0F, 0F 38, or 0F 3A opcode extension] | Opcode | Mod R/M | disp32 | [imm] |
                #   | C5 ... 2-byte VEX  | Opcode | Mod R/M | disp32 | [imm] |
                #   | C4 ... 3-byte VEX  | Opcode | Mod R/M | disp32 | [imm] |
                #   | 8F ... 3-byte XOP  | Opcode | Mod R/M | disp32 | [imm] |
                #   | 62 ... 4-byte EVEX | Opcode | Mod R/M | disp32 | [imm] |
                prefix_lengths = {
                    0xC5: 2,
                    0xC4: 3,
                    0x8F: 3,
                    0x62: 4
                }
                if self.bytecode[0] in prefix_lengths:
                    mod_rm_position = prefix_lengths[self.bytecode[0]] + 1
                else:
                    decode_position = 0
                    if self.bytecode[0] in [0x66, 0xF2, 0xF3]:
                        # Legacy prefix
                        decode_position += 1
                    if self.bytecode[decode_position] & 0xF0 == 0x40:
                        # REX prefix
                        decode_position += 1
                    if self.bytecode[decode_position] in [0x66, 0xF2, 0xF3]:
                        # Legacy prefix += 1
                        decode_position += 1
                    if self.bytecode[decode_position] == 0x0F:
                        # Opcode extension
                        decode_position += 1
                        if self.bytecode[decode_position] in [0x38, 0x3A]:
                            # 2-byte 0F 38 or 0F 3A opcode extension
                            decode_position += 1
                    # Opcode
                    mod_rm_position = decode_position + 1
                mod_rm = self.bytecode[mod_rm_position]
                rm = mod_rm & 0b111
                mode = mod_rm >> 6
                assert rm == 0b101 and mode == 0b00, \
                    "Encoding must use rip-relative disp32 addressing, can't have SIB byte"
                return Relocation(mod_rm_position + 1, RelocationType.rip_disp32, program_counter=len(self.bytecode))


class BranchInstruction(Instruction):
    def __init__(self, name, origin=None, prototype=None):
        super(BranchInstruction, self).__init__(name, origin=origin, prototype=prototype)
        self.is_conditional = name != "JMP"

    def _encode_label_branch(self, address, label_address=None, long_encoding=False):
        if label_address is None:
            encodings = [encode(0) for (_, encode) in self.encodings]
        else:
            encodings = []
            from peachpy.x86_64.encoding import Flags
            from peachpy.util import is_sint8, is_sint32
            for (flags, encode) in self.encodings:
                offset = label_address - (address + len(encode(0)))
                if flags & Flags.Rel8Label != 0 and is_sint8(offset) or \
                        flags & Flags.Rel32Label != 0 and is_sint32(offset):
                    encodings.append(encode(offset))
            if not encodings:
                raise ValueError("Can not encode offset to label %s" % self.label_name)
        assert len(encodings) <= 2, "At most 2 encodings expected for branch instructions with immediate code offset"
        if len(encodings) == 1:
            return True, encodings[0]
        else:
            if long_encoding:
                return True, max(encodings, key=len)
            else:
                return False, min(encodings, key=len)

    @property
    def label_name(self):
        from peachpy.x86_64.pseudo import Label
        if isinstance(self.operands[0], Label):
            return self.operands[0].name
