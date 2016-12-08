# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
import time

import peachpy.arm.instructions
import peachpy.arm.registers
from peachpy.arm.microarchitecture import Microarchitecture

active_function = None


class Function(object):
    def __init__(self, name, arguments, return_type=None,
                 target=Microarchitecture.Default,
                 abi=None,
                 collect_origin=False, dump_intermediate_assembly=False,
                 report_generation=True, report_live_registers=False):
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        for argument in self.arguments:
            argument.stack_offset = None
            argument.register = None
            if argument.is_size_integer or argument.is_pointer_integer or argument.is_pointer:
                argument.ctype.size = abi.pointer_size
            assert argument.size
        self.target = target
        self.abi = abi
        self.collect_origin = collect_origin
        self.dump_intermediate_assembly = dump_intermediate_assembly
        self.report_generation = report_generation
        self.report_live_registers = report_live_registers
        self.ticks = None

        # Assign argument locations
        from peachpy.arm.abi import ABI
        from peachpy.arm.registers import r0, r1, r2, r3
        if abi == ABI.GnuEABI or abi == ABI.GnuEABIHF:
            # Up to 4 first arguments are passed in registers, others passed through stack
            # Arguments smaller than 4 bytes are extended to 4 bytes (both when passed on stack or in a register).
            # 8-byte arguments occupy 2 general-purpose registers or 8 bytes on stack. When they are passed in
            # registers, the index of the first register must be even (i.e. they are passed in (r0, r1) or (r2, r3),
            # but not in (r1, r2). When 8-byte arguments are passed on stack, their location is aligned on 8 bytes,
            # skipping 4 bytes if necessary.
            argument_registers = (r0, r1, r2, r3)
            register_offset = 0
            stack_offset = 0
            for argument in self.arguments:
                if argument.size <= 4:
                    if register_offset < 4:
                        argument.register = argument_registers[register_offset]
                        register_offset += 1
                    else:
                        argument.stack_offset = stack_offset
                        stack_offset += 4
                elif argument.size == 8:
                    # First register index must be even
                    if register_offset % 2 == 1:
                        register_offset += 1
                    if register_offset < 4:
                        argument.register = (argument_registers[register_offset], argument_registers[register_offset+1])
                        register_offset += 2
                    else:
                        if stack_offset % 8 == 4:
                            stack_offset += 4
                        argument.stack_offset = stack_offset
                        stack_offset += 8
                else:
                    raise ValueError("Unsupported argument size {0}".format(argument.size))
        else:
            raise ValueError("Unsupported assembler ABI %s" % abi)

        self.instructions = list()
        self.constants = list()
        self.stack_frame = StackFrame(self.abi)
        self.local_variables_count = 0
        self.virtual_registers_count = 0x40
        self.conflicting_registers = dict()
        self.allocation_options = dict()
        self.unallocated_registers = list()

    def __enter__(self):
        import peachpy.stream
        global active_function

        if active_function is not None:
            raise ValueError('Function {0} was not detached'.format(active_function.name))
        if peachpy.stream.active_stream is not None:
            raise ValueError('Alternative instruction stream is active')
        active_function = self
        peachpy.stream.active_stream = self
        if self.report_generation:
            print("Generating function {Function} for microarchitecture {Microarchitecture} and ABI {ABI}"
                  .format(Function=self.name, Microarchitecture=self.target, ABI=self.abi))
            print("\tParsing source", end="")
            self.ticks = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        import peachpy.stream
        from peachpy.arm.instructions import Instruction

        peachpy.stream.active_stream = None
        if exc_type is None:
            try:
                self.generate_labels()
                self.decompose_instructions()
                self.reserve_registers()
                if self.report_generation:
                    elapsed = time.time() - self.ticks
                    print(" (%2.2f secs)" % elapsed)
                    print("\tRunning liveness analysis", end="")
                    self.ticks = time.time()
                self.determine_available_registers()
                self.determine_live_registers(exclude_parameter_loads=True)

                if self.dump_intermediate_assembly:
                    with open('%s.S' % self.symbol_name, "w") as intermediate_assembly_file:
                        for instruction in self.instructions:
                            if isinstance(instruction, Instruction):
                                consumed_registers = ", ".join(sorted(map(str, list(instruction.get_input_registers_list()))))
                                produced_registers = ", ".join(sorted(map(str, list(instruction.get_output_registers_list()))))
                                available_registers = ", ".join(sorted(map(str, list(instruction.available_registers))))
                                live_registers = ", ".join(sorted(map(str, list(instruction.live_registers))))
                                intermediate_assembly_file.write(str(instruction) + "\n")
                                intermediate_assembly_file.write("\tConsumed registers: " + consumed_registers + "\n")
                                intermediate_assembly_file.write(
                                    "\tProduced registers: " + produced_registers + "\n")
                                intermediate_assembly_file.write("\tLive registers: " + live_registers + "\n")
                                if instruction.line_number:
                                    intermediate_assembly_file.write(
                                        "\tLine: " + str(instruction.line_number) + "\n")
                                if instruction.source_code:
                                    intermediate_assembly_file.write("\tCode: " + instruction.source_code + "\n")
                            else:
                                intermediate_assembly_file.write(str(instruction) + "\n")

                if self.report_generation:
                    elapsed = time.time() - self.ticks
                    print(" (%2.2f secs)" % elapsed)
                    print("\tRunning register allocation", end="")
                    self.ticks = time.time()
                self.check_live_registers()
                self.determine_register_relations()
                self.allocate_registers()

                if self.report_generation:
                    elapsed = time.time() - self.ticks
                    print(" (%2.2f secs)" % elapsed)
                    print("\tGenerating code", end="")
                    self.ticks = time.time()
                self.remove_assume_statements()
                self.update_stack_frame()
                self.generate_parameter_loads()
                if self.report_live_registers:
                    self.determine_live_registers()
                self.generate_prolog_and_epilog()

                self.generate_constant_loads()
                self.optimize_instructions()
                if self.report_generation:
                    elapsed = time.time() - self.ticks
                    print(" (%2.2f secs)" % elapsed)
                    self.ticks = time.time()
            finally:
                self.detach()
        else:
            self.detach()

    def detach(self):
        import peachpy.stream
        global active_function
        if active_function is None:
            raise ValueError('Trying to detach a function while no function is active')
        active_function = None
        peachpy.stream.active_stream = None
        return self

    @property
    def assembly(self):
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.generic import BranchInstruction
        from peachpy.arm.pseudo import LabelQuasiInstruction
        import os

        function_label = self.name
        constants_label = self.name + "_constants"
        assembly = ""
        if len(self.constants) > 0:
            assembly += 'section .rodata.{Microarchitecture} progbits alloc noexec nowrite align={Alignment}'\
                .format(Microarchitecture=self.target.id, Alignment=32) + os.linesep
            assembly += constants_label + ':' + os.linesep
            data_declaration_map = {8: "DB", 16: "DW", 32: "DD", 64: "DQ", 128: "DO"}
            need_alignment = False
            for constant_bucket in self.constants:
                if need_alignment:
                    assembly += "\tALIGN {Alignment}".format(Alignment=constant_bucket.capacity) + os.linesep
                for constant in constant_bucket.constants:
                    assembly += "\t.{Label}: {Declaration} {Value}"\
                        .format(Label=constant.label,
                                Declaration=data_declaration_map[constant.size],
                                Value=", ".join([str(constant)] * constant.repeats)) + os.linesep
                need_alignment = not constant_bucket.is_full()
            assembly += os.linesep

        assembly += '.section .text.{Microarchitecture},"ax",%progbits'\
            .format(Microarchitecture=self.target.id) + os.linesep
        assembly += "BEGIN_ARM_FUNCTION " + function_label + os.linesep
        assembly += "\t" + self.gnu_arch_spec + os.linesep
        if self.gnu_fpu_spec:
            assembly += "\t" + self.gnu_fpu_spec + os.linesep
        for instruction in self.instructions:
            if isinstance(instruction, BranchInstruction):
                assembly += "\t" + "{0} L{1}.{2}"\
                    .format(instruction.name, self.name, instruction.operands[0].label) + os.linesep
            elif isinstance(instruction, Instruction):
                constant = instruction.get_constant()
                if constant is not None:
                    constant.prefix = constants_label
                assembly += "\t" + str(instruction) + os.linesep
            elif isinstance(instruction, LabelQuasiInstruction):
                assembly += "L{0}.{1}:".format(self.name, instruction.name) + os.linesep
            else:
                assembly += "\t" + str(instruction) + os.linesep
        assembly += "END_ARM_FUNCTION " + function_label + os.linesep
        assembly += os.linesep
        return assembly

    @property
    def gnu_arch_spec(self):
        from peachpy.arm.isa import Extension
        isa_extensions = self.isa_extensions
        if Extension.Div in isa_extensions:
            return ".cpu cortex-a15"
        elif Extension.V7MP in isa_extensions:
            return ".cpu cortex-a9"
        elif Extension.V7 in isa_extensions:
            return ".arch armv7-a"
        elif Extension.V6K in isa_extensions:
            return ".arch armv6zk"
        elif Extension.V6 in isa_extensions:
            return ".arch armv6"
        elif Extension.V5E in isa_extensions:
            return ".arch armv5te"
        else:
            return ".arch armv5t"

    @property
    def gnu_fpu_spec(self):
        from peachpy.arm.isa import Extension
        isa_extensions = self.isa_extensions
        if Extension.NEON2 in isa_extensions or Extension.VFP4 in isa_extensions:
            return ".fpu neon-vfpv4"
        elif Extension.NEONHP in isa_extensions or \
                Extension.VFPHP in isa_extensions and Extension.NEON in isa_extensions:
            return ".fpu neon-fp16"
        elif Extension.NEON in isa_extensions:
            return ".fpu neon"
        elif Extension.VFPHP in isa_extensions:
            if Extension.VFPd32 in isa_extensions:
                return ".fpu vfpv3-fp16"
            else:
                return ".fpu vfpv3-d16-fp16"
        elif Extension.VFP3 in isa_extensions:
            if Extension.VFPd32 in isa_extensions:
                return ".fpu vfpv3"
            else:
                return ".fpu vfpv3-d16"
        elif Extension.VFP in isa_extensions or Extension.VFP2 in isa_extensions:
            return
        elif Extension.VFP3 in isa_extensions:
            return ".fpu vfp"
        else:
            return None

    def add_instruction(self, instruction):
        from peachpy.arm.instructions import Instruction
        if instruction is None:
            return
        if isinstance(instruction, Instruction):
            for extension in instruction.isa_extensions:
                if extension not in self.target.extensions:
                    raise ValueError("{0} is not supported on the target microarchitecture".format(extension))
            local_variable = instruction.get_local_variable()
            if local_variable is not None:
                self.stack_frame.add_variable(local_variable.get_root())
            self.stack_frame.preserve_registers(instruction.get_output_registers_list())
        self.instructions.append(instruction)

    def add_instructions(self, instructions):
        for instruction in instructions:
            self.add_instruction(instruction)

    def decompose_instructions(self):
        from peachpy.arm.pseudo import ReturnInstruction
        new_instructions = list()
        for instruction in self.instructions:
            if isinstance(instruction, ReturnInstruction):
                new_instructions.extend(instruction.to_instruction_list())
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def generate_prolog_and_epilog(self):
        from peachpy.arm.generic import BranchExchangeInstruction
        from peachpy.arm.pseudo import LabelQuasiInstruction
        prologue_instructions = self.stack_frame.generate_prologue()
        epilogue_instructions = self.stack_frame.generate_epilogue()
        new_instructions = list()
        for instruction in self.instructions:
            if isinstance(instruction, LabelQuasiInstruction):
                new_instructions.append(instruction)
                if instruction.name == 'ENTRY':
                    new_instructions.extend(prologue_instructions)
            elif isinstance(instruction, BranchExchangeInstruction):
                new_instructions.extend(epilogue_instructions)
                new_instructions.append(instruction)
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def generate_labels(self):
        from peachpy.arm.pseudo import LabelQuasiInstruction
        from peachpy.arm.instructions import Operand
        for instruction in self.instructions:
            if isinstance(instruction, LabelQuasiInstruction):
                if instruction.name == 'ENTRY':
                    break
        else:
            self.instructions.insert(0, LabelQuasiInstruction(Operand("ENTRY")))

    def get_label_table(self):
        from peachpy.arm.pseudo import LabelQuasiInstruction
        label_table = dict()
        for index, instruction in enumerate(self.instructions):
            if isinstance(instruction, LabelQuasiInstruction):
                label_table[instruction.name] = index
        return label_table

    def find_entry_label(self):
        from peachpy.arm.pseudo import LabelQuasiInstruction
        for index, instruction in enumerate(self.instructions):
            if isinstance(instruction, LabelQuasiInstruction):
                if instruction.name == 'ENTRY':
                    return index
        raise ValueError('Instruction stream does not contain the ENTRY label')

    def find_exit_points(self):
        from peachpy.arm.generic import BranchExchangeInstruction
        ret_instructions = list()
        for index, instruction in enumerate(self.instructions):
            if isinstance(instruction, BranchExchangeInstruction):
                ret_instructions.append(index)
        return ret_instructions

    def determine_branches(self):
        from peachpy.arm.generic import BranchInstruction
        from peachpy.arm.pseudo import LabelQuasiInstruction
        label_table = self.get_label_table()
        for instruction in self.instructions:
            if isinstance(instruction, LabelQuasiInstruction):
                instruction.input_branches = set()

        for i, instruction in enumerate(self.instructions):
            if isinstance(instruction, BranchInstruction):
                target_label = instruction.operands[0].label
                target_index = label_table[target_label]
                self.instructions[target_index].input_branches.add(i)

    def reserve_registers(self):
        pass

    def determine_available_registers(self):
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.generic import BranchInstruction
        processed_branches = set()
        label_table = self.get_label_table()

        def mark_available_registers(instructions, start, initial_available_registers):
            available_registers = set(initial_available_registers)
            for i in range(start, len(instructions)):
                instruction = instructions[i]
                if isinstance(instruction, Instruction):
                    instruction.available_registers = set(available_registers)
                    if isinstance(instruction, BranchInstruction):
                        if i not in processed_branches:
                            target_label = instruction.operands[0].label
                            target_index = label_table[target_label]
                            processed_branches.add(i)
                            mark_available_registers(instructions, target_index, available_registers)
                        if not instruction.is_conditional():
                            return
                    else:
                        available_registers |= set(instruction.get_output_registers_list())

        current_index = self.find_entry_label()
        mark_available_registers(self.instructions, current_index, set())

    def determine_live_registers(self, exclude_parameter_loads=False):
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.generic import BranchInstruction
        from peachpy.arm.pseudo import LoadArgumentPseudoInstruction, LabelQuasiInstruction
        from peachpy.arm.registers import Register
        self.determine_branches()
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                live_registers = set()
            if isinstance(instruction, BranchInstruction):
                instruction.is_visited = False

        def mark_live_registers(instructions, exit_point, initial_live_registers):
            live_registers = dict(initial_live_registers)
            # Walk from the bottom to top of the linear block
            for i in range(exit_point, -1, -1):
                instruction = instructions[i]
                if isinstance(instruction, BranchInstruction) and not instruction.is_conditional and i != exit_point:
                    return
                elif isinstance(instruction, Instruction):
                    # First mark registers which are written to by this instruction as non-live
                    # Then mark registers which are read by this instruction as live
                    for output_register in instruction.get_output_registers_list():
                        register_id = output_register.id
                        register_mask = output_register.mask
                        if register_id in live_registers:
                            live_registers[register_id] &= ~register_mask
                            if live_registers[register_id] == 0:
                                del live_registers[register_id]

                    if not (exclude_parameter_loads and isinstance(instruction, LoadArgumentPseudoInstruction)):
                        for input_register in instruction.get_input_registers_list():
                            register_id = input_register.id
                            register_mask = input_register.mask
                            if register_id in live_registers:
                                live_registers[register_id] |= register_mask
                            else:
                                live_registers[register_id] = register_mask

                    # Merge with previously determined as live registers
                    for instruction_live_register in instruction.live_registers:
                        if instruction_live_register.id in live_registers:
                            live_registers[instruction_live_register.id] |= instruction_live_register.mask
                        else:
                            live_registers[instruction_live_register.id] = instruction_live_register.mask

                    instruction.live_registers = set([Register.from_parts(id, mask, expand=True)
                                                      for (id, mask) in live_registers.iteritems()])
                elif isinstance(instruction, LabelQuasiInstruction):
                    for entry_point in instruction.input_branches:
                        if not instructions[entry_point].is_visited:
                            instructions[entry_point].is_visited = True
                            mark_live_registers(instructions, entry_point, live_registers)

        exit_points = self.find_exit_points()
        for exit_point in exit_points:
            mark_live_registers(self.instructions, exit_point, set())

    def check_live_registers(self):
        pass

    # 		all_registers = self.abi.volatile_registers + list(reversed(self.abi.argument_registers)) + self.abi.callee_save_registers
    # 		available_registers = { Register.GPType: list(), Register.WMMXType: list(), Register.VFPType: list() }
    # 		for register in all_registers:
    # 			if register not in available_registers[register.regtype]:
    # 				available_registers[register.regtype].append(register)
    # 		for instruction in self.instructions:
    # 			live_registers = { Register.GPType: set(), Register.WMMXType: set(), Register.VFPType: set() }
    # 			if isinstance(instruction, Instruction):
    # 				for live_register in instruction.live_registers:
    # 					live_registers[live_register.regtype].add(live_register)
    # 				for register_type in live_registers.iterkeys():
    # 					if len(live_registers[register_type]) > len(available_registers[register_type]):
    # 						raise ValueError("Not enough available registers to allocate live registers at instruction {0}".format(instruction))

    def determine_register_relations(self):
        from peachpy import RegisterAllocationError
        from peachpy.arm.registers import Register, SRegister, DRegister, QRegister
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.vfpneon import NeonLoadStoreInstruction, VFPLoadStoreMultipleInstruction
        all_registers = self.abi.volatile_registers + list(
            reversed(self.abi.argument_registers)) + self.abi.callee_save_registers
        available_registers = {Register.GPType: list(), Register.WMMXType: list(), Register.VFPType: list()}
        for register in all_registers:
            if register.type == Register.GPType or register.type == Register.WMMXType:
                register_bitboard = 0x1 << register.get_physical_number()
                if register_bitboard not in available_registers[register.type]:
                    available_registers[register.type].append(register_bitboard)
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                virtual_live_registers = [register for register in instruction.live_registers if register.is_virtual]
                for registerX in virtual_live_registers:
                    if registerX.type == Register.VFPType:
                        if isinstance(registerX, SRegister) and registerX.parent:
                            registerX = registerX.parent
                        if isinstance(registerX, DRegister) and registerX.parent:
                            registerX = registerX.parent
                        if registerX.get_id() not in self.allocation_options:
                            if isinstance(registerX, SRegister):
                                self.allocation_options[registerX.id] = [(0x1 << n) for n in range(32)]
                            elif isinstance(registerX, DRegister):
                                if self.target.has_vfpd32:
                                    self.allocation_options[registerX.id] = [(0x3 << n) for n in range(0, 64, 2)]
                                else:
                                    self.allocation_options[registerX.id] = [(0x3 << n) for n in range(0, 32, 2)]
                            else:
                                self.allocation_options[registerX.id] = [(0xF << n) for n in range(0, 64, 4)]
                    else:
                        if registerX.id not in self.allocation_options:
                            self.allocation_options[registerX.id] = list(available_registers[registerX.type])

                    self.unallocated_registers.append((registerX.id, registerX.type))

                    # Setup the list of conflicting registers for each virtual register
                    if registerX.id not in self.conflicting_registers:
                        self.conflicting_registers[registerX.id] = set()
                    for registerY in virtual_live_registers:
                        # VFP registers have a conflict even they are of different size
                        if registerX.id != registerY.id and registerX.type == registerY.type:
                            self.conflicting_registers[registerX.id].add(registerY.id)

        # Mark available physical registers for each virtual register
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                virtual_live_registers = [register for register in instruction.live_registers if register.is_virtual]
                # If a physical register is live at some point, it can not be allocated for a virtual register
                physical_live_registers = [register for register in instruction.live_registers if
                                           not register.is_virtual]
                for virtual_register in virtual_live_registers:
                    for physical_register in physical_live_registers:
                        if virtual_register.type == physical_register.type:
                            virtual_register_id = virtual_register.id
                            physical_register_bitboard = physical_register.bitboard
                            self.allocation_options[virtual_register_id][:] = \
                                [possible_register_bitboard for possible_register_bitboard in
                                    self.allocation_options[virtual_register_id]
                                        if (possible_register_bitboard & physical_register_bitboard) == 0]

        # Detect group constraints
        constraints = dict()
        for instruction in self.instructions:
            if isinstance(instruction, NeonLoadStoreInstruction) or isinstance(instruction,
                                                                               VFPLoadStoreMultipleInstruction):
                if isinstance(instruction, NeonLoadStoreInstruction):
                    register_list = instruction.operands[0].get_registers_list()
                    physical_registers_count = 32
                else:
                    register_list = instruction.operands[1].get_registers_list()
                    physical_registers_count = 32 if self.target.has_vfpd32 else 16
                if len(register_list) > 1:
                    if all(isinstance(register, DRegister) for register in register_list):
                        register_id_list = list()
                        for register in register_list:
                            register_id = register.get_id()
                            if register_id not in register_id_list:
                                register_id_list.append(register_id)
                        register_id_list = tuple(register_id_list)
                        # Iterate possible allocations for this register list
                        # For VLD1/VST1 instructions all registers must be allocated to sequential physical registers
                        options = list()
                        for sequence_bitboard_position in range(0, 2 * physical_registers_count - 2 * len(
                                register_list) + 2, 2):
                            register_bitboards = [0x3 << (sequence_bitboard_position + 2 * i) for i in
                                                  range(len(register_list))]
                            for i, (bitboard, register) in enumerate(zip(register_bitboards, register_list)):
                                register_bitboards[i] = register.extend_bitboard(bitboard)
                            # Check that bitboard is available for allocation
                            for register, bitboard in zip(register_list, register_bitboards):
                                if bitboard not in self.allocation_options[register.get_id()]:
                                    break
                            else:
                                # Check that if registers with the same id use the same bitboard in this allocation
                                register_id_map = dict()
                                for register, bitboard in zip(register_list, register_bitboards):
                                    register_id = register.get_id()
                                    if register_id in register_id_map:
                                        if register_id_map[register_id] != bitboard:
                                            break
                                    else:
                                        register_id_map[register_id] = bitboard
                                else:
                                    # Check that allocation bitboards do not overlap:
                                    allocation_bitboard = 0
                                    for bitboard in register_id_map.itervalues():
                                        if (allocation_bitboard & bitboard) == 0:
                                            allocation_bitboard |= bitboard
                                        else:
                                            break
                                    else:
                                        ordered_bitboard_list = [register_id_map[register_id] for register_id in
                                                                 register_id_list]
                                        options.append(tuple(ordered_bitboard_list))
                        if options:
                            if len(register_id_list) > 1:
                                if register_id_list in constraints:
                                    constraints[register_id_list] = tuple(
                                        [option for option in constraints[register_id_list] if option in options])
                                else:
                                    constraints[register_id_list] = tuple(options)
                        else:
                            raise RegisterAllocationError("Imposible virtual register combination in instruction %s"
                                                          % instruction)
                    elif all(isinstance(register, SRegister) for register in register_list) and \
                            isinstance(instruction, VFPLoadStoreMultipleInstruction):
                        register_id_list = list()
                        for register in register_list:
                            register_id = register.id
                            if register_id not in register_id_list:
                                register_id_list.append(register_id)
                        register_id_list = tuple(register_id_list)
                        # Iterate possible allocations for this register list
                        # For VLDM/VSTM instructions all registers must be allocated to sequential physical registers
                        options = list()
                        for sequence_bitboard_position in range(0, 32 - len(register_list) + 1):
                            register_bitboards = [0x1 << (sequence_bitboard_position + i) for i in
                                                  range(len(register_list))]
                            for i, (bitboard, register) in enumerate(zip(register_bitboards, register_list)):
                                register_bitboards[i] = register.extend_bitboard(bitboard)
                            # Check that bitboard is available for allocation
                            for register, bitboard in zip(register_list, register_bitboards):
                                if bitboard not in self.allocation_options[register.id]:
                                    break
                            else:
                                # Check that if registers with the same id use the same bitboard in this allocation
                                register_id_map = dict()
                                for register, bitboard in zip(register_list, register_bitboards):
                                    register_id = register.id
                                    if register_id in register_id_map:
                                        if register_id_map[register_id] != bitboard:
                                            break
                                    else:
                                        register_id_map[register_id] = bitboard
                                else:
                                    # Check that allocation bitboards do not overlap:
                                    allocation_bitboard = 0
                                    for bitboard in register_id_map.itervalues():
                                        if (allocation_bitboard & bitboard) == 0:
                                            allocation_bitboard |= bitboard
                                        else:
                                            break
                                    else:
                                        ordered_bitboard_list = [register_id_map[register_id] for register_id in
                                                                 register_id_list]
                                        options.append(tuple(ordered_bitboard_list))
                        if options:
                            if len(register_id_list) > 1:
                                if register_id_list in constraints:
                                    constraints[register_id_list] = tuple(
                                        [option for option in constraints[register_id_list] if option in options])
                                else:
                                    constraints[register_id_list] = tuple(options)
                        else:
                            raise RegisterAllocationError(
                                "Imposible virtual register combination in instruction %s" % instruction)
                    else:
                        assert False
        report_register_constraints = False
        if report_register_constraints:
            for (register_list, options) in constraints.iteritems():
                print("REGISTER CONSTRAINTS: ", map(str, register_list))
                for option in options:
                    print("\t", map(lambda t: "%016X" % t, option))

        # Merging of different groups sharing a register will be implemented here sometime

        # Check that each register id appears only once
        constrained_register_id_list = [register_id for register_id_list in constraints.iterkeys() for register_id in
                                        register_id_list]
        assert (len(constrained_register_id_list) == len(set(constrained_register_id_list)))
        constrained_register_id_set = set(constrained_register_id_list)

        # Create a map from constrained register to constrained register group
        # 		constrained_register_map = dict()
        # 		for register_id_list in constraints.iterkeys():
        # 			for register_id in register_id_list:
        # 				constrained_register_map[register_id] = register_id_list

        # Remove individual registers from the set of unallocated registers and add the register group instead
        for constrained_register_id in constrained_register_id_list:
            while (constrained_register_id, Register.VFPType) in self.unallocated_registers:
                self.unallocated_registers.remove((constrained_register_id, Register.VFPType))
        for register_id_list in constraints.iterkeys():
            self.unallocated_registers.append((register_id_list, Register.VFPType))

        # 		print "UNALLOCATED REGISTERS:"
        # 		print "\t", self.unallocated_registers

        # Remove individual registers from the sets of conflicting registers and add the register group instead
        # 		for register_id_list in constraints.iterkeys():
        # 			self.conflicting_registers[register_id_list] = set()
        # 		for constrained_register_id in constrained_register_id_list:
        # 			self.conflicting_registers[constrained_register_map[constrained_register_id]].update(self.conflicting_registers[constrained_register_id])
        # 			del self.conflicting_registers[constrained_register_id]
        # 		for conflicting_registers_set in self.conflicting_registers.itervalues():
        # 			for constrained_register_id in constrained_register_id_list:
        # 				if constrained_register_id in conflicting_registers_set:
        # 					conflicting_registers_set.remove(constrained_register_id)
        # 					conflicting_registers_set.add(constrained_register_map[constrained_register_id])

        # Remove individual registers from the lists of allocation options and add the register group instead
        for constrained_register_id in constrained_register_id_list:
            del self.allocation_options[constrained_register_id]
        for register_id_list, constrained_options in constraints.iteritems():
            self.allocation_options[register_id_list] = list(options)

    def allocate_registers(self):
        from peachpy.arm.registers import Register
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.pseudo import LoadArgumentPseudoInstruction
        # Map from virtual register id to physical register
        register_allocation = dict()
        for (virtual_register_id, virtual_register_type) in self.unallocated_registers:
            register_allocation[virtual_register_id] = None

        def bind_register(virtual_register_id, physical_register):
            # Remove option to allocate any conflicting virtual register to the same physical register or its enclosing register
            physical_register_bitboard = physical_register.bitboard
            for conflicting_register_id in self.conflicting_registers[virtual_register_id]:
                if conflicting_register_id in self.allocation_options:
                    for allocation_bitboard in self.allocation_options[conflicting_register_id]:
                        if (allocation_bitboard & physical_register_bitboard) != 0:
                            self.allocation_options[conflicting_register_id].remove(allocation_bitboard)
            register_allocation[virtual_register_id] = physical_register

        def bind_registers(virtual_register_id_list, physical_register_id_list):
            # Remove option to allocate any conflicting virtual register to the same physical register or its enclosing register
            physical_register_bitboard_list = [physical_register.get_bitboard() for physical_register in
                                               physical_register_id_list]
            for virtual_register_id, physical_register_bitboard in zip(virtual_register_id_list,
                                                                       physical_register_bitboard_list):
                for conflicting_register_id in self.conflicting_registers[virtual_register_id]:
                    for allocation_key, allocation_option in self.allocation_options.iteritems():
                        if isinstance(allocation_key, tuple):
                            if conflicting_register_id in allocation_key:
                                conflicting_register_index = allocation_key.index(conflicting_register_id)
                                for bitboard_list in allocation_option:
                                    if (bitboard_list[conflicting_register_index] & physical_register_bitboard) != 0:
                                        allocation_option.remove(bitboard_list)
                        else:
                            if conflicting_register_id == allocation_key:
                                for bitboard in allocation_option:
                                    if (bitboard & physical_register_bitboard) != 0:
                                        allocation_option.remove(bitboard)

            for virtual_register_id, physical_register_id in zip(virtual_register_id_list, physical_register_id_list):
                register_allocation[virtual_register_id] = physical_register_id


        def is_allocated(virtual_register_id):
            return bool(register_allocation[virtual_register_id])

        # First allocate parameters
        for instruction in self.instructions:
            if isinstance(instruction, LoadArgumentPseudoInstruction):
                if instruction.argument.register:
                    if instruction.destination.register.is_virtual:
                        if not is_allocated(instruction.destination.register.id):
                            if instruction.argument.register.bitboard in self.allocation_options[
                                instruction.destination.register.id]:
                                bind_register(instruction.destination.register.id, instruction.argument.register)

        # Now allocate registers with special restrictions
        for virtual_register_id_list, virtual_register_type in self.unallocated_registers:
            if isinstance(virtual_register_id_list, tuple):
            # 				print "REGLIST: ", map(str, virtual_register_id_list)
                assert self.allocation_options[virtual_register_id_list]
                physical_register_bitboard_list = self.allocation_options[virtual_register_id_list][0]
                physcial_registers_list = [Register.from_bitboard(physical_register_bitboard, virtual_register_type) for
                                           physical_register_bitboard in physical_register_bitboard_list]
                bind_registers(virtual_register_id_list, physcial_registers_list)

        # Now allocate all other registers
        while self.unallocated_registers:
            virtual_register_id, virtual_register_type = self.unallocated_registers.pop(0)
            if not isinstance(virtual_register_id, tuple):
                if not is_allocated(virtual_register_id):
                    assert self.allocation_options[virtual_register_id]
                    physical_register_bitboard = self.allocation_options[virtual_register_id][0]
                    physical_register = Register.from_bitboard(physical_register_bitboard, virtual_register_type)
                    bind_register(virtual_register_id, physical_register)

        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                for input_register in instruction.get_input_registers_list():
                    if input_register.is_virtual:
                        input_register.bind(register_allocation[input_register.id])
                for output_register in instruction.get_output_registers_list():
                    if output_register.is_virtual:
                        if output_register.id in register_allocation:
                            output_register.bind(register_allocation[output_register.id])

    # Updates information about registers to be saved/restored in the function prologue/epilogue
    def update_stack_frame(self):
        from peachpy.arm.instructions import Instruction
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                self.stack_frame.preserve_registers(instruction.get_output_registers_list())

    def remove_assume_statements(self):
        from peachpy.arm.pseudo import AssumeInitializedPseudoInstruction
        new_instructions = list()
        for instruction in self.instructions:
            if isinstance(instruction, AssumeInitializedPseudoInstruction):
                continue
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def generate_parameter_loads(self):
        from peachpy.arm.registers import sp
        from peachpy.arm.generic import MOV, LDR
        from peachpy.arm.pseudo import LoadArgumentPseudoInstruction
        new_instructions = list()
        for instruction in self.instructions:
            if isinstance(instruction, LoadArgumentPseudoInstruction):
                parameter = instruction.argument
                if parameter.register:
                    # If parameter is in a register, use register-register move:
                    if instruction.destination.register != parameter.register:
                        # Parameter is in a different register than instruction destination, generate move:
                        new_instruction = MOV(instruction.destination.register, parameter.register)
                        new_instruction.live_registers = instruction.live_registers
                        new_instruction.available_registers = instruction.available_registers
                        new_instructions.append(new_instruction)
                    # If parameter is in the same register as instruction destination, no instruction needed:
                    #   MOV( instruction.destination == parameter.register_location, parameter.register_location )
                    # is a no-op
                else:
                    parameter_address = self.stack_frame.get_parameters_offset() + parameter.stack_offset
                    new_instruction = LDR(instruction.destination.register, [sp, parameter_address])
                    new_instruction.live_registers = instruction.live_registers
                    new_instruction.available_registers = instruction.available_registers
                    new_instructions.append(new_instruction)
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def generate_constant_loads(self):
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.pseudo import LoadConstantPseudoInstruction
        from peachpy import ConstantBucket
        max_alignment = 0
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                constant = instruction.get_constant()
                if constant is not None:
                    constant_alignment = constant.get_alignment()
                    constant_size = constant.size * constant.repeats
                    max_alignment = max(max_alignment, constant_alignment)

        constant_id = 0
        constant_label_map = dict()
        constant_buckets = dict()
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                constant = instruction.get_constant()
                if constant is not None:
                    if constant in constant_label_map:
                        constant.label = constant_label_map[constant]
                    else:
                        constant.label = "c" + str(constant_id)
                        constant_id += 1
                        constant_label_map[constant] = constant.label
                        constant_alignment = constant.get_alignment()
                        constant_size = constant.size * constant.repeats
                        if constant_alignment in constant_buckets:
                            constant_buckets[constant_alignment].add(constant)
                            if constant_buckets[constant_alignment].is_full():
                                del constant_buckets[constant_alignment]
                        else:
                            constant_bucket = ConstantBucket(max_alignment / 8)
                            constant_bucket.add(constant)
                            self.constants.append(constant_bucket)
                            if not constant_bucket.is_full():
                                constant_buckets[constant_alignment] = constant_bucket

        new_instructions = list()
        for instruction in self.instructions:
            if isinstance(instruction, LoadConstantPseudoInstruction):
                raise NotImplementedError()
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def optimize_instructions(self):
        from peachpy.arm.generic import MovInstruction
        from peachpy.arm.vfpneon import VfpNeonMovInstruction
        new_instructions = list()
        for instruction in self.instructions:
            # Remove moves where source and destination are the same

            if isinstance(instruction, MovInstruction):
                if len(instruction.operands) != 2 or instruction.operands[0] != instruction.operands[1]:
                    new_instructions.append(instruction)
            elif isinstance(instruction, VfpNeonMovInstruction):
                if instruction.operands[0] != instruction.operands[1]:
                    new_instructions.append(instruction)
            else:
                new_instructions.append(instruction)
        self.instructions = new_instructions

    def get_target(self):
        return self.target

    @property
    def isa_extensions(self):
        from peachpy.arm.instructions import Instruction
        from peachpy.arm.registers import QRegister, DRegister
        from peachpy.arm.isa import Extension, Extensions
        isa_extensions = Extensions()
        for instruction in self.instructions:
            if isinstance(instruction, Instruction):
                for extension in instruction.isa_extensions:
                    isa_extensions += extension
                if any(isinstance(register, QRegister) or
                        isinstance(register, DRegister) and register.is_extended for
                        register in instruction.get_registers_list()):
                    isa_extensions += Extension.VFPd32
        return isa_extensions

    def get_yeppp_isa_extensions(self):
        isa_extensions_map = {'V4': ('V4', None, None),
                              'V5': ( 'V5', None, None),
                              'V5E': ( 'V5E', None, None),
                              'V6': ( 'V6', None, None),
                              'V6K': ( 'V6K', None, None),
                              'V7': ( 'V7', None, None),
                              'V7MP': ( 'V7MP', None, None),
                              'Div': ( 'Div', None, None),
                              'Thumb': ( 'Thumb', None, None),
                              'Thumb2': ( 'Thumb2', None, None),
                              'VFP': ( 'VFP', None, None),
                              'VFP2': ( 'VFP2', None, None),
                              'VFP3': ( 'VFP3', None, None),
                              'VFPd32': ( 'VFPd32', None, None),
                              'VFP3HP': ( 'VFP3HP', None, None),
                              'VFP4': ( 'VFP4', None, None),
                              'VFPVectorMode': ( None, None, 'VFPVectorMode'),
                              'XScale': ( None, 'XScale', None),
                              'WMMX': ( None, 'WMMX', None),
                              'WMMX2': ( None, 'WMMX2', None),
                              'NEON': ( None, 'NEON', None),
                              'NEONHP': ( None, 'NEONHP', None),
                              'NEON2': ( None, 'NEON2', None)}
        (isa_extensions, simd_extensions, system_extensions) = (set(), set(), set())
        for isa_extension in self.get_isa_extensions():
            if isa_extension is not None:
                (isa_extension, simd_extension, system_extension) = isa_extensions_map[isa_extension]
                if isa_extension is not None:
                    isa_extensions.add(isa_extension)
                if simd_extension is not None:
                    simd_extensions.add(simd_extension)
                if system_extension is not None:
                    system_extensions.add(system_extension)
        isa_extensions = map(lambda id: "YepARMIsaFeature" + id, isa_extensions)
        if not isa_extensions:
            isa_extensions = ["YepIsaFeaturesDefault"]
        simd_extensions = map(lambda id: "YepARMSimdFeature" + id, simd_extensions)
        if not simd_extensions:
            simd_extensions = ["YepSimdFeaturesDefault"]
        system_extensions = map(lambda id: "YepARMSystemFeature" + id, system_extensions)
        if not system_extensions:
            system_extensions = ["YepSystemFeaturesDefault"]
        return (isa_extensions, simd_extensions, system_extensions)

    def allocate_local_variable(self):
        self.local_variables_count += 1
        return self.local_variables_count

    def allocate_q_register(self):
        self.virtual_registers_count += 1
        return (self.virtual_registers_count << 12) | 0x0F0

    def allocate_d_register(self):
        self.virtual_registers_count += 1
        return (self.virtual_registers_count << 12) | 0x300

    def allocate_s_register(self):
        self.virtual_registers_count += 1
        return (self.virtual_registers_count << 12) | 0x400

    def allocate_wmmx_register(self):
        self.virtual_registers_count += 1
        return (self.virtual_registers_count << 12) | 0x002

    def allocate_general_purpose_register(self):
        self.virtual_registers_count += 1
        return (self.virtual_registers_count << 12) | 0x001


class LocalVariable(object):
    def __init__(self, register_type):
        from peachpy.arm.registers import GeneralPurposeRegister, WMMXRegister, SRegister, DRegister, QRegister
        super(LocalVariable, self).__init__()
        if isinstance(register_type, int):
            self.size = register_type
        elif register_type == GeneralPurposeRegister:
            self.size = 4
        elif register_type == WMMXRegister:
            self.size = 8
        elif register_type == SRegister:
            self.size = 4
        elif register_type == DRegister:
            self.size = 8
        elif register_type == QRegister:
            self.size = 16
        else:
            raise ValueError('Unsupported register type {0}'.format(register_type))
        self.id = active_function.allocate_local_variable()
        self.address = None
        self.offset = 0
        self.parent = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        if self.is_subvariable():
            address = self.parent.get_address()
            if address is not None:
                address += self.offset
        else:
            address = self.address
        if address is not None:
            return "[{0}]".format(address)
        else:
            return "local-variable<{0}>".format(self.id)

    def is_subvariable(self):
        return self.parent is not None

    def get_parent(self):
        return self.parent

    def get_root(self):
        if self.is_subvariable():
            return self.get_parent().get_root()
        else:
            return self

    def get_address(self):
        if self.is_subvariable():
            return self.parent.get_address() + self.offset
        else:
            return self.address

    def get_size(self):
        return self.size

    def get_low(self):
        assert self.get_size() % 2 == 0
        child = LocalVariable(self.get_size() / 2)
        child.parent = self
        child.offset = 0
        return child

    def get_high(self):
        assert self.get_size() % 2 == 0
        child = LocalVariable(self.get_size() / 2)
        child.parent = self
        child.offset = self.get_size() / 2
        return child


class StackFrame(object):
    def __init__(self, abi):
        super(StackFrame, self).__init__()
        self.abi = abi
        self.general_purpose_registers = list()
        self.d_registers = list()
        self.s_variables = list()
        self.d_variables = list()
        self.q_variables = list()

    def preserve_registers(self, registers):
        for register in registers:
            self.preserve_register(register)

    def preserve_register(self, register):
        from peachpy.arm.registers import GeneralPurposeRegister, SRegister, DRegister, QRegister
        if isinstance(register, GeneralPurposeRegister):
            if not register in self.general_purpose_registers:
                if register in self.abi.callee_save_registers:
                    self.general_purpose_registers.append(register)
        elif isinstance(register, SRegister):
            if not register.is_virtual():
                register = register.get_parent()
                if not register in self.d_registers:
                    if register in self.abi.callee_save_registers:
                        self.d_registers.append(register)
        elif isinstance(register, DRegister):
            if not register in self.d_registers:
                if register in self.abi.callee_save_registers:
                    self.d_registers.append(register)
        elif isinstance(register, QRegister):
            d_low = register.get_low_part()
            d_high = register.get_high_part()
            if d_low not in self.d_registers:
                if register in self.abi.callee_save_registers:
                    self.d_registers.append(d_low)
            if d_high not in self.d_registers:
                if register in self.abi.callee_save_registers:
                    self.d_registers.append(d_high)
        else:
            raise TypeError("Unsupported register type {0}".format(type(register)))

    def add_variable(self, variable):
        if variable.get_size() == 16:
            if variable not in self.sse_variables:
                self.sse_variables.append(variable)
        elif variable.get_size() == 32:
            if variable not in self.avx_variables:
                self.avx_variables.append(variable)
        else:
            raise TypeError("Unsupported variable type {0}".format(type(variable)))

    def get_parameters_offset(self):
        parameters_offset = len(self.general_purpose_registers) * 4
        if parameters_offset % 8 == 4:
            parameters_offset += 4
        return parameters_offset + len(self.d_registers) * 8

    def generate_prologue(self):
        from peachpy.stream import InstructionStream
        from peachpy.arm.registers import r3
        from peachpy.arm.generic import PUSH
        from peachpy.arm.vfpneon import VPUSH
        with InstructionStream() as instructions:
            if self.general_purpose_registers:
                general_purpose_registers = list(self.general_purpose_registers)
                if len(general_purpose_registers) % 2 == 1:
                    general_purpose_registers.append(r3)
                PUSH(tuple(sorted(general_purpose_registers, key=lambda reg: reg.get_physical_number())))
            if self.d_registers:
                VPUSH(tuple(sorted(self.d_registers, key=lambda reg: reg.get_physical_number())))
        return list(iter(instructions))

    def generate_epilogue(self):
        from peachpy.stream import InstructionStream
        from peachpy.arm.registers import r3
        from peachpy.arm.generic import POP
        from peachpy.arm.vfpneon import VPOP
        with InstructionStream() as instructions:
            if self.d_registers:
                VPOP(tuple(sorted(self.d_registers, key=lambda reg: reg.get_physical_number())))
            if self.general_purpose_registers:
                general_purpose_registers = list(self.general_purpose_registers)
                if len(general_purpose_registers) % 2 == 1:
                    general_purpose_registers.append(r3)
                POP(tuple(sorted(general_purpose_registers, key=lambda reg: reg.get_physical_number())))
        return list(iter(instructions))


