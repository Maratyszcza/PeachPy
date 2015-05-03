from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister
from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, MOVSXD
from peachpy.x86_64.mmxsse import MOVQ, MOVAPS
from peachpy.stream import NullStream
from peachpy import Type


def load_register(dst_reg, src_reg, src_type, prototype):
    assert dst_reg.size >= src_reg.size
    assert isinstance(src_type, Type)
    with NullStream():
        if isinstance(dst_reg, GeneralPurposeRegister):
            if dst_reg.size == src_reg.size:
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
                    return MOVZX(dst_reg, src_reg, prototype=prototype)
        elif isinstance(dst_reg, MMXRegister):
            return MOVQ(dst_reg, src_reg, prototype=prototype)
        elif isinstance(dst_reg, XMMRegister):
            return MOVAPS(dst_reg, src_reg, prototype=prototype)
