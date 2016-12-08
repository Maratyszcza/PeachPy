# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
from opcodes.x86_64 import *
from codegen.code import CodeWriter, CodeBlock
import operator
import json


instruction_set = read_instruction_set()

active_code_writer = None

instruction_groups = json.load(open(os.path.join(os.path.dirname(__file__), "x86_64.json")))


def filter_instruction_forms(instruction_forms):
    """Removes the instruction forms that are currently not supported"""

    new_instruction_forms = list()
    for instruction_form in instruction_forms:
        if all([operand.type not in {"r8l", "r16l", "r32l", "moffs32", "moffs64"} for operand in instruction_form.operands]):
            new_instruction_forms.append(instruction_form)
    return new_instruction_forms


def generate_operand(operand):
    value_map = {
        "r8": "dl",
        "r16": "cx",
        "r32": "ebx",
        "r64": "rdi",
        "mm": "mm4",
        "xmm": "xmm7",
        "ymm": "ymm3",
        "m": "[r15+rsi*1-128]",
        "m8": "byte[r15+rsi*1+8]",
        "m16": "word[r15+rsi*1+16]",
        "m32": "dword[r15+rsi*1+32]",
        "m64": "qword[r15+rsi*1+64]",
        "m128": "oword[r15+rsi*1+128]",
        "m256": "hword[r15+rsi*1+256]",
        "imm4": "0b11",
        "imm8": "2",
        "imm16": "32000",
        "imm32": "0x10000000",
        "imm64": "0x100000000",
        "rel32": "rip+0",
        "rel8": "rip+0",
        "al": "al",
        "cl": "cl",
        "ax": "ax",
        "eax": "eax",
        "rax": "rax",
        "xmm0": "xmm0",
        "1": "1",
        "3": "3"
    }
    optype = operand.type
    return value_map.get(optype)


tab = " " * 4

with open("codegen/x86_64_nacl.py", "w") as out:
    print("from __future__ import print_function\n\
from peachpy.x86_64 import *\n\
\n\
instruction_list = []\n\
", file=out)
    for group, instruction_names in instruction_groups.iteritems():
        with CodeWriter() as code:
            code.line("# " + group)
            for name in instruction_names:

                # Instructions with `name` name
                name_instructions = filter(lambda i: i.name == name, instruction_set)
                if not name_instructions:
                    print("No forms for instruction: " + name)
                    continue
                assert len(name_instructions) == 1
                name_instruction = name_instructions[0]

                code.line()
                for instruction_form in filter_instruction_forms(name_instruction.forms):
                    operands = map(generate_operand, instruction_form.operands)
                    if not any(map(lambda op: op is None, operands)):
                        instruction_text = "%s(%s)" % (instruction_form.name, ", ".join(operands))
                        if any(map(operator.attrgetter("is_memory"), instruction_form.operands)):
                            code.line("instruction_list.append((\"%s\", (MOV(esi, esi), %s)))" % (str(instruction_form), instruction_text))
                        else:
                            code.line("instruction_list.append((\"%s\", (%s,)))" % (str(instruction_form), instruction_text))

        print(str(code), file=out)

    print("\n\
import operator\n\
\n\
bundles = open(\"codegen/x86_64_bundles.h\", \"w\")\n\
names = open(\"codegen/x86_64_names.h\", \"w\")\n\
\n\
print(\"static const uint8_t bundles[][32] = {\", file=bundles)\n\
print(\"static const char* names[] = {\", file=names)\n\
\n\
for (text, instructions) in instruction_list:\n\
    bundle = bytearray([0xF4] * 32)\n\
    encoding = sum(map(operator.methodcaller(\"encode\"), instructions), bytearray())\n\
    bundle[0:len(encoding)] = encoding\n\
    print(\"\\t{\" + \", \".join(map(lambda b: \"0x%02X\" % b, bundle)) + \"},\", file=bundles)\n\
    print(\"\\t\\\"%s\\\",\" % text, file=names)\n\
\n\
print(\"};\\n\", file=names)\n\
print(\"};\\n\", file=bundles)", file=out)