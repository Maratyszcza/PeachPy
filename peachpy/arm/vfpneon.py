# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import inspect

import peachpy.stream
import peachpy.arm.function
from peachpy.arm.instructions import Instruction, Operand
from peachpy.arm.isa import Extension


class VFPLoadStoreInstruction(Instruction):
    def __init__(self, name, register, address, origin=None):
        allowed_instructions = {'VLDR', 'VSTR'}
        if name in allowed_instructions:
            super(VFPLoadStoreInstruction, self).__init__(name, [register, address],
                                                          isa_extensions=Extension.VFP2, origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if (register.is_d_register() or register.is_s_register()) and address.is_memory_address_offset8_mod4():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, register, address))

    def get_input_registers_list(self):
        input_registers_list = self.operands[1].get_registers_list()
        if self.name == 'VSTR':
            input_registers_list += self.operands[0].get_registers_list()
        return input_registers_list

    def get_output_registers_list(self):
        if self.name == 'VLDR':
            return self.operands[0].get_registers_list()
        else:
            return list()


class VFPLoadStoreMultipleInstruction(Instruction):
    load_instructions = {"VLDM", "VLDMIA", "VLDMDB"}
    store_instructions = {"VSTM", "VSTMIA", "VSTMDB"}

    def __init__(self, name, address, register_list, origin=None):
        if name in VFPLoadStoreMultipleInstruction.load_instructions or \
                name in VFPLoadStoreMultipleInstruction.store_instructions:
            super(VFPLoadStoreMultipleInstruction, self).__init__(name, [address, register_list],
                                                                  isa_extensions=Extension.VFP2, origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if address.is_address_register() and register_list.is_d_register_list():
            pass
        elif address.is_address_register() and register_list.is_s_register_list():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, register_list, address))

    def get_input_registers_list(self):
        if self.name in VFPLoadStoreMultipleInstruction.store_instructions:
            return self.operands[0].get_registers_list() + self.operands[1].get_registers_list()
        else:
            return self.operands[0].get_registers_list()

    def get_output_registers_list(self):
        if self.name in VFPLoadStoreMultipleInstruction.load_instructions:
            return self.operands[1].get_registers_list()
        else:
            return list()


class NeonLoadStoreInstruction(Instruction):
    load_instructions = {"VLD1.8", "VLD1.16", "VLD1.32", "VLD1.64"}
    store_instructions = {"VST1.8", "VST1.16", "VST1.32", "VST1.64"}

    def __init__(self, name, register_list, address, increment, origin=None):
        if name not in NeonLoadStoreInstruction.load_instructions and \
                name not in NeonLoadStoreInstruction.store_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if register_list.is_vldst1_register_list() and \
                address.is_memory_address(offset_bits=0) and \
                increment.is_none():
            super(NeonLoadStoreInstruction, self).__init__(name, [register_list, address],
                                                           isa_extensions=Extension.NEON, origin=origin)
        elif register_list.is_vldst1_register_list() and \
                address.is_memory_address(offset_bits=0, allow_writeback=False) and \
                increment.is_general_purpose_register():
            super(NeonLoadStoreInstruction, self).__init__(name, [register_list, address, increment],
                                                           isa_extensions=Extension.NEON, origin=origin)
        elif register_list.is_vldst1_register_lanes_list() and \
                address.is_memory_address(offset_bits=0) and \
                increment.is_none():
            super(NeonLoadStoreInstruction, self).__init__(name, [register_list, address],
                                                           isa_extensions=Extension.NEON, origin=origin)
        elif register_list.is_vldst1_register_lanes_list() and \
                address.is_memory_address(offset_bits=0, allow_writeback=False) and \
                increment.is_general_purpose_register():
            super(NeonLoadStoreInstruction, self).__init__(name, [register_list, address, increment],
                                                           isa_extensions=Extension.NEON, origin=origin)
        else:
            if increment.is_none():
                raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, register_list, address))
            else:
                raise ValueError(
                    'Invalid operands in instruction {0} {1}, {2}, {3}'.format(name, register_list, address, increment))

    def get_input_registers_list(self):
        input_registers_list = self.operands[1].get_registers_list()
        if self.name in NeonLoadStoreInstruction.store_instructions:
            input_registers_list += self.operands[0].get_registers_list()
        if len(self.operands) == 3:
            input_registers_list += self.operands[2].get_registers_list()
        return input_registers_list

    def get_output_registers_list(self):
        output_registers_list = list()
        if self.name in NeonLoadStoreInstruction.load_instructions:
            output_registers_list += self.operands[0].get_registers_list()
        if len(self.operands) == 3 or self.operands[1].is_writeback_memory_address():
            output_registers_list += self.operands[1].get_writeback_registers_list()
        return output_registers_list


class VFPPushPopInstruction(Instruction):
    def __init__(self, name, register_list, origin=None):
        allowed_instructions = {'VPUSH', 'VPOP'}
        if name in allowed_instructions:
            super(VFPPushPopInstruction, self).__init__(name, [register_list],
                                                        isa_extensions=Extension.VFP2, origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if register_list.is_d_register_list():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}'.format(name, register_list))

    def get_input_registers_list(self):
        if self.name == 'VPUSH':
            return self.operands[0].get_registers_list()
        else:
            return list()

    def get_output_registers_list(self):
        if self.name == 'VPOP':
            return self.operands[0].get_registers_list()
        else:
            return list()


class VFPDoublePrecisionMultiplyAddInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        mla_instructions = ['VMLA.F64', 'VMLS.F64', 'VNMLA.F64', 'VNMLS.F64']
        fma_instructions = ['VFMA.F64', 'VFMS.F64', 'VFNMA.F64', 'VFNMS.F64']
        if name in mla_instructions:
            super(VFPDoublePrecisionMultiplyAddInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                           isa_extensions=Extension.VFP2, origin=origin)
        elif name in fma_instructions:
            super(VFPDoublePrecisionMultiplyAddInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                           isa_extensions=Extension.VFP4, origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if destination.is_d_register() and source_x.is_d_register() and source_y.is_d_register():
            pass
        else:
            raise ValueError(
                'Invalid operands in instruction {0} {1}, {2}, {3}'.format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list() + self.operands[1].get_registers_list() + self.operands[
            2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPSinglePrecisionMultiplyAddInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        mla_instructions = ['VNMLA.F32', 'VNMLS.F32']
        fma_instructions = ['VFNMA.F32', 'VFNMS.F32']
        if name in mla_instructions:
            super(VFPSinglePrecisionMultiplyAddInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                           isa_extensions=Extension.VFP2, origin=origin)
        elif name in fma_instructions:
            super(VFPSinglePrecisionMultiplyAddInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                           isa_extensions=Extension.VFP4, origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(mla_instructions + fma_instructions)))
        if destination.is_s_register() and source_x.is_s_register() and source_y.is_s_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list() + self.operands[1].get_registers_list() + self.operands[
            2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPNeonBinaryArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['VADD.F32', 'VSUB.F32', 'VMUL.F32']
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_s_register() and source_x.is_s_register() and source_y.is_s_register():
            super(VFPNeonBinaryArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                     isa_extensions=Extension.VFP2, origin=origin)
        elif destination.is_d_register() and source_x.is_d_register() and source_y.is_d_register():
            super(VFPNeonBinaryArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                     isa_extensions=Extension.NEON, origin=origin)
        elif destination.is_q_register() and source_x.is_q_register() and source_y.is_q_register():
            super(VFPNeonBinaryArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                     isa_extensions=Extension.NEON, origin=origin)
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPNeonMultiplyAddInstruction(Instruction):
    def __init__(self, name, accumulator, factor_x, factor_y, origin=None):
        mla_instructions = ['VMLA.F32', 'VMLS.F32']
        fma_instructions = ['VFMA.F32', 'VFMS.F32']
        if name not in mla_instructions and name not in fma_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if name in mla_instructions and \
                accumulator.is_s_register() and \
                factor_x.is_s_register() and \
                factor_y.is_s_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.VFP2, origin=origin)
        elif name in fma_instructions and \
                accumulator.is_s_register() and \
                factor_x.is_s_register() and \
                factor_y.is_s_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.VFP4, origin=origin)
        elif name in mla_instructions and \
                accumulator.is_d_register() and \
                factor_x.is_d_register() and \
                factor_y.is_d_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.NEON, origin=origin)
        elif name in mla_instructions and \
                accumulator.is_q_register() and \
                factor_x.is_q_register() and \
                factor_y.is_q_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.NEON, origin=origin)
        elif name in fma_instructions and \
                accumulator.is_d_register() and \
                factor_x.is_d_register() and \
                factor_y.is_d_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.NEON2, origin=origin)
        elif name in fma_instructions and \
                accumulator.is_q_register() and \
                factor_x.is_q_register() and \
                factor_y.is_q_register():
            super(VFPNeonMultiplyAddInstruction, self).__init__(name, [accumulator, factor_x, factor_y],
                                                                isa_extensions=Extension.NEON2, origin=origin)
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, accumulator, factor_x, factor_y))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list() + \
            self.operands[1].get_registers_list() + \
            self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPSinglePrecisionBinaryArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['VNMUL.F32', 'VDIV.F32']
        super(VFPSinglePrecisionBinaryArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                            isa_extensions=Extension.VFP2,
                                                                            origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_d_register() and source_x.is_s_register() and source_y.is_s_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPDoublePrecisionBinaryArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['VADD.F64', 'VSUB.F64', 'VMUL.F64', 'VNMUL.F32', 'VNMUL.F64', 'VDIV.F32', 'VDIV.F64']
        super(VFPDoublePrecisionBinaryArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                                            isa_extensions=Extension.VFP2,
                                                                            origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_d_register() and source_x.is_d_register() and source_y.is_d_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VFPDoublePrecisionUnaryArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source, origin=None):
        allowed_instructions = ['VABS.F64', 'VNEG.F64', 'VSQRT.F64']
        super(VFPDoublePrecisionUnaryArithmeticInstruction, self).__init__(name, [destination, source],
                                                                           isa_extensions=Extension.VFP2, origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_d_register() and source.is_d_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, destination, source))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class NeonArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['VADD.I8', 'VADD.I16', 'VADD.I32', 'VADD.I64',
                                'VSUB.I8', 'VSUB.I16', 'VSUB.I32', 'VSUB.I64',
                                'VMUL.I8', 'VMUL.I16', 'VMUL.I32',
                                'VMIN.S8', 'VMIN.S16', 'VMIN.S32', 'VMIN.U8', 'VMIN.U16', 'VMIN.U32', 'VMIN.F32',
                                'VMAX.S8', 'VMAX.S16', 'VMAX.S32', 'VMAX.U8', 'VMAX.U16', 'VMAX.U32', 'VMAX.F32',
                                'VABD.S8', 'VABD.S16', 'VABD.S32', 'VABD.U8', 'VABD.U16', 'VABD.U32', 'VABD.F32',
                                'VACGE.F32', 'VACGT.F32', 'VACLE.F32', 'VACLT.F32',
                                'VEOR', 'VORR', 'VORN', 'VAND', 'VBIC',
                                'VPADD.I8', 'VPADD.I16', 'VPADD.I32', 'VPADD.F32',
                                'VPMIN.S8', 'VPMIN.S16', 'VPMIN.S32', 'VPMIN.U8', 'VPMIN.U16', 'VPMIN.U32', 'VPMIN.F32',
                                'VPMAX.S8', 'VPMAX.S16', 'VPMAX.S32', 'VPMAX.U8', 'VPMAX.U16', 'VPMAX.U32', 'VPMAX.F32',
                                'VQADD.S8', 'VQADD.S16', 'VQADD.S32', 'VQADD.S64', 'VQADD.U8', 'VQADD.U16', 'VQADD.U32',
                                'VQADD.U64',
                                'VQSUB.S8', 'VQSUB.S16', 'VQSUB.S32', 'VQSUB.S64', 'VQSUB.U8', 'VQSUB.U16', 'VQSUB.U32',
                                'VQSUB.U64',
                                'VHADD.S8', 'VHADD.S16', 'VHADD.S32', 'VHADD.U8', 'VHADD.U16', 'VHADD.U32',
                                'VHSUB.S8', 'VHSUB.S16', 'VHSUB.S32', 'VHSUB.U8', 'VHSUB.U16', 'VHSUB.U32',
                                'VRHADD.S8', 'VRHADD.S16', 'VRHADD.S32', 'VRHADD.U8', 'VRHADD.U16', 'VRHADD.U32',
                                'VRECPS.F32', 'VRSQRTS.F32',
                                'VTST.8', 'VTST.16', 'VTST.32']
        super(NeonArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                        isa_extensions=Extension.NEON, origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_d_register() and source_x.is_d_register() and source_y.is_d_register():
            pass
        elif destination.is_q_register() and source_x.is_q_register() and source_y.is_q_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class NeonWideArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['VADDL.S8', 'VADDL.S16', 'VADDL.S32',
                                'VADDL.U8', 'VADDL.U16', 'VADDL.U32',
                                'VSUBL.S8', 'VSUBL.S16', 'VSUBL.S32',
                                'VSUBL.U8', 'VSUBL.U16', 'VSUBL.U32',
                                'VMULL.S8', 'VMULL.S16', 'VMULL.S32',
                                'VMULL.U8', 'VMULL.U16', 'VMULL.U32',
                                'VMULL.P8']
        super(NeonWideArithmeticInstruction, self).__init__(name, [destination, source_x, source_y],
                                                            isa_extensions=Extension.NEON, origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_q_register() and source_x.is_d_register() and source_y.is_d_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VfpNeonMovInstruction(Instruction):
    def __init__(self, name, destination, source, origin=None):
        if name == 'VMOV' and destination.is_q_register() and source.is_q_register():
            super(VfpNeonMovInstruction, self).__init__(name, [destination, source],
                                                        isa_extensions=Extension.NEON, origin=origin)
        elif name == 'VMOV' and destination.is_d_register() and source.is_d_register():
            super(VfpNeonMovInstruction, self).__init__(name, [destination, source],
                                                        isa_extensions=Extension.NEON, origin=origin)
        elif name == 'VMOV.F32' and destination.is_s_register() and source.is_s_register():
            super(VfpNeonMovInstruction, self).__init__(name, [destination, source],
                                                        isa_extensions=Extension.VFP2, origin=origin)
        elif name == 'VMOV.F64' and destination.is_d_register() and source.is_d_register():
            super(VfpNeonMovInstruction, self).__init__(name, [destination, source],
                                                        isa_extensions=Extension.VFP2, origin=origin)
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, destination, source))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class VADD:
    @staticmethod
    def I8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VADD.I8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VADD.I16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VADD.I32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VADD.I64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPNeonBinaryArithmeticInstruction('VADD.F32', Operand(destination), Operand(source_x),
                                                         Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionBinaryArithmeticInstruction('VADD.F64', Operand(destination), Operand(source_x),
                                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VADDL:
    @staticmethod
    def S8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.S8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.S16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.S32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.U8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.U16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VADDL.U32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VSUB:
    @staticmethod
    def I8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VSUB.I8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VSUB.I16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VSUB.I32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VSUB.I64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPNeonBinaryArithmeticInstruction('VSUB.F32', Operand(destination), Operand(source_x),
                                                         Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionBinaryArithmeticInstruction('VSUB.F64', Operand(destination), Operand(source_x),
                                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VSUBL:
    @staticmethod
    def S8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.S8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.S16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.S32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.U8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.U16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VSUBL.U32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMUL:
    @staticmethod
    def I8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMUL.I8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMUL.I16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMUL.I32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPNeonBinaryArithmeticInstruction('VMUL.F32', Operand(destination), Operand(source_x),
                                                         Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionBinaryArithmeticInstruction('VMUL.F64', Operand(destination), Operand(source_x),
                                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMULL:
    @staticmethod
    def S8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.S8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.S16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.S32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.U8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.U16', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.U32', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def P8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonWideArithmeticInstruction('VMULL.P8', Operand(destination), Operand(source_x),
                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMIN:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMIN.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMAX:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VMAX.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VABD:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VABD.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VACGE:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VACGE.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VACGT:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VACGT.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VACLE:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VACLE.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VACLT:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VACLT.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VAND(object):
    @staticmethod
    def __new__(cls, destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VAND', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VBIC(object):
    @staticmethod
    def __new__(cls, destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VBIC', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VORR(object):
    @staticmethod
    def __new__(cls, destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VORR', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VORN(object):
    @staticmethod
    def __new__(cls, destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VORN', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


def VEOR(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = NeonArithmeticInstruction('VEOR', Operand(destination), Operand(source_x), Operand(source_y),
                                            origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


class VPADD:
    @staticmethod
    def I8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPADD.I8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPADD.I16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPADD.I32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPADD.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VPMIN:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMIN.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VPMAX:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VPMAX.F32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VQADD:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.S64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQADD.U64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VQSUB:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.S64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VQSUB.U64', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VHADD:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHADD.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VHSUB:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.S16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.S32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.U16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VHSUB.U32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VRHADD:
    @staticmethod
    def S8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.S8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.S16', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def S32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.S32', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U8(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.U8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U16(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.U16', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def U32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRHADD.U32', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VRECPS:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRECPS.F32', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VRSQRTS:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = NeonArithmeticInstruction('VRSQRTS.F32', Operand(destination), Operand(source_x),
                                                Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VTST:
    @staticmethod
    def I8(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonArithmeticInstruction('VTST.8', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonArithmeticInstruction('VTST.16', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(destination, source_x, source_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonArithmeticInstruction('VTST.32', Operand(destination), Operand(source_x), Operand(source_y),
                                                origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VNMUL:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VNMUL.F32', Operand(destination), Operand(source_x),
                                                               Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionBinaryArithmeticInstruction('VNMUL.F64', Operand(destination),
                                                                    Operand(source_x), Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VDIV:
    @staticmethod
    def F32(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VDIV.F32', Operand(destination), Operand(source_x),
                                                               Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionBinaryArithmeticInstruction('VDIV.F64', Operand(destination), Operand(source_x),
                                                                    Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VSQRT:
    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionUnaryArithmeticInstruction('VSQRT.F64', Operand(destination), Operand(source_x),
                                                                   Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VABS:
    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionUnaryArithmeticInstruction('VABS.F64', Operand(destination), Operand(source_x),
                                                                   Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VNEG:
    @staticmethod
    def F64(destination, source_x, source_y=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        if source_y is None:
            (destination, source_x, source_y) = (destination, destination, source_x)
        instruction = VFPDoublePrecisionUnaryArithmeticInstruction('VNEG.F64', Operand(destination), Operand(source_x),
                                                                   Operand(source_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMLA:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPNeonMultiplyAddInstruction('VMLA.F32', Operand(accumulator), Operand(factor_x),
                                                    Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VMLA.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMLS:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPNeonMultiplyAddInstruction('VMLS.F32', Operand(accumulator), Operand(factor_x),
                                                    Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VMLS.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VNMLA:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VNMLA.F32', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VNMLA.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VNMLS:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VNMLS.F32', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VNMLS.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VFMA:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPNeonMultiplyAddInstruction('VFMA.F32', Operand(accumulator), Operand(factor_x),
                                                    Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VFMA.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VFMS:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPNeonMultiplyAddInstruction('VFMS.F32', Operand(accumulator), Operand(factor_x),
                                                    Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VFMS.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VFNMA:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VFNMA.F32', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VFNMA.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VFNMS:
    @staticmethod
    def F32(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPSinglePrecisionMultiplyAddInstruction('VFNMS.F32', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(accumulator, factor_x, factor_y):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VFPDoublePrecisionMultiplyAddInstruction('VFNMS.F64', Operand(accumulator), Operand(factor_x),
                                                               Operand(factor_y), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


def VLDR(register, address):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreInstruction("VLDR", Operand(register), Operand(address), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VSTR(register, address):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreInstruction("VSTR", Operand(register), Operand(address), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VLDM(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VLDM", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VLDMIA(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VLDMIA", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VLDMDB(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VLDMDB", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VSTM(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VSTM", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VSTMIA(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VSTMIA", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VSTMDB(source, destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPLoadStoreMultipleInstruction("VSTMDB", Operand(source), Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VPUSH(register_list):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPPushPopInstruction("VPUSH", Operand(register_list), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def VPOP(register_list):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = VFPPushPopInstruction("VPOP", Operand(register_list), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


class VLD1:
    @staticmethod
    def I8(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VLD1.8", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VLD1.16", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VLD1.32", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I64(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VLD1.64", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VLD1.32", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VST1:
    @staticmethod
    def I8(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VST1.8", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I16(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VST1.16", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I32(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VST1.32", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def I64(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VST1.64", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(address, register_list, increment=None):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = NeonLoadStoreInstruction("VST1.32", Operand(address), Operand(register_list), Operand(increment),
                                               origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction


class VMOV(object):
    @staticmethod
    def __new__(cls, destination, source):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VfpNeonMovInstruction('VMOV', Operand(destination), Operand(source), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F32(destination, source):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VfpNeonMovInstruction('VMOV.F32', Operand(destination), Operand(source), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction

    @staticmethod
    def F64(destination, source):
        origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
        instruction = VfpNeonMovInstruction('VMOV.F64', Operand(destination), Operand(source), origin=origin)
        if peachpy.stream.active_stream is not None:
            peachpy.stream.active_stream.add_instruction(instruction)
        return instruction
