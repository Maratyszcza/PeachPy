# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


import inspect

import peachpy.stream
from peachpy.x86_64.instructions import Instruction
from peachpy.x86_64.operand import check_operand, format_operand_type, is_r32


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
            * NACLJMP(r32, rZP)
        """

# - nacljmp %eXX,%rZP (sandboxed indirect jump)
#       AND(eXX, -32)
#       ADD(rXX, rZP)
#       JMP(rxx)

        origin = kwargs.get("origin")
        if origin is None and peachpy.x86_64.options.get_debug_level() > 0:
            origin = inspect.stack()
        super(NACLJMP, self).__init__("NACLJMP", origin=origin)
        self.operands = tuple(map(check_operand, args))
        self.encodings = []
        if len(self.operands) not in {1, 2}:
            raise SyntaxError("Instruction \"NACLJMP\" requires 1 or 2 operands")
        from peachpy.x86_64.registers import r15
        if len(self.operands) == 1:
            self.operands = tuple(list(self.operands) + [r15])
        if is_r32(self.operands[0]) and r15 == self.operands[1]:
            self._gas_name = "nacljmp"
            self.out_regs = (False, False)
            self.in_regs = (True, False)
            self.out_operands = (False, False)
        else:
            raise SyntaxError("Invalid operand types: NACLJMP " + ", ".join(map(format_operand_type, self.operands)))
        self._instructions = self._lower()
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(self)

    def _lower(self):
        from peachpy.stream import InstructionStream
        from peachpy.x86_64.generic import AND, ADD, JMP
        with InstructionStream() as stream:
            AND(self.operands[0], -32)
            ADD(self.operands[0].as_qword, self.operands[1])
            JMP(self.operands[0].as_qword)
        return stream.instructions

    def encode(self):
        import operator
        return sum(map(operator.methodcaller("encode"), self._instructions), bytearray())
