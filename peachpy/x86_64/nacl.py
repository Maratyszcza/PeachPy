# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


import inspect

import peachpy.stream
from peachpy.x86_64.instructions import Instruction
from peachpy.x86_64.operand import check_operand, format_operand_type, is_r32, is_imm32


# Permitted pseudo-instructions:
#
# - [rep] cmps %nacl:(%rsi),%nacl:(%rdi),%rZP (sandboxed cmps)
#       mov %esi,%esi
#       lea (%rZP,%rsi,1),%rsi
#       mov %edi,%edi
#       lea (%rZP,%rdi,1),%rdi
#       [rep] cmps (%rsi),(%rdi)
#
# - [rep] movs %nacl:(%rsi),%nacl:(%rdi),%rZP (sandboxed movs)
#       mov %esi,%esi
#       lea (%rZP,%rsi,1),%rsi
#       mov %edi,%edi
#       lea (%rZP,%rdi,1),%rdi
#       [rep] movs (%rsi),(%rdi)
#
# - naclasp ...,%rZP (sandboxed stack increment)
#       add ...,%esp
#       add %rZP,%rsp
#
# - naclcall %eXX,%rZP (sandboxed indirect call)
#       and $-32, %eXX
#       add %rZP, %rXX
#       call *%rXX
#   Note: the assembler ensures all calls (including naclcall) will end at the bundle boundary.
#
# - nacljmp %eXX,%rZP (sandboxed indirect jump)
#       and $-32,%eXX
#       add %rZP,%rXX
#       jmp *%rXX
#
# - naclrestbp ...,%rZP (sandboxed %ebp/rbp restore)
#       mov ...,%ebp
#       add %rZP,%rbp
#
# - naclrestsp ...,%rZP (sandboxed %esp/rsp restore)
#       mov ...,%esp
#       add %rZP,%rsp
#
# - naclrestsp_noflags ...,%rZP (sandboxed %esp/rsp restore)
#       mov ...,%esp
#       lea (%rsp,%rZP,1),%rsp
#
# - naclspadj $N,%rZP (sandboxed %esp/rsp restore from %rbp; incudes $N offset)
#       lea N(%rbp),%esp
#       add %rZP,%rsp
#
# - naclssp ...,%rZP (sandboxed stack decrement)
#       SUB(esp, ...)
#       ADD(rZP, rsp)
#
# - [rep] scas %nacl:(%rdi),%?ax,%rZP (sandboxed stos)
#       mov %edi,%edi
#       lea (%rZP,%rdi,1),%rdi
#       [rep] scas (%rdi),%?ax
#       [rep] stos %?ax,%nacl:(%rdi),%rZP
#
# - (sandboxed stos) mov %edi,%edi
#       LEA(rdi, [rZP + rdi*1])
#       REP.STOS([rdi], al/ax/eax/rax)


class NACLJMP(Instruction):
    """Sandboxed Indirect Jump"""
    def __init__(self, *args, **kwargs):
        """Supported forms:

            * NACLJMP(r32)
        """

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLJMP, self).__init__("NACLJMP", origin=origin, prototype=prototype)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) != 1:
            raise SyntaxError("Instruction \"NACLJMP\" requires 1 operand")
        self.in_regs = (True,)
        self.out_regs = (False,)
        self.out_operands = (True,)
        self._gas_name = "nacljmp"
        if not is_r32(self.operands[0]):
            raise SyntaxError("Invalid operand types: NACLJMP " + ", ".join(map(format_operand_type, self.operands)))
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import AND, ADD, JMP
        from peachpy.x86_64.registers import r15
        with InstructionStream() as stream:
            AND(self.operands[0], -32)
            ADD(self.operands[0].as_qword, r15)
            JMP(self.operands[0].as_qword)
        return stream.instructions

    def encode(self):
        import operator
        return bytearray().join(map(operator.methodcaller("encode"), self._lower()))


class NACLASP(Instruction):
    """Sandboxed RSP Increment (Addition)"""
    def __init__(self, *args, **kwargs):
        """Supported forms:

            * NACLASP(r32)
            * NACLASP(imm32)
        """

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLASP, self).__init__("NACLASP", origin=origin, prototype=prototype)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) != 1:
            raise SyntaxError("Instruction \"NACLASP\" requires 1 operand")
        self.in_regs = (True,)
        self.out_regs = (False,)
        self.out_operands = (True,)
        self._gas_name = "naclasp"
        if not is_r32(self.operands[0]) and not is_imm32(self.operands[0]):
            raise SyntaxError("Invalid operand types: NACLASP" + ", ".join(map(format_operand_type, self.operands)))
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import ADD
        from peachpy.x86_64.registers import esp, rsp, r15
        with InstructionStream() as stream:
            ADD(esp, self.operands[0])
            ADD(rsp, r15)
        return stream.instructions

    def encode(self):
        import operator
        return bytearray().join(map(operator.methodcaller("encode"), self._lower()))


class NACLSSP(Instruction):
    """Sandboxed RSP Decrement (Subtraction)"""
    def __init__(self, *args, **kwargs):
        """Supported forms:

            * NACLSSP(r32)
            * NACLSSP(imm32)
        """

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLSSP, self).__init__("NACLSSP", origin=origin, prototype=prototype)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) != 1:
            raise SyntaxError("Instruction \"NACLSSP\" requires 1 operand")
        self.in_regs = (True,)
        self.out_regs = (False,)
        self.out_operands = (True,)
        self._gas_name = "naclssp"
        if not is_r32(self.operands[0]) and not is_imm32(self.operands[0]):
            raise SyntaxError("Invalid operand types: NACLSSP" + ", ".join(map(format_operand_type, self.operands)))
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import SUB, ADD
        from peachpy.x86_64.registers import esp, rsp, r15
        with InstructionStream() as stream:
            SUB(esp, self.operands[0])
            ADD(rsp, r15)
        return stream.instructions

    def encode(self):
        import operator
        return bytearray().join(map(operator.methodcaller("encode"), self._lower()))


class NACLRESTSP(Instruction):
    """Sandboxed RSP Restore"""
    def __init__(self, *args, **kwargs):
        """Supported forms:

            * NACLRESTSP(r32)
        """

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLRESTSP, self).__init__("NACLRESTSP", origin=origin, prototype=prototype)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) != 1:
            raise SyntaxError("Instruction \"NACLRESTSP\" requires 1 operand")
        self.in_regs = (True,)
        self.out_regs = (False,)
        self.out_operands = (True,)
        self._gas_name = "naclrestsp"
        if is_r32(self.operands[0]):
            pass
        else:
            raise SyntaxError("Invalid operand types: NACLRESTSP " + ", ".join(map(format_operand_type, self.operands)))
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import MOV, ADD
        from peachpy.x86_64.registers import esp, rsp, r15
        with InstructionStream() as stream:
            MOV(esp, self.operands[0])
            ADD(rsp, r15)
        return stream.instructions

    def encode(self):
        import operator
        return bytearray().join(map(operator.methodcaller("encode"), self._lower()))


class NACLRESTBP(Instruction):
    """Sandboxed RBP Restore"""
    def __init__(self, *args, **kwargs):
        """Supported forms:

            * NACLRESTBP(r32)
        """

        origin = kwargs.get("origin")
        prototype = kwargs.get("prototype")
        if origin is None and prototype is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLRESTBP, self).__init__("NACLRESTBP", origin=origin, prototype=prototype)
        self.operands = tuple(map(check_operand, args))
        if len(self.operands) != 1:
            raise SyntaxError("Instruction \"NACLRESTBP\" requires 1 operand")
        self.in_regs = (True,)
        self.out_regs = (False,)
        self.out_operands = (True,)
        self._gas_name = "naclrestbp"
        if is_r32(self.operands[0]):
            pass
        else:
            raise SyntaxError("Invalid operand types: NACLRESTBP " + ", ".join(map(format_operand_type, self.operands)))
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import MOV, ADD
        from peachpy.x86_64.registers import ebp, rbp, r15
        with InstructionStream() as stream:
            MOV(ebp, self.operands[0])
            ADD(rbp, r15)
        return stream.instructions

    def encode(self):
        import operator
        return bytearray().join(map(operator.methodcaller("encode"), self._lower()))
