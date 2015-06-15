# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import inspect

import peachpy.stream
import peachpy.x86_64.options
import peachpy.x86_64.isa
from peachpy.x86_64.instructions import Instruction
from peachpy.x86_64.operand import check_operand, format_operand_type


class Label:
    def __init__(self, name=None):
        if name is None:
            import inspect
            import re

            source_line = inspect.stack()[1][4][0].strip()
            match = re.match("(?:\\w+\\.)*(\\w+)\\s*=\\s*(?:\\w+\\.)*Label\\(.*\\)", source_line)
            if match:
                name = match.group(1)
            else:
                match = re.match("\\s*with\\s+(?:\\w+\\.)*Label\\(.*\\)\\s+as\\s+(\\w+)\\s*:\\s*", source_line)
                if match:
                    name = match.group(1)
                else:
                    raise ValueError("Label name not specified")
        Label._check_name(name)
        self.name = name

    def __str__(self):
        """Returns a string representation of the name"""
        return self.name

    def format(self, assembly_format):
        assert assembly_format in {"peachpy", "gnu", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gnu', 'nasm', 'go'"

        if assembly_format == "go":
            # Go assembler rejects label names with a dot, so we replace it with Unicode middle dot symbol
            import six
            if six.PY2:
                return self.name.replace(".", "\xC2\xB7")
            else:
                import six
                return self.name.replace(".", six.unichr(0xB7))

        else:
            return str(self)

    @staticmethod
    def _check_name(name):
        """Verifies that the name is appropriate for a label"""
        if not isinstance(name, str):
            raise TypeError("Invalid label name %s: string required" % name)
        import re
        if not re.match("[_a-zA-Z]\\w*(?:\\.\\w+)*$", name):
            raise ValueError("Invalid label name " + name)
        if name.startswith("__") and name != "__entry__":
            raise ValueError("Invalid label name %s: names starting with __ are reserved for Peach-Py purposes" % name)


class LABEL(Instruction):
    def __init__(self, label, origin=None):
        label = check_operand(label)
        self.operands = (label,)
        super(LABEL, self).__init__("LABEL", origin=origin)
        if not isinstance(label, Label):
            raise SyntaxError("Invalid operand for LABEL statement: Label object expected")
        self.identifier = label.name
        self.input_branches = set()
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def __str__(self):
        return self.identifier + ':'

    def format(self, assembly_format, indent):
        assert assembly_format in {"peachpy", "gnu", "nasm", "go"}, \
            "Supported assembly formats are 'peachpy', 'gnu', 'nasm', 'go'"

        if assembly_format == "go":
            # Go assembler rejects label names with a dot, so we replace it with Unicode middle dot symbol
            import six
            if six.PY2:
                return self.identifier.replace(".", "\xC2\xB7") + ":"
            else:
                return self.identifier.replace(".", "\u00B7") + ":"
        else:
            return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise


class Loop:
    def __init__(self, name=None):
        if name is None:
            import inspect
            import re

            source_line = inspect.stack()[1][4][0].strip()
            match = re.match("(?:\\w+\\.)*(\\w+)\\s*=\\s*(?:\\w+\\.)*Loop\\(.*\\)", source_line)
            if match:
                name = match.group(1)
            else:
                match = re.match("\\s*with\\s+(?:\\w+\\.)*Loop\\(.*\\)\\s+as\\s+(\\w+)\\s*:\\s*", source_line)
                if match:
                    name = match.group(1)
                else:
                    raise ValueError("Loop name not specified")
        self.name = name
        self.begin = Label(self.name + ".begin")
        self.end = Label(self.name + ".end")

    def __enter__(self):
        LABEL(self.begin)

        from peachpy.x86_64.function import active_function
        if active_function is not None:
            active_function._indent_level += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        from peachpy.x86_64.function import active_function
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
        from peachpy.x86_64.function import active_function
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
                    if active_function.result_type.size < int_size(self.operands[0]):
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

    def format(self, assembly_format, indent):
        text = "\t" if indent else ""
        if assembly_format == "peachpy":
            return text + str(self)
        else:
            raise SyntaxError("Invalid assembly format \"%s\"" % assembly_format)


class LoadConstantPseudoInstruction(Instruction):
    def __init__(self, destination, source, origin=None):
        super(LoadConstantPseudoInstruction, self).__init__('<LOAD-CONSTANT>', origin=origin)
        if destination.is_register():
            self.destination = destination
        else:
            raise ValueError('Load constant pseudo-instruction expects a register as a destination')
        if source.is_constant():
            if destination.register.size * 8 == source.constant.size * source.constant.repeats:
                self.source = source
            elif destination.register.size == 16 and source.constant.size == 64 and source.constant.repeats == 1 and source.constant.basic_type == 'float64':
                self.source = source
            elif destination.register.size == 16 and source.constant.size == 32 and source.constant.repeats == 1 and source.constant.basic_type == 'float32':
                self.source = source
            else:
                raise ValueError('The size of constant should be the same as the size of register')
        else:
            raise ValueError('Load constant pseudo-instruction expects a Constant instance as a source')
        self.size = 4 + 4

    def __str__(self):
        return "LOAD.CONSTANT {0} = {1}".format(self.destination, self.source)


class AssumeInitializedPseudoInstruction(Instruction):
    def __init__(self, destination, origin=None):
        super(AssumeInitializedPseudoInstruction, self).__init__('<ASSUME-INITIALIZED>', origin=origin)
        if destination.is_register():
            self.destination = destination
        else:
            raise ValueError('Assume initialized pseudo-instruction expects a register as a destination')
        self.size = 0

    def __str__(self):
        return "ASSUME.INITIALIZED {0}".format(self.destination)


class LOAD:
    @staticmethod
    def CONSTANT(destination, source):
        from peachpy.x86_64.function import active_function
        origin = inspect.stack() if active_function.collect_origin else None
        instruction = LoadConstantPseudoInstruction(Operand(destination), Operand(source), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    class ARGUMENT(Instruction):
        def __init__(self, *args, **kwargs):
            from peachpy.x86_64.function import active_function
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
                    (argument.is_vector and argument.ctype != m64):
                pass
            else:
                raise ValueError("Unsupported combination of instruction operands")

            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(self)

        def format(self, assembly_format, indent):
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


    @staticmethod
    def ZERO(destination, ctype):
        from peachpy import Type
        if isinstance(ctype, Type):
            from peachpy.x86_64.registers import MMXRegister, SSERegister, AVXRegister
            from peachpy.x86_64.function import active_function
            if isinstance(destination, MMXRegister):
                PXOR(destination, destination)
            elif isinstance(destination, SSERegister):
                from peachpy.x86_64.avx import VXORPS, VXORPD, VPXOR
                from peachpy.x86_64.mmxsse import XORPS, XORPD, PXOR
                if ctype.is_floating_point:
                    if active_function.target.has_avx:
                        SIMD_XOR = {4: VXORPS, 8: VXORPD}[ctype.size]
                    else:
                        SIMD_XOR = {4: XORPS, 8: XORPD}[ctype.size]
                else:
                    SIMD_XOR = VPXOR if active_function.target.has_avx else PXOR
                SIMD_XOR(destination, destination)
            elif isinstance(destination, AVXRegister):
                LOAD.ZERO(destination.as_oword, ctype)
            else:
                raise TypeError("Unsupported regtype of destination register")
        else:
            raise TypeError("Type must be a C regtype")

    @staticmethod
    def ELEMENT(destination, source, ctype, increment_pointer=False):
        from peachpy import Type
        if isinstance(ctype, Type):
            from peachpy.x86_64.operand import Operand, byte, word, dword
            from peachpy.x86_64.function import active_function
            from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32, GeneralPurposeRegister16, GeneralPurposeRegister8, SSERegister, AVXRegister
            from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, ADD
            from peachpy.x86_64.mmxsse import MOVSS, MOVSD
            from peachpy.x86_64.avx import VMOVSS, VMOVSD
            if Operand(destination).is_register():
                if Operand(source).is_memory_address():
                    memory_size = ctype.get_size(peachpy.x86_64.function.active_function.abi)
                    source_address = source[0]
                    if isinstance(destination, GeneralPurposeRegister64):
                        if ctype.is_unsigned_integer or ctype.is_pointer:
                            if memory_size == 8:
                                MOV(destination, source)
                            elif memory_size == 4:
                                MOV(destination.get_dword(), source)
                            elif memory_size == 2:
                                MOVZX(destination.get_dword(), word[source_address])
                            elif memory_size == 1:
                                MOVZX(destination.get_dword(), byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        elif ctype.is_signed_integer:
                            if memory_size == 8:
                                MOV(destination, source)
                            elif memory_size == 4:
                                MOVSX(destination, dword[source_address])
                            elif memory_size == 2:
                                MOVSX(destination, word[source_address])
                            elif memory_size == 1:
                                MOVSX(destination, byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(destination, GeneralPurposeRegister32):
                        if ctype.is_unsigned_integer:
                            if memory_size == 4:
                                MOV(destination, source)
                            elif memory_size == 2:
                                MOVZX(destination, word[source_address])
                            elif memory_size == 1:
                                MOVZX(destination, byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        elif ctype.is_signed_integer:
                            if memory_size == 4:
                                MOV(destination, source)
                            elif memory_size == 2:
                                MOVSX(destination, word[source_address])
                            elif memory_size == 1:
                                MOVSX(destination, byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(destination, GeneralPurposeRegister16):
                        if ctype.is_unsigned_integer:
                            if memory_size == 2:
                                MOV(destination, source)
                            elif memory_size == 1:
                                MOVZX(destination, byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        elif ctype.is_signed_integer:
                            if memory_size == 2:
                                MOV(destination, source)
                            elif memory_size == 1:
                                MOVSX(destination, byte[source_address])
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(destination, GeneralPurposeRegister8):
                        if ctype.is_integer:
                            if memory_size == 1:
                                MOV(destination, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(destination, SSERegister):
                        if ctype.is_floating_point:
                            if memory_size == 4:
                                if active_function.target.has_avx:
                                    VMOVSS(destination, source)
                                else:
                                    MOVSS(destination, source)
                            elif memory_size == 8:
                                if active_function.target.has_avx:
                                    VMOVSD(destination, source)
                                else:
                                    MOVSD(destination, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(destination, AVXRegister):
                        if ctype.is_floating_point:
                            if memory_size == 4:
                                VMOVSS(destination.as_oword, source)
                            elif memory_size == 8:
                                VMOVSD(destination.as_oword, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    else:
                        raise TypeError("Destination must be a general-purpose register")
                    if increment_pointer:
                        ADD(source_address, memory_size)
                else:
                    raise TypeError("Source must be a memory operand")
            else:
                raise TypeError("Destination must be a register")
        else:
            raise TypeError("Type must be a C regtype")


class BROADCAST:
    @staticmethod
    def ELEMENT(destination, source, input_type, output_type=None):
        from peachpy import Type
        if output_type is None:
            output_type = input_type
        if isinstance(input_type, Type) and isinstance(output_type, Type):
            if input_type.is_integer:
                if not output_type.is_integer:
                    raise TypeError("Mismatch between input and output types")
                if input_type.is_unsigned_integer and not output_type.is_unsigned_integer:
                    raise TypeError("Mismatch between input and output types")
                if input_type.is_signed_integer and not output_type.is_signed_integer:
                    raise TypeError("Mismatch between input and output types")
                if input_type.size > output_type.size:
                    raise TypeError("Input regtype is wider than output regtype")
                from peachpy.x86_64.registers import SSERegister,\
                    GeneralPurposeRegister8, GeneralPurposeRegister16, GeneralPurposeRegister32, GeneralPurposeRegister64, GeneralPurposeRegister
                from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, IMUL
                from peachpy.x86_64.mmxsse import MOVD, MOVQ, PSHUFD, PUNPCKLQDQ

                if isinstance(destination, SSERegister) and input_type.size == 1:
                    if isinstance(source, GeneralPurposeRegister8):
                        pass
                    elif isinstance(source, GeneralPurposeRegister):
                        source = source.as_low_byte
                    else:
                        raise TypeError("Invalid source operand {0}".format(source))
                    if output_type.size == 1:
                        temp = GeneralPurposeRegister32()
                        MOVZX(temp, source)
                        IMUL(temp, temp, 0x01010101)
                        MOVD(destination, temp)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 2:
                        temp = GeneralPurposeRegister32()
                        if output_type.is_signed_integer:
                            MOVSX(temp.as_word, source)
                            source = temp.as_word
                        MOVZX(temp, source)
                        IMUL(temp, temp, 0x00010001)
                        MOVD(destination, temp)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 4:
                        temp = GeneralPurposeRegister32()
                        if output_type.is_signed_integer:
                            MOVSX(temp, source)
                        else:
                            MOVZX(temp, source)
                        MOVD(destination, temp)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 8:
                        if output_type.is_signed_integer:
                            temp = GeneralPurposeRegister64()
                            MOVSX(temp, source)
                            MOVQ(destination, temp)
                        else:
                            temp = GeneralPurposeRegister32()
                            MOVZX(temp, source)
                            MOVD(destination, temp)
                        PUNPCKLQDQ(destination, destination)
                    else:
                        raise TypeError("Unsupported output regtype {0}".format(output_type))
                elif isinstance(destination, SSERegister) and input_type.size == 2:
                    if isinstance(source, GeneralPurposeRegister16):
                        pass
                    elif isinstance(source, GeneralPurposeRegister32) or \
                            isinstance(source, GeneralPurposeRegister64):
                        source = source.as_word
                    else:
                        raise TypeError("Invalid source operand {0}".format(source))
                    if output_type.size == 2:
                        temp = GeneralPurposeRegister32()
                        MOVZX(temp, source)
                        IMUL(temp, temp, 0x00010001)
                        MOVD(destination, temp)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 4:
                        temp = peachpy.x86_64.register.GeneralPurposeRegister32()
                        if output_type.is_signed_integer:
                            MOVSX(temp, source)
                        else:
                            MOVZX(temp, source)
                        MOVD(destination, temp)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 8:
                        if output_type.is_signed_integer:
                            temp = peachpy.x86_64.register.GeneralPurposeRegister64()
                            MOVSX(temp, source)
                            MOVQ(destination, temp)
                        else:
                            temp = peachpy.x86_64.register.GeneralPurposeRegister32()
                            MOVZX(temp, source)
                            MOVD(destination, temp)
                        PUNPCKLQDQ(destination, destination)
                    else:
                        raise TypeError("Unsupported output regtype {0}".format(output_type))
                elif isinstance(destination, SSERegister) and input_type.size == 4:
                    if isinstance(source, GeneralPurposeRegister32):
                        pass
                    elif isinstance(source, GeneralPurposeRegister64):
                        source = source.get_dword()
                    else:
                        raise TypeError("Invalid source operand {0}".format(source))
                    if output_type.size == 4:
                        MOVD(destination, source)
                        PSHUFD(destination, destination, 0x00)
                    elif output_type.size == 8:
                        if output_type.is_signed_integer:
                            temp = GeneralPurposeRegister64()
                            MOVSX(temp, source)
                            MOVQ(destination, temp)
                        else:
                            MOVD(destination, source)
                        PUNPCKLQDQ(destination, destination)
                    else:
                        raise TypeError("Unsupported output regtype {0}".format(output_type))
                elif isinstance(destination, peachpy.x86_64.register.SSERegister) and input_type.size == 8:
                    if isinstance(source, peachpy.x86_64.register.GeneralPurposeRegister64):
                        pass
                    else:
                        raise TypeError("Invalid source operand {0}".format(source))
                    if output_type.size == 8:
                        MOVQ(destination, source)
                        PUNPCKLQDQ(destination, destination)
                    else:
                        raise TypeError("Unsupported output regtype {0}".format(output_type))
                else:
                    raise TypeError("Source must be a memory operand")
            else:
                raise TypeError("Unsupported input regtype {0}".format(input_type))
        else:
            raise TypeError("Input and output types must be C types")


class STORE:
    @staticmethod
    def ELEMENT(destination, source, ctype, increment_pointer=False):
        from peachpy import Type
        if isinstance(ctype, Type):
            if Operand(destination).is_memory_address():
                if Operand(source).is_register():
                    from peachpy.x86_64.function import active_function
                    from peachpy.x86_64.registers import GeneralPurposeRegister64, GeneralPurposeRegister32, GeneralPurposeRegister16, GeneralPurposeRegister8, SSERegister, AVXRegister
                    from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, ADD
                    from peachpy.x86_64.mmxsse import MOVSS, MOVSD
                    from peachpy.x86_64.avx import VMOVSS, VMOVSD
                    memory_size = ctype.get_size(peachpy.x86_64.function.active_function.abi)
                    if isinstance(source, peachpy.x86_64.registers.GeneralPurposeRegister64):
                        if ctype.is_integer:
                            if memory_size == 8:
                                MOV(destination, source)
                            elif memory_size == 4:
                                MOV(destination, source.get_dword())
                            elif memory_size == 2:
                                MOV(destination, source.get_word())
                            elif memory_size == 1:
                                MOV(destination, source.get_low_byte())
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        elif ctype.is_pointer:
                            if memory_size == 8:
                                MOV(destination, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(source, GeneralPurposeRegister32):
                        if ctype.is_integer:
                            if memory_size == 4:
                                MOV(destination, source)
                            elif memory_size == 2:
                                MOV(destination, source.get_word())
                            elif memory_size == 1:
                                MOV(destination, source.get_low_byte())
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(source, GeneralPurposeRegister16):
                        if ctype.is_integer:
                            if memory_size == 2:
                                MOV(destination, source)
                            elif memory_size == 1:
                                MOV(destination, source.get_low_byte())
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(source, GeneralPurposeRegister8):
                        if ctype.is_integer:
                            if memory_size == 1:
                                MOV(destination, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(source, SSERegister):
                        if ctype.is_floating_point:
                            if memory_size == 4:
                                if active_function.target.has_avx:
                                    VMOVSS(destination, source)
                                else:
                                    MOVSS(destination, source)
                            elif memory_size == 8:
                                if active_function.target.has_avx:
                                    VMOVSD(destination, source)
                                else:
                                    MOVSD(destination, source)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    elif isinstance(source, AVXRegister):
                        if ctype.is_floating_point:
                            if memory_size == 4:
                                VMOVSS(destination, source.as_oword)
                            elif memory_size == 8:
                                VMOVSD(destination, source.as_oword)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand regtype")
                    else:
                        raise TypeError("Source must be a general-purpose register")
                    if increment_pointer:
                        destination_address = destination[0]
                        ADD(destination_address, memory_size)
                else:
                    raise TypeError("Source must be a register")
            else:
                raise TypeError("Destination must be a memory operand")
        else:
            raise TypeError("Type must be a C regtype")

    class RESULT(Instruction):
        def __init__(self, *args, **kwargs):
            from peachpy.x86_64.function import active_function
            from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister
            from peachpy.util import is_int16, is_int32
            from peachpy.x86_64.abi import golang_amd64_abi, golang_amd64p32_abi

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
                assert target_function.abi in {golang_amd64_abi, golang_amd64p32_abi}
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

        def format(self, assembly_format, indent):
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


class ASSUME:
    @staticmethod
    def INITIALIZED(destination):
        from peachpy.x86_64.function import active_function
        origin = inspect.stack() if active_function.collect_origin else None
        instruction = AssumeInitializedPseudoInstruction(Operand(destination), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class INIT:
    @staticmethod
    def ONCE(register_class, constant, register=None):
        from peachpy.x86_64.function import active_function
        if register is None:
            origin = inspect.stack() if active_function.collect_origin else None
            register = register_class()
            instruction = LoadConstantPseudoInstruction(Operand(register), Operand(constant), origin=origin)
            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(instruction)
            return register
        else:
            return register


class REDUCE:
    @staticmethod
    def SUM(acc, input_type, output_type=None):
        from peachpy.x86_64.registers import SSERegister, AVXRegister
        from peachpy import Type, Yep32f, Yep64f
        if output_type is None:
            output_type = input_type
        if all(isinstance(register, AVXRegister) or isinstance(register, SSERegister) for register in acc):
            if isinstance(input_type, Type) and isinstance(output_type, Type):
                if input_type == output_type and input_type in {Yep32f, Yep64f}:
                    from peachpy.x86_64.mmxsse import ADDPS, ADDPD, ADDSS, ADDSD, MOVHLPS, HADDPS, HADDPD, MOVSHDUP,\
                        UNPCKLPS
                    from peachpy.x86_64.avx import VADDPS, VADDPD, VADDSS, VADDSD, VUNPCKHPD, VMOVSHDUP, VEXTRACTF128
                    from peachpy.x86_64.function import active_function
                    from peachpy.x86_64.uarch import Microarchitecture
                    if active_function.target.has_avx:
                        SIMD_ADD = {Yep32f: VADDPS, Yep64f: VADDPD}[input_type]
                        SCALAR_ADD = {Yep32f: VADDSS, Yep64f: VADDSD}[input_type]

                        def SIMD_H2L(destination, source):
                            VUNPCKHPD(destination, source, source)
                    else:
                        SIMD_ADD = {Yep32f: ADDPS, Yep64f: ADDPD}[input_type]
                        SCALAR_ADD = {Yep32f: ADDSS, Yep64f: ADDSD}[input_type]

                        def SIMD_H2L(destination, source):
                            ASSUME.INITIALIZED(destination)
                            MOVHLPS(destination, source)

                    def SIMD_REDUCE_ADD(acc):
                        if active_function.target == Microarchitecture.K10:
                            # On K10 HADDPS/HADDPD are efficient
                            if input_type.size == 4:
                                HADDPS(acc, acc)
                                HADDPS(acc, acc)
                            else:
                                HADDPD(acc, acc)
                        else:
                            # On all other CPUs HADDPS/HADDPD are decomposed into two unpack + one add microoperations,
                            # but we can do reduction with only one shuffle + one add
                            if isinstance(acc, AVXRegister):
                                temp = SSERegister()
                                VEXTRACTF128(temp, acc, 1)
                                acc = acc.as_oword
                                SIMD_ADD(acc, temp)
                            temp = SSERegister()
                            SIMD_H2L(temp, acc)
                            # SP floats need additional reduction step
                            if input_type == Yep32f:
                                SIMD_ADD(acc, temp)
                                if active_function.target.has_avx:
                                    VMOVSHDUP(temp, acc)
                                elif active_function.target.has_sse3:
                                    MOVSHDUP(temp, acc)
                                else:
                                    ASSUME.INITIALIZED(temp)
                                    UNPCKLPS(acc, acc)
                                    SIMD_H2L(temp, acc)
                            SCALAR_ADD(acc, temp)

                    for i in range(1, len(acc), 2):
                        if isinstance(acc[i - 1], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 1] = acc[i - 1].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_ADD(acc[i - 1], acc[i])
                    for i in range(2, len(acc), 4):
                        if isinstance(acc[i - 2], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 2] = acc[i - 2].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_ADD(acc[i - 2], acc[i])
                    for i in range(4, len(acc), 8):
                        if isinstance(acc[i - 4], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 4] = acc[i - 4].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_ADD(acc[i - 4], acc[i])
                    for i in range(8, len(acc), 16):
                        if isinstance(acc[i - 8], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 8] = acc[i - 8].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_ADD(acc[i - 8], acc[i])
                    SIMD_REDUCE_ADD(acc[0])
                else:
                    raise ValueError("Unsupported combination of input and output types")
            else:
                raise TypeError("Input and output types must be instances of C regtype")
        else:
            raise TypeError("Unsupported regtype of accumulator registers")

    @staticmethod
    def MAX(acc, input_type, output_type):
        from peachpy.x86_64.registers import SSERegister, AVXRegister
        from peachpy import Type, Yep32f, Yep64f
        if all(isinstance(register, AVXRegister) or isinstance(register, SSERegister) for register in acc):
            if isinstance(input_type, Type) and isinstance(output_type, Type):
                if input_type == output_type and input_type in {Yep32f, Yep64f}:
                    from peachpy.x86_64.mmxsse import MAXPS, MAXPD, MAXSS, MAXSD, MOVHLPS, MOVSHDUP, UNPCKLPS
                    from peachpy.x86_64.avx import VMAXPS, VMAXPD, VMAXSS, VMAXSD, VMOVSHDUP, VUNPCKHPD, VEXTRACTF128
                    from peachpy.x86_64.function import active_function
                    if active_function.target.has_avx:
                        SIMD_MAX = {Yep32f: VMAXPS, Yep64f: VMAXPD}[input_type]
                        SCALAR_MAX = {Yep32f: VMAXSS, Yep64f: VMAXSD}[input_type]

                        def SIMD_H2L(destination, source):
                            VUNPCKHPD(destination, source, source)
                    else:
                        SIMD_MAX = {Yep32f: MAXPS, Yep64f: MAXPD}[input_type]
                        SCALAR_MAX = {Yep32f: MAXSS, Yep64f: MAXSD}[input_type]

                        def SIMD_H2L(destination, source):
                            ASSUME.INITIALIZED(destination)
                            MOVHLPS(destination, source)

                    def SIMD_REDUCE_MAX(acc):
                        if isinstance(acc, AVXRegister):
                            temp = SSERegister()
                            VEXTRACTF128(temp, acc, 1)
                            acc = acc.as_oword
                            SIMD_MAX(acc, temp)
                        temp = SSERegister()
                        SIMD_H2L(temp, acc)
                        # SP floats need additional reduction step
                        if input_type == Yep32f:
                            SIMD_MAX(acc, temp)
                            if active_function.target.has_avx:
                                VMOVSHDUP(temp, acc)
                            elif active_function.target.has_sse3:
                                MOVSHDUP(temp, acc)
                            else:
                                ASSUME.INITIALIZED(temp)
                                UNPCKLPS(acc, acc)
                                SIMD_H2L(temp, acc)
                        SCALAR_MAX(acc, temp)

                    for i in range(1, len(acc), 2):
                        if isinstance(acc[i - 1], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 1] = acc[i - 1].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MAX(acc[i - 1], acc[i])
                    for i in range(2, len(acc), 4):
                        if isinstance(acc[i - 2], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 2] = acc[i - 2].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MAX(acc[i - 2], acc[i])
                    for i in range(4, len(acc), 8):
                        if isinstance(acc[i - 4], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 4] = acc[i - 4].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MAX(acc[i - 4], acc[i])
                    for i in range(8, len(acc), 16):
                        if isinstance(acc[i - 8], AVXRegister) or isinstance(acc[i], AVXRegister):
                            acc[i - 8] = acc[i - 8].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MAX(acc[i - 8], acc[i])
                    SIMD_REDUCE_MAX(acc[0])
                else:
                    raise ValueError("Unsupported combination of input and output types")
            else:
                raise TypeError("Input and output types must be instances of C regtype")
        else:
            raise TypeError("Unsupported regtype of accumulator registers")

    @staticmethod
    def MIN(acc, input_type, output_type):
        from peachpy.x86_64.registers import XMMRegister, YMMRegister
        from peachpy import Type, Yep32f, Yep64f
        if all(isinstance(register, (XMMRegister, YMMRegister)) for register in acc):
            if isinstance(input_type, Type) and isinstance(output_type, Type):
                if input_type == output_type and input_type in {Yep32f, Yep64f}:
                    from peachpy.x86_64.mmxsse import MINPS, MINPD, MINSS, MINSD, MOVHLPS, MOVSHDUP, UNPCKLPS
                    from peachpy.x86_64.avx import VMINPS, VMINPD, VMINSS, VMINSD, VEXTRACTF128, VMOVSHDUP, VUNPCKHPD
                    from peachpy.x86_64.function import active_function
                    if active_function.target.has_avx:
                        SIMD_MIN = {Yep32f: VMINPS, Yep64f: VMINPD}[input_type]
                        SCALAR_MIN = {Yep32f: VMINSS, Yep64f: VMINSD}[input_type]

                        def SIMD_H2L(destination, source):
                            VUNPCKHPD(destination, source, source)
                    else:
                        SIMD_MIN = {Yep32f: MINPS, Yep64f: MINPD}[input_type]
                        SCALAR_MIN = {Yep32f: MINSS, Yep64f: MINSD}[input_type]

                        def SIMD_H2L(destination, source):
                            ASSUME.INITIALIZED(destination)
                            MOVHLPS(destination, source)

                    def SIMD_REDUCE_MIN(acc):
                        if isinstance(acc, YMMRegister):
                            temp = XMMRegister()
                            VEXTRACTF128(temp, acc, 1)
                            acc = acc.as_oword
                            SIMD_MIN(acc, temp)
                        temp = XMMRegister()
                        SIMD_H2L(temp, acc)
                        # SP floats need additional reduction step
                        if input_type == Yep32f:
                            SIMD_MIN(acc, temp)
                            if active_function.target.has_avx:
                                VMOVSHDUP(temp, acc)
                            elif active_function.target.has_sse3:
                                MOVSHDUP(temp, acc)
                            else:
                                ASSUME.INITIALIZED(temp)
                                UNPCKLPS(acc, acc)
                                SIMD_H2L(temp, acc)
                        SCALAR_MIN(acc, temp)

                    for i in range(1, len(acc), 2):
                        if isinstance(acc[i - 1], YMMRegister) or isinstance(acc[i], YMMRegister):
                            acc[i - 1] = acc[i - 1].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MIN(acc[i - 1], acc[i])
                    for i in range(2, len(acc), 4):
                        if isinstance(acc[i - 2], YMMRegister) or isinstance(acc[i], YMMRegister):
                            acc[i - 2] = acc[i - 2].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MIN(acc[i - 2], acc[i])
                    for i in range(4, len(acc), 8):
                        if isinstance(acc[i - 4], YMMRegister) or isinstance(acc[i], YMMRegister):
                            acc[i - 4] = acc[i - 4].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MIN(acc[i - 4], acc[i])
                    for i in range(8, len(acc), 16):
                        if isinstance(acc[i - 8], YMMRegister) or isinstance(acc[i], YMMRegister):
                            acc[i - 8] = acc[i - 8].as_hword
                            acc[i] = acc[i].as_hword
                        SIMD_MIN(acc[i - 8], acc[i])
                    SIMD_REDUCE_MIN(acc[0])
                else:
                    raise ValueError("Unsupported combination of input and output types")
            else:
                raise TypeError("Input and output types must be instances of C regtype")
        else:
            raise TypeError("Unsupported regtype of accumulator registers")


class SWAP:
    @staticmethod
    def REGISTERS(register_x, register_y):
        from peachpy.x86_64.registers import Register
        if isinstance(register_x, Register) and isinstance(register_y, Register):
            if register_x.type == register_y.type and register_x.size == register_y.size:
                register_x.number, register_y.number = register_y.number, register_x.number
            else:
                raise ValueError("Registers {0} and {1} have incompatible register types"
                                 .format(register_x, register_y))
        else:
            raise TypeError("Arguments must be of register regtype")

