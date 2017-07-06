# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
from opcodes.x86_64 import *
from codegen.code import CodeWriter, CodeBlock
import os
import json
import subprocess
import tempfile


instruction_set = read_instruction_set()

instruction_groups = json.load(open(os.path.join(os.path.dirname(__file__), "x86_64.json")))


def filter_instruction_forms(instruction_forms):
    """Removes the instruction forms that are currently not supported"""

    new_instruction_forms = list()
    for instruction_form in instruction_forms:
        if all([operand.type not in {"r8l", "r16l", "r32l", "moffs32", "moffs64"} for operand in instruction_form.operands]):
            new_instruction_forms.append(instruction_form)
    return new_instruction_forms


def is_avx512_instruction_form(instruction_form):
    return instruction_form.isa_extensions and instruction_form.isa_extensions[0].name.startswith("AVX512")


def objcopy(*args):
    objdump_path = os.environ.get("OBJCOPY_FOR_X86", os.environ.get("OBJCOPY"))
    assert objdump_path, "objcopy not found, please set the environment variable OBJCOPY_FOR_X86"
    objdump_process = subprocess.Popen([objdump_path] + list(args),
                                       shell=False,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = objdump_process.communicate()
    if objdump_process.returncode != 0:
        print(stdoutdata)
        print(stderrdata)


def gas(*args):
    gas_path = os.environ.get("AS_FOR_X86", os.environ.get("GAS"))
    assert gas_path, "GNU assembler not found, please set the environment variable AS_FOR_X86"
    gas_process = subprocess.Popen([gas_path] + list(args),
                                   shell=False,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = gas_process.communicate()
    if gas_process.returncode != 0:
        print(stdoutdata)
        print(stderrdata)
    return stdoutdata.decode ('ascii', errors='replace')


def binutils_encode(assembly):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as asm_file:
        print(".text", file=asm_file)
        print(".intel_syntax noprefix", file=asm_file)
        print(assembly, file=asm_file)
    obj_file = tempfile.NamedTemporaryFile(delete=False)
    obj_file.close()
    bin_file = tempfile.NamedTemporaryFile(delete=False)
    bin_file.close()
    try:
        gas("-o", obj_file.name, asm_file.name)
        os.remove(asm_file.name)
        objcopy("-O", "binary", "-j", ".text", obj_file.name, bin_file.name)
        os.remove(obj_file.name)
    except OSError:
        print(assembly)
        raise
    bytecode = bytearray(open(bin_file.name, "rb").read())
    os.remove(bin_file.name)
    return "bytearray([%s])" % ", ".join(["0x%02X" % b for b in bytecode])


def generate_operand(operand, operand_number, peachpy=True, evex=False):
    value_map = {
        "r8": ["bl", "r9b", "dl", "r11b"],
        "r16": ["si", "r12w", "di", "r14w"],
        "r32": ["ebp", "r8d", "eax", "r10d"],
        "r64": ["rcx", "r15", "rax", "r13"],
        "mm": ["mm3", "mm5"],
        "xmm": ["xmm1", "xmm14", "xmm3", "xmm9"],
        "xmm{k}": "xmm5{k1}",
        "xmm{k}{z}": "xmm30{k2}{z}",
        "ymm": ["ymm2", "ymm15", "ymm4", "ymm10"],
        "ymm{k}": "ymm24{k3}",
        "ymm{k}{z}": "ymm19{k5}{z}",
        "zmm": ["zmm3", "zmm26", "zmm9", "zmm17"],
        "zmm{k}": "zmm26{k7}",
        "zmm{k}{z}": "zmm9{k6}{z}",
        "k": "k5",
        "k{k}": "k4{k6}",
        "m": "[r15 + rsi*8 - 128]",
        "m8": "byte[r14 + rdi*4 - 123]",
        "m16": "word[r13 + rbp*8 - 107]",
        "m32": "dword[r12 + rcx*8 - 99]",
        "m64": "qword[r11 + rdx*8 - 88]",
        "m64/m32bcst": "qword[r11 + rdx*8 - 88]",
        "m128": "oword[r10 + rax*8 - 77]",
        "m128/m32bcst": "oword[r10 + rax*8 - 77]",
        "m128/m64bcst": "oword[r10 + rax*8 - 77]",
        "m256": "hword[r9 + rbx*8 - 66]",
        "m256/m32bcst": "hword[r9 + rbx*8 - 66]",
        "m256/m64bcst": "hword[r9 + rbx*8 - 66]",
        "m512": "zword[r9 + rbx*8 - 66]",
        "m512/m32bcst": "zword[r9 + rbx*8 - 66]",
        "m512/m64bcst": "zword[r9 + rbx*8 - 66]",
        "m8{k}{z}": ["byte[r14 - 64]", "byte[r14 + 64]", "byte[r14 - 128]{k1}{z}"],
        "m16{k}{z}": ["word[r13 - 64]", "word[r13 + 64]", "word[r13 - 128]{k2}{z}"],
        "m32{k}{z}": ["dword[r12 - 64]", "dword[r12 + 64]", "dword[r12 - 128]{k3}{z}"],
        "m64{k}{z}": ["qword[r11 - 64]", "qword[r11 + 64]", "qword[r11 - 128]{k4}{z}"],
        "m128{k}{z}": ["oword[r10 - 64]", "oword[r10 + 64]", "oword[r10 - 128]{k5}{z}"],
        "m256{k}{z}": ["hword[r9 - 64]", "hword[r9 + 64]", "hword[r9 - 128]{k6}{z}"],
        "m512{k}{z}": ["zword[r8 - 64]", "zword[r8 + 64]", "zword[r8 - 128]{k7}{z}"],
        "m32{k}": ["dword[r12 - 64]", "dword[r12 + 64]", "dword[r12 - 128]{k5}"],
        "m64{k}": ["qword[r11 - 64]", "qword[r11 + 64]", "qword[r11 - 128]{k6}"],
        "vm32x": "[rsi + xmm0 * 4 - 128]",
        "vm32y": "[r11 + ymm8 * 4 + 48]",
        "vm32z": "[r15 + zmm19 * 4 - 16]",
        "vm64x": "[rsi + xmm1 * 8 + 40]",
        "vm64y": "[r11 + ymm9 * 8 - 56]",
        "vm64z": "[r15 + zmm20 * 8 + 72]",
        "vm32x{k}": "[rsi + xmm0 * 4 - 128]{k1}",
        "vm32y{k}": "[r11 + ymm8 * 4 + 48]{k2}",
        "vm32z{k}": "[r15 + zmm19 * 4 - 16]{k3}",
        "vm64x{k}": "[rsi + xmm1 * 8 + 40]{k4}",
        "vm64y{k}": "[r11 + ymm9 * 8 - 56]{k5}",
        "vm64z{k}": "[r15 + zmm20 * 8 + 72]{k6}",
        "imm4": "0b11",
        "imm8": "2",
        "imm16": "32000",
        "imm32": "0x10000000",
        "imm64": "0x100000000",
        # "rel32": "rip+0x11223344",
        # "rel8": "rip-100",
        "al": "al",
        "cl": "cl",
        "ax": "ax",
        "eax": "eax",
        "rax": "rax",
        "xmm0": "xmm0",
        "1": "1",
        "3": "3",
        "{sae}": "{sae}",
        "{er}": "{rn-sae}",
    }
    evex_value_map = {
        "xmm": ["xmm16", "xmm4", "xmm19", "xmm31"],
        "ymm": ["ymm17", "ymm5", "ymm20", "ymm30"],
        "m8": ["byte[r14 - 64]", "byte[r14 + 64]", "byte[r14 - 128]"],
        "m16": ["word[r13 - 64]", "word[r13 + 64]", "word[r13 - 128]"],
        "m32": ["dword[r12 - 64]", "dword[r12 + 64]", "dword[r12 - 128]"],
        "m64": ["qword[r11 - 64]", "qword[r11 + 64]", "qword[r11 - 128]"],
        "m128": ["oword[r10 - 64]", "oword[r10 + 64]", "oword[r10 - 128]"],
        "m256": ["hword[r9 - 64]", "hword[r9 + 64]", "hword[r9 - 128]"],
        "m512": ["zword[r8 - 64]", "zword[r8 + 64]", "zword[r8 - 128]"],
    }
    peachpy_value_map = {
        "vm32x{k}": "[rsi + xmm0(k1) * 4 - 128]",
        "vm32y{k}": "[r11 + ymm8(k2) * 4 + 48]",
        "vm32z{k}": "[r15 + zmm19(k3) * 4 - 16]",
        "vm64x{k}": "[rsi + xmm1(k4) * 8 + 40]",
        "vm64y{k}": "[r11 + ymm9(k5) * 8 - 56]",
        "vm64z{k}": "[r15 + zmm20(k6) * 8 + 72]",
    }
    optype = operand.type
    operand = value_map.get(optype)
    if evex:
        operand = evex_value_map.get(optype, operand)
    if peachpy:
        operand = peachpy_value_map.get(optype, operand)
    if isinstance(operand, list):
        operand = operand[operand_number]
    if operand is not None and not peachpy:
        operand = operand.\
            replace("byte", "BYTE PTR ").\
            replace("dword", "DWORD PTR").\
            replace("qword", "QWORD PTR").\
            replace("oword", "XMMWORD PTR").\
            replace("hword", "YMMWORD PTR").\
            replace("zword", "ZMMWORD PTR").\
            replace("word", "WORD PTR").\
            replace("rip", "$+2")
    if operand is not None and peachpy:
        for kn in range(1, 8):
            kreg = "k" + str(kn)
            operand = operand.replace("{" + kreg + "}", "(" + kreg + ")")
        operand = operand.replace("){z}", ".z)")
        operand = operand.replace("{rn-sae}", "{rn_sae}")
        operand = operand.replace("{rz-sae}", "{rz_sae}")
        operand = operand.replace("{ru-sae}", "{ru_sae}")
        operand = operand.replace("{rd-sae}", "{rd_sae}")
    return operand


tab = " " * 4

def main(package_root="."):
    for group, instruction_names in instruction_groups.items():
        with open(os.path.join (package_root, "test", "x86_64", "encoding", "test_%s.py" % group), "w") as out:
            with CodeWriter() as code:
                code.line("# This file is auto-generated by /codegen/x86_64_test_encoding.py")
                code.line("# Reference opcodes are generated by:")
                code.line("#     " + gas("--version").splitlines()[0])
                code.line()
                code.line("from peachpy.x86_64 import *")
                code.line("import unittest")
                code.line()
                code.line()
                for name in instruction_names:
                    code.line("class Test%s(unittest.TestCase):" % name)
                    with CodeBlock():
                        code.line("def runTest(self):")
                        with CodeBlock():
                            # Instructions with `name` name
                            name_instructions = list(filter(lambda i: i.name == name, instruction_set))
                            if not name_instructions:
                                print("No forms for instruction: " + name)
                                continue
                            assert len(name_instructions) == 1
                            name_instruction = name_instructions[0]

                            has_assertions = False
                            for instruction_form in filter_instruction_forms(name_instruction.forms):
                                is_avx512 = is_avx512_instruction_form(instruction_form)
                                peachpy_operands = [generate_operand(o, i, peachpy=True, evex=is_avx512) for (i, o)
                                                    in enumerate(instruction_form.operands)]
                                gas_operands = [generate_operand(o, i, peachpy=False, evex=is_avx512) for (i, o)
                                                in enumerate(instruction_form.operands)]
                                if not any(map(lambda op: op is None, gas_operands)):
                                    gas_assembly = "%s %s" % (instruction_form.name, ", ".join(gas_operands))
                                    peachpy_assembly = "%s(%s)" % (instruction_form.name, ", ".join(peachpy_operands))
                                    reference_bytecode = binutils_encode(gas_assembly)
                                    code.line("self.assertEqual(%s, %s.encode())" %
                                              (reference_bytecode, peachpy_assembly))
                                    has_assertions = True
                            if not has_assertions:
                                code.line("pass")
                            code.line()
                            code.line()

            print(str(code), file=out)

if __name__ == '__main__':
    main()

