# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.abi import ABI
from peachpy.abi import Endianness
from peachpy.x86_64.registers import rax, rbx, rcx, rdx, rsi, rdi, rbp, r8, r9, r10, r11, r12, r13, r14, r15, \
    xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15, \
    mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7
import peachpy.formats.elf.file
import peachpy.formats.mscoff


microsoft_x64_abi = ABI("Microsoft x64 ABI", endianness=Endianness.Little,
                        bool_size=1, wchar_size=2, short_size=2, int_size=4, long_size=4, longlong_size=8,
                        pointer_size=8, index_size=8,
                        stack_alignment=16, red_zone=0,
                        callee_save_registers=[rbx, rsi, rdi, rbp,
                                               r12, r13, r14, r15,
                                               xmm6, xmm7, xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                        argument_registers=[rcx, rdx, r8, r9,
                                            xmm0, xmm1, xmm2, xmm3],
                        volatile_registers=[rax, r10, r11,
                                            mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                            xmm4, xmm5],
                        mscoff_machine_type=peachpy.formats.mscoff.MachineType.x86_64)

system_v_x86_64_abi = ABI("SystemV x86-64 ABI", endianness=Endianness.Little,
                          bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=8, longlong_size=8,
                          pointer_size=8, index_size=8,
                          stack_alignment=16, red_zone=128,
                          callee_save_registers=[rbx, rbp, r12, r13, r14, r15],
                          argument_registers=[rdi, rsi, rdx, rcx, r8, r9, xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7],
                          volatile_registers=[rax, r10, r11,
                                              mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                              xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                          elf_class=peachpy.formats.elf.file.ElfClass.class64,
                          elf_data_encoding=peachpy.formats.elf.file.DataEncoding.little_endian,
                          elf_machine_type=peachpy.formats.elf.file.MachineType.x86_64)

linux_x32_abi = ABI("Linux X32 ABI", endianness=Endianness.Little,
                    bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=4, longlong_size=8,
                    pointer_size=4, index_size=4,
                    stack_alignment=16, red_zone=128,
                    callee_save_registers=[rbx, rbp, r12, r13, r14, r15],
                    argument_registers=[rdi, rsi, rdx, rcx, r8, r9,
                                        xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7],
                    volatile_registers=[rax, r10, r11,
                                        mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                        xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                    elf_class=peachpy.formats.elf.file.ElfClass.class32,
                    elf_data_encoding=peachpy.formats.elf.file.DataEncoding.little_endian,
                    elf_machine_type=peachpy.formats.elf.file.MachineType.x86_64)

native_client_x86_64_abi = ABI("Native Client x86-64 ABI", endianness=Endianness.Little,
                               bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=4, longlong_size=8,
                               pointer_size=4, index_size=4,
                               stack_alignment=16, red_zone=0,
                               callee_save_registers=[rbx, rbp, r12, r13, r14, r15],
                               argument_registers=[rdi, rsi, rdx, rcx, r8, r9,
                                                   xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7],
                               volatile_registers=[rax, r10, r11,
                                                   mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                                   xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                               restricted_registers=[rbp],
                               elf_class=peachpy.formats.elf.file.ElfClass.class64,
                               elf_data_encoding=peachpy.formats.elf.file.DataEncoding.little_endian,
                               elf_machine_type=peachpy.formats.elf.file.MachineType.x86_64)

gosyso_amd64_abi = ABI("Go/SysO x86-64 ABI", endianness=Endianness.Little,
                       bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=8, longlong_size=8,
                       pointer_size=8, index_size=8,
                       stack_alignment=8, red_zone=0,
                       callee_save_registers=[],
                       argument_registers=[],
                       volatile_registers=[rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15,
                                           mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                           xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8,
                                           xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                       elf_class=peachpy.formats.elf.file.ElfClass.class64,
                       elf_data_encoding=peachpy.formats.elf.file.DataEncoding.little_endian,
                       elf_machine_type=peachpy.formats.elf.file.MachineType.x86_64,
                       mscoff_machine_type=peachpy.formats.mscoff.MachineType.x86_64)

goasm_amd64_abi = ABI("Go/Asm x86-64 ABI", endianness=Endianness.Little,
                      bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=8, longlong_size=8,
                      pointer_size=8, index_size=8,
                      stack_alignment=8, red_zone=0,
                      callee_save_registers=[],
                      argument_registers=[],
                      volatile_registers=[rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15,
                                          mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                          xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8,
                                          xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15])

gosyso_amd64p32_abi = ABI("Go/SysO x32 ABI", endianness=Endianness.Little,
                          bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=8, longlong_size=8,
                          pointer_size=4, index_size=4,
                          stack_alignment=4, red_zone=0,
                          callee_save_registers=[],
                          argument_registers=[],
                          volatile_registers=[rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15,
                                             mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                             xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8,
                                             xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15],
                          elf_class=peachpy.formats.elf.file.ElfClass.class32,
                          elf_data_encoding=peachpy.formats.elf.file.DataEncoding.little_endian,
                          elf_machine_type=peachpy.formats.elf.file.MachineType.x86_64,
                          mscoff_machine_type=peachpy.formats.mscoff.MachineType.x86_64)

goasm_amd64p32_abi = ABI("Go/Asm x32 ABI", endianness=Endianness.Little,
                         bool_size=1, wchar_size=4, short_size=2, int_size=4, long_size=8, longlong_size=8,
                         pointer_size=4, index_size=4,
                         stack_alignment=4, red_zone=0,
                         callee_save_registers=[],
                         argument_registers=[],
                         volatile_registers=[rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15,
                                             mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7,
                                             xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8,
                                             xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15])


def detect(system_abi=False):
    """Detects host ABI (either process ABI or system ABI, depending on parameters)

    :param bool system_abi: specified whether system ABI or process ABI should be detected. The two may differ, e.g.
        when a 64-bit system runs 32-bit Python interpreter.

    :returns: the host ABI or None if the host is not recognized or is not x86-64.
    :rtype: ABI or None
    """
    import platform
    import os
    import struct
    (osname, node, release, version, machine, processor) = platform.uname()  # pylint:disable=unpacking-non-sequence
    pointer_size = struct.calcsize("P")
    if osname == "Darwin" and machine == "x86_64" and (system_abi or pointer_size == 8):
        return system_v_x86_64_abi
    elif osname == "FreeBSD" and machine == "amd64" and (system_abi or pointer_size == 8):
        return system_v_x86_64_abi
    elif osname == "Linux" and machine == "x86_64":
        if system_abi or pointer_size == 8:
            return system_v_x86_64_abi
        else:
            return linux_x32_abi
    elif osname == "Windows" and machine == "AMD64" and (system_abi or pointer_size == 8):
        return microsoft_x64_abi
    elif osname == "NaCl" and os.environ.get("NACL_ARCH") == "x86_64" and (system_abi or pointer_size == 4):
        return native_client_x86_64_abi
