# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import inspect

import peachpy.stream
import peachpy.x86_64.options
import peachpy.x86_64.isa
from peachpy.x86_64.instructions import Instruction
from peachpy.x86_64.operand import check_operand, format_operand_type
from peachpy.parse import parse_assigned_variable_name, parse_with_variable_name


class Label:
    def __init__(self, name=None):
        from peachpy.name import Name
        if name is None:
            import inspect
            self.name = (Name(prename=parse_assigned_variable_name(inspect.stack(), "Label")),)
        elif isinstance(name, tuple):
            assert all(isinstance(part, Name) for part in name), \
                "Name must a string or a tuple or Name objects"
            self.name = name
        else:
            Name.check_name(name)
            self.name = (Name(name=name),)
        self.line_number = None

    def __str__(self):
        """Returns a string representation of the name"""
        return ".".join(map(str, self.name))

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            # Go assembler rejects label names with a dot, so we replace it with underscore symbol
            return str(self).replace(".", "_")
        else:
            return str(self)

    @property
    def is_named(self):
        return not any(part.name is None for part in self.name)


class LABEL(Instruction):
    def __init__(self, label, origin=None):
        label = check_operand(label)
        super(LABEL, self).__init__("LABEL", origin=origin)
        self.operands = (label,)
        if not isinstance(label, Label):
            raise SyntaxError("Invalid operand for LABEL statement: Label object expected")
        self.identifier = label.name
        self.input_branches = set()
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def __str__(self):
        return ".".join(map(str, self.identifier)) + ":"

    def format(self, assembly_format, indent=False, line_number=None):
        assert assembly_format in {"peachpy", "gas", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gas', 'nasm', 'go'"

        if assembly_format == "go":
            # Go assembler rejects label names with a dot, so we replace it with underscore symbol
            return "_".join(map(str, self.identifier)) + ":"
        elif assembly_format == "gas":
            # GAS doesn't support named non-local labels
            if self.operands[0].line_number is None:
                return "." + str(self) + ":"
            else:
                return str(self.operands[0].line_number) + ": # " + str(self)
        else:
            return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise


class Loop:
    def __init__(self, name=None):
        from peachpy.name import Name
        if name is None:
            import inspect
            prename = parse_assigned_variable_name(inspect.stack(), "Loop")
            if prename is None:
                prename = parse_with_variable_name(inspect.stack(), "Loop")
            self.name = (Name(prename=prename),)
        elif isinstance(name, tuple):
            assert all(isinstance(part, Name) for part in name), \
                "Name must a string or a tuple or Name objects"
            self.name = name
        else:
            Name.check_name(name)
            self.name = (Name(name=name),)
        self.begin = Label(self.name + (Name(name="begin"),))
        self.end = Label(self.name + (Name(name="end"),))

    def __enter__(self):
        LABEL(self.begin)

        from peachpy.common.function import active_function
        if active_function is not None:
            active_function._indent_level += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        from peachpy.common.function import active_function
        if active_function is not None:
            active_function._indent_level -= 1

        if exc_type is None:
            LABEL(self.end)
        else:
            raise


class Block:
    def __init__(self, name=None):
        from peachpy.name import Name
        if name is None:
            import inspect
            prename = parse_assigned_variable_name(inspect.stack(), "Block")
            if prename is None:
                prename = parse_with_variable_name(inspect.stack(), "Block")
            self.name = (Name(prename=prename),)
        elif isinstance(name, tuple):
            assert all(isinstance(part, Name) for part in name), \
                "Name must a string or a tuple or Name objects"
            self.name = name
        else:
            Name.check_name(name)
            self.name = (Name(name=name),)
        self.begin = Label(self.name + (Name(name="begin"),))
        self.end = Label(self.name + (Name(name="end"),))

    def __enter__(self):
        LABEL(self.begin)

        from peachpy.common.function import active_function
        if active_function is not None:
            active_function._indent_level += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        from peachpy.common.function import active_function
        if active_function is not None:
            active_function._indent_level -= 1

        if exc_type is None:
            LABEL(self.end)
        else:
            raise


class ALIGN(Instruction):
    supported_alignments = (2, 4, 8, 16, 32)

    def __init__(self, alignment, origin=None):
        super(ALIGN, self).__init__('ALIGN', origin=origin)
        if not isinstance(alignment, int):
            raise TypeError("The alignment value must be an integer")
        if alignment not in ALIGN.supported_alignments:
            raise ValueError("The alignment value {0} is not in the list of supported alignments ({1})"
                             .format(alignment, ", ".join(ALIGN.supported_alignments)))
        self.alignment = alignment
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def __str__(self):
        return "align {0}".format(self.alignment)


class RETURN(Instruction):
    def __init__(self, *args, **kwargs):
        from peachpy.common.function import active_function
        from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(RETURN, self).__init__("RETURN", origin=origin)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) == 0:
            # It is not an error to return nothing from a function with a return type
            self.in_regs = tuple()
            self.out_regs = tuple()
            self.out_operands = tuple()
        elif len(self.operands) == 1:
            # It is an error to return something from a void function
            from peachpy.util import is_int64, int_size
            if active_function.result_type is None:
                raise ValueError("Void function should not return a value")
            if active_function.result_type.is_integer or active_function.result_type.is_pointer:
                if is_int64(self.operands[0]):
                    if active_function.result_type.size is None and int_size(self.operands[0]) > 4 or\
                        active_function.result_type.size is not None and \
                            active_function.result_type.size < int_size(self.operands[0]):
                        raise ValueError("Value {0} can not be represented with return type {1}".
                                         format(str(self.operands[0]), str(active_function.result_type)))
                    self.in_regs = (False,)
                    self.out_regs = (False,)
                    self.out_operands = (False,)
                elif isinstance(self.operands[0], GeneralPurposeRegister):
                    if active_function.result_type.size < self.operands[0].size:
                        raise ValueError("Register {0} can not be converted to return type {1}".
                                         format(str(self.operands[0]), str(active_function.result_type)))
                    self.in_regs = (True,)
                    self.out_regs = (False,)
                    self.out_operands = (False,)
                else:
                    raise TypeError("Invalid operand type: RETURN {0} for {1} function".
                                    format(str(self.operands[0]), str(active_function.result_type)))
            elif active_function.result_type.is_floating_point:
                if isinstance(self.operands[0], XMMRegister):
                    self.in_regs = (True,)
                    self.out_regs = (False,)
                    self.out_operands = (False,)
                else:
                    raise TypeError("Invalid operand type: RETURN {0} for {1} function".
                                    format(str(self.operands[0]), str(active_function.result_type)))
            elif active_function.result_type.is_vector:
                if isinstance(self.operands[0], (MMXRegister, XMMRegister, YMMRegister)) and \
                        active_function.result_type.size == self.operands[0].size:
                    self.in_regs = (True,)
                    self.out_regs = (False,)
                    self.out_operands = (False,)
                else:
                    raise TypeError("Invalid operand type: RETURN {0} for {1} function".
                                    format(str(self.operands[0]), str(active_function.result_type)))
            else:
                raise SyntaxError("Invalid operand type: RETURN " + ", ".join(map(format_operand_type, self.operands)))
        else:
            raise SyntaxError("Pseudo-instruction \"RETURN\" requires 0 or 1 operands")
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def __str__(self):
        if len(self.operands) == 0:
            return "RETURN"
        else:
            return "RETURN " + ", ".join(map(str, self.operands))

    def format(self, assembly_format, indent=False, line_number=None):
        text = "\t" if indent else ""
        if assembly_format == "peachpy":
            return text + str(self)
        else:
            raise SyntaxError("Invalid assembly format \"%s\"" % assembly_format)


class LOAD:
    class ARGUMENT(Instruction):
        def __init__(self, *args, **kwargs):
            from peachpy.common.function import active_function
            from peachpy.x86_64.registers import GeneralPurposeRegister, XMMRegister, YMMRegister
            from peachpy.x86_64 import m64

            origin = kwargs.get("origin")
            prototype = kwargs.get("prototype")
            if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
                origin = inspect.stack()
            super(LOAD.ARGUMENT, self).__init__("LOAD.ARGUMENT", origin=origin)
            self.operands = tuple(map(check_operand, args))
            self.out_regs = (True, False)
            self.in_regs = (False, False)
            if len(self.operands) != 2:
                raise SyntaxError("Instruction \"LOAD.ARGUMENT\" requires 2 operands")

            # Check source (second) operand
            if not isinstance(self.operands[1], peachpy.Argument):
                raise TypeError('The source operand to LOAD.ARGUMENT must be of Argument type')
            argument = active_function._find_argument(self.operands[1])
            if argument is None:
                raise ValueError('%s is not an argument of the active function' % str(self.operands[1]))

            # Check destination (first) operand
            if isinstance(self.operands[0], GeneralPurposeRegister) and (argument.is_integer or argument.is_pointer):
                if argument.size is not None and self.operands[0].size < argument.size:
                    raise ValueError("Destination register %s is too narrow for the argument %s"
                                     % (self.operands[0], argument))
            elif isinstance(self.operands[0], (XMMRegister, YMMRegister)) and argument.is_floating_point:
                pass
            elif isinstance(self.operands[0], (XMMRegister, YMMRegister)) and \
                    (argument.is_vector and argument.c_type != m64):
                pass
            else:
                raise ValueError("Unsupported combination of instruction operands")

            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(self)

        def format(self, assembly_format, indent=False, line_number=None):
            assert assembly_format in {"peachpy", "go"}, \
                "Supported assembly formats are 'peachpy' and 'go'"

            text = "\t" if indent else ""
            if assembly_format == "go":
                from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32, \
                    GeneralPurposeRegister16, GeneralPurposeRegister8, GeneralPurposeRegister, \
                    MMXRegister, XMMRegister, YMMRegister
                assert isinstance(self.operands[0], (GeneralPurposeRegister, MMXRegister, XMMRegister)), \
                    "LOAD.ARGUMENT must load into a general-purpose, mmx, or xmm register"
                if isinstance(self.operands[0], GeneralPurposeRegister8):
                    return text + "MOVB %s+%d(FP), %s" % \
                        (self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
                elif isinstance(self.operands[0], GeneralPurposeRegister16):
                    mov_name = {
                        (True, 1): "MOVWLSX",
                        (True, 2): "MOVW",
                        (False, 1): "MOVWLZX",
                        (False, 2): "MOVW"
                    }[(self.operands[1].is_signed_integer, self.operands[1].size)]
                    return text + "%s %s+%d(FP), %s" % \
                        (mov_name, self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
                elif isinstance(self.operands[0], GeneralPurposeRegister32):
                    mov_name = {
                        (True, 1): "MOVBLSX",
                        (True, 2): "MOVWLSX",
                        (True, 4): "MOVL",
                        (False, 1): "MOVBLZX",
                        (False, 2): "MOVWLZX",
                        (False, 4): "MOVL"
                    }[(self.operands[1].is_signed_integer, self.operands[1].size)]
                    return text + "%s %s+%d(FP), %s" % \
                        (mov_name, self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
                elif isinstance(self.operands[0], GeneralPurposeRegister64):
                    mov_name = {
                        (True, 1): "MOVBQSX",
                        (True, 2): "MOVWQSX",
                        (True, 4): "MOVLQSX",
                        (True, 8): "MOVQ",
                        (False, 1): "MOVBQZX",
                        (False, 2): "MOVWQZX",
                        (False, 4): "MOVLQZX",
                        (False, 8): "MOVQ"
                    }[(self.operands[1].is_signed_integer, self.operands[1].size)]
                    return text + "%s %s+%d(FP), %s" % \
                        (mov_name, self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
                elif isinstance(self.operands[0], MMXRegister):
                    mov_name = {
                        4: "MOVD",
                        8: "MOVQ"
                    }[self.operands[1].size]
                    return text + "%s %s+%d(FP), %s" % \
                        (mov_name, self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
                elif isinstance(self.operands[0], XMMRegister):
                    mov_name = {
                        4: "MOVD",
                        8: "MOVQ"
                    }[self.operands[1].size]
                    return text + "%s %s+%d(FP), %s" % \
                        (mov_name, self.operands[1].name, self.operands[1].stack_offset, self.operands[0].format("go"))
            else:
                return text + str(self)


class STORE:
    class RESULT(Instruction):
        def __init__(self, *args, **kwargs):
            from peachpy.common.function import active_function
            from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister
            from peachpy.util import is_int16, is_int32
            from peachpy.x86_64.abi import goasm_amd64_abi, goasm_amd64p32_abi

            origin = kwargs.get("origin")
            prototype = kwargs.get("prototype")
            if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
                origin = inspect.stack()
            super(STORE.RESULT, self).__init__("STORE.RESULT", origin=origin)
            self.operands = tuple(map(check_operand, args))
            self.out_regs = (False,)
            self.in_regs = (True,)
            if len(self.operands) != 1:
                raise SyntaxError("Instruction \"STORE.RESULT\" requires 1 operand")

            target_function = active_function
            destination_offset = None
            if target_function is None:
                target_function = kwargs.get("target_function")
                assert target_function.abi in {goasm_amd64_abi, goasm_amd64p32_abi}
                destination_offset = target_function.result_offset
            if target_function.result_type is None:
                raise ValueError("STORE.RESULT can't be used with void functions")
            self.destination_type = target_function.result_type
            self.destination_size = self.destination_type.size
            # Will be updated during ABI binding (ABIFunction._lower_pseudoinstructions)
            self.destination_offset = destination_offset

            if isinstance(self.operands[0], GeneralPurposeRegister):
                if self.operands[0].size != self.destination_size:
                    raise ValueError("Can not store result in register %s: size mismatch with return type %s"
                                     % (str(self.operands[0]), str(self.destination_type)))
            elif isinstance(self.operands[0], MMXRegister):
                if self.destination_size not in {4, 8}:
                    raise ValueError("Can not store result in register %s: size mismatch with return type %s"
                                     % (str(self.operands[0]), str(self.destination_type)))
            elif isinstance(self.operands[0], XMMRegister):
                if self.destination_size not in {4, 8}:
                    raise ValueError("Can not store result in register %s: size mismatch with return type %s"
                                     % (str(self.operands[0]), str(self.destination_type)))
            elif isinstance(self.operands[0], YMMRegister):
                raise ValueError("Can not store result in register %s: unsupported register type")
            elif is_int32(self.operands[0]):
                if not self.destination_type.is_integer:
                    raise ValueError("Can not store integer result %d: type mismatch with result type %s"
                                     % (self.operands[0], str(self.destination_type)))
                if is_int16(self.operands[0]) and self.destination_size < 2:
                    raise ValueError("Can not store integer result %d: size mismatch with result type %s"
                                     % (self.operands[0], str(self.destination_type)))
                if is_int32(self.operands[0]) and self.destination_size < 4:
                    raise ValueError("Can not store integer result %d: size mismatch with result type %s"
                                     % (self.operands[0], str(self.destination_type)))

            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(self)

        def format(self, assembly_format, indent=False, line_number=None):
            assert assembly_format in {"peachpy", "go"}, \
                "Supported assembly formats are 'peachpy' and 'go'"

            text = "\t" if indent else ""
            if assembly_format == "go":
                from peachpy.x86_64.registers import MMXRegister, XMMRegister
                from peachpy.x86_64.operand import format_operand

                if isinstance(self.operands[0], MMXRegister):
                    mov_name = {
                        4: "MOVD",
                        8: "MOVQ"
                    }[self.destination_size]
                elif isinstance(self.operands[0], XMMRegister):
                    if self.destination_type.is_floating_point:
                        mov_name = {
                            4: "MOVSS",
                            8: "MOVSD"
                        }[self.destination_size]
                    else:
                        mov_name = {
                            4: "MOVD",
                            8: "MOVQ"
                        }[self.destination_size]
                else:
                    mov_name = {
                        1: "MOVB",
                        2: "MOVW",
                        4: "MOVL",
                        8: "MOVQ"
                    }[self.destination_size]
                return text + "%s %s, ret+%d(FP)" % \
                    (mov_name, format_operand(self.operands[0], "go"), self.destination_offset)

            else:
                return text + str(self)


class SWAP:
    @staticmethod
    def REGISTERS(register_x, register_y):
        from peachpy.x86_64.registers import Register
        if isinstance(register_x, Register) and isinstance(register_y, Register):
            if register_x.kind == register_y.kind and register_x.size == register_y.size:
                register_x.virtual_id, register_y.virtual_id = register_y.virtual_id, register_x.virtual_id
                register_x.physical_id, register_y.physical_id = register_y.physical_id, register_x.physical_id
            else:
                raise ValueError("Registers {0} and {1} have incompatible register types"
                                 .format(register_x, register_y))
        else:
            raise TypeError("Arguments must be of register regtype")


def REDUCE(reduction_instruction, registers):
    if not isinstance(registers, (tuple, list)):
        raise ValueError("List or tuple of registers expected")
    offset = 1
    while offset < len(registers):
        for i in range(offset, len(registers), 2 * offset):
            reduction_instruction(registers[i - offset], registers[i])
        offset *= 2
    return registers[0]


class IACA:

    class START(Instruction):
        def __init__(self, *args, **kwargs):
            origin = kwargs.get("origin")
            prototype = kwargs.get("prototype")
            if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
                origin = inspect.stack()
            super(IACA.START, self).__init__("IACA.START", origin=origin)

            self.operands = tuple(map(check_operand, args))
            if len(self.operands) == 0:
                # It is not an error to return nothing from a function with a return type
                self.in_regs = tuple()
                self.out_regs = tuple()
                self.out_operands = tuple()
                self.encodings.append((0x0, lambda op: bytearray([0x0F, 0x0B, 0xBB, 0x6F, 0x00, 0x00, 0x00, 0x64, 0x67, 0x90])))
            else:
                raise SyntaxError("Pseudo-instruction \"IACA.START\" requires 0 operands")
            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(self)

    class END(Instruction):
        def __init__(self, *args, **kwargs):
            origin = kwargs.get("origin")
            prototype = kwargs.get("prototype")
            if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
                origin = inspect.stack()
            super(IACA.END, self).__init__("IACA.END", origin=origin)

            self.operands = tuple(map(check_operand, args))
            if len(self.operands) == 0:
                self.in_regs = tuple()
                self.out_regs = tuple()
                self.out_operands = tuple()
                self.encodings.append((0x0, lambda op: bytearray([0xBB, 0xDE, 0x00, 0x00, 0x00, 0x64, 0x67, 0x90, 0x0F, 0x0B])))
            else:
                raise SyntaxError("Pseudo-instruction \"IACA.END\" requires 0 operands")
            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(self)
