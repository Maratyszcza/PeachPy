# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import inspect

import peachpy.stream
import peachpy.arm.function
from peachpy.arm.instructions import QuasiInstruction, Instruction, Operand
from peachpy.arm.isa import Extension


class ArithmeticInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['ADD', 'ADDEQ', 'ADDNE', 'ADDCS', 'ADDHS', 'ADDCC', 'ADDLO', 'ADDMI', 'ADDPL', 'ADDVS',
                                'ADDVC', 'ADDHI', 'ADDLS', 'ADDGE', 'ADDLT', 'ADDGT', 'ADDLE',
                                'ADDS', 'ADDSEQ', 'ADDSNE', 'ADDSCS', 'ADDSHS', 'ADDSCC', 'ADDSLO', 'ADDSMI', 'ADDSPL',
                                'ADDSVS', 'ADDSVC', 'ADDSHI', 'ADDSLS', 'ADDSGE', 'ADDSLT', 'ADDSGT', 'ADDSLE',
                                'ADC', 'ADCEQ', 'ADCNE', 'ADCCS', 'ADCHS', 'ADCCC', 'ADCLO', 'ADCMI', 'ADCPL', 'ADCVS',
                                'ADCVC', 'ADCHI', 'ADCLS', 'ADCGE', 'ADCLT', 'ADCGT', 'ADCLE',
                                'ADCS', 'ADCSEQ', 'ADCSNE', 'ADCSCS', 'ADCSHS', 'ADCSCC', 'ADCSLO', 'ADCSMI', 'ADCSPL',
                                'ADCSVS', 'ADCSVC', 'ADCSHI', 'ADCSLS', 'ADCSGE', 'ADCSLT', 'ADCSGT', 'ADCSLE',
                                'SUB', 'SUBEQ', 'SUBNE', 'SUBCS', 'SUBHS', 'SUBCC', 'SUBLO', 'SUBMI', 'SUBPL', 'SUBVS',
                                'SUBVC', 'SUBHI', 'SUBLS', 'SUBGE', 'SUBLT', 'SUBGT', 'SUBLE',
                                'SUBS', 'SUBSEQ', 'SUBSNE', 'SUBSCS', 'SUBSHS', 'SUBSCC', 'SUBSLO', 'SUBSMI', 'SUBSPL',
                                'SUBSVS', 'SUBSVC', 'SUBSHI', 'SUBSLS', 'SUBSGE', 'SUBSLT', 'SUBSGT', 'SUBSLE',
                                'SBC', 'SBCEQ', 'SBCNE', 'SBCCS', 'SBCHS', 'SBCCC', 'SBCLO', 'SBCMI', 'SBCPL', 'SBCVS',
                                'SBCVC', 'SBCHI', 'SBCLS', 'SBCGE', 'SBCLT', 'SBCGT', 'SBCLE',
                                'SBCS', 'SBCSEQ', 'SBCSNE', 'SBCSCS', 'SBCSHS', 'SBCSCC', 'SBCSLO', 'SBCSMI', 'SBCSPL',
                                'SBCSVS', 'SBCSVC', 'SBCSHI', 'SBCSLS', 'SBCSGE', 'SBCSLT', 'SBCSGT', 'SBCSLE',
                                'RSB', 'RSBEQ', 'RSBNE', 'RSBCS', 'RSBHS', 'RSBCC', 'RSBLO', 'RSBMI', 'RSBPL', 'RSBVS',
                                'RSBVC', 'RSBHI', 'RSBLS', 'RSBGE', 'RSBLT', 'RSBGT', 'RSBLE',
                                'RSBS', 'RSBSEQ', 'RSBSNE', 'RSBSCS', 'RSBSHS', 'RSBSCC', 'RSBSLO', 'RSBSMI', 'RSBSPL',
                                'RSBSVS', 'RSBSVC', 'RSBSHI', 'RSBSLS', 'RSBSGE', 'RSBSLT', 'RSBSGT', 'RSBSLE',
                                'RSC', 'RSCEQ', 'RSCNE', 'RSCCS', 'RSCHS', 'RSCCC', 'RSCLO', 'RSCMI', 'RSCPL', 'RSCVS',
                                'RSCVC', 'RSCHI', 'RSCLS', 'RSCGE', 'RSCLT', 'RSCGT', 'RSCLE',
                                'RSCS', 'RSCSEQ', 'RSCSNE', 'RSCSCS', 'RSCSHS', 'RSCSCC', 'RSCSLO', 'RSCSMI', 'RSCSPL',
                                'RSCSVS', 'RSCSVC', 'RSCSHI', 'RSCSLS', 'RSCSGE', 'RSCSLT', 'RSCSGT', 'RSCSLE',
                                'AND', 'ANDEQ', 'ANDNE', 'ANDCS', 'ANDHS', 'ANDCC', 'ANDLO', 'ANDMI', 'ANDPL', 'ANDVS',
                                'ANDVC', 'ANDHI', 'ANDLS', 'ANDGE', 'ANDLT', 'ANDGT', 'ANDLE',
                                'ANDS', 'ANDSEQ', 'ANDSNE', 'ANDSCS', 'ANDSHS', 'ANDSCC', 'ANDSLO', 'ANDSMI', 'ANDSPL',
                                'ANDSVS', 'ANDSVC', 'ANDSHI', 'ANDSLS', 'ANDSGE', 'ANDSLT', 'ANDSGT', 'ANDSLE',
                                'BIC', 'BICEQ', 'BICNE', 'BICCS', 'BICHS', 'BICCC', 'BICLO', 'BICMI', 'BICPL', 'BICVS',
                                'BICVC', 'BICHI', 'BICLS', 'BICGE', 'BICLT', 'BICGT', 'BICLE',
                                'BICS', 'BICSEQ', 'BICSNE', 'BICSCS', 'BICSHS', 'BICSCC', 'BICSLO', 'BICSMI', 'BICSPL',
                                'BICSVS', 'BICSVC', 'BICSHI', 'BICSLS', 'BICSGE', 'BICSLT', 'BICSGT', 'BICSLE',
                                'ORR', 'ORREQ', 'ORRNE', 'ORRCS', 'ORRHS', 'ORRCC', 'ORRLO', 'ORRMI', 'ORRPL', 'ORRVS',
                                'ORRVC', 'ORRHI', 'ORRLS', 'ORRGE', 'ORRLT', 'ORRGT', 'ORRLE',
                                'ORRS', 'ORRSEQ', 'ORRSNE', 'ORRSCS', 'ORRSHS', 'ORRSCC', 'ORRSLO', 'ORRSMI', 'ORRSPL',
                                'ORRSVS', 'ORRSVC', 'ORRSHI', 'ORRSLS', 'ORRSGE', 'ORRSLT', 'ORRSGT', 'ORRSLE',
                                'EOR', 'EOREQ', 'EORNE', 'EORCS', 'EORHS', 'EORCC', 'EORLO', 'EORMI', 'EORPL', 'EORVS',
                                'EORVC', 'EORHI', 'EORLS', 'EORGE', 'EORLT', 'EORGT', 'EORLE',
                                'EORS', 'EORSEQ', 'EORSNE', 'EORSCS', 'EORSHS', 'EORSCC', 'EORSLO', 'EORSMI', 'EORSPL',
                                'EORSVS', 'EORSVC', 'EORSHI', 'EORSLS', 'EORSGE', 'EORSLT', 'EORSGT', 'EORSLE']
        super(ArithmeticInstruction, self).__init__(name, [destination, source_x, source_y], origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_general_purpose_register() and source_x.is_general_purpose_register() and source_y.is_modified_immediate12():
            pass
        elif destination.is_general_purpose_register() and source_x.is_general_purpose_register() and source_y.is_shifted_general_purpose_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def is_conditional(self):
        return self.name[-2:] in {"EQ", "NE", "CS", "CC", "LO", "MI", "PL", "VS", "VC", "HI", "LS", "GE", "LT", "GT",
                                  "LE"}

    def get_input_registers_list(self):
        if self.is_conditional():
            return self.operands[0].get_registers_list() + self.operands[1].get_registers_list() + self.operands[
                2].get_registers_list()
        else:
            return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class ShiftInstruction(Instruction):
    def __init__(self, name, destination, source_x, source_y, origin=None):
        allowed_instructions = ['LSL', 'LSR', 'ASR']
        super(ShiftInstruction, self).__init__(name, [destination, source_x, source_y], origin=origin)
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_general_purpose_register() and source_x.is_general_purpose_register() and source_y.is_immediate5():
            pass
        elif destination.is_general_purpose_register() and source_x.is_general_purpose_register() and source_y.is_general_purpose_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                             .format(name, destination, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[1].get_registers_list() + self.operands[2].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class CompareInstruction(Instruction):
    def __init__(self, name, source_x, source_y, origin=None):
        allowed_instructions = ['CMP', 'CMPEQ', 'CMPNE', 'CMPCS', 'CMPHS', 'CMPCC', 'CMPLO', 'CMPMI', 'CMPPL', 'CMPVS',
                                'CMPVC', 'CMPHI', 'CMPLS', 'CMPGE', 'CMPLT', 'CMPGT', 'CMPLE',
                                'TEQ', 'TEQEQ', 'TEQNE', 'TEQCS', 'TEQHS', 'TEQCC', 'TEQLO', 'TEQMI', 'TEQPL', 'TEQVS',
                                'TEQVC', 'TEQHI', 'TEQLS', 'TEQGE', 'TEQLT', 'TEQGT', 'TEQLE',
                                'TST', 'TSTEQ', 'TSTNE', 'TSTCS', 'TSTHS', 'TSTCC', 'TSTLO', 'TSTMI', 'TSTPL', 'TSTVS',
                                'TSTVC', 'TSTHI', 'TSTLS', 'TSTGE', 'TSTLT', 'TSTGT', 'TSTLE',
                                'TEQ', 'TEQEQ', 'TEQNE', 'TEQCS', 'TEQHS', 'TEQCC', 'TEQLO', 'TEQMI', 'TEQPL', 'TEQVS',
                                'TEQVC', 'TEQHI', 'TEQLS', 'TEQGE', 'TEQLT', 'TEQGT', 'TEQLE']
        if name in allowed_instructions:
            super(CompareInstruction, self).__init__(name, [source_x, source_y], origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if source_x.is_general_purpose_register() and source_y.is_modified_immediate12():
            pass
        elif source_x.is_general_purpose_register() and source_y.is_general_purpose_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, source_x, source_y))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list() + self.operands[1].get_registers_list()

    def get_output_registers_list(self):
        return list()


class MovInstruction(Instruction):
    def __init__(self, name, destination, source, origin=None):
        allowed_instructions = ['MOV', 'MOVEQ', 'MOVNE', 'MOVCS', 'MOVHS', 'MOVCC', 'MOVLO', 'MOVMI', 'MOVPL', 'MOVVS',
                                'MOVVC', 'MOVHI', 'MOVLS', 'MOVGE', 'MOVLT', 'MOVGT', 'MOVLE',
                                'MOVS', 'MOVSEQ', 'MOVSNE', 'MOVSCS', 'MOVSHS', 'MOVSCC', 'MOVSLO', 'MOVSMI', 'MOVSPL',
                                'MOVSVS', 'MOVSVC', 'MOVSHI', 'MOVSLS', 'MOVSGE', 'MOVSLT', 'MOVSGT', 'MOVSLE']
        if name in allowed_instructions:
            super(MovInstruction, self).__init__(name, [destination, source], origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'
                             .format(name, ", ".join(allowed_instructions)))
        if destination.is_general_purpose_register() and source.is_modified_immediate12():
            pass
        elif destination.is_general_purpose_register() and source.is_general_purpose_register():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, destination, source))

    def is_conditional(self):
        return self.name[-2:] in {"EQ", "NE", "CS", "CC", "LO", "MI", "PL", "VS", "VC", "HI", "LS", "GE", "LT", "GT",
                                  "LE"}

    def get_input_registers_list(self):
        if self.is_conditional():
            return self.operands[0].get_registers_list() + self.operands[1].get_registers_list()
        else:
            return self.operands[1].get_registers_list()

    def get_output_registers_list(self):
        return self.operands[0].get_registers_list()


class LoadStoreInstruction(Instruction):
    load_instructions = ['LDR', 'LDRH', 'LDRSH', 'LDRB', 'LDRSB']
    store_instructions = ['STR', 'STRB', 'STRH']

    def __init__(self, name, register, address, increment, origin=None):
        allowed_instructions = LoadStoreInstruction.load_instructions + LoadStoreInstruction.store_instructions
        if name not in allowed_instructions:
            raise ValueError('Instruction {0} is not one of the allowed instructions ({1})'.format(name, ", ".join(
                allowed_instructions)))
        if register.is_general_purpose_register() and address.is_memory_address(offset_bits=8) and increment.is_none():
            super(LoadStoreInstruction, self).__init__(name, [register, address], origin=origin)
        elif name in {'STR', 'LDR', 'LDRB',
                      'STRB'} and register.is_general_purpose_register() and address.is_memory_address(
                offset_bits=12) and increment.is_none():
            super(LoadStoreInstruction, self).__init__(name, [register, address], origin=origin)
        elif register.is_general_purpose_register() and address.is_memory_address(offset_bits=0,
                                                                                  allow_writeback=False) and increment.is_offset8():
            super(LoadStoreInstruction, self).__init__(name, [register, address, increment], origin=origin)
        elif register.is_general_purpose_register() and address.is_memory_address(offset_bits=0,
                                                                                  allow_writeback=False) and increment.is_offset12():
            super(LoadStoreInstruction, self).__init__(name, [register, address, increment], origin=origin)
        else:
            if increment.is_none():
                raise ValueError('Invalid operands in instruction {0} {1}, {2}'.format(name, register, address))
            else:
                raise ValueError('Invalid operands in instruction {0} {1}, {2}, {3}'
                                 .format(name, register, address, increment))

    def get_input_registers_list(self):
        input_registers_list = self.operands[
            0].get_registers_list() if self.name in LoadStoreInstruction.store_instructions else list()
        for operand in self.operands[1:]:
            input_registers_list += operand.get_registers_list()
        return input_registers_list

    def get_output_registers_list(self):
        output_registers_list = self.operands[
            0].get_registers_list() if self.name in LoadStoreInstruction.load_instructions else list()
        if len(self.operands) > 2 or self.operands[1].is_preindexed_memory_address():
            output_registers_list.append(self.operands[1].base)
        return output_registers_list


class PushPopInstruction(Instruction):
    def __init__(self, name, register_list, origin=None):
        allowed_instructions = {'PUSH', 'POP'}
        if name in allowed_instructions:
            super(PushPopInstruction, self).__init__(name, [register_list], origin=origin)
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if register_list.is_general_purpose_register_list():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}'.format(name, register_list))

    def get_input_registers_list(self):
        if self.name == 'PUSH':
            return self.operands[0].get_registers_list()
        else:
            return list()

    def get_output_registers_list(self):
        if self.name == 'POP':
            return self.operands[0].get_registers_list()
        else:
            return list()


class BranchInstruction(Instruction):
    def __init__(self, name, destination, origin=None):
        allowed_instructions = {'B', 'BEQ', 'BNE', 'BCS', 'BHS', 'BCC', 'BLO', 'BMI', 'BPL', 'BVS', 'BVC', 'BHI', 'BLS',
                                'BGE', 'BLT', 'BGT', 'BLE'}
        if name in allowed_instructions:
            super(BranchInstruction, self).__init__(name, [destination], origin=origin)
            self.is_visited = False
        else:
            raise ValueError('Instruction {0} is not one of the allowed instructions'.format(name))
        if destination.is_label():
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}'.format('BX', destination))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list()

    def get_output_registers_list(self):
        return list()

    def is_conditional(self):
        return not self.name == 'B'

    def __str__(self):
        return self.name + " L" + str(self.operands[0])


class BranchExchangeInstruction(Instruction):
    def __init__(self, destination, origin=None):
        from peachpy.arm.registers import lr
        super(BranchExchangeInstruction, self).__init__('BX', [destination], origin=origin)
        if destination.is_general_purpose_register() and destination.register == lr:
            pass
        else:
            raise ValueError('Invalid operands in instruction {0} {1}'.format('BX', destination))

    def get_input_registers_list(self):
        return self.operands[0].get_registers_list()

    def get_output_registers_list(self):
        return list()


class BreakInstruction(Instruction):
    def __init__(self, origin=None):
        super(BreakInstruction, self).__init__('BKPT', (), origin=origin)

    def __str__(self):
        return "BKPT"

    def get_input_registers_list(self):
        return []

    def get_output_registers_list(self):
        return []

    def get_constant(self):
        return None

    def get_local_variable(self):
        return None


def BX(destination):
    instruction = BranchExchangeInstruction(Operand(destination))
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BKPT():
    instruction = BreakInstruction()
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADD(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADD', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADDSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADDSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ADCSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ADCSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUB(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUB', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SUBSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SUBSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def SBCSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('SBCSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSB(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSB', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSBSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSBSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def RSCSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('RSCSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def AND(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('AND', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ANDSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ANDSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BIC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BIC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BICSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('BICSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORR(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORR', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORREQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORREQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ORRSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('ORRSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EOR(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EOR', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EOREQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EOREQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSEQ(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSEQ', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSNE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSNE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSCS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSCS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSHS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSHS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSCC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSCC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSLO(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSLO', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSMI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSMI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSPL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSPL', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSVS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSVS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSVC(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSVC', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSHI(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSHI', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSLS(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSLS', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSGE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSGE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSLT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSLT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSGT(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSGT', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def EORSLE(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ArithmeticInstruction('EORSLE', Operand(destination), Operand(source_x), Operand(source_y),
                                        origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LSL(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ShiftInstruction('LSL', Operand(destination), Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LSR(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ShiftInstruction('LSR', Operand(destination), Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def ASR(destination, source_x, source_y=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    if source_y is None:
        (destination, source_x, source_y) = (destination, destination, source_x)
    instruction = ShiftInstruction('ASR', Operand(destination), Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMP(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMP', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPEQ(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPEQ', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPNE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPNE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPCS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPCS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPHS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPHS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPCC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPCC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPLO(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPLO', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPMI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPMI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPPL(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPPL', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPVS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPVS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPVC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPVC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPHI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPHI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPLS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPLS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPGE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPGE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPLT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPLT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPGT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPGT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMPLE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMPLE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMN(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMN', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNEQ(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNEQ', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNNE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNNE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNCS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNCS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNHS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNHS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNCC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNCC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNLO(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNLO', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNMI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNMI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNPL(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNPL', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNVS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNVS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNVC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNVC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNHI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNHI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNLS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNLS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNGE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNGE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNLT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNLT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNGT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNGT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def CMNLE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('CMNLE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TST(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TST', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTEQ(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTEQ', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTNE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTNE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTCS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTCS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTHS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTHS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTCC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTCC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTLO(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTLO', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTMI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTMI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTPL(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTPL', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTVS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTVS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTVC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTVC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTHI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTHI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTLS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTLS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTGE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTGE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTLT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTLT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTGT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTGT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TSTLE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TSTLE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQ(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQ', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQEQ(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQEQ', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQNE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQNE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQCS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQCS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQHS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQHS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQCC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQCC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQLO(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQLO', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQMI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQMI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQPL(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQPL', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQVS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQVS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQVC(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQVC', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQHI(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQHI', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQLS(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQLS', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQGE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQGE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQLT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQLT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQGT(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQGT', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def TEQLE(source_x, source_y):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = CompareInstruction('TEQLE', Operand(source_x), Operand(source_y), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOV(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOV', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVEQ(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVEQ', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVNE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVNE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVCS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVCS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVHS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVHS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVCC(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVCC', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVLO(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVLO', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVMI(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVMI', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVPL(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVPL', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVVS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVVS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVVC(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVVC', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVHI(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVHI', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVLS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVLS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVGE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVGE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVLT(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVLT', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVGT(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVGT', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVLE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVLE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSEQ(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSEQ', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSNE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSNE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSCS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSCS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSHS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSHS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSCC(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSCC', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSLO(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSLO', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSMI(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSMI', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSPL(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSPL', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSVS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSVS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSVC(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSVC', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSHI(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSHI', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSLS(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSLS', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSGE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSGE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSLT(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSLT', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSGT(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSGT', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def MOVSLE(destination, source):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = MovInstruction('MOVSLE', Operand(destination), Operand(source), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def PUSH(register_list):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = PushPopInstruction('PUSH', Operand(register_list), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def POP(register_list):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = PushPopInstruction('POP', Operand(register_list), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LDR(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('LDR', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def STR(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('STR', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LDRH(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('LDRH', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LDRSH(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('LDRSH', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def STRH(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('STRH', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LDRB(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('LDRB', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def LDRSB(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('LDRSB', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def STRB(register, address, increment=None):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = LoadStoreInstruction('STRB', Operand(register), Operand(address), Operand(increment), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def B(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('B', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BEQ(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BEQ', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BNE(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BNE', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BCS(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BCS', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BHS(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BHS', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BCC(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BCC', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BLO(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BLO', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BMI(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BMI', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BPL(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BPL', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BVS(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BVS', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BVC(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BVC', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BHI(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BHI', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BLS(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BLS', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BGE(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BGE', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BLT(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BLT', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BGT(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BGT', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


def BLE(destination):
    origin = inspect.stack() if peachpy.arm.function.active_function.collect_origin else None
    instruction = BranchInstruction('BLE', Operand(destination), origin=origin)
    if peachpy.stream.active_stream is not None:
        peachpy.stream.active_stream.add_instruction(instruction)
    return instruction


