from peachpy.x86_64.registers import GeneralPurposeRegister, MMXRegister, XMMRegister, YMMRegister
from peachpy.x86_64.generic import MOV, MOVZX, MOVSX, MOVSXD
from peachpy.x86_64.mmxsse import MOVQ, MOVAPS, MOVAPD, MOVSS, MOVSD, MOVDQA
from peachpy.x86_64.avx import VMOVAPS, VMOVAPD, VMOVSS, VMOVSD, VMOVDQA
from peachpy.x86_64.operand import dword, word, byte
from peachpy.stream import NullStream
from peachpy.x86_64 import m128, m128d, m128i, m256, m256d, m256i
from peachpy import Type


def load_register(dst_reg, src_reg, data_type, prototype):
    assert dst_reg.size >= src_reg.size
    assert isinstance(data_type, Type)
    with NullStream():
        if isinstance(dst_reg, GeneralPurposeRegister):
            if dst_reg.size == src_reg.size:
                if dst_reg != src_reg or dst_reg.size == 4:
                    return MOV(dst_reg, src_reg, prototype=prototype)
            elif (dst_reg.size, src_reg.size) == (8, 4):
                if data_type.is_signed_integer:
                    return MOVSXD(dst_reg, src_reg, prototype=prototype)
                else:
                    return MOV(dst_reg.as_dword, src_reg, prototype=prototype)
            else:
                if data_type.is_signed_integer:
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
                if data_type.is_floating_point:
                    assert data_type.size in [4, 8]
                    xmm_fp_mov = {
                        (4, True): VMOVAPS,
                        (4, False): MOVSS,
                        (8, True): VMOVAPD,
                        (8, False): MOVSD
                    }[(data_type.size, bool(prototype.avx_mode))]
                    return xmm_fp_mov(dst_reg, src_reg, prototype=prototype)
                else:
                    assert data_type in [m128, m128d, m128i]
                    xmm_mov = {
                        (m128, True): VMOVAPS,
                        (m128, False): MOVAPS,
                        (m128d, True): VMOVAPD,
                        (m128d, False): MOVAPD,
                        (m128i, True): VMOVDQA,
                        (m128i, False): MOVDQA
                    }[(data_type, bool(prototype.avx_mode))]
                    return xmm_mov(dst_reg, src_reg, prototype=prototype)
        elif isinstance(dst_reg, YMMRegister):
            if dst_reg != src_reg:
                ymm_mov = {
                    m256: VMOVAPS,
                    m256d: VMOVAPD,
                    m256i: VMOVDQA
                }[data_type]
                return ymm_mov(dst_reg, src_reg, prototype=prototype)
        else:
            assert False, "Unexpected type: " + dst_reg.__class__


def load_memory(dst_reg, src_address, src_type, prototype):
    assert dst_reg.size >= src_type.size
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
