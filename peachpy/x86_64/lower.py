from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister
from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, MOVSXD
from peachpy.x86_64.mmxsse import MOVQ, MOVAPS
from peachpy.x86_64.operand import dword, word, byte
from peachpy.stream import NullStream
from peachpy import Type


def load_register(dst_reg, src_reg, src_type, prototype):
    assert dst_reg.size >= src_reg.size
    assert isinstance(src_type, Type)
    with NullStream():
        if isinstance(dst_reg, GeneralPurposeRegister):
            if dst_reg.size == src_reg.size:
                if dst_reg != src_reg or dst_reg.size == 4:
                    return MOV(dst_reg, src_reg, prototype=prototype)
            elif (dst_reg.size, src_reg.size) == (8, 4):
                if src_type.is_signed_integer:
                    return MOVSXD(dst_reg, src_reg, prototype=prototype)
                else:
                    return MOV(dst_reg.as_dword, src_reg, prototype=prototype)
            else:
                if src_type.is_signed_integer:
                    return MOVSX(dst_reg, src_reg, prototype=prototype)
                else:
                    if dst_reg.size == 8:
                        return MOVZX(dst_reg.as_dword, src_reg, prototype=prototype)
                    else:
                        return MOVZX(dst_reg, src_reg, prototype=prototype)
        elif isinstance(dst_reg, MMXRegister):
            if dst_reg != src_reg:
                return MOVQ(dst_reg, src_reg, prototype=prototype)
        elif isinstance(dst_reg, XMMRegister):
            return MOVAPS(dst_reg, src_reg, prototype=prototype)


def load_memory(dst_reg, src_address, src_type, prototype):
    assert dst_reg >= src_type.size
    assert isinstance(src_type, Type)
    with NullStream():
        if isinstance(dst_reg, GeneralPurposeRegister):
            if dst_reg.size == src_type.size:
                return MOV(dst_reg, [src_address], prototype=prototype)
            elif (dst_reg.size, src_type.size) == (8, 4):
                if src_type.is_signed_integer:
                    return MOVSXD(dst_reg, dword[src_address], prototype=prototype)
                else:
                    return MOV(dst_reg.as_dword, dword[src_address], prototype=prototype)
            else:
                size_spec = {
                    1: byte,
                    2: word,
                    4: dword
                }[src_type.size]
                if src_type.is_signed_integer:
                    return MOVSX(dst_reg, size_spec[src_address], prototype=prototype)
                else:
                    if dst_reg.size == 8:
                        return MOVZX(dst_reg.as_dword, size_spec[src_address], prototype=prototype)
                    else:
                        return MOVZX(dst_reg, size_spec[src_address], prototype=prototype)
