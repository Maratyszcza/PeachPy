from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister
from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, MOVSXD
from peachpy.x86_64.mmxsse import MOVQ, MOVAPS, MOVAPD, MOVSS, MOVSD, MOVDQA
from peachpy.x86_64.avx import VMOVAPS, VMOVAPD, VMOVSS, VMOVSD, VMOVDQA
from peachpy.x86_64.operand import dword, word, byte
from peachpy.stream import NullStream
from peachpy.x86_64 import m128, m128d, m128i
from peachpy import Type


def load_register(dst_reg, src_reg, is_signed_integer, prototype):
    assert dst_reg.size >= src_reg.size
    assert isinstance(is_signed_integer, bool)
    with NullStream():
        if isinstance(dst_reg, GeneralPurposeRegister):
            if dst_reg.size == src_reg.size:
                if dst_reg != src_reg or dst_reg.size == 4:
                    return MOV(dst_reg, src_reg, prototype=prototype)
            elif (dst_reg.size, src_reg.size) == (8, 4):
                if is_signed_integer:
                    return MOVSXD(dst_reg, src_reg, prototype=prototype)
                else:
                    return MOV(dst_reg.as_dword, src_reg, prototype=prototype)
            else:
                if is_signed_integer:
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
            if dst_reg != src_reg:
                if prototype.avx_mode:
                    return VMOVAPS(dst_reg, src_reg, prototype=prototype)
                else:
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
        elif isinstance(dst_reg, MMXRegister):
            return MOVQ(dst_reg, [src_address], prototype)
        elif isinstance(dst_reg, XMMRegister):
            if src_type.is_floating_point:
                assert src_type.size in [4, 8]
                if src_type.size == 4:
                    if prototype.avx_mode:
                        return VMOVSS(dst_reg, [src_address], prototype=prototype)
                    else:
                        return MOVSS(dst_reg, [src_address], prototype=prototype)
                else:
                    if prototype.avx_mode:
                        return VMOVSD(dst_reg, [src_address], prototype=prototype)
                    else:
                        return MOVSD(dst_reg, [src_address], prototype=prototype)
            else:
                assert src_type in [m128, m128d, m128i]
                if src_type == m128:
                    if prototype.avx_mode:
                        return VMOVAPS(dst_reg, [src_address], prototype=prototype)
                    else:
                        return MOVAPS(dst_reg, [src_address], prototype=prototype)
                elif src_type == m128d:
                    if prototype.avx_mode:
                        return VMOVAPD(dst_reg, [src_address], prototype=prototype)
                    else:
                        return MOVAPD(dst_reg, [src_address], prototype=prototype)
                else:
                    if prototype.avx_mode:
                        return VMOVDQA(dst_reg, [src_address], prototype=prototype)
                    else:
                        return MOVDQA(dst_reg, [src_address], prototype=prototype)
