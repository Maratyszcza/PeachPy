# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import inspect

import peachpy.stream
from peachpy.arm.instructions import QuasiInstruction, Instruction, Operand


class Label(object):
    def __init__(self, name):
        super(Label, self).__init__()
        self.name = name

    def __str__(self):
        return "<LABEL:" + self.name + '>'


class LabelQuasiInstruction(QuasiInstruction):
    def __init__(self, name, origin=None):
        super(LabelQuasiInstruction, self).__init__('<LABEL>', origin=origin)
        if name.is_label():
            self.name = name.label
        else:
            raise TypeError("Name must be an Label or string")
        self.input_branches = set()

    def __str__(self):
        return "L" + self.name + ':'


class AlignQuasiInstruction(QuasiInstruction):
    supported_alignments = [2, 4, 8, 16, 32]

    def __init__(self, alignment, origin=None):
        super(AlignQuasiInstruction, self).__init__('<ALIGN>', origin=origin)
        if isinstance(alignment, int):
            if alignment in AlignQuasiInstruction.supported_alignments:
                self.alignment = alignment
            else:
                raise ValueError("The alignment value {0} is not in the list of supported alignments ({1})"
                                 .format(alignment, ", ".join(AlignQuasiInstruction.supported_alignments)))
        else:
            raise TypeError("The alignment value must be an integer")

    def __str__(self):
        return "align {0}".format(self.alignment)


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
            elif destination.register.size == 16 and \
                    source.constant.size == 64 and \
                    source.constant.repeats == 1 and \
                    source.constant.basic_type == 'float64':
                self.source = source
            elif destination.register.size == 16 and \
                    source.constant.size == 32 and \
                    source.constant.repeats == 1 and \
                    source.constant.basic_type == 'float32':
                self.source = source
            else:
                raise ValueError('The size of constant should be the same as the size of register')
        else:
            raise ValueError('Load constant pseudo-instruction expects a Constant instance as a source')
        self.size = 4 + 4

    def __str__(self):
        return "LOAD.CONSTANT {0} = {1}".format(self.destination, self.source)

    def get_input_registers_list(self):
        return list()

    def get_output_registers_list(self):
        return [self.destination.register]

    def get_constant(self):
        return self.source.constant

    def get_local_variable(self):
        return None


class LoadArgumentPseudoInstruction(Instruction):
    def __init__(self, destination, source, origin=None):
        from peachpy.arm.function import active_function
        from peachpy import Argument, Yep32f, Yep64f
        super(LoadArgumentPseudoInstruction, self).__init__('<LOAD-PARAMETER>', [destination, source], origin=origin)
        if isinstance(source, Argument):
            argument = active_function.find_argument(source)
            if argument is not None:
                self.argument = argument
            else:
                raise ValueError('{0} is not an argument of the active function'.format(source))
        else:
            raise TypeError('LOAD.ARGUMENT expects an Argument object as a source')
        if destination.is_general_purpose_register() and \
                (argument.is_integer or argument.is_pointer or argument.is_codeunit):
            if destination.register.size >= argument.size:
                self.destination = destination
            else:
                raise ValueError('Destination register %s is too narrow for the argument %s' % (destination, argument))
        elif destination.is_s_register() and source.ctype == Yep32f:
            self.destination = destination
        elif destination.is_d_register() and source.ctype == Yep64f:
            self.destination = destination
        else:
            raise ValueError('Unsupported combination of instruction operands')

    def __str__(self):
        return "LOAD.ARGUMENT {0} = {1}".format(self.destination, self.argument)

    def get_input_registers_list(self):
        from peachpy.arm.registers import sp
        if self.argument.register:
            return [self.argument.register]
        else:
            return [sp]

    def get_output_registers_list(self):
        return [self.destination.register]


class ReturnInstruction(QuasiInstruction):
    def __init__(self, return_value=None, origin=None):
        super(ReturnInstruction, self).__init__('RETURN', origin=origin)
        if return_value.is_none():
            self.return_value = None
        elif return_value.is_modified_immediate12():
            self.return_value = return_value.immediate
        else:
            raise ValueError('Return value is not representable as a 12-bit modified immediate integer')

    def to_instruction_list(self):
        from peachpy.stream import InstructionStream
        from peachpy.arm.registers import r0, lr
        from peachpy.arm.generic import MOV, BX
        return_instructions = InstructionStream()
        with return_instructions:
            if self.return_value is None:
                pass
            else:
                MOV(r0, self.return_value)
            BX(lr)
        return list(iter(return_instructions))

    def __str__(self):
        return "RETURN {0}".format(self.return_value)

    def get_input_registers_list(self):
        from peachpy.arm.registers import sp
        return [sp]

    def get_output_registers_list(self):
        from peachpy.arm.registers import sp
        return [sp]

    def get_constant(self):
        return None

    def get_local_variable(self):
        return None


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

    def get_input_registers_list(self):
        return list()

    def get_output_registers_list(self):
        return [self.destination.register]

    def get_constant(self):
        return None

    def get_local_variable(self):
        return None


def LABEL(name):
    instruction = LabelQuasiInstruction(Operand(name))
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction

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
                    raise ValueError('Loop name is unspecified')
        self.name = name
        self.begin = Label(self.name + ".begin")
        self.end = Label(self.name + ".end")

    def __enter__(self):
        LABEL(self.begin)
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            LABEL(self.end)


def ALIGN(alignment):
    instruction = AlignQuasiInstruction(alignment)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RETURN(return_value=None):
    instruction = ReturnInstruction(Operand(return_value))
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


class LOAD:
    @staticmethod
    def CONSTANT(destination, source):
        from peachpy.arm.function import active_function
        origin = inspect.stack() if active_function.collect_origin else None
        instruction = LoadConstantPseudoInstruction(Operand(destination), Operand(source), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def ARGUMENT(destination, source):
        from peachpy.arm.function import active_function
        origin = inspect.stack() if active_function.collect_origin else None
        instruction = LoadArgumentPseudoInstruction(Operand(destination), source, origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def ARGUMENTS():
        from peachpy.arm.function import active_function
        from peachpy.arm.registers import GeneralPurposeRegister, SRegister, DRegister
        from peachpy import Yep32f, Yep64f
        registers = list()
        for argument in active_function.arguments:
            if argument.is_pointer or argument.is_integer or argument.is_codeunit:
                if argument.size <= 4:
                    register = GeneralPurposeRegister()
                    LOAD.ARGUMENT(register, argument)
                else:
                    raise NotImplementedError("TODO: Handle 8-byte integers")
            elif argument.is_floating_point:
                if argument.ctype == Yep32f:
                    register = SRegister()
                    LOAD.ARGUMENT(register, argument)
                elif argument.ctype == Yep64f:
                    register = DRegister()
                    LOAD.ARGUMENT(register, argument)
                else:
                    raise TypeError("Unknown floating-point type %s" % argument.ctype)
            else:
                raise TypeError("Unknown argument type %s" % argument.ctype)
            registers.append(register)
        return tuple(registers)

    @staticmethod
    def ZERO(destination, ctype):
        if isinstance(ctype, peachpy.c.Type):
        # 			if isinstance(destination, SRegister):
        # 				PXOR( destination, destination )
        # 			elif isinstance(destination, DRegister):
        # 				if ctype.is_floating_point():
        # 					if Target.has_avx():
        # 						SIMD_XOR = {4: VXORPS, 8: VXORPD }[ctype.get_size()]
        # 					else:
        # 						SIMD_XOR = {4: XORPS, 8: XORPD}[ctype.get_size()]
        # 				else:
        # 					SIMD_XOR = VPXOR if Target.has_avx() else PXOR
        # 				SIMD_XOR( destination, destination )
        # 			elif isinstance(destination, QRegister):
        # 				LOAD.ZERO( destination.get_oword(), ctype )
        # 			else:
            raise TypeError("Unsupported type of destination register")
        else:
            raise TypeError("Type must be a C type")

    @staticmethod
    def ELEMENT(destination, source, ctype, increment_pointer=False):
        from peachpy.arm.function import active_function
        from peachpy.arm.instructions import Operand
        from peachpy.arm.registers import Register, GeneralPurposeRegister, SRegister, DRegister
        from peachpy.arm.generic import LDR, LDRH, LDRSH, LDRB, LDRSB, ADD
        from peachpy.arm.vfpneon import VLDR
        from peachpy import Type
        if not isinstance(ctype, Type):
            raise TypeError("Type must be a C type")
        if isinstance(destination, Register):
            raise TypeError("Destination must be a register")
        if not Operand(source).is_memory_address():
            raise TypeError("Source must be a memory operand")
        memory_size = ctype.get_size(active_function.abi)
        if isinstance(destination, GeneralPurposeRegister):
            if ctype.is_unsigned_integer:
                if memory_size == 4:
                    if increment_pointer:
                        LDR(destination, source, memory_size)
                    else:
                        LDR(destination, source)
                elif memory_size == 2:
                    if increment_pointer:
                        LDRH(destination, source, memory_size)
                    else:
                        LDRH(destination, source)
                elif memory_size == 1:
                    if increment_pointer:
                        LDRB(destination, source, memory_size)
                    else:
                        LDRB(destination, source)
                else:
                    raise ValueError("Invalid memory operand size {0}".format(memory_size))
            elif ctype.is_signed_integer:
                if memory_size == 4:
                    if increment_pointer:
                        LDR(destination, source, memory_size)
                    else:
                        LDR(destination, source)
                elif memory_size == 2:
                    if increment_pointer:
                        LDRSH(destination, source, memory_size)
                    else:
                        LDRSH(destination, source)
                elif memory_size == 1:
                    if increment_pointer:
                        LDRSB(destination, source, memory_size)
                    else:
                        LDRSB(destination, source)
                else:
                    raise ValueError("Invalid memory operand size {0}".format(memory_size))
            else:
                raise TypeError("Invalid memory operand type")
        elif isinstance(destination, SRegister):
            if ctype.is_floating_point:
                if memory_size == 4:
                    VLDR(destination, source)
                    if increment_pointer:
                        address_register = Operand(source).get_registers_list()[0]
                        ADD(address_register, memory_size)
                else:
                    raise ValueError("Invalid memory operand size {0}".format(memory_size))
            else:
                raise TypeError("Invalid memory operand type")
        elif isinstance(destination, DRegister):
            if ctype.is_floating_point:
                if memory_size == 8:
                    VLDR(destination, source)
                    if increment_pointer:
                        address_register = Operand(source).get_registers_list()[0]
                        ADD(address_register, memory_size)
                else:
                    raise ValueError("Invalid memory operand size {0}".format(memory_size))
            else:
                raise TypeError("Invalid memory operand type")
        else:
            raise TypeError("Unsupported destination type")


class STORE:
    @staticmethod
    def ELEMENT(destination, source, ctype, increment_pointer=False):
        from peachpy.arm.function import active_function
        from peachpy.arm.instructions import Operand
        from peachpy.arm.registers import GeneralPurposeRegister, SRegister, DRegister
        from peachpy.arm.generic import STR, STRH, STRB, ADD
        from peachpy.arm.vfpneon import VSTR
        if isinstance(ctype, peachpy.c.Type):
            if Operand(destination).is_memory_address():
                if Operand(source).is_register():
                    memory_size = ctype.get_size(active_function.abi)
                    if isinstance(source, GeneralPurposeRegister):
                        if ctype.is_integer():
                            if memory_size == 4:
                                if increment_pointer:
                                    STR(source, destination, memory_size)
                                else:
                                    STR(source, destination)
                            elif memory_size == 2:
                                if increment_pointer:
                                    STRH(source, destination, memory_size)
                                else:
                                    STRH(source, destination)
                            elif memory_size == 1:
                                if increment_pointer:
                                    STRB(source, destination, memory_size)
                                else:
                                    STRB(source, destination)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand type")
                    elif isinstance(source, SRegister):
                        if ctype.is_floating_point():
                            if memory_size == 4:
                                VSTR(source, destination)
                                if increment_pointer:
                                    address_register = Operand(destination).get_registers_list()[0]
                                    ADD(address_register, memory_size)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand type")
                    elif isinstance(source, DRegister):
                        if ctype.is_floating_point():
                            if memory_size == 8:
                                VSTR(source, destination)
                                if increment_pointer:
                                    address_register = Operand(destination).get_registers_list()[0]
                                    ADD(address_register, memory_size)
                            else:
                                raise ValueError("Invalid memory operand size {0}".format(memory_size))
                        else:
                            raise TypeError("Invalid memory operand type")
                    else:
                        raise TypeError("Source must be a general-purpose register")
                else:
                    raise TypeError("Source must be a register")
            else:
                raise TypeError("Destination must be a memory operand")
        else:
            raise TypeError("Type must be a C type")


class ASSUME:
    @staticmethod
    def INITIALIZED(destination):
        from peachpy.arm.function import active_function
        origin = inspect.stack() if active_function.collect_origin else None
        instruction = AssumeInitializedPseudoInstruction(Operand(destination), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class INIT:
    @staticmethod
    def ONCE(register_class, constant, register=None):
        if register is None:
            origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
            register = register_class()
            instruction = LoadConstantPseudoInstruction(Operand(register), Operand(constant), origin=origin)
            if peachpy.stream.active_stream is not None:
                peachpy.stream.active_stream.add_instruction(instruction)
            return register
        else:
            return register


class REDUCE:
    @staticmethod
    def SUM(acc, input_type, output_type):
        raise NotImplementedError("Needs ARM implementation")

    @staticmethod
    def MAX(acc, input_type, output_type):
        raise NotImplementedError("Needs ARM implementation")

    @staticmethod
    def MIN(acc, input_type, output_type):
        raise NotImplementedError("Needs ARM implementation")

class SWAP:
    @staticmethod
    def REGISTERS(register_x, register_y):
        from peachpy.arm.registers import Register
        if isinstance(register_x, Register) and isinstance(register_y, Register):
            if register_x.type == register_y.type and register_x.size == register_y.size:
                register_x.number, register_y.number = register_y.number, register_x.number
            else:
                raise ValueError(
                    "Registers {0} and {1} have incompatible register types".format(register_x, register_y))
        else:
            raise TypeError("Arguments must be of register type")


