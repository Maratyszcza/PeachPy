# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.abi import ABI
from peachpy.abi import Endianness
from peachpy.formats.elf.file import ElfClass, MachineType, DataEncoding
from peachpy.arm.registers import r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, \
    d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, \
    d16, d17, d18, d19, d20, d21, d22, d23, d24, d25, d26, d27, d28, d29, d30, d31


arm_gnueabi = ABI("GNU Soft-Float ARM EABI", endianness=Endianness.Little,
                  bool_size=1, wchar_size=2, short_size=2, int_size=4, long_size=4, longlong_size=8,
                  pointer_size=4, index_size=4,
                  stack_alignment=8, red_zone=0,
                  callee_save_registers=[r4, r5, r6, r7, r8, r9, r10, r11,
                                         d8, d9, d10, d11, d12, d13, d14, d15],
                  argument_registers=[r0, r1, r2, r3],
                  volatile_registers=[r12,
                                      d0, d1, d2, d3, d4, d5, d6, d7,
                                      d16, d17, d18, d19, d20, d21, d22, d23,
                                      d24, d25, d26, d27, d28, d29, d30, d31],
                  elf_class=ElfClass.class32,
                  elf_data_encoding=DataEncoding.little_endian,
                  elf_machine_type=MachineType.arm)

arm_gnueabihf = ABI("GNU Hard-Float ARM EABI", endianness=Endianness.Little,
                    bool_size=1, wchar_size=2, short_size=2, int_size=4, long_size=4, longlong_size=8,
                    pointer_size=4, index_size=4,
                    stack_alignment=8, red_zone=0,
                    callee_save_registers=[r4, r5, r6, r7, r8, r9, r10, r11,
                                           d8, d9, d10, d11, d12, d13, d14, d15],
                    argument_registers=[r0, r1, r2, r3],
                    volatile_registers=[r12,
                                        d0, d1, d2, d3, d4, d5, d6, d7,
                                        d16, d17, d18, d19, d20, d21, d22, d23,
                                        d24, d25, d26, d27, d28, d29, d30, d31],
                    elf_class=ElfClass.class32,
                    elf_data_encoding=DataEncoding.little_endian,
                    elf_machine_type=MachineType.arm)
