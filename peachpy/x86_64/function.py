# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
import os
import operator
import bisect
import collections
import six

import peachpy
import peachpy.writer
import peachpy.name
import peachpy.x86_64.instructions
import peachpy.x86_64.registers
import peachpy.x86_64.avx
import peachpy.x86_64.options
import peachpy.x86_64.meta


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
        :param Type result_type: the return type of the function. None if the function returns no value (void function).
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

        :ivar dict _named_constants: a dictionary that maps names of literal constants to Constant objects.
            As instructions are added the dictionary is used to track constants with same names, but different content.
        """
        self.name = name
        self.arguments = arguments
        self.result_type = result_type
        if package is None:
            self.package = peachpy.x86_64.options.package
        self.package = package
        if target is None:
            target = peachpy.x86_64.options.target
        if target is None:
            target = peachpy.x86_64.uarch.default
        if not isinstance(target, peachpy.x86_64.uarch.Microarchitecture):
            raise TypeError("%s is not an valid CPU target" % str(target))
        self.target = target
        if debug_level is None:
            self.debug_level = peachpy.x86_64.options.debug_level
        else:
            self.debug_level = int(debug_level)

        from peachpy.x86_64.pseudo import Label
        from peachpy.name import Name
        self.entry = Label((Name("__entry__", None),))

        self._indent_level = 1

        self._instructions = list()

        # This set is only used to ensure that all labels references in branches are defined
        self._label_names = set()
        # Map from id of Name objects to their copies.
        # This ensures that Name objects without name can be compared for equality using id
        self._names_memo = dict()
        self._scope = peachpy.name.Namespace(None)

        self._local_variables_count = 0
        self._virtual_general_purpose_registers_count = 0
        self._virtual_mmx_registers_count = 0
        self._virtual_xmm_registers_count = 0
        self._virtual_mask_registers_count = 0

        from peachpy.x86_64 import m256, m256d, m256i
        avx_types = [m256, m256d, m256i]
        self.avx_environment = any([arg.c_type in avx_types for arg in self.arguments]) or self.result_type in avx_types
        self._avx_prolog = None

        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, KRegister
        from peachpy.common import RegisterAllocator
        self._register_allocators = {
            GeneralPurposeRegister._kind: RegisterAllocator(),
            MMXRegister._kind: RegisterAllocator(),
            XMMRegister._kind: RegisterAllocator(),
            KRegister._kind: RegisterAllocator()
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

        def c_to_go_type(c_type):
            assert isinstance(c_type, peachpy.Type)
            if c_type.is_pointer:
                if c_type.base is not None:
                    return "*" + c_to_go_type(c_type.base)
                else:
                    return "uintptr"
            elif c_type.is_bool:
                return "boolean"
            elif c_type.is_size_integer:
                return "int" if c_type.is_signed_integer else "uint"
            elif c_type.is_signed_integer:
                return {
                    1: "int8",
                    2: "int16",
                    4: "int32",
                    8: "int64"
                }[c_type.size]
            elif c_type.is_unsigned_integer:
                return {
                    1: "uint8",
                    2: "uint16",
                    4: "uint32",
                    8: "uint64"
                }[c_type.size]
            elif c_type.is_floating_point:
                return {
                    4: "float32",
                    8: "float64"
                }[c_type.size]
            else:
                return None

        go_argument_types = list(map(c_to_go_type, map(operator.attrgetter("c_type"), self.arguments)))
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

    @property
    def isa_extensions(self):
        from peachpy.x86_64.isa import Extensions
        extensions = set()
        for instruction in self._instructions:
            extensions.update(instruction.isa_extensions)
        return Extensions(*extensions)

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
            if peachpy.x86_64.options.rtl_dump_file:
                peachpy.x86_64.options.rtl_dump_file.write(self.format_instructions())
            self._check_live_registers()
            self._preallocate_registers()
            self._bind_registers()
            self._scope.assign_names()
            if peachpy.x86_64.options.abi is not None:
                abi_function = self.finalize(peachpy.x86_64.options.abi)

                for writer in peachpy.writer.active_writers:
                    writer.add_function(abi_function)
        else:
            raise

    def attach(self):
        """Makes active the function and its associated instruction stream.

        While the instruction stream is active, generated instructions are added to this function.

        While the function is active, generated instructions are checked for compatibility with the function target.
        """
        import peachpy.stream
        import peachpy.common.function

        if peachpy.common.function.active_function is not None:
            raise ValueError("Can not attach the function: alternative function %s is active" %
                             peachpy.common.function.active_function.name)
        if peachpy.stream.active_stream is not None:
            raise ValueError("Can not attach the function instruction stream: alternative instruction stream is active")
        peachpy.common.function.active_function = self
        peachpy.stream.active_stream = self
        return self

    def detach(self):
        """Make the function and its associated instruction stream no longer active.

        The function and its instruction stream must be active before calling the method.
        """
        import peachpy.stream
        import peachpy.common.function
        if peachpy.common.function.active_function is None:
            raise ValueError("Can not detach the function: no function is active")
        if peachpy.common.function.active_function is not self:
            raise ValueError("Can not detach the function: a different function is active")
        peachpy.common.function.active_function = None
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
            self._scope.add_scoped_name(instruction.identifier)
            self._label_names.add(instruction.identifier)

        constant = instruction.constant
        if constant is not None:
            self._scope.add_scoped_name(constant.name)

        # Check that the instruction is supported by the target ISA
        for extension in instruction.isa_extensions:
            if self.target is not None and extension not in self.target.extensions:
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

        if self.entry.name not in self._scope.names:
            self._instructions.insert(0, LABEL(self.entry))
            self._scope.add_scoped_name(self.entry.name)
            self._label_names.add(self.entry.name)

    def _check_undefined_labels(self):
        """Verifies that all labels referenced by branch instructions are defined"""

        from peachpy.x86_64.instructions import BranchInstruction
        referenced_label_names = set()
        for instruction in self._instructions:
            if isinstance(instruction, BranchInstruction) and instruction.label_name:
                referenced_label_names.add(instruction.label_name)
        if not referenced_label_names.issubset(self._label_names):
            undefined_label_names = referenced_label_names.difference(self._label_names)
            raise ValueError("Undefined labels found: " +
                             ", ".join(map(lambda name: ".".join(map(str, name)), undefined_label_names)))

    def _remove_unused_labels(self):
        """Removes labels that are not referenced by any instruction"""

        from peachpy.x86_64.instructions import BranchInstruction
        from peachpy.x86_64.pseudo import LABEL

        referenced_label_names = set()
        for instruction in self._instructions:
            if isinstance(instruction, BranchInstruction) and instruction.label_name:
                referenced_label_names.add(instruction.label_name)
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

                self.processed_input_blocks = set()
                self.processed_output_blocks = set()

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

            def reset_processed_blocks(self):
                self.processed_input_blocks = set()
                self.processed_output_blocks = set()

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

            def analyze_availability(self, extra_available_registers):
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

            def analyze_liveness(self, extra_live_registers):
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

            def forward_pass(self, processing_function, instructions, input_state):
                output_state = processing_function(self, instructions, input_state)
                for output_block in self.output_blocks:
                    if output_block.start_position not in self.processed_output_blocks:
                        self.processed_output_blocks.add(output_block.start_position)
                        output_block.forward_pass(processing_function, instructions, output_state)

            def backward_pass(self, processing_function, instructions, input_state):
                output_state = processing_function(self, instructions, input_state)
                for input_block in self.input_blocks:
                    if input_block.start_position not in self.processed_input_blocks:
                        self.processed_input_blocks.add(input_block.start_position)
                        input_block.backward_pass(processing_function, instructions, output_state)

            def propogate_sse_avx_state_forward(self, instructions, is_avx_environment):
                from peachpy.x86_64.avx import VZEROALL, VZEROUPPER
                from peachpy.x86_64.pseudo import LOAD, STORE
                avx_state = True if is_avx_environment else None

                def propogate_forward(block, instructions, avx_state):
                    for instruction in instructions[block.start_position:block.end_position]:
                        if isinstance(instruction, (VZEROUPPER, VZEROALL)):
                            avx_state = None
                        elif instruction.avx_mode is None:
                            # Instruction without a mode
                            if isinstance(instruction, (LOAD.ARGUMENT, STORE.RESULT, RETURN, RET, LABEL)):
                                # Some pseudo-instructions need AVX/SSE mode for lowering
                                instruction.avx_mode = avx_state
                        elif instruction.avx_mode:
                            # AVX-mode instruction
                            avx_state = True
                        else:
                            # SSE-mode instruction
                            if avx_state:
                                raise TypeError("AVX-mode instruction {0} follows an SSE-mode instruction".
                                                format(instruction))
                            avx_state = False
                    return avx_state
                self.forward_pass(propogate_forward, instructions, avx_state)

            def propogate_sse_state_backward(self, instructions, is_avx_environment):
                from peachpy.x86_64.pseudo import LOAD, STORE
                avx_state = True if is_avx_environment else None

                def propogate_sse_backward(block, instructions, avx_state):
                    for instruction in reversed(instructions[block.start_position:block.end_position]):
                        if instruction.avx_mode is not None:
                            avx_state = instruction.avx_mode
                        elif avx_state is not None and not avx_state:
                            if isinstance(instruction, (LOAD.ARGUMENT, STORE.RESULT, RETURN, RET, LABEL)):
                                instruction.avx_mode = avx_state
                    return avx_state
                self.backward_pass(propogate_sse_backward, instructions, avx_state)

            def propogate_avx_state_backward(self, instructions, is_avx_environment):
                from peachpy.x86_64.pseudo import LOAD, STORE
                avx_state = True if is_avx_environment else None

                def propogate_avx_backward(block, instructions, avx_state):
                    for instruction in reversed(instructions[block.start_position:block.end_position]):
                        if instruction.avx_mode is not None:
                            avx_state = instruction.avx_mode
                        elif avx_state:
                            if isinstance(instruction, (LOAD.ARGUMENT, STORE.RESULT, RETURN, RET, LABEL)):
                                instruction.avx_mode = avx_state
                self.backward_pass(propogate_avx_backward, instructions, avx_state)


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
        basic_blocks_map[entry_position].analyze_availability(dict())
        for exit_position in exit_positions:
            basic_blocks_map[exit_position].analyze_liveness(dict())

        # Analyze SSE/AVX mode
        basic_blocks_map[entry_position].propogate_sse_avx_state_forward(self._instructions, self.avx_environment)
        for exit_position in exit_positions:
            basic_blocks_map[exit_position].propogate_sse_state_backward(self._instructions, self.avx_environment)
        for basic_block in basic_blocks:
            basic_block.reset_processed_blocks()
        for exit_position in exit_positions:
            basic_blocks_map[exit_position].propogate_avx_state_backward(self._instructions, self.avx_environment)
        self._avx_prolog = self._instructions[entry_position].avx_mode

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
        output_registers = set()
        for instruction in self._instructions:
            instruction_registers = instruction.input_registers
            instruction_registers.update(output_registers)
            for instruction_register in instruction_registers:
                if instruction_register.is_virtual:
                    conflict_internal_ids = [reg_id for (reg_id, reg_mask)
                                             in six.iteritems(instruction._live_registers)
                                             if reg_mask & instruction_register.mask != 0]
                    self._register_allocators[instruction_register.kind].add_conflicts(
                        instruction_register.virtual_id, conflict_internal_ids)
            physical_registers = [r for r in instruction_registers
                                  if not r.is_virtual]
            if physical_registers:
                from peachpy.x86_64.registers import Register
                live_virtual_registers = \
                    Register._reconstruct_multiple({reg_id: reg_mask for (reg_id, reg_mask)
                                                   in six.iteritems(instruction._live_registers)
                                                   if reg_id < 0})
                for live_virtual_register in live_virtual_registers:
                    conflict_internal_ids = [reg._internal_id for reg in physical_registers
                                             if reg.mask & live_virtual_register.mask != 0]
                    self._register_allocators[live_virtual_register.kind].add_conflicts(
                        live_virtual_register.virtual_id, conflict_internal_ids)
            output_registers = instruction.output_registers

    def _check_live_registers(self):
        """Checks that the number of live registers does not exceed the number of physical registers for each insruction
        """
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, KRegister
        max_live_registers = {
            GeneralPurposeRegister._kind: 15,
            MMXRegister._kind: 8,
            XMMRegister._kind: 16,
            KRegister._kind: 8
        }
        for instruction in self._instructions:
            live_registers = max_live_registers.copy()
            for reg in instruction.live_registers:
                live_registers[reg.kind] -= 1
            if any(surplus_count < 0 for surplus_count in six.itervalues(live_registers)):
                if instruction.source_file is not None and instruction.line_number is not None:
                    raise peachpy.RegisterAllocationError(
                        "The number of live virtual registers exceeds physical constaints %s at %s:%d" %
                            (str(instruction), instruction.source_file, instruction.line_number))
                else:
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
            - SAR r/m, cl
            - SAL r/m, cl
            - SHL r/m, cl
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
                if xmm0_operand.is_virtual:
                    # Check that xmm0 is not live at this instruction
                    if instruction._live_registers.get(xmm0._internal_id, 0) & XMMRegister._mask != 0:
                        raise RegisterAllocationError(
                            ("Instruction %s requires operand 3 to be allocated to xmm0 register, " +
                            "but xmm0 is a live register") % str(instruction.name))
                    xmm0_binded_registers.add(xmm0_operand._internal_id)
            elif instruction.name in {"SAL", "SAR", "SHL", "SHR", "ROL", "ROR", "RCL", "RCR"}:
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
                assert len(instruction.operands) == 3, \
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
            for register in instruction.register_objects:
                if register.is_virtual:
                    register.physical_id = \
                        self._register_allocators[register.kind].register_allocations.get(
                            register._internal_id, register.physical_id)

    def _allocate_local_variable(self):
        """Returns a new unique ID for a local variable"""
        self._local_variables_count += 1
        return self._local_variables_count

    def _allocate_mask_register_id(self):
        """Returns a new unique ID for a virtual mask (k) register"""
        self._virtual_mask_registers_count += 1
        return self._virtual_mask_registers_count

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
        :ivar int stack_offset: offset from the end of return address on the stack to the location of the argument on
            stack or None if the argument is passed in a register and has no stack location. Note that in Microsoft X64
            ABI the first four arguments are passed in registers but have stack space reserved for their storage.
            For these arguments both register and stack_offset are non-null.
        :ivar peachpy.x86_64.operand.MemoryAddress address: address of the argument on stack, relative to rsp or rbp.
            The value of this attribute is None until after register allocation. In Golang ABIs this attribute is never
            initialized because to load arguments from stack Golang uses its own pseudo-register FP, which is not
            representable in PeachPy (LOAD.ARGUMENT pseudo-instructions use stack_offset instead when formatted as
            Golang assembly).
        """
        assert isinstance(argument, peachpy.Argument), \
            "Architecture-specific argument must be constructed from generic Argument object"
        from peachpy.x86_64.abi import ABI
        assert isinstance(abi, ABI), "ABI object expected"
        from copy import deepcopy
        super(Argument, self).__init__(deepcopy(argument.c_type), argument.name)
        if self.c_type.size is None:
            self.c_type.size = self.c_type.get_size(abi)
        self.abi = abi
        self.register = None
        self.address = None
        self.stack_offset = None
        self.save_on_stack = False

    @property
    def passed_on_stack(self):
        return self.register is None


class ABIFunction:
    """ABI-specific x86-64 assembly function.

    A function consists of C signature, ABI, and a list of instructions without virtual registers.
    """

    def __init__(self, function, abi):
        from peachpy.x86_64.abi import ABI, \
            microsoft_x64_abi, system_v_x86_64_abi, linux_x32_abi, native_client_x86_64_abi, \
            gosyso_amd64_abi, gosyso_amd64p32_abi, goasm_amd64_abi, goasm_amd64p32_abi
        from copy import deepcopy
        assert isinstance(function, Function), "Function object expected"
        assert isinstance(abi, ABI), "ABI object expected"
        self.name = function.name
        self.arguments = [Argument(argument, abi) for argument in function.arguments]
        self.result_type = function.result_type
        self.result_offset = None
        self.package = function.package
        self.target = function.target
        self.isa_extensions = function.isa_extensions
        self.abi = abi
        self.c_signature = function.c_signature
        self.go_signature = function.go_signature

        self.avx_environment = function.avx_environment
        self._avx_prolog = function._avx_prolog

        from peachpy.x86_64.registers import rsp
        self._stack_base = rsp
        self._stack_frame_size = 0
        self._stack_frame_alignment = self.abi.stack_alignment
        self._local_variables_size = 0

        self._instructions = deepcopy(function._instructions)
        self._register_allocators = deepcopy(function._register_allocators)

        if abi == microsoft_x64_abi:
            self._setup_windows_arguments()
        elif abi in {system_v_x86_64_abi, linux_x32_abi, native_client_x86_64_abi}:
            self._setup_unix_arguments()
        elif abi in {gosyso_amd64_abi, gosyso_amd64p32_abi, goasm_amd64_abi, goasm_amd64p32_abi}:
            self._setup_golang_arguments()
        else:
            raise ValueError("Unsupported ABI: %s" % str(abi))

        self._update_argument_loads(function.arguments)

        self._layout_local_variables()

        self._allocate_registers()
        self._bind_registers()

        self._clobbered_registers = self._analyze_clobbered_registers()
        self._update_stack_frame()
        self._update_argument_addresses()

        self._lower_argument_loads()
        self._lower_pseudoinstructions()
        self._filter_instruction_encodings()

        self.mangled_name = self.mangle_name()

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
                        argument.c_type == m64:
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
                if argument.size in {4, 8, 16}:
                    pass
                elif argument.size == 32:
                    argument.register = argument.register.as_ymm
                elif argument.size == 64:
                    argument.register = argument.register.as_zmm
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
        from peachpy.x86_64.abi import gosyso_amd64_abi, gosyso_amd64p32_abi, goasm_amd64_abi, goasm_amd64p32_abi
        assert self.abi in {gosyso_amd64_abi, gosyso_amd64p32_abi, goasm_amd64_abi, goasm_amd64p32_abi}, \
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

    def _layout_local_variables(self):
        from peachpy.x86_64.registers import rsp

        local_variables_set = set()
        local_variables_list = list()
        for instruction in self._instructions:
            local_variable = instruction.local_variable
            if local_variable is not None:
                local_variable = local_variable.root
                if local_variable not in local_variables_set:
                    local_variables_set.add(local_variable)
                    local_variables_list.append(local_variable)
        if local_variables_list:
            local_variables_list = list(sorted(local_variables_list, key=lambda var: var.size))
            self._stack_frame_alignment = max(var.alignment for var in local_variables_list)
            local_variable_address = 0
            from peachpy.util import roundup
            for local_variable in local_variables_list:
                local_variable_address = roundup(local_variable_address, local_variable.alignment)
                local_variable._address = local_variable_address
                local_variable_address += local_variable.size
            self._local_variables_size = local_variable_address

            for instruction in self._instructions:
                local_variable = instruction.local_variable
                if local_variable is not None:
                    assert local_variable.address is not None
                    memory_address = instruction.memory_address
                    assert memory_address is not None
                    assert memory_address.base == rsp
                    instruction.memory_address.displacement = local_variable.address

    def _allocate_registers(self):
        for register_kind, register_allocator in six.iteritems(self._register_allocators):
            register_allocator.set_allocation_options(self.abi, register_kind)

        from peachpy.x86_64.pseudo import LOAD
        from peachpy.x86_64.registers import Register, GeneralPurposeRegister, MMXRegister, XMMRegister, KRegister
        for instruction in self._instructions:
            if isinstance(instruction, LOAD.ARGUMENT):
                dst_reg = instruction.operands[0]
                src_arg = instruction.operands[1]
                assert isinstance(dst_reg, Register)
                assert isinstance(src_arg, Argument)
                if dst_reg.is_virtual and src_arg.register is not None:
                    self._register_allocators[dst_reg.kind]\
                        .try_allocate_register(dst_reg.virtual_id, src_arg.register.physical_id)

        for register_allocator in six.itervalues(self._register_allocators):
            register_allocator.allocate_registers()

    def _lower_argument_loads(self):
        from peachpy.x86_64.pseudo import LOAD
        from peachpy.x86_64.abi import goasm_amd64_abi, goasm_amd64p32_abi
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister
        from peachpy.x86_64.lower import load_register, load_memory
        if self.abi == goasm_amd64_abi or self.abi == goasm_amd64p32_abi:
            # Like PeachPy, Go assembler uses pseudo-instructions for argument loads
            return
        lowered_instructions = []
        for (i, instruction) in enumerate(self._instructions):
            if isinstance(instruction, LOAD.ARGUMENT):
                assert isinstance(instruction.operands[0],
                                  (GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister)), \
                    "Lowering LOAD.ARGUMENT is supported only for general-purpose, mmx, xmm, and ymm target registers"
                if instruction.operands[1].register is not None:
                    # The argument is passed to function in a register
                    ld_reg = load_register(instruction.operands[0],
                                           instruction.operands[1].register,
                                           instruction.operands[1].c_type,
                                           prototype=instruction)
                    if ld_reg is not None:
                        lowered_instructions.append(ld_reg)
                else:
                    # The argument is passed to function on stack
                    ld_mem = load_memory(instruction.operands[0],
                                         instruction.operands[1].address,
                                         instruction.operands[1].c_type,
                                         prototype=instruction)
                    lowered_instructions.append(ld_mem)
            else:
                lowered_instructions.append(instruction)
        self._instructions = lowered_instructions

    def _lower_pseudoinstructions(self):
        from peachpy.x86_64.pseudo import RETURN, STORE
        from peachpy.x86_64.mmxsse import MOVAPS
        from peachpy.x86_64.avx import VMOVAPS, VZEROUPPER
        from peachpy.x86_64.generic import PUSH, SUB, ADD, XOR, MOV, POP, RET, AND, LEA
        from peachpy.x86_64.nacl import NACLJMP, NACLRESTBP, NACLRESTSP, NACLASP, NACLSSP
        from peachpy.x86_64.lower import load_register
        from peachpy.x86_64.abi import native_client_x86_64_abi, \
            gosyso_amd64_abi, gosyso_amd64p32_abi, goasm_amd64_abi, goasm_amd64p32_abi
        from peachpy.x86_64.registers import GeneralPurposeRegister64, XMMRegister, rsp, rbp, eax
        from peachpy.util import is_uint32, is_sint32, is_int
        from peachpy.stream import InstructionStream
        # The new list with lowered instructions
        instructions = list()
        # Generate prologue
        cloberred_xmm_registers = list()
        cloberred_general_purpose_registers = list()
        with InstructionStream() as prolog_stream:
            # 1. Save clobbered general-purpose registers with PUSH instruction
            # 2. If there are clobbered XMM registers, allocate space for them on stack (subtract stack pointer)
            # 3. Save clobbered XMM registers on stack with (V)MOVAPS instruction
            for reg in self._clobbered_registers:
                assert isinstance(reg, (GeneralPurposeRegister64, XMMRegister)), \
                    "Internal error: unexpected register %s in clobber list" % str(reg)
                if isinstance(reg, GeneralPurposeRegister64):
                    cloberred_general_purpose_registers.append(reg)
                    PUSH(reg)
                else:
                    cloberred_xmm_registers.append(reg)
            # If stack needs to be realigned
            if self._stack_frame_alignment > self.abi.stack_alignment:
                cloberred_general_purpose_registers.append(rbp)
                PUSH(rbp)
                MOV(rbp, rsp)
            if cloberred_xmm_registers or self._local_variables_size != 0:
                # Total size of the stack frame less what is already adjusted with PUSH instructions
                stack_adjustment = \
                    self._stack_frame_size - len(cloberred_general_purpose_registers) * GeneralPurposeRegister64.size
                if self.abi != native_client_x86_64_abi:
                    SUB(rsp, stack_adjustment + self._local_variables_size)
                    if self._stack_frame_alignment > self.abi.stack_alignment:
                        AND(rsp, -self._stack_frame_alignment)
                else:
                    if self._stack_frame_alignment > self.abi.stack_alignment:
                        # Note: do not modify rcx/rdx/r8/r9 as they may contain function arguments
                        LEA(eax, [rsp - (stack_adjustment + self._local_variables_size)])
                        AND(eax, -self._stack_frame_alignment)
                        NACLRESTSP(eax)
                    else:
                        NACLSSP(stack_adjustment + self._local_variables_size)
            for i, xmm_reg in enumerate(cloberred_xmm_registers):
                movaps = VMOVAPS if self._avx_prolog else MOVAPS
                movaps([rsp + self._local_variables_size + i * XMMRegister.size], xmm_reg)

        # TODO: handle situations when entry point is in the middle of a function
        instructions.extend(prolog_stream.instructions)

        for instruction in self._instructions:
            if isinstance(instruction, RETURN):
                from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister, \
                    rax, eax, ax, al, rcx, ecx, mm0, xmm0, ymm0
                is_goasm_abi = self.abi in {goasm_amd64_abi, goasm_amd64p32_abi}
                is_gosyso_abi = self.abi in {gosyso_amd64_abi, gosyso_amd64p32_abi}
                with InstructionStream() as epilog_stream:
                    # Save return value
                    if instruction.operands:
                        assert len(instruction.operands) == 1
                        if is_int(instruction.operands[0]):
                            assert self.result_type.is_integer or self.result_type.is_pointer
                            # Return immediate constant
                            if is_goasm_abi:
                                # Return value must be saved on stack with STORE.RESULT pseudo-instruction
                                if self.result_type.size <= 4 or is_sint32(instruction.operands[0]):
                                    # STORE.RESULT will assemble to one of the forms:
                                    # - MOV m8, imm8
                                    # - MOV m16, imm16
                                    # - MOV m32, imm32
                                    # - MOV m64, imm32
                                    STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                                else:
                                    # STORE.RESULT can't be used directly (MOV m64, imm64 doesn't exist), instead use
                                    # MOV rax, imm64 + MOV m64, rax (STORE.RESULT)
                                    MOV(eax, instruction.operands[0], prototype=instruction)
                                    STORE.RESULT(eax, prototype=instruction, target_function=self)
                            else:
                                # Return value is returned in:
                                # - eax register if result type is not greater than 4 bytes
                                # - rax register if result type is greater than 8 bytes
                                if instruction.operands[0] == 0:
                                    # - Zero eax register (high 32 bits of rax register clear automatically)
                                    XOR(eax, eax, prototype=instruction)
                                elif self.result_type.size <= 4 or is_uint32(instruction.operands[0]):
                                    # - If the result type is not greater than 4 bytes, directly mov it to eax register
                                    # - If the result type is greater than 4 bytes, but the result value is
                                    #   representable as unsigned 32-bit literal, mov it to eax register and the high
                                    #   32 bits of rax will be cleared automatically
                                    MOV(eax, instruction.operands[0], prototype=instruction)
                                else:
                                    # - Either negative 32-bit constant (would use MOV rax, imm32 form)
                                    # - Or large 64-bit constant (would use MOV rax, imm64 form)
                                    MOV(rax, instruction.operands[0], prototype=instruction)
                        elif isinstance(instruction.operands[0], GeneralPurposeRegister):
                            if is_goasm_abi and instruction.operands[0].size == self.result_type.size:
                                STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                            else:
                                result_reg = eax if self.result_type.size <= 4 else rax
                                epilog_stream.add_instruction(load_register(result_reg,
                                                              instruction.operands[0],
                                                              self.result_type,
                                                              prototype=instruction))
                                if is_goasm_abi:
                                    result_subreg = {
                                        1: al,
                                        2: ax,
                                        4: eax,
                                        8: rax
                                    }[self.result_type.size]
                                    STORE.RESULT(result_subreg, prototype=instruction, target_function=self)
                        elif isinstance(instruction.operands[0], MMXRegister):
                            epilog_stream.add_instruction(load_register(mm0,
                                                          instruction.operands[0],
                                                          self.result_type,
                                                          prototype=instruction))
                        elif isinstance(instruction.operands[0], XMMRegister):
                            if self.result_type.is_floating_point and is_goasm_abi:
                                assert self.result_type.size in {4, 8}
                                STORE.RESULT(instruction.operands[0], prototype=instruction, target_function=self)
                            else:
                                epilog_stream.add_instruction(load_register(xmm0,
                                                              instruction.operands[0],
                                                              self.result_type,
                                                              prototype=instruction))
                        elif isinstance(instruction.operands[0], YMMRegister):
                            epilog_stream.add_instruction(load_register(ymm0,
                                                          instruction.operands[0],
                                                          self.result_type,
                                                          prototype=instruction))
                        else:
                            assert False
                    if instruction.avx_mode and not self.avx_environment:
                        VZEROUPPER(prototype=instruction)
                    # Generate epilog
                    # 1. Restore clobbered XMM registers on stack with (V)MOVAPS instruction
                    # 2. If there are clobbered XMM registers, release their space on stack (increment stack pointer)
                    # 3. Restore clobbered general-purpose registers with PUSH instruction
                    for i, xmm_reg in enumerate(cloberred_xmm_registers):
                        movaps = VMOVAPS if self.avx_environment else MOVAPS
                        movaps(xmm_reg, [rsp + self._local_variables_size + i * XMMRegister.size])
                    if self._stack_frame_alignment > self.abi.stack_alignment:
                        # Restore rsp value from rbp
                        MOV(rsp, rbp)
                    elif cloberred_xmm_registers or self._local_variables_size != 0:
                        # Total size of the stack frame less what will be adjusted with POP instructions
                        stack_adjustment = self._stack_frame_size - \
                            len(cloberred_general_purpose_registers) * GeneralPurposeRegister64.size
                        if self.abi != native_client_x86_64_abi:
                            ADD(rsp, stack_adjustment + self._local_variables_size)
                        else:
                            NACLASP(stack_adjustment + self._local_variables_size)
                    # Important: registers must be POPed in reverse order
                    for reg in reversed(cloberred_general_purpose_registers):
                        if reg == rbp and self.abi == native_client_x86_64_abi:
                            POP(rcx)
                            NACLRESTBP(ecx)
                        else:
                            POP(reg)
                    # Return from the function
                    if self.abi == native_client_x86_64_abi:
                        POP(rcx, prototype=instruction)
                        NACLJMP(ecx)
                    else:
                        RET(prototype=instruction)
                instructions.extend(epilog_stream.instructions)
            elif isinstance(instruction, STORE.RESULT):
                instruction.destination_offset = self.result_offset
                instructions.append(instruction)
            else:
                if self.abi == native_client_x86_64_abi and instruction.name != "LEA":
                    from peachpy.x86_64.operand import is_m
                    memory_operands = list(filter(lambda op: is_m(op), instruction.operands))
                    if memory_operands:
                        assert len(memory_operands) == 1, \
                            "x86-64 instructions can not have more than 1 explicit memory operand"
                        memory_address = memory_operands[0].address
                        from peachpy.x86_64.operand import MemoryAddress
                        if isinstance(memory_address, MemoryAddress):
                            if memory_address.index is not None:
                                raise ValueError("NaCl does not allow index addressing")
                            from peachpy.x86_64.registers import rbp, rsp, r15
                            if memory_address.base is not None and memory_address.base not in {rbp, rsp, r15}:
                                # Base register is not a restricted register: needs transformation
                                memory_address.index = memory_address.base
                                memory_address.scale = 1
                                memory_address.base = r15
                instructions.append(instruction)
        self._instructions = instructions

    def _filter_instruction_encodings(self):
        for instruction in self._instructions:
            instruction.encodings = instruction._filter_encodings()

    def _update_argument_addresses(self):
        for argument in self.arguments:
            if argument.stack_offset is not None:
                argument.address = self._argument_stack_base + argument.stack_offset

    def _analyze_clobbered_registers(self):
        from peachpy.x86_64.registers import GeneralPurposeRegister, XMMRegister, YMMRegister, ZMMRegister
        output_subregisters = set()
        for instruction in self._instructions:
            output_subregisters.update(instruction.output_registers)
        output_registers = set()
        for subreg in output_subregisters:
            if isinstance(subreg, GeneralPurposeRegister):
                output_registers.add(subreg.as_qword)
            elif isinstance(subreg, (XMMRegister, YMMRegister, ZMMRegister)):
                output_registers.add(subreg.as_xmm)
            # Other register types are volatile registers for all x86-64 ABIs
        return list(sorted(filter(lambda reg: reg in self.abi.callee_save_registers, output_registers)))

    def _update_stack_frame(self):
        from peachpy.x86_64.registers import GeneralPurposeRegister64, XMMRegister, rbp, rsp
        clobbered_general_purpose_registers = 0
        clobbered_xmm_registers = 0
        for reg in self._clobbered_registers:
            assert isinstance(reg, (GeneralPurposeRegister64, XMMRegister)), \
                "Internal error: unexpected register %s in clobber list" % str(reg)
            if isinstance(reg, GeneralPurposeRegister64):
                clobbered_general_purpose_registers += 1
            else:
                clobbered_xmm_registers += 1
        # If the stack needs to be aligned, rbp register needs to be preserved too
        if self._stack_frame_alignment > self.abi.stack_alignment:
            clobbered_general_purpose_registers += 1
        self._stack_frame_size = \
            clobbered_general_purpose_registers * GeneralPurposeRegister64.size + \
            clobbered_xmm_registers * XMMRegister.size
        # 1. On function entry stack is misaligned by 8
        # 2. Each clobbered general-purpose register is pushed as 8 bytes
        # 3. If the number of clobbered general-purpose registers is odd, the stack will be misaligned by 8 after they
        #    are pushed on stack
        # 4. If additionally there are clobbered XMM registers, we need to subtract 8 from stack to make it aligned
        #    by 16 after the general-purpose registers are pushed
        if (clobbered_xmm_registers != 0 or self._local_variables_size != 0) and clobbered_general_purpose_registers % 2 == 0:
            self._stack_frame_size += 8

        # Set stack_argument_base
        return_address_size = 8
        if self._stack_frame_alignment > self.abi.stack_alignment:
            # rsp is realigned, argument addressing uses rbp
            saved_rbp_size = 8
            self._argument_stack_base = rbp + return_address_size + saved_rbp_size
        else:
            # argument addressing uses rsp
            self._argument_stack_base = rsp + return_address_size + self._stack_frame_size + self._local_variables_size

    def _bind_registers(self):
        """Iterates through the list of instructions and assigns physical IDs to allocated registers"""

        for instruction in self._instructions:
            for register in instruction.register_objects:
                if register.is_virtual:
                    register.physical_id = \
                        self._register_allocators[register.kind].register_allocations[register.virtual_id]

    def format_code(self, assembly_format="peachpy", line_separator=os.linesep, indent=True, line_number=1):
        """Returns code of assembly instructions comprising the function"""

        code = []
        if assembly_format == "gas":
            # Pre-assign line number to labels
            from peachpy.x86_64.pseudo import LABEL
            for i, instruction in enumerate(self._instructions):
                if isinstance(instruction, LABEL):
                    instruction.operands[0].line_number = line_number + i

        for i, instruction in enumerate(self._instructions):
            from peachpy.x86_64.instructions import Instruction
            # if isinstance(instruction, Instruction):
            #     try:
            #         hex_string = " ".join("%02X" % byte for byte in instruction.encode())
            #         code.append("    " + "# " + hex_string)
            #     except Exception as e:
            #         import sys
            #         code.append(e.message)
            #         # raise
            code.append(instruction.format(assembly_format=assembly_format, indent=indent, line_number=line_number + i))
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def format(self, assembly_format="peachpy", line_separator=os.linesep, line_number=1):
        """Formats assembly listing of the function according to specified parameters"""

        if assembly_format == "go":
            # Arguments for TEXT directive in Go assembler
            package_string = self.package
            if package_string is None:
                package_string = ""
            if six.PY2:
                text_arguments = [package_string + "\xC2\xB7" + self.mangled_name + "(SB)"]
            else:
                text_arguments = [package_string + "\u00B7" + self.mangled_name + "(SB)"]

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
        elif assembly_format == "gas":
            from peachpy.util import ilog2
            code_alignment = 16
            code = [
                "#ifdef __APPLE__",
                ".section __TEXT,__text,regular,pure_instructions",
                ".globl _{name}".format(name=self.mangled_name),
                ".p2align {ilog2alignment}, 0x90".format(
                    ilog2alignment=ilog2(code_alignment)),
                "_{name}:".format(name=self.mangled_name),
                "#else /* !__APPLE__ */",
                ".text",
                ".p2align {ilog2alignment},,{max_alignment_bytes}".format(
                    ilog2alignment=ilog2(code_alignment),
                    max_alignment_bytes=code_alignment - 1),
                ".globl " + self.mangled_name,
                ".type {name}, @function".format(name=self.mangled_name),
                "{name}:".format(name=self.mangled_name),
                "#endif /* !__APPLE */",
            ]
        else:
            code = []

        code += self.format_code(assembly_format, line_separator=None, indent=True, line_number=line_number + len(code))
        if assembly_format == "gas":
            code += [
                "#ifndef __APPLE__",
                ".size {name}, .-{name}".format(name=self.mangled_name),
                "#endif /* !__APPLE__ */",
            ]

        if assembly_format in ["go", "gas"]:
            # Add trailing line or assembler will refuse to compile
            code.append("")
        if line_separator is None:
            return code
        else:
            return str(line_separator).join(code)

    def encode(self):
        return EncodedFunction(self)

    @property
    def metadata(self):
        metadata = collections.OrderedDict([
            ("entry", "function"),
            ("name", self.name),
            ("symbol", self.mangled_name),
            ("return",  "void" if self.result_type is None else str(self.result_type)),
            ("arguments", [collections.OrderedDict([
                ("name", argument.name),
                ("type", str(argument.c_type))]) for argument in self.arguments]),
            ("arch", "x86-64"),
            ("abi", str(self.abi)),
            ("uarch", self.target.name),
            ("isa", [str(extension) for extension in self.isa_extensions.minify()])
        ])
        return metadata

    def mangle_name(self):
        import peachpy.x86_64.options
        import string
        name = peachpy.x86_64.options.name_mangling \
            .replace("${Name}", self.name) \
            .replace("${name}", self.name.lower()) \
            .replace("${NAME}", self.name.upper()) \
            .replace("${uArch}", self.target.id) \
            .replace("${uarch}", self.target.id.lower()) \
            .replace("${UARCH}", self.target.id.upper()) \
            .replace("${ISA}", "_".join([extension.safe_name for extension in self.isa_extensions.minify()])) \
            .replace("${isa}", "_".join([extension.safe_name.lower() for extension in self.isa_extensions.minify()]))
        return name


class InstructionBundle:
    def __init__(self, capacity, address):
        if capacity not in {16, 32, 64}:
            raise ValueError("Bundle capacity must be 16, 32, or 64")
        self.capacity = capacity
        self.address = address
        self.size = 0
        self._instructions = []
        # Map from instruction position to tuple (label address, long encoding, short range)
        self.branch_info_map = dict()

    @property
    def padding(self):
        return self.capacity - self.size

    def add(self, instructions):
        from peachpy.x86_64.instructions import Instruction
        assert isinstance(instructions, list)
        assert all(isinstance(instruction, Instruction) for instruction in instructions), \
            "Instruction instance expected"
        bytecode = bytearray().join([instruction.encode() for instruction in instructions])
        if self.size + len(bytecode) <= self.capacity:
            self.size += len(bytecode)
            for instruction in instructions:
                instruction.bytecode = instruction.encode()
                self._instructions.append(instruction)
        else:
            raise BufferError()

    def add_label_branch(self, instruction, label_address=None, long_encoding=False):
        from peachpy.x86_64.instructions import BranchInstruction
        assert isinstance(instruction, BranchInstruction), \
            "BranchInstruction instance expected"
        long_encoding, bytecode = instruction._encode_label_branch(self.address + self.size, label_address, long_encoding)
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
                branch_pos = label_address - self.address - len(bytecode)
                branch_pos_max = min(branch_pos + 128, self.capacity)
            else:
                branch_pos_max = self.capacity
            instruction.bytecode = bytecode
            self.branch_info_map[len(self._instructions)] = (label_address, long_encoding, branch_pos_max)
            self._instructions.append(instruction)
        else:
            raise BufferError()

    def optimize(self):
        from peachpy.x86_64.instructions import BranchInstruction
        from peachpy.x86_64.pseudo import LABEL

        if any(isinstance(instruction, (BranchInstruction, LABEL)) for instruction in self._instructions):
            return

        def suitable_encodings(instruction):
            return [(encoding, length) for (length, encoding) in six.iteritems(instruction.encode_length_options())
                    if 0 < length - len(instruction.bytecode) <= self.padding]

        while self.size < self.capacity:
            suitable_instructions = [instr for instr in self._instructions if any(suitable_encodings(instr))]
            if not suitable_instructions:
                break

            shortest_suitable_instruction = min(suitable_instructions, key=lambda instr: len(instr.bytecode))
            new_encoding, new_length = min(suitable_encodings(shortest_suitable_instruction),
                                           key=operator.itemgetter(1))
            self.size += new_length - len(shortest_suitable_instruction.bytecode)
            assert self.size <= self.capacity
            shortest_suitable_instruction.bytecode = new_encoding

    def finalize(self):
        from peachpy.x86_64.generic import NOP
        while self.capacity > self.size:
            self.add([NOP()])
        self.size = self.capacity

    @property
    def label_address_map(self):
        from peachpy.x86_64.pseudo import LABEL
        label_address_map = dict()
        code_address = self.address
        for instruction in self._instructions:
            if isinstance(instruction, LABEL):
                label_address_map[instruction.identifier] = code_address
            else:
                code_address += len(instruction.bytecode)
        return label_address_map

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
        self.mangled_name = function.mangled_name
        self.arguments = list(map(copy, function.arguments))
        self.result_type = function.result_type
        self.target = function.target
        self.abi = function.abi

        from peachpy.x86_64.meta import Section, SectionType
        from peachpy.x86_64.abi import native_client_x86_64_abi
        if self.abi == native_client_x86_64_abi:
            # Align with HLT instruction
            self.code_section = Section(SectionType.code, alignment_byte=0xF4)
            self.code_section.alignment = 32
        else:
            # Align with INT 3 instruction
            self.code_section = Section(SectionType.code, alignment_byte=0xCC)
            self.code_section.alignment = 16

        self.const_section = Section(SectionType.const_data)

        self._instructions = deepcopy(function._instructions)

        self._constant_symbol_map = dict()
        self._layout_literal_constants()
        self._encode()

    def _layout_literal_constants(self):
        from peachpy.encoder import Encoder
        from peachpy.x86_64.meta import Symbol, SymbolType
        encoder = Encoder(self.abi.endianness)

        constants = list()
        for instruction in self._instructions:
            constant = instruction.constant
            if constant is not None:
                constants.append(constant)

        max_constant_size = 0
        max_constant_alignment = 0
        if constants:
            max_constant_size = max(constant.size for constant in constants)
            max_constant_alignment = max(constant.alignment for constant in constants)
        self.const_section.alignment = max_constant_alignment

        # Unsorted list of Symbol objects for constants
        constant_symbols = list()
        # This set is used to ensure that each constant is added only once
        constant_names_set = set()
        if max_constant_size != 0:
            # Map from constant value (as bytes) to address in the const data section
            constants_address_map = dict()

            for instruction in self._instructions:
                constant = instruction.constant
                if constant is not None:
                    constant_value = bytes(constant.encode(encoder))
                    if constant_value not in constants_address_map:
                        # Add the new constant to the section
                        assert constant.size == max_constant_size, \
                            "Handling of functions with constant literals of different size is not implemented"
                        assert constant.alignment == max_constant_alignment, \
                            "Handling of functions with constant literals of different alignment is not implemented"
                        constants_address_map[constant_value] = len(self.const_section)
                        self.const_section.content += constant_value
                    if constant.name not in constant_names_set:
                        constant_names_set.add(constant.name)
                        const_symbol = Symbol(constants_address_map[constant_value],
                                              SymbolType.literal_constant,
                                              name=constant.name,
                                              size=constant.size)
                        constant_symbols.append(const_symbol)
                        self._constant_symbol_map[constant.name] = const_symbol
        for constant_symbol in sorted(constant_symbols, key=lambda sym: (sym.offset, -sym.size)):
            self.const_section.add_symbol(constant_symbol)

    def _encode(self):
        from peachpy.x86_64.pseudo import LABEL
        from peachpy.x86_64.instructions import BranchInstruction
        label_address_map = dict()
        long_branches = set()

        # Special post-processing for Native Client SFI
        from peachpy.x86_64.abi import native_client_x86_64_abi
        if self.abi == native_client_x86_64_abi:
            has_updated_branches = True
            has_unresolved_labels = True
            bundles = list()
            while has_updated_branches or has_unresolved_labels:
                code_address = 0
                has_updated_branches = False
                has_unresolved_labels = False
                bundles = list()
                current_bundle = InstructionBundle(32, code_address)
                for (i, instruction) in enumerate(self._instructions):
                    if isinstance(instruction, LABEL):
                        label_address_map[instruction.identifier] = code_address
                        current_bundle.add([instruction])
                    elif isinstance(instruction, BranchInstruction) and instruction.label_name:
                        label_address = label_address_map.get(instruction.label_name)
                        if label_address is None:
                            has_unresolved_labels = True
                        was_long = i in long_branches
                        is_long, instruction.bytecode = instruction._encode_label_branch(code_address, label_address,
                                                                                         long_encoding=was_long)
                        if is_long and not was_long:
                            long_branches.add(i)
                            has_updated_branches = True
                        try:
                            current_bundle.add_label_branch(instruction, label_address, is_long)
                        except BufferError:
                            bundles.append(current_bundle)
                            current_bundle = InstructionBundle(32, current_bundle.address + current_bundle.capacity)
                            current_bundle.add_label_branch(instruction, label_address, is_long)
                    else:
                        instruction_group = [instruction]

                        memory_address = instruction.memory_address
                        from peachpy.x86_64.operand import MemoryAddress
                        if isinstance(memory_address, MemoryAddress) and memory_address.index is not None:
                            from peachpy.stream import NullStream
                            with NullStream():
                                from peachpy.x86_64.generic import MOV
                                instruction_group.insert(0,
                                    MOV(memory_address.index.as_dword, memory_address.index.as_dword)
                                )
                        try:
                            current_bundle.add(instruction_group)
                        except BufferError:
                            bundles.append(current_bundle)
                            current_bundle = InstructionBundle(32, current_bundle.address + current_bundle.capacity)
                            current_bundle.add(instruction_group)
                    code_address = current_bundle.address + current_bundle.size
                bundles.append(current_bundle)
            self._instructions = list()
            for bundle in bundles:
                bundle.optimize()
                for instruction in bundle._instructions:
                    constant = instruction.constant
                    if constant:
                        relocation = instruction.relocation
                        for index in range(relocation.offset, relocation.offset + 4):
                            instruction.bytecode[index] = 0
                        relocation.offset += len(self.code_section)
                        relocation.program_counter += len(self.code_section)
                        relocation.symbol = self._constant_symbol_map[instruction.constant.name]
                        self.code_section.add_relocation(relocation)

                    if instruction.bytecode:
                        self.code_section.content += instruction.bytecode
                if bundle.size < bundle.capacity:
                    if bundle is not bundles[-1]:
                        self.code_section.content += self._encode_nops(bundle.capacity - bundle.size)
                    else:
                        self.code_section.content += self._encode_abort(bundle.capacity - bundle.size)
        else:
            has_updated_branches = True
            has_unresolved_labels = True
            while has_updated_branches or has_unresolved_labels:
                code_address = 0
                has_updated_branches = False
                has_unresolved_labels = False
                for (i, instruction) in enumerate(self._instructions):
                    if isinstance(instruction, LABEL):
                        label_address_map[instruction.identifier] = code_address
                    elif isinstance(instruction, BranchInstruction) and instruction.label_name:
                        label_address = label_address_map.get(instruction.label_name)
                        if label_address is None:
                            has_unresolved_labels = True
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

            for instruction in self._instructions:
                constant = instruction.constant
                if constant:
                    relocation = instruction.relocation
                    for index in range(relocation.offset, relocation.offset + 4):
                        instruction.bytecode[index] = 0
                    relocation.offset += len(self.code_section)
                    relocation.program_counter += len(self.code_section)
                    relocation.symbol = self._constant_symbol_map[instruction.constant.name]
                    self.code_section.add_relocation(relocation)

                if instruction.bytecode:
                    self.code_section.content += instruction.bytecode

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
        from peachpy.x86_64.abi import native_client_x86_64_abi, goasm_amd64_abi, goasm_amd64p32_abi
        if self.abi == native_client_x86_64_abi:
            # Use HLT instructions
            return bytearray([0xF4] * length)
        elif self.abi in {goasm_amd64_abi, goasm_amd64p32_abi}:
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
            return str(line_separator).join(filter(bool, code))

    def load(self):
        return ExecutableFuntion(self)


class ExecutableFuntion:
    def __init__(self, function):
        assert isinstance(function, EncodedFunction), "EncodedFunction object expected"
        import peachpy.x86_64.abi
        process_abi = peachpy.x86_64.abi.detect()
        if process_abi != function.abi:
            raise ValueError("Function ABI (%s) does not match process ABI (%s)" %
                             (str(function.abi), str(process_abi)))

        self.code_segment = bytearray(function.code_section.content)
        self.const_segment = bytearray(function.const_section.content)

        import peachpy.loader
        self.loader = peachpy.loader.Loader(len(self.code_segment), len(self.const_segment))

        # Apply relocations
        from peachpy.x86_64.meta import RelocationType
        from peachpy.util import is_sint32
        for relocation in function.code_section.relocations:
            assert relocation.type == RelocationType.rip_disp32
            assert relocation.symbol in function.const_section.symbols
            old_value = self.code_segment[relocation.offset] | \
                (self.code_segment[relocation.offset + 1] << 8) | \
                (self.code_segment[relocation.offset + 2] << 16) | \
                (self.code_segment[relocation.offset + 3] << 24)
            new_value = old_value + \
                (self.loader.data_address + relocation.symbol.offset) - \
                (self.loader.code_address + relocation.program_counter)
            assert is_sint32(new_value)
            self.code_segment[relocation.offset] = new_value & 0xFF
            self.code_segment[relocation.offset + 1] = (new_value >> 8) & 0xFF
            self.code_segment[relocation.offset + 2] = (new_value >> 16) & 0xFF
            self.code_segment[relocation.offset + 3] = (new_value >> 24) & 0xFF
        assert not function.const_section.relocations

        self.loader.copy_code(self.code_segment)
        self.loader.copy_data(self.const_segment)

        import ctypes
        result_type = None if function.result_type is None else function.result_type.as_ctypes_type
        argument_types = [arg.c_type.as_ctypes_type for arg in function.arguments]
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
        self._address = None
        self._offset = 0
        self.parent = None

    def __eq__(self, other):
        return isinstance(other, LocalVariable) and self.root is other.root and \
            self.size == other.size and self.offset == other.offset

    def __ne__(self, other):
        return not isinstance(other, LocalVariable) or self.root is not other.root or \
            self.size != other.size or self.offset != other.offset

    def __hash__(self):
        return id(self.root) ^ hash(self.size) ^ hash(self.offset)

    def __str__(self):
        if self.address is not None:
            return "[" + str(self.address) + "]"
        else:
            return "local-variable<%d[%d:%d]>" % (id(self.root), self.offset, self.offset + self.size)

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
    def offset(self):
        node = self
        offset = 0
        while node.parent is not None:
            offset += node._offset
            node = node.parent
        return offset

    @property
    def address(self):
        if self.is_subvariable:
            base_address = self.root.address
            if base_address is not None:
                return base_address + self.offset
        else:
            return self._address

    @property
    def lo(self):
        assert self.size % 2 == 0
        child = LocalVariable(self.size // 2, min(self.size // 2, self.alignment))
        child.parent = self
        child._offset = 0
        return child

    @property
    def hi(self):
        assert self.size % 2 == 0
        child = LocalVariable(self.size // 2, min(self.size // 2, self.alignment))
        child.parent = self
        child._offset = self.size // 2
        return child
