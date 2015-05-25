# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
import os
import operator
import bisect
import collections
import six

import peachpy
import peachpy.writer
import peachpy.x86_64.instructions
import peachpy.x86_64.registers
import peachpy.x86_64.avx
import peachpy.x86_64.options

active_function = None


class Function:
    """Generalized x86-64 assembly function.

    A function consists of C signature and a list of instructions.

    On this level the function is supposed to be compatible with multiple ABIs. In particular, instructions may have
    virtual registers, and instruction stream may contain pseudo-instructions, such as LOAD.ARGUMENT or RETURN.
    """

    def __init__(self, name, arguments, result_type=None,
                 package=None,
                 target=None,
                 debug_level=None):
        """
        :param str name: name of the function without mangling (as in C language).
        :param tuple arguments: a tuple of :class:`peachpy.Argument` objects.
        :param Type return_type: the return type of the function. None if the function returns no value (void function).
        :param str package: the name of the Go package containing this function.
        :param Microarchitecture target: the target microarchitecture for this function.
        :param int debug_level: the verbosity level for debug information collected for instructions. 0 means no
            debug information, 1 and above enables information about the lines of Python code that originated an
            instruction. Collecting debug information increases processing time by several times.
        :ivar Label entry: a label that marks the entry point of the function. A user can place the entry point in any
            place in the function by defining this label with LABEL pseudo-instruction. If this label is not defined
            by the user, it will be placed automatically before the first instruction of the function.

        :ivar int _indent_level: the level of indentation for this instruction in assembly listings. Indentation level
            is changed by Loop statements.
        :ivar list _instructions: the list of :class:`Instruction` objects that comprise the function code.

        :ivar set _label_names: a set of string names of LABEL quasi-instructions in the function. The set is populated
            as instructions are added and is intended to track duplicate labels.
        """
        self.name = name
        self.arguments = arguments
        self.result_type = result_type
        if package is None:
            self.package = peachpy.x86_64.options.package
        self.package = package
        if target is None:
            self.target = peachpy.x86_64.options.target
        self.target = target

        self.target = target
        if debug_level is None:
            self.debug_level = peachpy.x86_64.options.debug_level
        else:
            self.debug_level = int(debug_level)

        from peachpy.x86_64.pseudo import Label
        self.entry = Label("__entry__")

        self._indent_level = 1

        self._instructions = list()

        self._label_names = set()

        self._local_variables_count = 0
        self._virtual_general_purpose_registers_count = 0
        self._virtual_mmx_registers_count = 0
        self._virtual_xmm_registers_count = 0

        from collections import defaultdict
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister
        self._conflicting_registers = {
            # Map from virtual register id to internal id of conflicting registers
            GeneralPurposeRegister._kind: defaultdict(set),
            MMXRegister._kind: defaultdict(set),
            XMMRegister._kind: defaultdict(set)
        }
        self._register_allocations = {
            # Map from internal register id to physical register id
            GeneralPurposeRegister._kind: dict(),
            MMXRegister._kind: dict(),
            XMMRegister._kind: dict()
        }

    @property
    def c_signature(self):
        """C signature (including parameter names) for the function"""

        signature = "void" if self.result_type is None else str(self.result_type)
        signature = signature + " " + self.name
        signature = signature + "(" + ", ".join(map(str, self.arguments)) + ")"
        return signature

    @property
    def go_signature(self):
        """Go signature (including parameter names) for the function.

        None if the function argument or return type is incompatible with Go"""

        def c_to_go_type(ctype):
            assert isinstance(ctype, peachpy.Type)
            assert not ctype.is_pointer or not ctype.base.is_pointer
            if ctype.is_pointer:
                return "*" + c_to_go_type(ctype.base)
            elif ctype.is_bool:
                return "boolean"
            elif ctype.is_size_integer:
                return "int" if ctype.is_signed_integer else "uint"
            elif ctype.is_signed_integer:
                return {
                    1: "int8",
                    2: "int16",
                    4: "int32",
                    8: "int64"
                }[ctype.size]
            elif ctype.is_unsigned_integer:
                return {
                    1: "uint8",
                    2: "uint16",
                    4: "uint32",
                    8: "uint64"
                }[ctype.size]
            elif ctype.is_floating_point:
                return {
                    4: "float32",
                    8: "float64"
                }[ctype.size]
            else:
                return None

        go_argument_types = list(map(c_to_go_type, map(operator.attrgetter("ctype"), self.arguments)))
        # Some of the C types doesn't have a Go analog
        if not(all(map(bool, go_argument_types))):
            return None

        go_arguments = map(lambda name_gotype: " ".join(name_gotype),
                           zip(map(operator.attrgetter("name"), self.arguments), go_argument_types))
        if self.result_type is None:
            return "func %s(%s)" % (self.name, ", ".join(go_arguments))
        else:
            go_result_type = c_to_go_type(self.result_type)
            if go_result_type is None:
                return None
            else:
                return "func %s(%s) %s" % (self.name, ", ".join(go_arguments), go_result_type)

    def __enter__(self):
        self.attach()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach()
        if exc_type is None:
            self._add_default_labels()
            self._check_undefined_labels()
            self._remove_unused_labels()
            self._analize()
            self._check_live_registers()
            self._preallocate_registers()
            self._bind_registers()
            if peachpy.x86_64.options.abi is not None:
                abi_function = self.finalize(peachpy.x86_64.options.abi)

                if peachpy.writer.active_writer is not None:
                    peachpy.writer.active_writer.add_function(abi_function)
        else:
            raise

    def attach(self):
        """Makes active the function and its associated instruction stream.

        While the instruction stream is active, generated instructions are added to this function.

        While the function is active, generated instructions are checked for compatibility with the function target.
        """
        import peachpy.stream
        global active_function

        if active_function is not None:
            raise ValueError("Can not attach the function: alternative function %s is active" % active_function.name)
        if peachpy.stream.active_stream is not None:
            raise ValueError("Can not attach the function instruction stream: alternative instruction stream is active")
        active_function = self
        peachpy.stream.active_stream = self
        return self

    def detach(self):
        """Make the function and its associated instruction stream no longer active.

        The function and its instruction stream must be active before calling the method.
        """
        import peachpy.stream
        global active_function
        if active_function is None:
            raise ValueError("Can not detach the function: no function is active")
        if active_function is not self:
            raise ValueError("Can not detach the function: a different function is active")
        active_function = None
        peachpy.stream.active_stream = None
        return self

    @staticmethod
    def _check_arguments(args):
        # Check types
        if not isinstance(args, (list, tuple)):
            raise TypeError("Invalid arguments types (%s): a tuple or list of function arguments expected" % str(args))
        for i, arg in enumerate(args):
            if not isinstance(arg, Argument):
                raise TypeError("Invalid argument object for argument #%d (%s): peachpy.Argument expected" %
                                (i, str(arg)))
        # mapping from argument name to argument number
        names = dict()

        # First check argument names for arguments with explicit names
        for i, arg in enumerate(args):
            if arg.name:
                if arg.name in names:
                    raise ValueError("Argument #%d (%s) has the same name as argument #%d (%s)" %
                                     (i, str(arg), names[arg.name], args[names[arg.name]]))
                names[arg.name] = i

    def _find_argument(self, argument_target):
        from peachpy import Argument
        assert isinstance(argument_target, (Argument, str)), \
            "Either Argument object or argument name expected"
        if isinstance(argument_target, Argument):
            if argument_target in self.arguments:
                return argument_target
            else:
                return None
        else:
            return next((argument for argument in self.arguments if argument.name == argument_target), None)

    def add_instruction(self, instruction):
        # If instruction is None, do nothing
        if instruction is None:
            return

        from peachpy.x86_64.instructions import Instruction
        if not isinstance(instruction, Instruction):
            raise TypeError("Instruction object expected")

        from peachpy.x86_64.pseudo import LABEL

        # Check that label with the same name is not added twice
        if isinstance(instruction, LABEL):
            if instruction.identifier in self._label_names:
                raise ValueError("A label named %s already exists in the function" % instruction.identifier)
            self._label_names.add(instruction.identifier)

        # Check that the instruction is supported by the target ISA
        for extension in instruction.isa_extensions:
            if extension not in self.target.extensions:
                raise ValueError("{0} is not supported on the target microarchitecture".format(extension))

        instruction._indent_level = self._indent_level
        self._instructions.append(instruction)

    def add_instructions(self, instructions):
        for instruction in instructions:
            self.add_instruction(instruction)

    def finalize(self, abi):
        from peachpy.x86_64.abi import ABI
        if not isinstance(abi, ABI):
            raise TypeError("%s is not an ABI object" % str(abi))
        return ABIFunction(self, abi)

    def _add_default_labels(self):
        """Adds default labels if they are not defined"""

        from peachpy.x86_64.pseudo import LABEL

        if self.entry.name not in self._label_names:
            self._instructions.insert(0, LABEL(self.entry))
            self._label_names.add(self.entry.name)

    def _check_undefined_labels(self):
        """Verifies that all labels referenced by branch instructions are defined"""

        from peachpy.x86_64.instructions import BranchInstruction
        referenced_label_names = set(
            [instruction.label_name for instruction in self._instructions
             if isinstance(instruction, BranchInstruction) and instruction.label_name])
        if not referenced_label_names.issubset(self._label_names):
            raise ValueError("Undefined labels found: " +
                             ", ".join(referenced_label_names.difference(self._label_names)))

    def _remove_unused_labels(self):
        """Removes labels that are not referenced by any instruction"""

        from peachpy.x86_64.instructions import BranchInstruction
        from peachpy.x86_64.pseudo import LABEL

        referenced_label_names = set(
            [instruction.label_name for instruction in self._instructions
             if isinstance(instruction, BranchInstruction) and instruction.label_name])
        unreferenced_label_names = self._label_names.difference(referenced_label_names)
        # Do not remove entry label if it is in the middle of the function
        if self.entry.name in unreferenced_label_names:
            if not isinstance(self._instructions[0], LABEL) or self._instructions[0].identifier != self.entry.name:
                unreferenced_label_names.remove(self.entry.name)
        # Remove LABEL pseudo-instructions with unreferenced label names
        self._instructions = [instruction for instruction in self._instructions
                              if not isinstance(instruction, LABEL) or
                              instruction.identifier not in unreferenced_label_names]
        self._label_names.difference_update(unreferenced_label_names)

    def _analize(self):
        from peachpy.x86_64.instructions import BranchInstruction
        from peachpy.x86_64.pseudo import LABEL, RETURN
        from peachpy.x86_64.generic import RET

        # Query input/output registers for each instruction
        input_registers = []
        output_registers = []
        for instruction in self._instructions:
            input_registers.append(instruction.input_registers_masks)
            output_registers.append(instruction.output_registers_masks)

        # Map from label name to its quasi-instruction number in the stream
        labels = {instruction.identifier: i for (i, instruction)
                  in enumerate(self._instructions) if isinstance(instruction, LABEL)}
        entry_position = 0
        if self.entry.name in self._label_names:
            entry_position = labels[self.entry.name]
        branch_instructions = [(i, instruction) for (i, instruction) in enumerate(self._instructions) if
                               isinstance(instruction, BranchInstruction) and instruction.label_name]
        # Basic blocks start at function entry position or on branch target
        basic_block_starts = {entry_position}
        for (i, branch_instruction) in branch_instructions:
            basic_block_starts.add(labels[branch_instruction.label_name])
            if branch_instruction.is_conditional:
                basic_block_starts.add(i+1)
        basic_block_starts = sorted(basic_block_starts)
        # Basic block ends on a referenced label instruction or right after return/branch instructions
        basic_block_ends = [i + int(not isinstance(instruction, LABEL)) for (i, instruction)
                            in enumerate(self._instructions) if
                            isinstance(instruction, (BranchInstruction, RETURN, RET, LABEL))]
        # TODO: check that the last block with an uncoditional branch/return instruction
        basic_block_bounds = [(start, basic_block_ends[bisect.bisect_right(basic_block_ends, start)])
                              for start in basic_block_starts]

        class BasicBlock:
            def __init__(self, start_position, end_position, input_registers_list, output_registers_list):
                self.start_position = start_position
                self.end_position = end_position
                self.input_registers_list = input_registers_list
                self.output_registers_list = output_registers_list

                self.consumed_register_masks = collections.defaultdict(int)
                self.produced_register_masks = collections.defaultdict(int)

                self.live_register_masks = collections.defaultdict(int)
                self.available_register_masks = collections.defaultdict(int)

                self.is_reachable = False

                self.liveness_analysis_passes = 0
                self.availability_analysis_passes = 0

                self.input_blocks = list()
                self.output_blocks = list()

                # Mark available and consumed registers:
                # - If a register is consumed by an instruction but not produced by preceding instructions of the basic
                #   block, the register is consumed by the basic block
                # - If a register is produced by an instruction, it becomes available for the subsequent instructions
                #   of the basic block and counts as produced by the basic block
                for (input_registers, output_registers) in zip(input_registers_list, output_registers_list):
                    for (input_register_id, input_register_mask) in six.iteritems(input_registers):
                        consumed_mask = input_register_mask & ~self.produced_register_masks[input_register_id]
                        if consumed_mask != 0:
                            self.consumed_register_masks[input_register_id] |= consumed_mask
                    for (output_register_id, output_register_mask) in six.iteritems(output_registers):
                        self.produced_register_masks[output_register_id] |= output_register_mask

            @property
            def available_registers_list(self):
                from peachpy.x86_64.registers import Register
                available_registers_list = []
                available_registers_masks = self.available_register_masks.copy()
                for output_registers in self.output_registers_list:
                    # Record available registers for current instruction
                    available_registers_list.append(available_registers_masks.copy())
                    # Update with output registers for current instruction
                    for (output_register_id, output_register_mask) in six.iteritems(output_registers):
                        available_registers_masks[output_register_id] = \
                            available_registers_masks.get(output_register_id, 0) | output_register_mask
                return available_registers_list

            @property
            def live_registers_list(self):
                from peachpy.x86_64.registers import Register
                live_registers_list = []
                live_registers_masks = self.live_register_masks.copy()
                for (input_registers, output_registers) in \
                        reversed(list(zip(self.input_registers_list, self.output_registers_list))):
                    # Mark register written by the instruction as non-live
                    for (output_register_id, output_register_mask) in six.iteritems(output_registers):
                        if output_register_id in live_registers_masks:
                            new_live_register_mask = live_registers_masks[output_register_id] & ~output_register_mask
                            if new_live_register_mask != 0:
                                live_registers_masks[output_register_id] = new_live_register_mask
                            else:
                                del live_registers_masks[output_register_id]
                    # Mark registers read by the instruction as live
                    for (input_register_id, input_register_mask) in six.iteritems(input_registers):
                        live_registers_masks[input_register_id] = \
                            live_registers_masks.get(input_register_id, 0) | input_register_mask
                    # Record available registers for current instruction
                    live_registers_list.append(live_registers_masks.copy())
                live_registers_list.reverse()
                return live_registers_list

            def __str__(self):
                return "[%d, %d)" % (self.start_position, self.end_position)

            def __repr__(self):
                return str(self)

            def analyze_availability(self, extra_available_registers=dict()):
                self.availability_analysis_passes += 1

                if self.availability_analysis_passes == 1:
                    # First pass: add registers produced by the block and propagate further
                    self.available_register_masks.update(extra_available_registers)
                    if self.output_blocks:
                        # Add registers produced by this block
                        for (produced_reg_id, produced_reg_mask) in six.iteritems(self.produced_register_masks):
                            extra_available_registers[produced_reg_id] =\
                                extra_available_registers.get(produced_reg_id, 0) | produced_reg_mask
                else:
                    # Subsequent passes: compute and propagate only the input registers that were not processed before
                    for (reg_id, extra_reg_mask) in list(six.iteritems(extra_available_registers)):
                        old_reg_mask = self.available_register_masks[reg_id]
                        update_reg_mask = extra_reg_mask & ~old_reg_mask
                        if update_reg_mask != 0:
                            self.available_register_masks[reg_id] |= extra_reg_mask
                        if self.output_blocks:
                            if update_reg_mask != 0:
                                extra_available_registers[reg_id] = update_reg_mask
                            else:
                                del extra_available_registers[reg_id]

                if self.output_blocks and (extra_available_registers or self.availability_analysis_passes == 1):
                    for output_block in self.output_blocks[1:]:
                        # The dict needs to be copied because output blocks can change it
                        output_block.analyze_availability(extra_available_registers.copy())
                    # Optimization: do not create a copy of the dict
                    self.output_blocks[0].analyze_availability(extra_available_registers)

            def analyze_liveness(self, extra_live_registers=dict()):
                # Update in liveness analysis consists of three steps:
                # 1. Update live registers for this basic block.
                # 2. Mark registers which are produced to by the basic block as non-live.
                # 3. Mark registers which are consumed by the basic block as live (only on first pass).

                self.liveness_analysis_passes += 1

                # Steps 1 and 2
                for (reg_id, extra_reg_mask) in list(six.iteritems(extra_live_registers)):
                    old_reg_mask = self.live_register_masks[reg_id]
                    update_reg_mask = extra_reg_mask & ~old_reg_mask
                    if update_reg_mask != 0:
                        self.live_register_masks[reg_id] |= extra_reg_mask
                    if self.input_blocks:
                        # On the first pass do not modify the extra live registers masks that are passed to input blocks
                        # On subsequent passes only the novel live registers need to be passed further
                        if self.liveness_analysis_passes == 1:
                            update_reg_mask = extra_reg_mask
                        update_reg_mask &= ~self.produced_register_masks.get(reg_id, 0)
                        if update_reg_mask != 0:
                            extra_live_registers[reg_id] = update_reg_mask
                        else:
                            del extra_live_registers[reg_id]

                # Step 3
                if self.input_blocks:
                    if self.liveness_analysis_passes == 1:
                        for (consumed_reg_id, consumed_reg_mask) in six.iteritems(self.consumed_register_masks):
                            extra_live_registers[consumed_reg_id] =\
                                extra_live_registers.get(consumed_reg_id, 0) | consumed_reg_mask

                if self.input_blocks and (extra_live_registers or self.liveness_analysis_passes == 1):
                    for input_block in self.input_blocks[1:]:
                        # The dict needs to be copied because input blocks can change it
                        input_block.analyze_liveness(extra_live_registers.copy())
                    # Optimization: do not create a copy of the dict
                    self.input_blocks[0].analyze_liveness(extra_live_registers)

            def analyze_reachability(self):
                if not self.is_reachable:
                    self.is_reachable = True
                    for output_block in self.output_blocks:
                        output_block.analyze_reachability()

        basic_blocks = list(map(lambda start_end:
                           BasicBlock(start_end[0], start_end[1],
                                      input_registers[start_end[0]:start_end[1]],
                                      output_registers[start_end[0]:start_end[1]]),
                           basic_block_bounds))
        # Map from block start position to BasicBlock object
        basic_blocks_map = {basic_block_start: basic_block
                            for (basic_block_start, basic_block) in zip(basic_block_starts, basic_blocks)}
        # Set output basic blocks for each basic block object
        for (i, basic_block) in enumerate(basic_blocks):
            # Consider last instruction of the basic block
            last_instruction = self._instructions[basic_block.end_position - 1]
            if isinstance(last_instruction, (RET, RETURN)):
                # Basic block that ends with a return instruction has no output blocks
                pass
            elif isinstance(last_instruction, BranchInstruction) and last_instruction.label_name:
                # Basic block that ends with a branch instruction can jump to the block at branch label
                target_position = labels[last_instruction.label_name]
                basic_block.output_blocks = [basic_blocks_map[target_position]]
                if last_instruction.is_conditional:
                    # Basic blocks that end with a conditional branch instruction can fall through to the next block
                    basic_block.output_blocks.append(basic_blocks[i+1])
            else:
                # Basic block ends before a label and continues to the next basic block
                basic_block.output_blocks = [basic_blocks[i+1]]
        # Set input basic blocks for each basic block object
        for basic_block in basic_blocks:
            basic_block.input_blocks = list(filter(lambda bb: basic_block in bb.output_blocks, basic_blocks))

        # Analyze which blocks can be reached from the entry point
        basic_blocks_map[entry_position].analyze_reachability()
        exit_positions = [block.start_position for block in basic_blocks if not block.output_blocks]

        # Analyze register lifetime
        basic_blocks_map[entry_position].analyze_availability()
        for exit_position in exit_positions:
            basic_blocks_map[exit_position].analyze_liveness()

        # Reconstruct live and available registers for the whole instruction sequence
        for basic_block in basic_blocks:
            for (instruction, available_registers, live_registers) in \
                    zip(self._instructions[basic_block.start_position:basic_block.end_position],
                        basic_block.available_registers_list, basic_block.live_registers_list):
                instruction._live_registers = live_registers
                instruction._available_registers = available_registers
            # Remove referenced to input/output blocks to avoid memory leaks due to cycles in ref graph
            basic_block.input_blocks = None
            basic_block.output_blocks = None

        # Analyze conflicting registers
        for instruction in self._instructions:
            virtual_registers = list(filter(operator.attrgetter("is_virtual"), instruction.registers))
            for virtual_register in virtual_registers:
                # TODO: generalize conflicts
                conflicting_ids = [reg_id for (reg_id, reg_mask)
                                   in six.iteritems(instruction._live_registers)
                                   if reg_mask & virtual_register.mask != 0]
                self._conflicting_registers[virtual_register.kind][-virtual_register.virtual_id]\
                    .update(conflicting_ids)

    def _check_live_registers(self):
        """Checks that the number of live registers does not exceed the number of physical registers for each insruction
        """
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, MaskRegister
        max_live_registers = {
            GeneralPurposeRegister._kind: 15,
            MMXRegister._kind: 8,
            XMMRegister._kind: 16,
            MaskRegister._kind: 8
        }
        for instruction in self._instructions:
            live_registers = max_live_registers.copy()
            for reg in instruction.live_registers:
                live_registers[reg.kind] -= 1
            if any(map(lambda c: c < 0, six.itervalues(live_registers))):
                raise peachpy.RegisterAllocationError(
                    "The number of live virtual registers exceeds physical constaints %s" % str(instruction))

    def _preallocate_registers(self):
        """Allocates registers that can be binded only to a single virtual register.

        Several instructions accept only a fixed a register as their operand. If a virtual register is supplied as such
        operand, it must be binded to the fixed register accepted by instruction encoding.

        These instructions are:

            - BLENDVPS xmm, xmm/m128, xmm0
            - BLENDVPD xmm, xmm/m128, xmm0
            - PBLENDVB xmm, xmm/m128, xmm0
            - SHA256RNDS2 xmm, xmm/m128, xmm0
            - SHR r/m, cl
            - SHL r/m, cl
            - SAR r/m, cl
            - SAL r/m, cl
            - ROR r/m, cl
            - ROL r/m, cl
            - SHRD r/m, r, cl
            - SHLD r/m, r, cl
        """

        from peachpy.x86_64.registers import GeneralPurposeRegister, XMMRegister, GeneralPurposeRegister8, xmm0, cl
        from peachpy import RegisterAllocationError
        cl_binded_registers = set()
        xmm0_binded_registers = set()
        for instruction in self._instructions:
            if instruction.name in {"BLENDVPD", "BLENDVPS", "PBLENDVB", "SHA256RNDS2"}:
                assert len(instruction.operands) == 3, \
                    "expected 3 operands, got %d (%s)" % \
                    (len(instruction.operands), ", ".join(map(str, instruction.operands)))
                xmm0_operand = instruction.operands[2]
                assert isinstance(xmm0_operand, XMMRegister), \
                    "expected xmm registers in the 3rd operand, got %s" % str(xmm0_operand)
                # Check that xmm0 is not live at this instruction
                if instruction._live_registers.get(xmm0._internal_id, 0) & XMMRegister._mask != 0:
                    raise RegisterAllocationError(
                        "Instruction %s requires operand 3 to be allocated to xmm0 register, " +
                        "but xmm0 is a live register" % instruction.name)
                if xmm0_operand.is_virtual:
                    xmm0_binded_registers.add(xmm0_operand._internal_id)
            elif instruction.name in {"SAL", "SAR", "SHL", "SHR", "ROL", "ROR"}:
                assert len(instruction.operands) == 2, \
                    "expected 2 operands, got %d (%s)" % \
                    (len(instruction.operands), ", ".join(map(str, instruction.operands)))
                count_operand = instruction.operands[1]
                # The count operand can be cl or imm8
                if isinstance(count_operand, GeneralPurposeRegister8) and count_operand.is_virtual:
                    # Check that cl is not live at this instruction
                    if instruction._live_registers.get(cl._internal_id, 0) & GeneralPurposeRegister8._mask != 0:
                        raise RegisterAllocationError(
                            "Instruction %s requires operand 2 to be allocated to cl register, " +
                            "but cl is a live register" % instruction.name)

                    cl_binded_registers.add(count_operand._internal_id)
            elif instruction.name in {"SHLD", "SHRD"}:
                assert len(instruction.operands) == 2, \
                    "expected 3 operands, got %d (%s)" % \
                    (len(instruction.operands), ", ".join(map(str, instruction.operands)))
                count_operand = instruction.operands[2]
                # The count operand can be cl or imm8
                if isinstance(count_operand, GeneralPurposeRegister8) and count_operand.is_virtual:
                    # Check that cl is not live at this instruction
                    if instruction._live_registers.get(cl._internal_id, 0) & GeneralPurposeRegister8._mask != 0:
                        raise RegisterAllocationError(
                            "Instruction %s requires operand 3 to be allocated to cl register, " +
                            "but cl is a live register" % instruction.name)

                    cl_binded_registers.add(count_operand._internal_id)

        # Check that cl-binded registers are not mutually conflicting
        for cl_register in cl_binded_registers:
            other_cl_registers = filter(operator.methodcaller("__ne__", cl_register), cl_binded_registers)
            conflicting_registers = self._conflicting_registers[1][cl_register]
            if any([other_register in conflicting_registers for other_register in other_cl_registers]):
                raise RegisterAllocationError("Two conflicting virtual registers are requred to bind to cl")

        # Check that xmm0-binded registers are not mutually conflicting
        for xmm0_register in xmm0_binded_registers:
            other_xmm0_registers = filter(operator.methodcaller("__ne__", xmm0_register), xmm0_binded_registers)
            conflicting_registers = self._conflicting_registers[3][xmm0_register]
            if any([other_register in conflicting_registers for other_register in other_xmm0_registers]):
                raise RegisterAllocationError("Two conflicting virtual registers are requred to bind to xmm0")

        # Commit register allocations
        for cl_register in cl_binded_registers:
            self._register_allocations[GeneralPurposeRegister._kind][cl_register] = cl.physical_id
        for xmm0_register in xmm0_binded_registers:
            self._register_allocations[XMMRegister._kind][xmm0_register] = xmm0.physical_id

    def _bind_registers(self):
        """Iterates through the list of instructions and assigns physical IDs to allocated registers"""

        for instruction in self._instructions:
            for register in instruction.registers:
                if register.is_virtual:
                    register.physical_id = \
                        self._register_allocations[register.kind].get(register._internal_id, register.physical_id)

    def _allocate_local_variable(self):
        """Returns a new unique ID for a local variable"""
        self._local_variables_count += 1
        return self._local_variables_count

    def _allocate_xmm_register_id(self):
        """Returns a new unique ID for a virtual SSE/AVX/AVX-512 (xmm/ymm/zmm) register"""
        self._virtual_xmm_registers_count += 1
        return self._virtual_xmm_registers_count

    def _allocate_mmx_register_id(self):
        """Returns a new unique ID for a virtual MMX (mm) register"""
        self._virtual_mmx_registers_count += 1
        return self._virtual_mmx_registers_count

    def _allocate_general_purpose_register_id(self):
        """Returns a new unique ID for a virtual general-purpose register"""
        self._virtual_general_purpose_registers_count += 1
        return self._virtual_general_purpose_registers_count

    def __str__(self):
        """Returns string representation of the function signature and instructions"""

        return self.format()

    def format_instructions(self, line_separator=os.linesep):
        """Formats instruction listing including data on input, output, available and live registers"""

        from peachpy.x86_64.pseudo import LABEL, ALIGN
        code = []
        tab = " " * 4
        for instruction in self._instructions:
            code.append(instruction.format("peachpy", indent=False))
            if not isinstance(instruction, (LABEL, ALIGN)):
                code.append(tab + "In regs:    " + ", ".join(sorted(map(str, instruction.input_registers))))
                code.append(tab + "Out regs:   " + ", ".join(sorted(map(str, instruction.output_registers))))
                code.append(tab + "Live regs:  " + ", ".join(sorted(map(str, instruction.live_registers))))
                code.append(tab + "Avail regs: " + ", ".join(sorted(map(str, instruction.available_registers))))
            code.append("")
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def format(self, line_separator=os.linesep):
        """Formats assembly listing of the function according to specified parameters"""

        code = [self.c_signature]
        for instruction in self._instructions:
            code.append(instruction.format("peachpy", indent=True))
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)


class Argument(peachpy.Argument):
    def __init__(self, argument, abi):
        """Extends generic Argument object with x86-64 specific attributes required for stack frame construction

        :ivar peachpy.x86_64.registers.Register register: the register in which the argument is passed to the function
            or None if the argument is passed on stack.
        :ivar peachpy.x86_64.operand.MemoryAddress rsp_offset: offset from the value of rsp on function entry to the
            location of the argument on stack or None if the argument is passed in a register and has no stack location.
            Note that in Microsoft X64 ABI the first four arguments are passed in registers but have stack space
            reserved for their storage. For these arguments both register and rsp_offset are non-null.
        """
        assert isinstance(argument, peachpy.Argument), \
            "Architecture-specific argument must be constructed from generic Argument object"
        from peachpy.x86_64.abi import ABI
        assert isinstance(abi, ABI), "ABI object expected"
        from copy import deepcopy
        super(Argument, self).__init__(deepcopy(argument.ctype), argument.name)
        self.abi = abi
        self.register = None
        self.rsp_offset = None
        self.save_on_stack = False

    @property
    def size(self):
        """Returns argument size in bytes.

        Argument size is ABI-dependent. If the function is finalized for a different ABI, the size might be different.
        """
        return self.ctype.get_size(self.abi)

    @property
    def passed_on_stack(self):
        return self.register is None


class ABIFunction:
    """ABI-specific x86-64 assembly function.

    A function consists of C signature, ABI, and a list of instructions without virtual registers.
    """

    def __init__(self, function, abi):
        from peachpy.x86_64.abi import ABI, microsoft_x64_abi, system_v_x86_64_abi, linux_x32_abi, \
            native_client_x86_64_abi, golang_amd64_abi, golang_amd64p32_abi
        from copy import copy, deepcopy
        assert isinstance(function, Function), "Function object expected"
        assert isinstance(abi, ABI), "ABI object expected"
        self.name = function.name
        self.arguments = list(map(lambda arg: Argument(arg, abi), function.arguments))
        self.result_type = function.result_type
        self.result_offset = None
        self.package = function.package
        self.target = function.target
        self.abi = abi
        self.c_signature = function.c_signature
        self.go_signature = function.go_signature

        self._instructions = deepcopy(function._instructions)
        self._conflicting_registers = function._conflicting_registers.copy()
        self._register_allocations = function._register_allocations.copy()

        # if any(map(bool, self._conflicting_registers.itervalues())):
        #     from peachpy import RegisterAllocationError
        #     raise RegisterAllocationError("Register allocation is not supported yet")

        if abi == microsoft_x64_abi:
            self._setup_windows_arguments()
        elif abi in {system_v_x86_64_abi, linux_x32_abi, native_client_x86_64_abi}:
            self._setup_unix_arguments()
        elif abi in {golang_amd64_abi, golang_amd64p32_abi}:
            self._setup_golang_arguments()
        else:
            raise ValueError("Unsupported ABI: %s" % str(abi))

        self.clobbered_registers = self._analyze_clobbered_registers()

        self._update_argument_loads(function.arguments)

        self._allocate_registers()
        self._bind_registers()

        self._lower_argument_loads()
        self._lower_pseudoinstructions()
        # self._lower_complex_instructions
        self._filter_instruction_encodings()

        # self.stack_frame = StackFrame(self.abi)

    def _update_argument_loads(self, arguments):
        from peachpy.x86_64.pseudo import LOAD
        for instruction in self._instructions:
            if isinstance(instruction, LOAD.ARGUMENT):
                instruction.operands = \
                    (instruction.operands[0], self.arguments[arguments.index(instruction.operands[1])])
                if instruction.operands[1].register in instruction.available_registers:
                    instruction.operands[1].save_on_stack = True

    def _setup_windows_arguments(self):
        from peachpy.x86_64.abi import microsoft_x64_abi
        assert self.abi == microsoft_x64_abi, \
            "This function must only be used with Microsoft x64 ABI"
        # The first 4 arguments are passed in registers, others are on stack.
        # 8 bytes on stack is reserved for each parameter (regardless of their size).
        # On-stack space is also reserved, but not initialized, for parameters passed in registers.
        # Arguments are NOT extended to 8 bytes, and high bytes of registers/stack cells may contain garbage.
        from peachpy.x86_64 import m64
        from peachpy.x86_64.registers import rcx, rdx, r8, r9, xmm0, xmm1, xmm2, xmm3
        floating_point_argument_registers = (xmm0, xmm1, xmm2, xmm3)
        integer_argument_registers = (rcx, rdx, r8, r9)
        for (index, argument) in enumerate(self.arguments):
            argument.passed_by_reference = argument.is_vector and argument != m64
            if index < 4:
                if argument.is_floating_point:
                    argument.register = floating_point_argument_registers[index]
                elif argument.is_integer or \
                        argument.is_pointer or \
                        argument.is_codeunit or \
                        argument.is_mask or \
                        argument.ctype == m64:
                    argument_register = integer_argument_registers[index]
                    argument.register = {
                        1: argument_register.as_low_byte,
                        2: argument_register.as_word,
                        4: argument_register.as_dword,
                        8: argument_register
                    }[argument.size]
                elif argument.is_vector:
                    argument.register = integer_argument_registers[index]
                else:
                    assert False
            # Stack offset does not include return address
            argument.stack_offset = index * 8

    def _setup_unix_arguments(self):
        from peachpy.x86_64.abi import system_v_x86_64_abi, linux_x32_abi, native_client_x86_64_abi
        assert self.abi in {system_v_x86_64_abi, linux_x32_abi, native_client_x86_64_abi}, \
            "This function must only be used with System V x86-64, Linux x32 or Native Client x86-64 SFI ABI"

        from peachpy.x86_64.registers import rdi, rsi, rdx, rcx, r8, r9, \
            xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7
        # The first 6 integer/pointer arguments are passed in general-purpose registers.
        # The first 8 floating-point arguments are passed in SSE registers.
        # For all integer arguments in excess of 6 and floating-point arguments in excess the caller reserves
        # 8 bytes on stack.
        # Arguments smaller than 4 bytes are extended (with sign-extension, if needed) to 4 bytes.
        # For 4-byte and smaller arguments passed on stack the high 4 bytes are not initialized.
        # For 4-byte and smaller arguments passed in registers the high 4 bytes are zero-initialized.
        # X32 and Native Client ABIs were not much tested, but they seem similar
        available_floating_point_registers = [xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7]
        available_integer_registers = [rdi, rsi, rdx, rcx, r8, r9]

        # Stack offset does not include return address
        stack_offset = 0
        for argument in self.arguments:
            if (argument.is_floating_point or argument.is_vector) and len(available_floating_point_registers) > 0:
                argument.register = available_floating_point_registers.pop(0)
                if argument.size == 8 or argument.size == 16:
                    pass
                elif argument.size == 32:
                    argument.register = argument.register.as_hword
                else:
                    assert False
            elif (argument.is_integer or argument.is_pointer or argument.is_codeunit) \
                    and len(available_integer_registers) > 0:
                argument_register = available_integer_registers.pop(0)
                argument.register = {
                    1: argument_register.as_dword,
                    2: argument_register.as_dword,
                    4: argument_register.as_dword,
                    8: argument_register
                }[argument.size]
            elif argument.is_vector or argument.is_mask:
                assert False
            else:
                argument.stack_offset = stack_offset
                stack_offset += 8

    def _setup_golang_arguments(self):
        from peachpy.x86_64.abi import golang_amd64_abi, golang_amd64p32_abi
        assert self.abi in {golang_amd64_abi, golang_amd64p32_abi}, \
            "This function must only be used with Golang AMD64 or AMD64p32 ABI"

        from peachpy.util import roundup
        # All arguments are passed on stack

        # Stack offset does not include the return address
        stack_offset = 0
        for index, argument in enumerate(self.arguments):
            # Arguments are aligned on stack
            stack_offset = roundup(stack_offset, argument.size)
            argument.stack_offset = stack_offset
            stack_offset += argument.size
        if self.result_type is not None:
            self.result_offset = roundup(stack_offset, self.result_type.size)

    def _allocate_registers(self):
        from peachpy.x86_64.registers import Register, GeneralPurposeRegister, MMXRegister, XMMRegister
        from peachpy.util import unique, append_unique

        allocation_options = {
            # Map from virtual register id to a list of possible allocations in priority order
            GeneralPurposeRegister._kind: dict(),
            MMXRegister._kind: dict(),
            XMMRegister._kind: dict()
        }
        from peachpy.x86_64.pseudo import LOAD
        for vreg_kind, vreg_ids in six.iteritems(self._conflicting_registers):
            for vreg_id in vreg_ids:
                allocation_options[vreg_kind][vreg_id] = []

        for instruction in self._instructions:
            if isinstance(instruction, LOAD.ARGUMENT):
                dst_reg = instruction.operands[0]
                src_arg = instruction.operands[1]
                assert isinstance(dst_reg, Register)
                assert isinstance(src_arg, Argument)
                if dst_reg.is_virtual and src_arg.register is not None:
                    allocation_options[dst_reg.kind][dst_reg._internal_id] = [src_arg.register.physical_id]

        # A list of physical register IDs ordered by allocation priority:
        # - Volatile and argument registers go first
        # - Then allocation may use non-volatile registers
        physical_register_ids = list(map(operator.attrgetter("physical_id"), self.abi.volatile_registers +
                                         list(reversed(self.abi.argument_registers)) + self.abi.callee_save_registers))
        for vreg_kind, vreg_ids in six.iteritems(allocation_options):
            for vreg_id in vreg_ids:
                allocation_options[vreg_kind][vreg_id] = \
                    unique(allocation_options[vreg_kind][vreg_id] + physical_register_ids)
                for conflicting_reg_id in self._conflicting_registers[vreg_kind][vreg_id]:
                    if conflicting_reg_id >= 0 and conflicting_reg_id in allocation_options[vreg_kind][vreg_id]:
                        allocation_options[vreg_kind][vreg_id].remove(conflicting_reg_id)
                # print("%d -> %s" % (vreg_id, str(allocation_options[vreg_kind][vreg_id])))

        # Allocate registers
        for vreg_kind, vreg_ids in six.iteritems(allocation_options):
            # Choose the register to allocate
            for vreg_id in vreg_ids:
                if not vreg_ids[vreg_id]:
                    raise Exception("Not physical registers for vreg_id = " + str(vreg_id))
                physical_id = vreg_ids[vreg_id].pop(0)
                for vconflict_id in self._conflicting_registers[vreg_kind][vreg_id]:
                    if vconflict_id in vreg_ids:
                        valloc_ids = vreg_ids[vconflict_id]
                        try:
                            valloc_ids.remove(physical_id)
                        except ValueError:
                            pass
                self._register_allocations[vreg_kind][vreg_id] = physical_id

    def _lower_argument_loads(self):
        from peachpy.x86_64.pseudo import LOAD
        from peachpy.x86_64.generic import MOV
        from peachpy.x86_64.mmxsse import MOVQ, MOVAPS
        from peachpy.x86_64.abi import golang_amd64_abi, golang_amd64p32_abi
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister
        from peachpy.x86_64.lower import load_register
        if self.abi == golang_amd64_abi or self.abi == golang_amd64p32_abi:
            # Like Peach-Py, Go assembler uses pseudo-instructions for argument loads
            return
        lowered_instructions = []
        for (i, instruction) in enumerate(self._instructions):
            if isinstance(instruction, LOAD.ARGUMENT):
                assert isinstance(instruction.operands[0],
                                  (GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister)), \
                    "Lowering LOAD.ARGUMENT is supported only for general-purpose, mmx, xmm, and ymm target registers"
                if instruction.operands[0] == instruction.operands[1].register:
                    # LOAD.ARGUMENT loads to the same register as passed in the argument; no actions needed
                    pass
                else:
                    lowered_instructions.append(load_register(instruction.operands[0],
                                                              instruction.operands[1].register,
                                                              instruction.operands[1].ctype,
                                                              prototype=instruction))
            else:
                lowered_instructions.append(instruction)
        self._instructions = lowered_instructions

    def _lower_pseudoinstructions(self):
        from peachpy.x86_64.pseudo import RETURN, STORE
        from peachpy.x86_64.abi import native_client_x86_64_abi, golang_amd64_abi, golang_amd64p32_abi
        from peachpy.util import is_uint32, is_int64
        from peachpy.stream import InstructionStream
        # The new list with lowered instructions
        instructions = list()
        for instruction in self._instructions:
            if isinstance(instruction, RETURN):
                from peachpy.x86_64 import m64, m128, m128d, m128i, m256, m256d, m256i
                from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister, \
                    rax, eax, ax, al, rcx, ecx, mm0, xmm0, ymm0
                from peachpy.x86_64.generic import XOR, MOV, MOVSX, MOVZX, POP, RET
                from peachpy.x86_64.mmxsse import MOVQ, MOVSS, MOVSD, MOVDQA, MOVAPD, MOVAPS
                from peachpy.x86_64.avx import VMOVDQA, VMOVAPD, VMOVAPS
                is_golang_abi = self.abi in {golang_amd64_abi, golang_amd64p32_abi}
                with InstructionStream() as stream:
                    # Save return value
                    if instruction.operands:
                        assert len(instruction.operands) == 1
                        if instruction.operands[0] == 0 and not is_golang_abi:
                            XOR(eax, eax, prototype=instruction)
                        elif is_uint32(instruction.operands[0]):
                            if is_golang_abi:
                                STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                            else:
                                MOV(eax, instruction.operands[0], prototype=instruction)
                        elif is_int64(instruction.operands[0]):
                            MOV(rax, instruction.operands[0], prototype=instruction)
                            if is_golang_abi:
                                STORE.RESULT(rax, prototype=instruction, target_function=self)
                        elif isinstance(instruction.operands[0], GeneralPurposeRegister):
                            if is_golang_abi and instruction.operands[0].size == self.result_type.size:
                                STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                            else:
                                if instruction.operands[0].size < 4:
                                    if self.result_type.is_signed_integer:
                                        if self.result_type <= 4:
                                            MOVSX(eax, instruction.operands[0], prototype=instruction)
                                        else:
                                            MOVSX(rax, instruction.operands[0], prototype=instruction)
                                    else:
                                        MOVZX(eax, instruction.operands[0], prototype=instruction)
                                elif instruction.operands[0].size == 4:
                                    if self.result_type.is_signed_integer:
                                        if self.result_type == 8:
                                            MOVSX(rax, instruction.operands[0], prototype=instruction)
                                        else:
                                            MOV(eax, instruction.operands[0], prototype=instruction)
                                    else:
                                        MOV(eax, instruction.operands[0], prototype=instruction)
                                else:
                                    MOV(rax, instruction.operands[0], prototype=instruction)
                                if is_golang_abi:
                                    reg_acc = {
                                        1: al,
                                        2: ax,
                                        4: eax,
                                        8: rax
                                    }[self.result_type.size]
                                    STORE.RESULT(reg_acc, prototype=instruction, target_function=self)
                        elif isinstance(instruction.operands[0], MMXRegister):
                            assert self.result_type == m64
                            if instruction.operands[0] != mm0:
                                MOVQ(mm0, instruction.operands[0], prototype=instruction)
                        elif isinstance(instruction.operands[0], XMMRegister):
                            if self.result_type.is_floating_point:
                                assert self.result_type.size in {4, 8}
                                if is_golang_abi:
                                    STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                                else:
                                    if instruction.operands[0] != xmm0:
                                        if self.result_type.size == 4:
                                            MOVSS(xmm0, instruction.operands[0], prototype=instruction)
                                        else:
                                            MOVSD(xmm0, instruction.operands[0], prototype=instruction)
                            else:
                                assert self.result_type in {m128, m128d, m128i}
                                if instruction.operands[0] != xmm0:
                                    MOV128 = {
                                        m128i: MOVDQA,
                                        m128d: MOVAPD,
                                        m128: MOVAPS
                                    }[self.result_type]
                                    MOV128(xmm0, instruction.operands[0], prototype=instruction)
                        elif isinstance(instruction.operands[0], YMMRegister):
                            assert self.result_type in {m256, m256d, m256i}
                            if instruction.operands[0] != ymm0:
                                MOV256 = {
                                    m256i: VMOVDQA,
                                    m256d: VMOVAPD,
                                    m256: VMOVAPS
                                }[self.result_type]
                                MOV256(ymm0, instruction.operands[0], prototype=instruction)
                        else:
                            assert False
                    # Return from the function
                    if self.abi == native_client_x86_64_abi:
                        from peachpy.x86_64.nacl import NACLJMP
                        POP(rcx, prototype=instruction)
                        NACLJMP(ecx)
                    else:
                        RET(prototype=instruction)
                instructions.extend(stream.instructions)
            elif isinstance(instruction, STORE.RESULT):
                instruction.destination_offset = self.result_offset
                instructions.append(instruction)
            else:
                if self.abi == native_client_x86_64_abi:
                    from peachpy.x86_64.operand import is_m
                    memory_operands = list(filter(lambda op: is_m(op), instruction.operands))
                    if memory_operands:
                        assert len(memory_operands) == 1, \
                            "x86-64 instructions can not have more than 1 explicit memory operand"
                        memory_address = memory_operands[0].address
                        if memory_address.index is not None:
                            raise ValueError("NaCl does allow index addressing")
                        from peachpy.x86_64.registers import rbp, rsp, r15
                        if memory_address.base is not None and memory_address.base not in {rbp, rsp, r15}:
                            # Base register is not a restricted register: needs transformation
                            with InstructionStream():
                                from peachpy.x86_64.generic import MOV
                                instructions.append(MOV(memory_address.base.as_dword, memory_address.base.as_dword))
                            memory_address.index = memory_address.base
                            memory_address.scale = 1
                            memory_address.base = r15
                instructions.append(instruction)
        self._instructions = instructions

    def _filter_instruction_encodings(self):
        for instruction in self._instructions:
            instruction.encodings = instruction._filter_encodings()

    def _analyze_clobbered_registers(self):
        output_registers = set()
        for instruction in self._instructions:
            output_registers.update(instruction.output_registers)
        return list(sorted(filter(lambda reg: reg in self.abi.callee_save_registers, output_registers)))

    def _bind_registers(self):
        """Iterates through the list of instructions and assigns physical IDs to allocated registers"""

        for instruction in self._instructions:
            for register in instruction.registers:
                if register.is_virtual:
                    register.physical_id = \
                        self._register_allocations[register.kind].get(register._internal_id, register.physical_id)

    def format_code(self, assembly_format="peachpy", line_separator=os.linesep, indent=True):
        """Returns code of assembly instructions comprising the function"""

        code = []
        for instruction in self._instructions:
            from peachpy.x86_64.instructions import Instruction
            # if isinstance(instruction, Instruction):
            #     try:
            #         hex_string = " ".join("%02X" % byte for byte in instruction.encode())
            #         code.append("    " + "# " + hex_string)
            #     except Exception as e:
            #         import sys
            #         code.append(e.message)
            #         # raise
            code.append(instruction.format(assembly_format=assembly_format, indent=indent))
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def format(self, assembly_format="peachpy", line_separator=os.linesep):
        """Formats assembly listing of the function according to specified parameters"""

        if assembly_format == "go":
            import operator

            # Arguments for TEXT directive in Go assembler
            package_string = self.package
            if package_string is None:
                package_string = ""
            if six.PY2:
                text_arguments = [package_string + "\xC2\xB7" + self.name + "(SB)"]
            else:
                text_arguments = [package_string + "\u00B7" + self.name + "(SB)"]

            text_arguments.append("4")
            stack_size = sum(map(operator.attrgetter("size"), self.arguments))
            if self.result_offset is not None:
                stack_size = self.result_offset + self.result_type.size
            if stack_size == 0:
                text_arguments.append("$0")
            else:
                text_arguments.append("$0-%d" % stack_size)

            code = ["TEXT " + ",".join(text_arguments)]
            if self.go_signature is not None:
                code.insert(0, "// " + self.go_signature)
        else:
            code = []

        code.extend(self.format_code(assembly_format, line_separator=None, indent=True))
        if assembly_format == "go":
            # Add trailing line or assembler will refuse to compile
            code.append("")
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def encode(self):
        return EncodedFunction(self)


class InstructionBundle:
    def __init__(self, capacity, start_address):
        if capacity not in {16, 32, 64}:
            raise ValueError("Bundle capacity must be 16, 32, or 64")
        self.capacity = capacity
        self.start_address = start_address
        self.size = 0
        self._instructions = []
        # Map from instruction position to tuple (label address, long encoding, short range)
        self.branch_info_map = dict()

    def add(self, instruction):
        from peachpy.x86_64.instructions import Instruction
        assert isinstance(instruction, Instruction), \
            "Instruction instance expected"
        bytecode = instruction.encode()
        if self.capacity - self.size > len(bytecode):
            self.size += len(bytecode)
            instruction.bytecode = bytecode
            self._instructions.append(instruction)
        else:
            raise BufferError()

    def add_label_branch(self, instruction, label_address=None, long_encoding=False):
        from peachpy.x86_64.instructions import BranchInstruction
        assert isinstance(instruction, BranchInstruction), \
            "BranchInstruction instance expected"
        long_encoding, bytecode = instruction._encode_label_branch(self.end_address, label_address, long_encoding)
        if self.capacity - self.size > len(bytecode):
            self.size += len(bytecode)
            if not long_encoding and label_address is not None:
                # offset = label_address - self.end_address
                # -> self.end_address = label_address - offset
                # -> branch_address = label_address - len(bytecode) - offset
                # -> branch_position = label_address - self.start_address - len(bytecode) - offset
                #
                # -> branch_pos >= label_address - self.start_address - len(bytecode) - 127
                # -> branch_pos <= label_address - self.start_address - len(bytecode) + 128
                branch_pos = label_address - self.start_address - len(bytecode)
                branch_pos_max = min(branch_pos + 128, self.capacity)
            else:
                branch_pos_max = self.capacity
            instruction.bytecode = bytecode
            self.branch_info_map[len(self._instructions)] = (label_address, long_encoding, branch_pos_max)
            self._instructions.append(instruction)
        else:
            raise BufferError()

    def realign(self):
        from peachpy.x86_64.instructions import BranchInstruction, Instruction
        from peachpy.x86_64.pseudo import LABEL
        from peachpy.util import diff
        encoding_options = []
        for i, instruction in enumerate(self._instructions):
            assert isinstance(instruction, Instruction)
            if isinstance(instruction, BranchInstruction):
                (label_address, long_encoding, branch_pos_max) = self.branch_info_map[i]
                length_encoding_map = dict()
                _, bytecode = instruction._encode_label_branch(self.end_address, label_address, long_encoding)
                encoding_options.append(list())
            else:
                length_options = instruction.encode_length_options().keys()
                min_length = min(length_options)
                encoding_options.append(
                    diff(sorted([length - min_length for length in length_options])))
        gap = self.capacity - self.size


    @property
    def label_address_map(self):
        from peachpy.x86_64.pseudo import LABEL
        label_address_map = dict()
        code_address = self.start_address
        for instruction in self._instructions:
            if isinstance(instruction, LABEL):
                label_address_map[instruction.identifier] = code_address
            else:
                code_address += len(instruction.bytecode)
        return label_address_map

    @property
    def end_address(self):
        return self.start_address + self.size

    def __len__(self):
        return self.size


class EncodedFunction:
    """ABI-specific x86-64 assembly function.

    A function consists of C signature, ABI, and a list of instructions without virtual registers.
    """

    def __init__(self, function):
        from copy import copy, deepcopy
        assert isinstance(function, ABIFunction), "ABIFunction object expected"
        self.name = function.name
        self.arguments = list(map(copy, function.arguments))
        self.result_type = function.result_type
        self.target = function.target
        self.abi = function.abi

        self._instructions = deepcopy(function._instructions)
        self._register_allocations = function._register_allocations.copy()

        self._encode()

    def _encode(self):
        from peachpy.x86_64.pseudo import LABEL
        from peachpy.x86_64.instructions import BranchInstruction
        label_address_map = dict()
        long_branches = set()

        has_updated_branches = True
        while has_updated_branches:
            code_address = 0
            has_updated_branches = False
            for (i, instruction) in enumerate(self._instructions):
                if isinstance(instruction, LABEL):
                    label_address_map[instruction.identifier] = code_address
                elif isinstance(instruction, BranchInstruction) and instruction.label_name:
                    label_address = label_address_map.get(instruction.label_name)
                    was_long = i in long_branches
                    is_long, instruction.bytecode = instruction._encode_label_branch(code_address, label_address,
                                                                                     long_encoding=was_long)
                    if is_long and not was_long:
                        long_branches.add(i)
                        has_updated_branches = True
                else:
                    instruction.bytecode = instruction.encode()
                if instruction.bytecode:
                    code_address += len(instruction.bytecode)

    def _encode_nops(self, length):
        assert 1 <= length <= 31
        from peachpy.x86_64.encoding import nop
        if length <= 15:
            return nop(length)
        elif length <= 30:
            return nop(length // 2) + nop(length - length // 2)
        else:
            return nop(8) + nop(8) + nop(15)

    def _encode_abort(self, length):
        from peachpy.x86_64.abi import native_client_x86_64_abi, golang_amd64_abi, golang_amd64p32_abi
        if self.abi == native_client_x86_64_abi:
            # Use HLT instructions
            return bytearray([0xF4] * length)
        elif self.abi in {golang_amd64_abi, golang_amd64p32_abi}:
            # Use a single INT 3 instruction as alignment is not supported anyway
            return bytearray([0xCD])
        else:
            # Use INT 3 instructions
            return bytearray([0xCD] * length)

    def format_code(self, assembly_format="peachpy", line_separator=os.linesep, indent=True):
        """Returns code of assembly instructions comprising the function"""

        code = []
        for instruction in self._instructions:
            code.append(instruction.format_encoding(indent=indent))
            code.append(instruction.format(assembly_format=assembly_format, indent=indent))
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(filter(lambda line: line is not None, code))

    def format(self, assembly_format="peachpy", line_separator=os.linesep):
        """Formats assembly listing of the function according to specified parameters"""

        if assembly_format == "go":
            # Arguments for TEXT directive in Go assembler
            text_arguments = ["%s\xC2\xB7%s(SB)" % (self.package_name, self.name)]

            text_arguments.append("4")
            text_arguments.append("$0")

            code = ["TEXT " + ",".join(text_arguments)]
        else:
            code = []

        code.extend(self.format_code(assembly_format, line_separator=None, indent=True))
        if assembly_format == "go":
            # Add trailing line or assembler will refuse to compile
            code.append("")
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def load(self):
        return ExecutableFuntion(self)

    @property
    def as_bytearray(self):
        return sum(filter(bool, map(operator.attrgetter("bytecode"), self._instructions)), bytearray())


class ExecutableFuntion:
    def __init__(self, function):
        from peachpy.util import roundup
        assert isinstance(function, EncodedFunction), "EncodedFunction object expected"

        self.code_segment = function.as_bytearray

        import peachpy.loader
        self.loader = peachpy.loader.Loader(len(self.code_segment))
        self.loader.copy_code(self.code_segment)

        import ctypes
        result_type = None if function.result_type is None else function.result_type.as_ctypes_type
        argument_types = [arg.ctype.as_ctypes_type for arg in function.arguments]
        self.function_type = ctypes.CFUNCTYPE(result_type, *argument_types)
        self.function_pointer = self.function_type(self.loader.code_address)

    def __call__(self, *args):
        return self.function_pointer(*args)

    def __del__(self):
        del self.loader
        self.loader = None
        self.function_pointer = None


class LocalVariable:
    def __init__(self, size_option, alignment=None):
        from peachpy.util import is_int
        if alignment is not None and not is_int(alignment):
            raise TypeError("alignment %s is not an integer" % str(alignment))
        if alignment is not None and alignment <= 0:
            raise ValueError("alignment %d is not a positive integer" % alignment)
        self.alignment = alignment
        if is_int(size_option):
            if size_option <= 0:
                raise ValueError("size %d is not a positive integer" % size_option)
            self.size = size_option
        elif isinstance(size_option, peachpy.x86_64.registers.Register):
            self.size = size_option.size
        else:
            raise TypeError('Unsupported size specification %s: register or integer expected' % size_option)
        if self.alignment is None:
            self.alignment = self.size
        self._id = active_function.allocate_local_variable()
        self._address = None
        self.offset = 0
        self.parent = None

    def __eq__(self, other):
        return isinstance(other, LocalVariable) and self._id == other._id

    def __ne__(self, other):
        return not isinstance(other, LocalVariable) or self._id != other._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        if self.address is not None:
            return "[{0}]".format(self.address)
        else:
            return "local-variable<{0}>".format(self._id)

    def __repr__(self):
        return str(self)

    @property
    def is_subvariable(self):
        return self.parent is not None

    @property
    def root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def address(self):
        node = self
        offset = 0
        while node.parent is not None:
            offset += node.offset
            node = node.parent
        return node._address + offset

    @property
    def low_half(self):
        assert self.size % 2 == 0
        child = LocalVariable(self.size // 2)
        child.parent = self
        child.offset = 0
        return child

    @property
    def high_half(self):
        assert self.size % 2 == 0
        child = LocalVariable(self.size // 2)
        child.parent = self
        child.offset = self.size // 2
        return child


class StackFrame(object):
    # Stack structure:
    # +---------------------------------------------------+
    # | On-stack parameters                               |
    # +---------------------------------------------------+
    # | Return address                                    |
    # +---------------------------------------------------+
    # | Preserved general-purpose registers               |
    # +---------------------------------------------------+
    # | Alignment                                         |
    # +---------------------------------------------------+
    # | Alignment bytes                                   |
    # +---------------------------------------------------+
    # | Preserved SSE registers                           |
    # +---------------------------------------------------+
    # | SSE local variables                               |
    # +---------------------------------------------------+
    # | AVX local variables                               |
    # +---------------------------------------------------+
    def __init__(self, abi):
        super(StackFrame, self).__init__()
        self.abi = abi
        self.general_purpose_registers = list()
        self.sse_registers = list()
        self.sse_variables = list()
        self.avx_variables = list()

    def preserve_registers(self, registers):
        for register in registers:
            self.preserve_register(register)

    def preserve_register(self, register):
        if isinstance(register, peachpy.x86_64.registers.GeneralPurposeRegister8):
            register = register.as_qword
        elif isinstance(register, peachpy.x86_64.registers.GeneralPurposeRegister16):
            register = register.as_qword
        elif isinstance(register, peachpy.x86_64.registers.GeneralPurposeRegister32):
            register = register.as_qword
        elif isinstance(register, peachpy.x86_64.registers.YMMRegister):
            register = register.as_xmm

        if register not in self.abi.callee_save_registers:
            return

        if isinstance(register, peachpy.x86_64.registers.GeneralPurposeRegister64):
            if register not in self.general_purpose_registers:
                self.general_purpose_registers.append(register)
        elif isinstance(register, peachpy.x86_64.registers.SSERegister):
            if register not in self.sse_registers:
                self.sse_registers.append(register)
        else:
            raise TypeError("Unsupported register regtype {0}".format(type(register)))

    def add_variable(self, variable):
        if variable.get_size() == 16:
            if variable not in self.sse_variables:
                self.sse_variables.append(variable)
        elif variable.get_size() == 32:
            if variable not in self.avx_variables:
                self.avx_variables.append(variable)
        else:
            raise TypeError("Unsupported variable regtype {0}".format(type(variable)))

    def get_parameters_address(self, use_rbp):
        if use_rbp:
            return peachpy.x86_64.registers.rbp + 16
        else:
            parameters_offset = 8 + \
                                len(self.general_purpose_registers) * 8 + \
                                len(self.sse_registers) * 16 + \
                                len(self.sse_variables) * 16
            # Take into account alignment for 16-byte entried on stack
            if len(self.general_purpose_registers) % 2 == 0 and (self.sse_registers or self.sse_variables):
                parameters_offset += 8
            return peachpy.x86_64.registers.rsp + parameters_offset

    def generate_prologue(self, use_avx, use_rbp):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.registers import rax, rbp, rsp
        from peachpy.x86_64.generic import PUSH, MOV, AND, SUB
        # from peachpy.x86_64.mmxsse import MOVAPS
        # from peachpy.x86_64.avx import VMOVAPS
        with InstructionStream() as instructions:
        # Save general-purpose registers on stack
            if use_rbp:
                PUSH(rbp)
                MOV(rbp, rsp)
            for register in self.general_purpose_registers:
                PUSH(register)
            # This parameters address is valid only is RBP is not used
            self.parameters_address = rsp + len(self.general_purpose_registers) * 8
            variables_size = len(self.sse_variables) * 16 + len(self.avx_variables) * 32
            if len(self.avx_variables) != 0:
                # Align stack on 32
                if use_rbp:
                    # Old stack pointer is already preserved in RBP
                    AND(rsp, -32)
                else:
                    MOV(rax, rsp)
                    SUB(rsp, 8)
                    AND(rsp, -32)
                    MOV([rsp], rax)
                stack_frame_size = len(self.sse_registers) * 16 + variables_size
                if stack_frame_size % 32 != 0:
                    stack_frame_size += 16
                assert stack_frame_size % 32 == 0
                SUB(rsp, stack_frame_size)
            else:
                if len(self.sse_registers) + len(self.sse_variables) != 0:
                    # Align stack on 16
                    stack_frame_size = len(self.sse_registers) * 16 + variables_size
                    if len(self.general_purpose_registers) % 2 == 0:
                        stack_frame_size += 8
                    SUB(rsp, stack_frame_size)
                    self.parameters_address += stack_frame_size
            # Save floating-point registers on stack
            for index, sse_register in enumerate(self.sse_registers):
                if use_avx:
                    VMOVAPS([rsp + variables_size + index * 16], sse_register)
                else:
                    MOVAPS([rsp + variables_size + index * 16], sse_register)

            # Assign addresses to local variables
            variable_offset = 0
            for variable in self.avx_variables + self.sse_variables:
                variable.address = rsp + variable_offset
                variable_offset += variable.get_size()

            # Fix parameters_address is RBP is used
            if use_rbp:
                self.parameters_address = rbp + 8

        return list(iter(instructions))

    def generate_epilogue(self, use_mmx, use_avx, use_rbp):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import MOV, POP, ADD
        # from peachpy.x86_64.mmxsse import MOVAPS, EMMS
        # from peachpy.x86_64.avx import VMOVAPS, VZEROUPPER
        with InstructionStream() as instructions:
            variables_size = len(self.sse_variables) * 16 + len(self.avx_variables) * 32
            # Restore floating-point registers from stack
            for index, sse_register in enumerate(self.sse_registers):
                if use_avx:
                    VMOVAPS(sse_register, [peachpy.x86_64.registers.rsp + variables_size + index * 16])
                else:
                    MOVAPS(sse_register, [peachpy.x86_64.registers.rsp + variables_size + index * 16])

            if use_rbp:
                MOV(peachpy.x86_64.registers.rsp, peachpy.x86_64.registers.rbp)
                POP(peachpy.x86_64.registers.rbp)
            else:
                # Restore stack pointer
                if len(self.avx_variables) != 0:
                    stack_frame_size = len(self.sse_registers) * 16 + variables_size
                    if stack_frame_size % 32 != 0:
                        stack_frame_size += 16

                    MOV(peachpy.x86_64.registers.rsp, [peachpy.x86_64.registers.rsp + stack_frame_size])
                else:
                    if len(self.sse_registers) + len(self.sse_variables) != 0:
                        stack_frame_size = len(self.sse_registers) * 16 + variables_size
                        if len(self.general_purpose_registers) % 2 == 0:
                            stack_frame_size += 8
                        ADD(peachpy.x86_64.registers.rsp, stack_frame_size)

            # Restore general-purpose registers from stack
            for register in reversed(self.general_purpose_registers):
                POP(register)
            if use_mmx:
                EMMS()
            if use_avx:
                VZEROUPPER()

        return list(iter(instructions))
