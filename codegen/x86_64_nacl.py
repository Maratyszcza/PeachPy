# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import print_function
from peachpy.x86_64 import *

instruction_list = []

# avx

instruction_list.append(("VMOVSS xmm, m32", (MOV(esi, esi), VMOVSS(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VMOVSS m32, xmm", (MOV(esi, esi), VMOVSS(dword[r15+rsi*1+32], xmm7))))
instruction_list.append(("VMOVSS xmm, xmm, xmm", (VMOVSS(xmm7, xmm7, xmm7),)))

instruction_list.append(("VEXTRACTPS r32, xmm, imm8", (VEXTRACTPS(ebx, xmm7, 2),)))
instruction_list.append(("VEXTRACTPS m32, xmm, imm8", (MOV(esi, esi), VEXTRACTPS(dword[r15+rsi*1+32], xmm7, 2))))

instruction_list.append(("VINSERTPS xmm, xmm, xmm, imm8", (VINSERTPS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VINSERTPS xmm, xmm, m32, imm8", (MOV(esi, esi), VINSERTPS(xmm7, xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("VADDSS xmm, xmm, xmm", (VADDSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDSS xmm, xmm, m32", (MOV(esi, esi), VADDSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VSUBSS xmm, xmm, xmm", (VSUBSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSUBSS xmm, xmm, m32", (MOV(esi, esi), VSUBSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VMULSS xmm, xmm, xmm", (VMULSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMULSS xmm, xmm, m32", (MOV(esi, esi), VMULSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VDIVSS xmm, xmm, xmm", (VDIVSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VDIVSS xmm, xmm, m32", (MOV(esi, esi), VDIVSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VSQRTSS xmm, xmm, xmm", (VSQRTSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSQRTSS xmm, xmm, m32", (MOV(esi, esi), VSQRTSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VROUNDSS xmm, xmm, xmm, imm8", (VROUNDSS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VROUNDSS xmm, xmm, m32, imm8", (MOV(esi, esi), VROUNDSS(xmm7, xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("VMINSS xmm, xmm, xmm", (VMINSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMINSS xmm, xmm, m32", (MOV(esi, esi), VMINSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VMAXSS xmm, xmm, xmm", (VMAXSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMAXSS xmm, xmm, m32", (MOV(esi, esi), VMAXSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VRCPSS xmm, xmm, xmm", (VRCPSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VRCPSS xmm, xmm, m32", (MOV(esi, esi), VRCPSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VRSQRTSS xmm, xmm, xmm", (VRSQRTSS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VRSQRTSS xmm, xmm, m32", (MOV(esi, esi), VRSQRTSS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VCMPSS xmm, xmm, xmm, imm8", (VCMPSS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VCMPSS xmm, xmm, m32, imm8", (MOV(esi, esi), VCMPSS(xmm7, xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("VCOMISS xmm, xmm", (VCOMISS(xmm7, xmm7),)))
instruction_list.append(("VCOMISS xmm, m32", (MOV(esi, esi), VCOMISS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VUCOMISS xmm, xmm", (VUCOMISS(xmm7, xmm7),)))
instruction_list.append(("VUCOMISS xmm, m32", (MOV(esi, esi), VUCOMISS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VMOVSD xmm, m64", (MOV(esi, esi), VMOVSD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VMOVSD m64, xmm", (MOV(esi, esi), VMOVSD(qword[r15+rsi*1+64], xmm7))))
instruction_list.append(("VMOVSD xmm, xmm, xmm", (VMOVSD(xmm7, xmm7, xmm7),)))

instruction_list.append(("VADDSD xmm, xmm, xmm", (VADDSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDSD xmm, xmm, m64", (MOV(esi, esi), VADDSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VSUBSD xmm, xmm, xmm", (VSUBSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSUBSD xmm, xmm, m64", (MOV(esi, esi), VSUBSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMULSD xmm, xmm, xmm", (VMULSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMULSD xmm, xmm, m64", (MOV(esi, esi), VMULSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VDIVSD xmm, xmm, xmm", (VDIVSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VDIVSD xmm, xmm, m64", (MOV(esi, esi), VDIVSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VSQRTSD xmm, xmm, xmm", (VSQRTSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSQRTSD xmm, xmm, m64", (MOV(esi, esi), VSQRTSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VROUNDSD xmm, xmm, xmm, imm8", (VROUNDSD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VROUNDSD xmm, xmm, m64, imm8", (MOV(esi, esi), VROUNDSD(xmm7, xmm7, qword[r15+rsi*1+64], 2))))

instruction_list.append(("VMINSD xmm, xmm, xmm", (VMINSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMINSD xmm, xmm, m64", (MOV(esi, esi), VMINSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMAXSD xmm, xmm, xmm", (VMAXSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMAXSD xmm, xmm, m64", (MOV(esi, esi), VMAXSD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VCMPSD xmm, xmm, xmm, imm8", (VCMPSD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VCMPSD xmm, xmm, m64, imm8", (MOV(esi, esi), VCMPSD(xmm7, xmm7, qword[r15+rsi*1+64], 2))))

instruction_list.append(("VCOMISD xmm, xmm", (VCOMISD(xmm7, xmm7),)))
instruction_list.append(("VCOMISD xmm, m64", (MOV(esi, esi), VCOMISD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VUCOMISD xmm, xmm", (VUCOMISD(xmm7, xmm7),)))
instruction_list.append(("VUCOMISD xmm, m64", (MOV(esi, esi), VUCOMISD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMOVAPS xmm, xmm", (VMOVAPS(xmm7, xmm7),)))
instruction_list.append(("VMOVAPS xmm, m128", (MOV(esi, esi), VMOVAPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVAPS ymm, ymm", (VMOVAPS(ymm3, ymm3),)))
instruction_list.append(("VMOVAPS ymm, m256", (MOV(esi, esi), VMOVAPS(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVAPS m128, xmm", (MOV(esi, esi), VMOVAPS(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVAPS m256, ymm", (MOV(esi, esi), VMOVAPS(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVUPS xmm, xmm", (VMOVUPS(xmm7, xmm7),)))
instruction_list.append(("VMOVUPS xmm, m128", (MOV(esi, esi), VMOVUPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVUPS ymm, ymm", (VMOVUPS(ymm3, ymm3),)))
instruction_list.append(("VMOVUPS ymm, m256", (MOV(esi, esi), VMOVUPS(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVUPS m128, xmm", (MOV(esi, esi), VMOVUPS(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVUPS m256, ymm", (MOV(esi, esi), VMOVUPS(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVLPS m64, xmm", (MOV(esi, esi), VMOVLPS(qword[r15+rsi*1+64], xmm7))))
instruction_list.append(("VMOVLPS xmm, xmm, m64", (MOV(esi, esi), VMOVLPS(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMOVHPS m64, xmm", (MOV(esi, esi), VMOVHPS(qword[r15+rsi*1+64], xmm7))))
instruction_list.append(("VMOVHPS xmm, xmm, m64", (MOV(esi, esi), VMOVHPS(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMASKMOVPS xmm, xmm, m128", (MOV(esi, esi), VMASKMOVPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMASKMOVPS ymm, ymm, m256", (MOV(esi, esi), VMASKMOVPS(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMASKMOVPS m128, xmm, xmm", (MOV(esi, esi), VMASKMOVPS(oword[r15+rsi*1+128], xmm7, xmm7))))
instruction_list.append(("VMASKMOVPS m256, ymm, ymm", (MOV(esi, esi), VMASKMOVPS(hword[r15+rsi*1+256], ymm3, ymm3))))

instruction_list.append(("VMOVMSKPS r32, xmm", (VMOVMSKPS(ebx, xmm7),)))
instruction_list.append(("VMOVMSKPS r32, ymm", (VMOVMSKPS(ebx, ymm3),)))

instruction_list.append(("VMOVNTPS m128, xmm", (MOV(esi, esi), VMOVNTPS(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVNTPS m256, ymm", (MOV(esi, esi), VMOVNTPS(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VBROADCASTSS xmm, xmm", (VBROADCASTSS(xmm7, xmm7),)))
instruction_list.append(("VBROADCASTSS xmm, m32", (MOV(esi, esi), VBROADCASTSS(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VBROADCASTSS ymm, xmm", (VBROADCASTSS(ymm3, xmm7),)))
instruction_list.append(("VBROADCASTSS ymm, m32", (MOV(esi, esi), VBROADCASTSS(ymm3, dword[r15+rsi*1+32]))))

instruction_list.append(("VMOVSLDUP xmm, xmm", (VMOVSLDUP(xmm7, xmm7),)))
instruction_list.append(("VMOVSLDUP xmm, m128", (MOV(esi, esi), VMOVSLDUP(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVSLDUP ymm, ymm", (VMOVSLDUP(ymm3, ymm3),)))
instruction_list.append(("VMOVSLDUP ymm, m256", (MOV(esi, esi), VMOVSLDUP(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMOVSHDUP xmm, xmm", (VMOVSHDUP(xmm7, xmm7),)))
instruction_list.append(("VMOVSHDUP xmm, m128", (MOV(esi, esi), VMOVSHDUP(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVSHDUP ymm, ymm", (VMOVSHDUP(ymm3, ymm3),)))
instruction_list.append(("VMOVSHDUP ymm, m256", (MOV(esi, esi), VMOVSHDUP(ymm3, hword[r15+rsi*1+256]))))



instruction_list.append(("VMOVAPD xmm, xmm", (VMOVAPD(xmm7, xmm7),)))
instruction_list.append(("VMOVAPD xmm, m128", (MOV(esi, esi), VMOVAPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVAPD ymm, ymm", (VMOVAPD(ymm3, ymm3),)))
instruction_list.append(("VMOVAPD ymm, m256", (MOV(esi, esi), VMOVAPD(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVAPD m128, xmm", (MOV(esi, esi), VMOVAPD(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVAPD m256, ymm", (MOV(esi, esi), VMOVAPD(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVUPD xmm, xmm", (VMOVUPD(xmm7, xmm7),)))
instruction_list.append(("VMOVUPD xmm, m128", (MOV(esi, esi), VMOVUPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVUPD ymm, ymm", (VMOVUPD(ymm3, ymm3),)))
instruction_list.append(("VMOVUPD ymm, m256", (MOV(esi, esi), VMOVUPD(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVUPD m128, xmm", (MOV(esi, esi), VMOVUPD(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVUPD m256, ymm", (MOV(esi, esi), VMOVUPD(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVLPD m64, xmm", (MOV(esi, esi), VMOVLPD(qword[r15+rsi*1+64], xmm7))))
instruction_list.append(("VMOVLPD xmm, xmm, m64", (MOV(esi, esi), VMOVLPD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMOVHPD m64, xmm", (MOV(esi, esi), VMOVHPD(qword[r15+rsi*1+64], xmm7))))
instruction_list.append(("VMOVHPD xmm, xmm, m64", (MOV(esi, esi), VMOVHPD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VMASKMOVPD xmm, xmm, m128", (MOV(esi, esi), VMASKMOVPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMASKMOVPD ymm, ymm, m256", (MOV(esi, esi), VMASKMOVPD(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMASKMOVPD m128, xmm, xmm", (MOV(esi, esi), VMASKMOVPD(oword[r15+rsi*1+128], xmm7, xmm7))))
instruction_list.append(("VMASKMOVPD m256, ymm, ymm", (MOV(esi, esi), VMASKMOVPD(hword[r15+rsi*1+256], ymm3, ymm3))))

instruction_list.append(("VMOVMSKPD r32, xmm", (VMOVMSKPD(ebx, xmm7),)))
instruction_list.append(("VMOVMSKPD r32, ymm", (VMOVMSKPD(ebx, ymm3),)))

instruction_list.append(("VMOVNTPD m128, xmm", (MOV(esi, esi), VMOVNTPD(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVNTPD m256, ymm", (MOV(esi, esi), VMOVNTPD(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VBROADCASTSD ymm, xmm", (VBROADCASTSD(ymm3, xmm7),)))
instruction_list.append(("VBROADCASTSD ymm, m64", (MOV(esi, esi), VBROADCASTSD(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VMOVDDUP xmm, xmm", (VMOVDDUP(xmm7, xmm7),)))
instruction_list.append(("VMOVDDUP xmm, m64", (MOV(esi, esi), VMOVDDUP(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VMOVDDUP ymm, ymm", (VMOVDDUP(ymm3, ymm3),)))
instruction_list.append(("VMOVDDUP ymm, m256", (MOV(esi, esi), VMOVDDUP(ymm3, hword[r15+rsi*1+256]))))



instruction_list.append(("VADDPS xmm, xmm, xmm", (VADDPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDPS xmm, xmm, m128", (MOV(esi, esi), VADDPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VADDPS ymm, ymm, ymm", (VADDPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VADDPS ymm, ymm, m256", (MOV(esi, esi), VADDPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VHADDPS xmm, xmm, xmm", (VHADDPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VHADDPS xmm, xmm, m128", (MOV(esi, esi), VHADDPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VHADDPS ymm, ymm, ymm", (VHADDPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VHADDPS ymm, ymm, m256", (MOV(esi, esi), VHADDPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VSUBPS xmm, xmm, xmm", (VSUBPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSUBPS xmm, xmm, m128", (MOV(esi, esi), VSUBPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VSUBPS ymm, ymm, ymm", (VSUBPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VSUBPS ymm, ymm, m256", (MOV(esi, esi), VSUBPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VHSUBPS xmm, xmm, xmm", (VHSUBPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VHSUBPS xmm, xmm, m128", (MOV(esi, esi), VHSUBPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VHSUBPS ymm, ymm, ymm", (VHSUBPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VHSUBPS ymm, ymm, m256", (MOV(esi, esi), VHSUBPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VADDSUBPS xmm, xmm, xmm", (VADDSUBPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDSUBPS xmm, xmm, m128", (MOV(esi, esi), VADDSUBPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VADDSUBPS ymm, ymm, ymm", (VADDSUBPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VADDSUBPS ymm, ymm, m256", (MOV(esi, esi), VADDSUBPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMULPS xmm, xmm, xmm", (VMULPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMULPS xmm, xmm, m128", (MOV(esi, esi), VMULPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMULPS ymm, ymm, ymm", (VMULPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMULPS ymm, ymm, m256", (MOV(esi, esi), VMULPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VDIVPS xmm, xmm, xmm", (VDIVPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VDIVPS xmm, xmm, m128", (MOV(esi, esi), VDIVPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VDIVPS ymm, ymm, ymm", (VDIVPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VDIVPS ymm, ymm, m256", (MOV(esi, esi), VDIVPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VSQRTPS xmm, xmm", (VSQRTPS(xmm7, xmm7),)))
instruction_list.append(("VSQRTPS xmm, m128", (MOV(esi, esi), VSQRTPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VSQRTPS ymm, ymm", (VSQRTPS(ymm3, ymm3),)))
instruction_list.append(("VSQRTPS ymm, m256", (MOV(esi, esi), VSQRTPS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VADDPD xmm, xmm, xmm", (VADDPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDPD xmm, xmm, m128", (MOV(esi, esi), VADDPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VADDPD ymm, ymm, ymm", (VADDPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VADDPD ymm, ymm, m256", (MOV(esi, esi), VADDPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VHADDPD xmm, xmm, xmm", (VHADDPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VHADDPD xmm, xmm, m128", (MOV(esi, esi), VHADDPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VHADDPD ymm, ymm, ymm", (VHADDPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VHADDPD ymm, ymm, m256", (MOV(esi, esi), VHADDPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VSUBPD xmm, xmm, xmm", (VSUBPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VSUBPD xmm, xmm, m128", (MOV(esi, esi), VSUBPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VSUBPD ymm, ymm, ymm", (VSUBPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VSUBPD ymm, ymm, m256", (MOV(esi, esi), VSUBPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VHSUBPD xmm, xmm, xmm", (VHSUBPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VHSUBPD xmm, xmm, m128", (MOV(esi, esi), VHSUBPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VHSUBPD ymm, ymm, ymm", (VHSUBPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VHSUBPD ymm, ymm, m256", (MOV(esi, esi), VHSUBPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VADDSUBPD xmm, xmm, xmm", (VADDSUBPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VADDSUBPD xmm, xmm, m128", (MOV(esi, esi), VADDSUBPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VADDSUBPD ymm, ymm, ymm", (VADDSUBPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VADDSUBPD ymm, ymm, m256", (MOV(esi, esi), VADDSUBPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMULPD xmm, xmm, xmm", (VMULPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMULPD xmm, xmm, m128", (MOV(esi, esi), VMULPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMULPD ymm, ymm, ymm", (VMULPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMULPD ymm, ymm, m256", (MOV(esi, esi), VMULPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VDIVPD xmm, xmm, xmm", (VDIVPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VDIVPD xmm, xmm, m128", (MOV(esi, esi), VDIVPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VDIVPD ymm, ymm, ymm", (VDIVPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VDIVPD ymm, ymm, m256", (MOV(esi, esi), VDIVPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VSQRTPD xmm, xmm", (VSQRTPD(xmm7, xmm7),)))
instruction_list.append(("VSQRTPD xmm, m128", (MOV(esi, esi), VSQRTPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VSQRTPD ymm, ymm", (VSQRTPD(ymm3, ymm3),)))
instruction_list.append(("VSQRTPD ymm, m256", (MOV(esi, esi), VSQRTPD(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VROUNDPS xmm, xmm, imm8", (VROUNDPS(xmm7, xmm7, 2),)))
instruction_list.append(("VROUNDPS xmm, m128, imm8", (MOV(esi, esi), VROUNDPS(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VROUNDPS ymm, ymm, imm8", (VROUNDPS(ymm3, ymm3, 2),)))
instruction_list.append(("VROUNDPS ymm, m256, imm8", (MOV(esi, esi), VROUNDPS(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VMINPS xmm, xmm, xmm", (VMINPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMINPS xmm, xmm, m128", (MOV(esi, esi), VMINPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMINPS ymm, ymm, ymm", (VMINPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMINPS ymm, ymm, m256", (MOV(esi, esi), VMINPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMAXPS xmm, xmm, xmm", (VMAXPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMAXPS xmm, xmm, m128", (MOV(esi, esi), VMAXPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMAXPS ymm, ymm, ymm", (VMAXPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMAXPS ymm, ymm, m256", (MOV(esi, esi), VMAXPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VRCPPS xmm, xmm", (VRCPPS(xmm7, xmm7),)))
instruction_list.append(("VRCPPS xmm, m128", (MOV(esi, esi), VRCPPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VRCPPS ymm, ymm", (VRCPPS(ymm3, ymm3),)))
instruction_list.append(("VRCPPS ymm, m256", (MOV(esi, esi), VRCPPS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VRSQRTPS xmm, xmm", (VRSQRTPS(xmm7, xmm7),)))
instruction_list.append(("VRSQRTPS xmm, m128", (MOV(esi, esi), VRSQRTPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VRSQRTPS ymm, ymm", (VRSQRTPS(ymm3, ymm3),)))
instruction_list.append(("VRSQRTPS ymm, m256", (MOV(esi, esi), VRSQRTPS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VDPPS xmm, xmm, xmm, imm8", (VDPPS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VDPPS xmm, xmm, m128, imm8", (MOV(esi, esi), VDPPS(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VDPPS ymm, ymm, ymm, imm8", (VDPPS(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VDPPS ymm, ymm, m256, imm8", (MOV(esi, esi), VDPPS(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VCMPPS xmm, xmm, xmm, imm8", (VCMPPS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VCMPPS xmm, xmm, m128, imm8", (MOV(esi, esi), VCMPPS(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VCMPPS ymm, ymm, ymm, imm8", (VCMPPS(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VCMPPS ymm, ymm, m256, imm8", (MOV(esi, esi), VCMPPS(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VTESTPS xmm, xmm", (VTESTPS(xmm7, xmm7),)))
instruction_list.append(("VTESTPS xmm, m128", (MOV(esi, esi), VTESTPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VTESTPS ymm, ymm", (VTESTPS(ymm3, ymm3),)))
instruction_list.append(("VTESTPS ymm, m256", (MOV(esi, esi), VTESTPS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VROUNDPD xmm, xmm, imm8", (VROUNDPD(xmm7, xmm7, 2),)))
instruction_list.append(("VROUNDPD xmm, m128, imm8", (MOV(esi, esi), VROUNDPD(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VROUNDPD ymm, ymm, imm8", (VROUNDPD(ymm3, ymm3, 2),)))
instruction_list.append(("VROUNDPD ymm, m256, imm8", (MOV(esi, esi), VROUNDPD(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VMINPD xmm, xmm, xmm", (VMINPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMINPD xmm, xmm, m128", (MOV(esi, esi), VMINPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMINPD ymm, ymm, ymm", (VMINPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMINPD ymm, ymm, m256", (MOV(esi, esi), VMINPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMAXPD xmm, xmm, xmm", (VMAXPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VMAXPD xmm, xmm, m128", (MOV(esi, esi), VMAXPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMAXPD ymm, ymm, ymm", (VMAXPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VMAXPD ymm, ymm, m256", (MOV(esi, esi), VMAXPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VDPPD xmm, xmm, xmm, imm8", (VDPPD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VDPPD xmm, xmm, m128, imm8", (MOV(esi, esi), VDPPD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VCMPPD xmm, xmm, xmm, imm8", (VCMPPD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VCMPPD xmm, xmm, m128, imm8", (MOV(esi, esi), VCMPPD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VCMPPD ymm, ymm, ymm, imm8", (VCMPPD(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VCMPPD ymm, ymm, m256, imm8", (MOV(esi, esi), VCMPPD(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VTESTPD xmm, xmm", (VTESTPD(xmm7, xmm7),)))
instruction_list.append(("VTESTPD xmm, m128", (MOV(esi, esi), VTESTPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VTESTPD ymm, ymm", (VTESTPD(ymm3, ymm3),)))
instruction_list.append(("VTESTPD ymm, m256", (MOV(esi, esi), VTESTPD(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VANDPS xmm, xmm, xmm", (VANDPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VANDPS xmm, xmm, m128", (MOV(esi, esi), VANDPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VANDPS ymm, ymm, ymm", (VANDPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VANDPS ymm, ymm, m256", (MOV(esi, esi), VANDPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VANDNPS xmm, xmm, xmm", (VANDNPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VANDNPS xmm, xmm, m128", (MOV(esi, esi), VANDNPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VANDNPS ymm, ymm, ymm", (VANDNPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VANDNPS ymm, ymm, m256", (MOV(esi, esi), VANDNPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VORPS xmm, xmm, xmm", (VORPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VORPS xmm, xmm, m128", (MOV(esi, esi), VORPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VORPS ymm, ymm, ymm", (VORPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VORPS ymm, ymm, m256", (MOV(esi, esi), VORPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VXORPS xmm, xmm, xmm", (VXORPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VXORPS xmm, xmm, m128", (MOV(esi, esi), VXORPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VXORPS ymm, ymm, ymm", (VXORPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VXORPS ymm, ymm, m256", (MOV(esi, esi), VXORPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VBLENDPS xmm, xmm, xmm, imm8", (VBLENDPS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VBLENDPS xmm, xmm, m128, imm8", (MOV(esi, esi), VBLENDPS(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VBLENDPS ymm, ymm, ymm, imm8", (VBLENDPS(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VBLENDPS ymm, ymm, m256, imm8", (MOV(esi, esi), VBLENDPS(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VBLENDVPS xmm, xmm, xmm, xmm", (VBLENDVPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VBLENDVPS xmm, xmm, m128, xmm", (MOV(esi, esi), VBLENDVPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VBLENDVPS ymm, ymm, ymm, ymm", (VBLENDVPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VBLENDVPS ymm, ymm, m256, ymm", (MOV(esi, esi), VBLENDVPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VANDPD xmm, xmm, xmm", (VANDPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VANDPD xmm, xmm, m128", (MOV(esi, esi), VANDPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VANDPD ymm, ymm, ymm", (VANDPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VANDPD ymm, ymm, m256", (MOV(esi, esi), VANDPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VANDNPD xmm, xmm, xmm", (VANDNPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VANDNPD xmm, xmm, m128", (MOV(esi, esi), VANDNPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VANDNPD ymm, ymm, ymm", (VANDNPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VANDNPD ymm, ymm, m256", (MOV(esi, esi), VANDNPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VORPD xmm, xmm, xmm", (VORPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VORPD xmm, xmm, m128", (MOV(esi, esi), VORPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VORPD ymm, ymm, ymm", (VORPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VORPD ymm, ymm, m256", (MOV(esi, esi), VORPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VXORPD xmm, xmm, xmm", (VXORPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VXORPD xmm, xmm, m128", (MOV(esi, esi), VXORPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VXORPD ymm, ymm, ymm", (VXORPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VXORPD ymm, ymm, m256", (MOV(esi, esi), VXORPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VBLENDPD xmm, xmm, xmm, imm8", (VBLENDPD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VBLENDPD xmm, xmm, m128, imm8", (MOV(esi, esi), VBLENDPD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VBLENDPD ymm, ymm, ymm, imm8", (VBLENDPD(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VBLENDPD ymm, ymm, m256, imm8", (MOV(esi, esi), VBLENDPD(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VBLENDVPD xmm, xmm, xmm, xmm", (VBLENDVPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VBLENDVPD xmm, xmm, m128, xmm", (MOV(esi, esi), VBLENDVPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VBLENDVPD ymm, ymm, ymm, ymm", (VBLENDVPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VBLENDVPD ymm, ymm, m256, ymm", (MOV(esi, esi), VBLENDVPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VUNPCKLPS xmm, xmm, xmm", (VUNPCKLPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VUNPCKLPS xmm, xmm, m128", (MOV(esi, esi), VUNPCKLPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VUNPCKLPS ymm, ymm, ymm", (VUNPCKLPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VUNPCKLPS ymm, ymm, m256", (MOV(esi, esi), VUNPCKLPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VUNPCKHPS xmm, xmm, xmm", (VUNPCKHPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VUNPCKHPS xmm, xmm, m128", (MOV(esi, esi), VUNPCKHPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VUNPCKHPS ymm, ymm, ymm", (VUNPCKHPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VUNPCKHPS ymm, ymm, m256", (MOV(esi, esi), VUNPCKHPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMOVLHPS xmm, xmm, xmm", (VMOVLHPS(xmm7, xmm7, xmm7),)))

instruction_list.append(("VMOVHLPS xmm, xmm, xmm", (VMOVHLPS(xmm7, xmm7, xmm7),)))

instruction_list.append(("VSHUFPS xmm, xmm, xmm, imm8", (VSHUFPS(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VSHUFPS xmm, xmm, m128, imm8", (MOV(esi, esi), VSHUFPS(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VSHUFPS ymm, ymm, ymm, imm8", (VSHUFPS(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VSHUFPS ymm, ymm, m256, imm8", (MOV(esi, esi), VSHUFPS(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPERMPS ymm, ymm, ymm", (VPERMPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPERMPS ymm, ymm, m256", (MOV(esi, esi), VPERMPS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPERMILPS xmm, xmm, imm8", (VPERMILPS(xmm7, xmm7, 2),)))
instruction_list.append(("VPERMILPS xmm, xmm, xmm", (VPERMILPS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPERMILPS xmm, xmm, m128", (MOV(esi, esi), VPERMILPS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPERMILPS xmm, m128, imm8", (MOV(esi, esi), VPERMILPS(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPERMILPS ymm, ymm, imm8", (VPERMILPS(ymm3, ymm3, 2),)))
instruction_list.append(("VPERMILPS ymm, ymm, ymm", (VPERMILPS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPERMILPS ymm, ymm, m256", (MOV(esi, esi), VPERMILPS(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VPERMILPS ymm, m256, imm8", (MOV(esi, esi), VPERMILPS(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VUNPCKLPD xmm, xmm, xmm", (VUNPCKLPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VUNPCKLPD xmm, xmm, m128", (MOV(esi, esi), VUNPCKLPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VUNPCKLPD ymm, ymm, ymm", (VUNPCKLPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VUNPCKLPD ymm, ymm, m256", (MOV(esi, esi), VUNPCKLPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VUNPCKHPD xmm, xmm, xmm", (VUNPCKHPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VUNPCKHPD xmm, xmm, m128", (MOV(esi, esi), VUNPCKHPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VUNPCKHPD ymm, ymm, ymm", (VUNPCKHPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VUNPCKHPD ymm, ymm, m256", (MOV(esi, esi), VUNPCKHPD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VSHUFPD xmm, xmm, xmm, imm8", (VSHUFPD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VSHUFPD xmm, xmm, m128, imm8", (MOV(esi, esi), VSHUFPD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VSHUFPD ymm, ymm, ymm, imm8", (VSHUFPD(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VSHUFPD ymm, ymm, m256, imm8", (MOV(esi, esi), VSHUFPD(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPERMPD ymm, ymm, imm8", (VPERMPD(ymm3, ymm3, 2),)))
instruction_list.append(("VPERMPD ymm, m256, imm8", (MOV(esi, esi), VPERMPD(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPERMILPD xmm, xmm, imm8", (VPERMILPD(xmm7, xmm7, 2),)))
instruction_list.append(("VPERMILPD xmm, xmm, xmm", (VPERMILPD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPERMILPD xmm, xmm, m128", (MOV(esi, esi), VPERMILPD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPERMILPD xmm, m128, imm8", (MOV(esi, esi), VPERMILPD(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPERMILPD ymm, ymm, imm8", (VPERMILPD(ymm3, ymm3, 2),)))
instruction_list.append(("VPERMILPD ymm, ymm, ymm", (VPERMILPD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPERMILPD ymm, ymm, m256", (MOV(esi, esi), VPERMILPD(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VPERMILPD ymm, m256, imm8", (MOV(esi, esi), VPERMILPD(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VMOVD r32, xmm", (VMOVD(ebx, xmm7),)))
instruction_list.append(("VMOVD xmm, r32", (VMOVD(xmm7, ebx),)))
instruction_list.append(("VMOVD xmm, m32", (MOV(esi, esi), VMOVD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VMOVD m32, xmm", (MOV(esi, esi), VMOVD(dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("VMOVQ r64, xmm", (VMOVQ(rdi, xmm7),)))
instruction_list.append(("VMOVQ xmm, r64", (VMOVQ(xmm7, rdi),)))
instruction_list.append(("VMOVQ xmm, xmm", (VMOVQ(xmm7, xmm7),)))
instruction_list.append(("VMOVQ xmm, m64", (MOV(esi, esi), VMOVQ(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VMOVQ m64, xmm", (MOV(esi, esi), VMOVQ(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("VMOVDQA xmm, xmm", (VMOVDQA(xmm7, xmm7),)))
instruction_list.append(("VMOVDQA xmm, m128", (MOV(esi, esi), VMOVDQA(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVDQA ymm, ymm", (VMOVDQA(ymm3, ymm3),)))
instruction_list.append(("VMOVDQA ymm, m256", (MOV(esi, esi), VMOVDQA(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVDQA m128, xmm", (MOV(esi, esi), VMOVDQA(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVDQA m256, ymm", (MOV(esi, esi), VMOVDQA(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVDQU xmm, xmm", (VMOVDQU(xmm7, xmm7),)))
instruction_list.append(("VMOVDQU xmm, m128", (MOV(esi, esi), VMOVDQU(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVDQU ymm, ymm", (VMOVDQU(ymm3, ymm3),)))
instruction_list.append(("VMOVDQU ymm, m256", (MOV(esi, esi), VMOVDQU(ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VMOVDQU m128, xmm", (MOV(esi, esi), VMOVDQU(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVDQU m256, ymm", (MOV(esi, esi), VMOVDQU(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VLDDQU xmm, m128", (MOV(esi, esi), VLDDQU(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VLDDQU ymm, m256", (MOV(esi, esi), VLDDQU(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMASKMOVD xmm, xmm, m128", (MOV(esi, esi), VPMASKMOVD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMASKMOVD ymm, ymm, m256", (MOV(esi, esi), VPMASKMOVD(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VPMASKMOVD m128, xmm, xmm", (MOV(esi, esi), VPMASKMOVD(oword[r15+rsi*1+128], xmm7, xmm7))))
instruction_list.append(("VPMASKMOVD m256, ymm, ymm", (MOV(esi, esi), VPMASKMOVD(hword[r15+rsi*1+256], ymm3, ymm3))))

instruction_list.append(("VPMASKMOVQ xmm, xmm, m128", (MOV(esi, esi), VPMASKMOVQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMASKMOVQ ymm, ymm, m256", (MOV(esi, esi), VPMASKMOVQ(ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VPMASKMOVQ m128, xmm, xmm", (MOV(esi, esi), VPMASKMOVQ(oword[r15+rsi*1+128], xmm7, xmm7))))
instruction_list.append(("VPMASKMOVQ m256, ymm, ymm", (MOV(esi, esi), VPMASKMOVQ(hword[r15+rsi*1+256], ymm3, ymm3))))

instruction_list.append(("VMASKMOVDQU xmm, xmm", (VMASKMOVDQU(xmm7, xmm7),)))

instruction_list.append(("VMOVNTDQ m128, xmm", (MOV(esi, esi), VMOVNTDQ(oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VMOVNTDQ m256, ymm", (MOV(esi, esi), VMOVNTDQ(hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VMOVNTDQA xmm, m128", (MOV(esi, esi), VMOVNTDQA(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VMOVNTDQA ymm, m256", (MOV(esi, esi), VMOVNTDQA(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMOVSXBW xmm, xmm", (VPMOVSXBW(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXBW xmm, m64", (MOV(esi, esi), VPMOVSXBW(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVSXBW ymm, xmm", (VPMOVSXBW(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXBW ymm, m128", (MOV(esi, esi), VPMOVSXBW(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMOVSXBD xmm, xmm", (VPMOVSXBD(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXBD xmm, m32", (MOV(esi, esi), VPMOVSXBD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VPMOVSXBD ymm, xmm", (VPMOVSXBD(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXBD ymm, m64", (MOV(esi, esi), VPMOVSXBD(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VPMOVSXBQ xmm, xmm", (VPMOVSXBQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXBQ xmm, m16", (MOV(esi, esi), VPMOVSXBQ(xmm7, word[r15+rsi*1+16]))))
instruction_list.append(("VPMOVSXBQ ymm, xmm", (VPMOVSXBQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXBQ ymm, m32", (MOV(esi, esi), VPMOVSXBQ(ymm3, dword[r15+rsi*1+32]))))

instruction_list.append(("VPMOVSXWD xmm, xmm", (VPMOVSXWD(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXWD xmm, m64", (MOV(esi, esi), VPMOVSXWD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVSXWD ymm, xmm", (VPMOVSXWD(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXWD ymm, m128", (MOV(esi, esi), VPMOVSXWD(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMOVSXWQ xmm, xmm", (VPMOVSXWQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXWQ xmm, m32", (MOV(esi, esi), VPMOVSXWQ(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VPMOVSXWQ ymm, xmm", (VPMOVSXWQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXWQ ymm, m64", (MOV(esi, esi), VPMOVSXWQ(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VPMOVSXDQ xmm, xmm", (VPMOVSXDQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVSXDQ xmm, m64", (MOV(esi, esi), VPMOVSXDQ(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVSXDQ ymm, xmm", (VPMOVSXDQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVSXDQ ymm, m128", (MOV(esi, esi), VPMOVSXDQ(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMOVZXBW xmm, xmm", (VPMOVZXBW(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXBW xmm, m64", (MOV(esi, esi), VPMOVZXBW(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVZXBW ymm, xmm", (VPMOVZXBW(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXBW ymm, m128", (MOV(esi, esi), VPMOVZXBW(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMOVZXBD xmm, xmm", (VPMOVZXBD(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXBD xmm, m32", (MOV(esi, esi), VPMOVZXBD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VPMOVZXBD ymm, xmm", (VPMOVZXBD(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXBD ymm, m64", (MOV(esi, esi), VPMOVZXBD(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VPMOVZXBQ xmm, xmm", (VPMOVZXBQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXBQ xmm, m16", (MOV(esi, esi), VPMOVZXBQ(xmm7, word[r15+rsi*1+16]))))
instruction_list.append(("VPMOVZXBQ ymm, xmm", (VPMOVZXBQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXBQ ymm, m32", (MOV(esi, esi), VPMOVZXBQ(ymm3, dword[r15+rsi*1+32]))))

instruction_list.append(("VPMOVZXWD xmm, xmm", (VPMOVZXWD(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXWD xmm, m64", (MOV(esi, esi), VPMOVZXWD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVZXWD ymm, xmm", (VPMOVZXWD(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXWD ymm, m128", (MOV(esi, esi), VPMOVZXWD(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMOVZXWQ xmm, xmm", (VPMOVZXWQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXWQ xmm, m32", (MOV(esi, esi), VPMOVZXWQ(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VPMOVZXWQ ymm, xmm", (VPMOVZXWQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXWQ ymm, m64", (MOV(esi, esi), VPMOVZXWQ(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VPMOVZXDQ xmm, xmm", (VPMOVZXDQ(xmm7, xmm7),)))
instruction_list.append(("VPMOVZXDQ xmm, m64", (MOV(esi, esi), VPMOVZXDQ(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPMOVZXDQ ymm, xmm", (VPMOVZXDQ(ymm3, xmm7),)))
instruction_list.append(("VPMOVZXDQ ymm, m128", (MOV(esi, esi), VPMOVZXDQ(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPEXTRB r32, xmm, imm8", (VPEXTRB(ebx, xmm7, 2),)))
instruction_list.append(("VPEXTRB m8, xmm, imm8", (MOV(esi, esi), VPEXTRB(byte[r15+rsi*1+8], xmm7, 2))))

instruction_list.append(("VPEXTRW r32, xmm, imm8", (VPEXTRW(ebx, xmm7, 2),)))
instruction_list.append(("VPEXTRW m16, xmm, imm8", (MOV(esi, esi), VPEXTRW(word[r15+rsi*1+16], xmm7, 2))))

instruction_list.append(("VPEXTRD r32, xmm, imm8", (VPEXTRD(ebx, xmm7, 2),)))
instruction_list.append(("VPEXTRD m32, xmm, imm8", (MOV(esi, esi), VPEXTRD(dword[r15+rsi*1+32], xmm7, 2))))

instruction_list.append(("VPEXTRQ r64, xmm, imm8", (VPEXTRQ(rdi, xmm7, 2),)))
instruction_list.append(("VPEXTRQ m64, xmm, imm8", (MOV(esi, esi), VPEXTRQ(qword[r15+rsi*1+64], xmm7, 2))))

instruction_list.append(("VPINSRB xmm, xmm, r32, imm8", (VPINSRB(xmm7, xmm7, ebx, 2),)))
instruction_list.append(("VPINSRB xmm, xmm, m8, imm8", (MOV(esi, esi), VPINSRB(xmm7, xmm7, byte[r15+rsi*1+8], 2))))

instruction_list.append(("VPINSRW xmm, xmm, r32, imm8", (VPINSRW(xmm7, xmm7, ebx, 2),)))
instruction_list.append(("VPINSRW xmm, xmm, m16, imm8", (MOV(esi, esi), VPINSRW(xmm7, xmm7, word[r15+rsi*1+16], 2))))

instruction_list.append(("VPINSRD xmm, xmm, r32, imm8", (VPINSRD(xmm7, xmm7, ebx, 2),)))
instruction_list.append(("VPINSRD xmm, xmm, m32, imm8", (MOV(esi, esi), VPINSRD(xmm7, xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("VPINSRQ xmm, xmm, r64, imm8", (VPINSRQ(xmm7, xmm7, rdi, 2),)))
instruction_list.append(("VPINSRQ xmm, xmm, m64, imm8", (MOV(esi, esi), VPINSRQ(xmm7, xmm7, qword[r15+rsi*1+64], 2))))





instruction_list.append(("VPTEST xmm, xmm", (VPTEST(xmm7, xmm7),)))
instruction_list.append(("VPTEST xmm, m128", (MOV(esi, esi), VPTEST(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPTEST ymm, ymm", (VPTEST(ymm3, ymm3),)))
instruction_list.append(("VPTEST ymm, m256", (MOV(esi, esi), VPTEST(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMOVMSKB r32, xmm", (VPMOVMSKB(ebx, xmm7),)))
instruction_list.append(("VPMOVMSKB r32, ymm", (VPMOVMSKB(ebx, ymm3),)))

instruction_list.append(("VPADDB xmm, xmm, xmm", (VPADDB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDB xmm, xmm, m128", (MOV(esi, esi), VPADDB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDB ymm, ymm, ymm", (VPADDB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDB ymm, ymm, m256", (MOV(esi, esi), VPADDB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDW xmm, xmm, xmm", (VPADDW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDW xmm, xmm, m128", (MOV(esi, esi), VPADDW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDW ymm, ymm, ymm", (VPADDW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDW ymm, ymm, m256", (MOV(esi, esi), VPADDW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDD xmm, xmm, xmm", (VPADDD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDD xmm, xmm, m128", (MOV(esi, esi), VPADDD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDD ymm, ymm, ymm", (VPADDD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDD ymm, ymm, m256", (MOV(esi, esi), VPADDD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDQ xmm, xmm, xmm", (VPADDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDQ xmm, xmm, m128", (MOV(esi, esi), VPADDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDQ ymm, ymm, ymm", (VPADDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDQ ymm, ymm, m256", (MOV(esi, esi), VPADDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDSB xmm, xmm, xmm", (VPADDSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDSB xmm, xmm, m128", (MOV(esi, esi), VPADDSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDSB ymm, ymm, ymm", (VPADDSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDSB ymm, ymm, m256", (MOV(esi, esi), VPADDSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDSW xmm, xmm, xmm", (VPADDSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDSW xmm, xmm, m128", (MOV(esi, esi), VPADDSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDSW ymm, ymm, ymm", (VPADDSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDSW ymm, ymm, m256", (MOV(esi, esi), VPADDSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDUSB xmm, xmm, xmm", (VPADDUSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDUSB xmm, xmm, m128", (MOV(esi, esi), VPADDUSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDUSB ymm, ymm, ymm", (VPADDUSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDUSB ymm, ymm, m256", (MOV(esi, esi), VPADDUSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPADDUSW xmm, xmm, xmm", (VPADDUSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPADDUSW xmm, xmm, m128", (MOV(esi, esi), VPADDUSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPADDUSW ymm, ymm, ymm", (VPADDUSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPADDUSW ymm, ymm, m256", (MOV(esi, esi), VPADDUSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHADDW xmm, xmm, xmm", (VPHADDW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHADDW xmm, xmm, m128", (MOV(esi, esi), VPHADDW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHADDW ymm, ymm, ymm", (VPHADDW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHADDW ymm, ymm, m256", (MOV(esi, esi), VPHADDW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHADDD xmm, xmm, xmm", (VPHADDD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHADDD xmm, xmm, m128", (MOV(esi, esi), VPHADDD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHADDD ymm, ymm, ymm", (VPHADDD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHADDD ymm, ymm, m256", (MOV(esi, esi), VPHADDD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHADDSW xmm, xmm, xmm", (VPHADDSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHADDSW xmm, xmm, m128", (MOV(esi, esi), VPHADDSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHADDSW ymm, ymm, ymm", (VPHADDSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHADDSW ymm, ymm, m256", (MOV(esi, esi), VPHADDSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBB xmm, xmm, xmm", (VPSUBB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBB xmm, xmm, m128", (MOV(esi, esi), VPSUBB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBB ymm, ymm, ymm", (VPSUBB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBB ymm, ymm, m256", (MOV(esi, esi), VPSUBB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBW xmm, xmm, xmm", (VPSUBW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBW xmm, xmm, m128", (MOV(esi, esi), VPSUBW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBW ymm, ymm, ymm", (VPSUBW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBW ymm, ymm, m256", (MOV(esi, esi), VPSUBW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBD xmm, xmm, xmm", (VPSUBD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBD xmm, xmm, m128", (MOV(esi, esi), VPSUBD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBD ymm, ymm, ymm", (VPSUBD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBD ymm, ymm, m256", (MOV(esi, esi), VPSUBD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBQ xmm, xmm, xmm", (VPSUBQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBQ xmm, xmm, m128", (MOV(esi, esi), VPSUBQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBQ ymm, ymm, ymm", (VPSUBQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBQ ymm, ymm, m256", (MOV(esi, esi), VPSUBQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBSB xmm, xmm, xmm", (VPSUBSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBSB xmm, xmm, m128", (MOV(esi, esi), VPSUBSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBSB ymm, ymm, ymm", (VPSUBSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBSB ymm, ymm, m256", (MOV(esi, esi), VPSUBSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBSW xmm, xmm, xmm", (VPSUBSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBSW xmm, xmm, m128", (MOV(esi, esi), VPSUBSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBSW ymm, ymm, ymm", (VPSUBSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBSW ymm, ymm, m256", (MOV(esi, esi), VPSUBSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBUSB xmm, xmm, xmm", (VPSUBUSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBUSB xmm, xmm, m128", (MOV(esi, esi), VPSUBUSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBUSB ymm, ymm, ymm", (VPSUBUSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBUSB ymm, ymm, m256", (MOV(esi, esi), VPSUBUSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSUBUSW xmm, xmm, xmm", (VPSUBUSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSUBUSW xmm, xmm, m128", (MOV(esi, esi), VPSUBUSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSUBUSW ymm, ymm, ymm", (VPSUBUSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSUBUSW ymm, ymm, m256", (MOV(esi, esi), VPSUBUSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHSUBW xmm, xmm, xmm", (VPHSUBW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHSUBW xmm, xmm, m128", (MOV(esi, esi), VPHSUBW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHSUBW ymm, ymm, ymm", (VPHSUBW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHSUBW ymm, ymm, m256", (MOV(esi, esi), VPHSUBW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHSUBD xmm, xmm, xmm", (VPHSUBD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHSUBD xmm, xmm, m128", (MOV(esi, esi), VPHSUBD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHSUBD ymm, ymm, ymm", (VPHSUBD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHSUBD ymm, ymm, m256", (MOV(esi, esi), VPHSUBD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPHSUBSW xmm, xmm, xmm", (VPHSUBSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPHSUBSW xmm, xmm, m128", (MOV(esi, esi), VPHSUBSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPHSUBSW ymm, ymm, ymm", (VPHSUBSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPHSUBSW ymm, ymm, m256", (MOV(esi, esi), VPHSUBSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXSB xmm, xmm, xmm", (VPMAXSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXSB xmm, xmm, m128", (MOV(esi, esi), VPMAXSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXSB ymm, ymm, ymm", (VPMAXSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXSB ymm, ymm, m256", (MOV(esi, esi), VPMAXSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXSW xmm, xmm, xmm", (VPMAXSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXSW xmm, xmm, m128", (MOV(esi, esi), VPMAXSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXSW ymm, ymm, ymm", (VPMAXSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXSW ymm, ymm, m256", (MOV(esi, esi), VPMAXSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXSD xmm, xmm, xmm", (VPMAXSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXSD xmm, xmm, m128", (MOV(esi, esi), VPMAXSD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXSD ymm, ymm, ymm", (VPMAXSD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXSD ymm, ymm, m256", (MOV(esi, esi), VPMAXSD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXUB xmm, xmm, xmm", (VPMAXUB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXUB xmm, xmm, m128", (MOV(esi, esi), VPMAXUB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXUB ymm, ymm, ymm", (VPMAXUB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXUB ymm, ymm, m256", (MOV(esi, esi), VPMAXUB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXUW xmm, xmm, xmm", (VPMAXUW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXUW xmm, xmm, m128", (MOV(esi, esi), VPMAXUW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXUW ymm, ymm, ymm", (VPMAXUW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXUW ymm, ymm, m256", (MOV(esi, esi), VPMAXUW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMAXUD xmm, xmm, xmm", (VPMAXUD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMAXUD xmm, xmm, m128", (MOV(esi, esi), VPMAXUD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMAXUD ymm, ymm, ymm", (VPMAXUD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMAXUD ymm, ymm, m256", (MOV(esi, esi), VPMAXUD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINSB xmm, xmm, xmm", (VPMINSB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINSB xmm, xmm, m128", (MOV(esi, esi), VPMINSB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINSB ymm, ymm, ymm", (VPMINSB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINSB ymm, ymm, m256", (MOV(esi, esi), VPMINSB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINSW xmm, xmm, xmm", (VPMINSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINSW xmm, xmm, m128", (MOV(esi, esi), VPMINSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINSW ymm, ymm, ymm", (VPMINSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINSW ymm, ymm, m256", (MOV(esi, esi), VPMINSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINSD xmm, xmm, xmm", (VPMINSD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINSD xmm, xmm, m128", (MOV(esi, esi), VPMINSD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINSD ymm, ymm, ymm", (VPMINSD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINSD ymm, ymm, m256", (MOV(esi, esi), VPMINSD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINUB xmm, xmm, xmm", (VPMINUB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINUB xmm, xmm, m128", (MOV(esi, esi), VPMINUB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINUB ymm, ymm, ymm", (VPMINUB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINUB ymm, ymm, m256", (MOV(esi, esi), VPMINUB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINUW xmm, xmm, xmm", (VPMINUW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINUW xmm, xmm, m128", (MOV(esi, esi), VPMINUW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINUW ymm, ymm, ymm", (VPMINUW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINUW ymm, ymm, m256", (MOV(esi, esi), VPMINUW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMINUD xmm, xmm, xmm", (VPMINUD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMINUD xmm, xmm, m128", (MOV(esi, esi), VPMINUD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMINUD ymm, ymm, ymm", (VPMINUD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMINUD ymm, ymm, m256", (MOV(esi, esi), VPMINUD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSLLW xmm, xmm, imm8", (VPSLLW(xmm7, xmm7, 2),)))
instruction_list.append(("VPSLLW xmm, xmm, xmm", (VPSLLW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSLLW xmm, xmm, m128", (MOV(esi, esi), VPSLLW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSLLW ymm, ymm, imm8", (VPSLLW(ymm3, ymm3, 2),)))
instruction_list.append(("VPSLLW ymm, ymm, xmm", (VPSLLW(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSLLW ymm, ymm, m128", (MOV(esi, esi), VPSLLW(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSLLD xmm, xmm, imm8", (VPSLLD(xmm7, xmm7, 2),)))
instruction_list.append(("VPSLLD xmm, xmm, xmm", (VPSLLD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSLLD xmm, xmm, m128", (MOV(esi, esi), VPSLLD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSLLD ymm, ymm, imm8", (VPSLLD(ymm3, ymm3, 2),)))
instruction_list.append(("VPSLLD ymm, ymm, xmm", (VPSLLD(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSLLD ymm, ymm, m128", (MOV(esi, esi), VPSLLD(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSLLQ xmm, xmm, imm8", (VPSLLQ(xmm7, xmm7, 2),)))
instruction_list.append(("VPSLLQ xmm, xmm, xmm", (VPSLLQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSLLQ xmm, xmm, m128", (MOV(esi, esi), VPSLLQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSLLQ ymm, ymm, imm8", (VPSLLQ(ymm3, ymm3, 2),)))
instruction_list.append(("VPSLLQ ymm, ymm, xmm", (VPSLLQ(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSLLQ ymm, ymm, m128", (MOV(esi, esi), VPSLLQ(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSRLW xmm, xmm, imm8", (VPSRLW(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRLW xmm, xmm, xmm", (VPSRLW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRLW xmm, xmm, m128", (MOV(esi, esi), VPSRLW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRLW ymm, ymm, imm8", (VPSRLW(ymm3, ymm3, 2),)))
instruction_list.append(("VPSRLW ymm, ymm, xmm", (VPSRLW(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSRLW ymm, ymm, m128", (MOV(esi, esi), VPSRLW(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSRLD xmm, xmm, imm8", (VPSRLD(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRLD xmm, xmm, xmm", (VPSRLD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRLD xmm, xmm, m128", (MOV(esi, esi), VPSRLD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRLD ymm, ymm, imm8", (VPSRLD(ymm3, ymm3, 2),)))
instruction_list.append(("VPSRLD ymm, ymm, xmm", (VPSRLD(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSRLD ymm, ymm, m128", (MOV(esi, esi), VPSRLD(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSRLQ xmm, xmm, imm8", (VPSRLQ(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRLQ xmm, xmm, xmm", (VPSRLQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRLQ xmm, xmm, m128", (MOV(esi, esi), VPSRLQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRLQ ymm, ymm, imm8", (VPSRLQ(ymm3, ymm3, 2),)))
instruction_list.append(("VPSRLQ ymm, ymm, xmm", (VPSRLQ(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSRLQ ymm, ymm, m128", (MOV(esi, esi), VPSRLQ(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSRAW xmm, xmm, imm8", (VPSRAW(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRAW xmm, xmm, xmm", (VPSRAW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRAW xmm, xmm, m128", (MOV(esi, esi), VPSRAW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRAW ymm, ymm, imm8", (VPSRAW(ymm3, ymm3, 2),)))
instruction_list.append(("VPSRAW ymm, ymm, xmm", (VPSRAW(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSRAW ymm, ymm, m128", (MOV(esi, esi), VPSRAW(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSRAD xmm, xmm, imm8", (VPSRAD(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRAD xmm, xmm, xmm", (VPSRAD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRAD xmm, xmm, m128", (MOV(esi, esi), VPSRAD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRAD ymm, ymm, imm8", (VPSRAD(ymm3, ymm3, 2),)))
instruction_list.append(("VPSRAD ymm, ymm, xmm", (VPSRAD(ymm3, ymm3, xmm7),)))
instruction_list.append(("VPSRAD ymm, ymm, m128", (MOV(esi, esi), VPSRAD(ymm3, ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VPSLLVD xmm, xmm, xmm", (VPSLLVD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSLLVD xmm, xmm, m128", (MOV(esi, esi), VPSLLVD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSLLVD ymm, ymm, ymm", (VPSLLVD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSLLVD ymm, ymm, m256", (MOV(esi, esi), VPSLLVD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSLLVQ xmm, xmm, xmm", (VPSLLVQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSLLVQ xmm, xmm, m128", (MOV(esi, esi), VPSLLVQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSLLVQ ymm, ymm, ymm", (VPSLLVQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSLLVQ ymm, ymm, m256", (MOV(esi, esi), VPSLLVQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSRLVD xmm, xmm, xmm", (VPSRLVD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRLVD xmm, xmm, m128", (MOV(esi, esi), VPSRLVD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRLVD ymm, ymm, ymm", (VPSRLVD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSRLVD ymm, ymm, m256", (MOV(esi, esi), VPSRLVD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSRLVQ xmm, xmm, xmm", (VPSRLVQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRLVQ xmm, xmm, m128", (MOV(esi, esi), VPSRLVQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRLVQ ymm, ymm, ymm", (VPSRLVQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSRLVQ ymm, ymm, m256", (MOV(esi, esi), VPSRLVQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSRAVD xmm, xmm, xmm", (VPSRAVD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSRAVD xmm, xmm, m128", (MOV(esi, esi), VPSRAVD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSRAVD ymm, ymm, ymm", (VPSRAVD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSRAVD ymm, ymm, m256", (MOV(esi, esi), VPSRAVD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULLW xmm, xmm, xmm", (VPMULLW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULLW xmm, xmm, m128", (MOV(esi, esi), VPMULLW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULLW ymm, ymm, ymm", (VPMULLW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULLW ymm, ymm, m256", (MOV(esi, esi), VPMULLW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULHW xmm, xmm, xmm", (VPMULHW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULHW xmm, xmm, m128", (MOV(esi, esi), VPMULHW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULHW ymm, ymm, ymm", (VPMULHW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULHW ymm, ymm, m256", (MOV(esi, esi), VPMULHW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULHUW xmm, xmm, xmm", (VPMULHUW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULHUW xmm, xmm, m128", (MOV(esi, esi), VPMULHUW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULHUW ymm, ymm, ymm", (VPMULHUW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULHUW ymm, ymm, m256", (MOV(esi, esi), VPMULHUW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULLD xmm, xmm, xmm", (VPMULLD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULLD xmm, xmm, m128", (MOV(esi, esi), VPMULLD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULLD ymm, ymm, ymm", (VPMULLD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULLD ymm, ymm, m256", (MOV(esi, esi), VPMULLD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULDQ xmm, xmm, xmm", (VPMULDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULDQ xmm, xmm, m128", (MOV(esi, esi), VPMULDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULDQ ymm, ymm, ymm", (VPMULDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULDQ ymm, ymm, m256", (MOV(esi, esi), VPMULDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULUDQ xmm, xmm, xmm", (VPMULUDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULUDQ xmm, xmm, m128", (MOV(esi, esi), VPMULUDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULUDQ ymm, ymm, ymm", (VPMULUDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULUDQ ymm, ymm, m256", (MOV(esi, esi), VPMULUDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMULHRSW xmm, xmm, xmm", (VPMULHRSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMULHRSW xmm, xmm, m128", (MOV(esi, esi), VPMULHRSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMULHRSW ymm, ymm, ymm", (VPMULHRSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMULHRSW ymm, ymm, m256", (MOV(esi, esi), VPMULHRSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMADDWD xmm, xmm, xmm", (VPMADDWD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMADDWD xmm, xmm, m128", (MOV(esi, esi), VPMADDWD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMADDWD ymm, ymm, ymm", (VPMADDWD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMADDWD ymm, ymm, m256", (MOV(esi, esi), VPMADDWD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPMADDUBSW xmm, xmm, xmm", (VPMADDUBSW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMADDUBSW xmm, xmm, m128", (MOV(esi, esi), VPMADDUBSW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPMADDUBSW ymm, ymm, ymm", (VPMADDUBSW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPMADDUBSW ymm, ymm, m256", (MOV(esi, esi), VPMADDUBSW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPAVGB xmm, xmm, xmm", (VPAVGB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPAVGB xmm, xmm, m128", (MOV(esi, esi), VPAVGB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPAVGB ymm, ymm, ymm", (VPAVGB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPAVGB ymm, ymm, m256", (MOV(esi, esi), VPAVGB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPAVGW xmm, xmm, xmm", (VPAVGW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPAVGW xmm, xmm, m128", (MOV(esi, esi), VPAVGW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPAVGW ymm, ymm, ymm", (VPAVGW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPAVGW ymm, ymm, m256", (MOV(esi, esi), VPAVGW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSADBW xmm, xmm, xmm", (VPSADBW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSADBW xmm, xmm, m128", (MOV(esi, esi), VPSADBW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSADBW ymm, ymm, ymm", (VPSADBW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSADBW ymm, ymm, m256", (MOV(esi, esi), VPSADBW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VMPSADBW xmm, xmm, xmm, imm8", (VMPSADBW(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VMPSADBW xmm, xmm, m128, imm8", (MOV(esi, esi), VMPSADBW(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VMPSADBW ymm, ymm, ymm, imm8", (VMPSADBW(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VMPSADBW ymm, ymm, m256, imm8", (MOV(esi, esi), VMPSADBW(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPHMINPOSUW xmm, xmm", (VPHMINPOSUW(xmm7, xmm7),)))
instruction_list.append(("VPHMINPOSUW xmm, m128", (MOV(esi, esi), VPHMINPOSUW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPCMPEQB xmm, xmm, xmm", (VPCMPEQB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPEQB xmm, xmm, m128", (MOV(esi, esi), VPCMPEQB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPEQB ymm, ymm, ymm", (VPCMPEQB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPEQB ymm, ymm, m256", (MOV(esi, esi), VPCMPEQB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPEQW xmm, xmm, xmm", (VPCMPEQW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPEQW xmm, xmm, m128", (MOV(esi, esi), VPCMPEQW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPEQW ymm, ymm, ymm", (VPCMPEQW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPEQW ymm, ymm, m256", (MOV(esi, esi), VPCMPEQW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPEQD xmm, xmm, xmm", (VPCMPEQD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPEQD xmm, xmm, m128", (MOV(esi, esi), VPCMPEQD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPEQD ymm, ymm, ymm", (VPCMPEQD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPEQD ymm, ymm, m256", (MOV(esi, esi), VPCMPEQD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPEQQ xmm, xmm, xmm", (VPCMPEQQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPEQQ xmm, xmm, m128", (MOV(esi, esi), VPCMPEQQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPEQQ ymm, ymm, ymm", (VPCMPEQQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPEQQ ymm, ymm, m256", (MOV(esi, esi), VPCMPEQQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPGTB xmm, xmm, xmm", (VPCMPGTB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPGTB xmm, xmm, m128", (MOV(esi, esi), VPCMPGTB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPGTB ymm, ymm, ymm", (VPCMPGTB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPGTB ymm, ymm, m256", (MOV(esi, esi), VPCMPGTB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPGTW xmm, xmm, xmm", (VPCMPGTW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPGTW xmm, xmm, m128", (MOV(esi, esi), VPCMPGTW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPGTW ymm, ymm, ymm", (VPCMPGTW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPGTW ymm, ymm, m256", (MOV(esi, esi), VPCMPGTW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPGTD xmm, xmm, xmm", (VPCMPGTD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPGTD xmm, xmm, m128", (MOV(esi, esi), VPCMPGTD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPGTD ymm, ymm, ymm", (VPCMPGTD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPGTD ymm, ymm, m256", (MOV(esi, esi), VPCMPGTD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPCMPGTQ xmm, xmm, xmm", (VPCMPGTQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMPGTQ xmm, xmm, m128", (MOV(esi, esi), VPCMPGTQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMPGTQ ymm, ymm, ymm", (VPCMPGTQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMPGTQ ymm, ymm, m256", (MOV(esi, esi), VPCMPGTQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPABSB xmm, xmm", (VPABSB(xmm7, xmm7),)))
instruction_list.append(("VPABSB xmm, m128", (MOV(esi, esi), VPABSB(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPABSB ymm, ymm", (VPABSB(ymm3, ymm3),)))
instruction_list.append(("VPABSB ymm, m256", (MOV(esi, esi), VPABSB(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPABSW xmm, xmm", (VPABSW(xmm7, xmm7),)))
instruction_list.append(("VPABSW xmm, m128", (MOV(esi, esi), VPABSW(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPABSW ymm, ymm", (VPABSW(ymm3, ymm3),)))
instruction_list.append(("VPABSW ymm, m256", (MOV(esi, esi), VPABSW(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPABSD xmm, xmm", (VPABSD(xmm7, xmm7),)))
instruction_list.append(("VPABSD xmm, m128", (MOV(esi, esi), VPABSD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPABSD ymm, ymm", (VPABSD(ymm3, ymm3),)))
instruction_list.append(("VPABSD ymm, m256", (MOV(esi, esi), VPABSD(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSIGNB xmm, xmm, xmm", (VPSIGNB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSIGNB xmm, xmm, m128", (MOV(esi, esi), VPSIGNB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSIGNB ymm, ymm, ymm", (VPSIGNB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSIGNB ymm, ymm, m256", (MOV(esi, esi), VPSIGNB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSIGNW xmm, xmm, xmm", (VPSIGNW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSIGNW xmm, xmm, m128", (MOV(esi, esi), VPSIGNW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSIGNW ymm, ymm, ymm", (VPSIGNW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSIGNW ymm, ymm, m256", (MOV(esi, esi), VPSIGNW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSIGND xmm, xmm, xmm", (VPSIGND(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSIGND xmm, xmm, m128", (MOV(esi, esi), VPSIGND(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSIGND ymm, ymm, ymm", (VPSIGND(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSIGND ymm, ymm, m256", (MOV(esi, esi), VPSIGND(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPAND xmm, xmm, xmm", (VPAND(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPAND xmm, xmm, m128", (MOV(esi, esi), VPAND(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPAND ymm, ymm, ymm", (VPAND(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPAND ymm, ymm, m256", (MOV(esi, esi), VPAND(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPANDN xmm, xmm, xmm", (VPANDN(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPANDN xmm, xmm, m128", (MOV(esi, esi), VPANDN(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPANDN ymm, ymm, ymm", (VPANDN(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPANDN ymm, ymm, m256", (MOV(esi, esi), VPANDN(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPOR xmm, xmm, xmm", (VPOR(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPOR xmm, xmm, m128", (MOV(esi, esi), VPOR(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPOR ymm, ymm, ymm", (VPOR(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPOR ymm, ymm, m256", (MOV(esi, esi), VPOR(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPXOR xmm, xmm, xmm", (VPXOR(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPXOR xmm, xmm, m128", (MOV(esi, esi), VPXOR(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPXOR ymm, ymm, ymm", (VPXOR(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPXOR ymm, ymm, m256", (MOV(esi, esi), VPXOR(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPBLENDW xmm, xmm, xmm, imm8", (VPBLENDW(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPBLENDW xmm, xmm, m128, imm8", (MOV(esi, esi), VPBLENDW(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPBLENDW ymm, ymm, ymm, imm8", (VPBLENDW(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VPBLENDW ymm, ymm, m256, imm8", (MOV(esi, esi), VPBLENDW(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPBLENDVB xmm, xmm, xmm, xmm", (VPBLENDVB(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPBLENDVB xmm, xmm, m128, xmm", (MOV(esi, esi), VPBLENDVB(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VPBLENDVB ymm, ymm, ymm, ymm", (VPBLENDVB(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VPBLENDVB ymm, ymm, m256, ymm", (MOV(esi, esi), VPBLENDVB(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VPBLENDD xmm, xmm, xmm, imm8", (VPBLENDD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPBLENDD xmm, xmm, m128, imm8", (MOV(esi, esi), VPBLENDD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPBLENDD ymm, ymm, ymm, imm8", (VPBLENDD(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VPBLENDD ymm, ymm, m256, imm8", (MOV(esi, esi), VPBLENDD(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPUNPCKLBW xmm, xmm, xmm", (VPUNPCKLBW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKLBW xmm, xmm, m128", (MOV(esi, esi), VPUNPCKLBW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKLBW ymm, ymm, ymm", (VPUNPCKLBW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKLBW ymm, ymm, m256", (MOV(esi, esi), VPUNPCKLBW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKLWD xmm, xmm, xmm", (VPUNPCKLWD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKLWD xmm, xmm, m128", (MOV(esi, esi), VPUNPCKLWD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKLWD ymm, ymm, ymm", (VPUNPCKLWD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKLWD ymm, ymm, m256", (MOV(esi, esi), VPUNPCKLWD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKLDQ xmm, xmm, xmm", (VPUNPCKLDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKLDQ xmm, xmm, m128", (MOV(esi, esi), VPUNPCKLDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKLDQ ymm, ymm, ymm", (VPUNPCKLDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKLDQ ymm, ymm, m256", (MOV(esi, esi), VPUNPCKLDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKLQDQ xmm, xmm, xmm", (VPUNPCKLQDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKLQDQ xmm, xmm, m128", (MOV(esi, esi), VPUNPCKLQDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKLQDQ ymm, ymm, ymm", (VPUNPCKLQDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKLQDQ ymm, ymm, m256", (MOV(esi, esi), VPUNPCKLQDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKHBW xmm, xmm, xmm", (VPUNPCKHBW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKHBW xmm, xmm, m128", (MOV(esi, esi), VPUNPCKHBW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKHBW ymm, ymm, ymm", (VPUNPCKHBW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKHBW ymm, ymm, m256", (MOV(esi, esi), VPUNPCKHBW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKHWD xmm, xmm, xmm", (VPUNPCKHWD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKHWD xmm, xmm, m128", (MOV(esi, esi), VPUNPCKHWD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKHWD ymm, ymm, ymm", (VPUNPCKHWD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKHWD ymm, ymm, m256", (MOV(esi, esi), VPUNPCKHWD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKHDQ xmm, xmm, xmm", (VPUNPCKHDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKHDQ xmm, xmm, m128", (MOV(esi, esi), VPUNPCKHDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKHDQ ymm, ymm, ymm", (VPUNPCKHDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKHDQ ymm, ymm, m256", (MOV(esi, esi), VPUNPCKHDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPUNPCKHQDQ xmm, xmm, xmm", (VPUNPCKHQDQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPUNPCKHQDQ xmm, xmm, m128", (MOV(esi, esi), VPUNPCKHQDQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPUNPCKHQDQ ymm, ymm, ymm", (VPUNPCKHQDQ(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPUNPCKHQDQ ymm, ymm, m256", (MOV(esi, esi), VPUNPCKHQDQ(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPACKSSWB xmm, xmm, xmm", (VPACKSSWB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPACKSSWB xmm, xmm, m128", (MOV(esi, esi), VPACKSSWB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPACKSSWB ymm, ymm, ymm", (VPACKSSWB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPACKSSWB ymm, ymm, m256", (MOV(esi, esi), VPACKSSWB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPACKSSDW xmm, xmm, xmm", (VPACKSSDW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPACKSSDW xmm, xmm, m128", (MOV(esi, esi), VPACKSSDW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPACKSSDW ymm, ymm, ymm", (VPACKSSDW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPACKSSDW ymm, ymm, m256", (MOV(esi, esi), VPACKSSDW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPACKUSWB xmm, xmm, xmm", (VPACKUSWB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPACKUSWB xmm, xmm, m128", (MOV(esi, esi), VPACKUSWB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPACKUSWB ymm, ymm, ymm", (VPACKUSWB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPACKUSWB ymm, ymm, m256", (MOV(esi, esi), VPACKUSWB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPACKUSDW xmm, xmm, xmm", (VPACKUSDW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPACKUSDW xmm, xmm, m128", (MOV(esi, esi), VPACKUSDW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPACKUSDW ymm, ymm, ymm", (VPACKUSDW(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPACKUSDW ymm, ymm, m256", (MOV(esi, esi), VPACKUSDW(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSHUFB xmm, xmm, xmm", (VPSHUFB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHUFB xmm, xmm, m128", (MOV(esi, esi), VPSHUFB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHUFB ymm, ymm, ymm", (VPSHUFB(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPSHUFB ymm, ymm, m256", (MOV(esi, esi), VPSHUFB(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPSHUFLW xmm, xmm, imm8", (VPSHUFLW(xmm7, xmm7, 2),)))
instruction_list.append(("VPSHUFLW xmm, m128, imm8", (MOV(esi, esi), VPSHUFLW(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPSHUFLW ymm, ymm, imm8", (VPSHUFLW(ymm3, ymm3, 2),)))
instruction_list.append(("VPSHUFLW ymm, m256, imm8", (MOV(esi, esi), VPSHUFLW(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPSHUFHW xmm, xmm, imm8", (VPSHUFHW(xmm7, xmm7, 2),)))
instruction_list.append(("VPSHUFHW xmm, m128, imm8", (MOV(esi, esi), VPSHUFHW(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPSHUFHW ymm, ymm, imm8", (VPSHUFHW(ymm3, ymm3, 2),)))
instruction_list.append(("VPSHUFHW ymm, m256, imm8", (MOV(esi, esi), VPSHUFHW(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPSHUFD xmm, xmm, imm8", (VPSHUFD(xmm7, xmm7, 2),)))
instruction_list.append(("VPSHUFD xmm, m128, imm8", (MOV(esi, esi), VPSHUFD(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPSHUFD ymm, ymm, imm8", (VPSHUFD(ymm3, ymm3, 2),)))
instruction_list.append(("VPSHUFD ymm, m256, imm8", (MOV(esi, esi), VPSHUFD(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPERMD ymm, ymm, ymm", (VPERMD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VPERMD ymm, ymm, m256", (MOV(esi, esi), VPERMD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPERMQ ymm, ymm, imm8", (VPERMQ(ymm3, ymm3, 2),)))
instruction_list.append(("VPERMQ ymm, m256, imm8", (MOV(esi, esi), VPERMQ(ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPSLLDQ xmm, xmm, imm8", (VPSLLDQ(xmm7, xmm7, 2),)))
instruction_list.append(("VPSLLDQ ymm, ymm, imm8", (VPSLLDQ(ymm3, ymm3, 2),)))

instruction_list.append(("VPSRLDQ xmm, xmm, imm8", (VPSRLDQ(xmm7, xmm7, 2),)))
instruction_list.append(("VPSRLDQ ymm, ymm, imm8", (VPSRLDQ(ymm3, ymm3, 2),)))

instruction_list.append(("VPALIGNR xmm, xmm, xmm, imm8", (VPALIGNR(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPALIGNR xmm, xmm, m128, imm8", (MOV(esi, esi), VPALIGNR(xmm7, xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPALIGNR ymm, ymm, ymm, imm8", (VPALIGNR(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VPALIGNR ymm, ymm, m256, imm8", (MOV(esi, esi), VPALIGNR(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPBROADCASTB xmm, xmm", (VPBROADCASTB(xmm7, xmm7),)))
instruction_list.append(("VPBROADCASTB xmm, m8", (MOV(esi, esi), VPBROADCASTB(xmm7, byte[r15+rsi*1+8]))))
instruction_list.append(("VPBROADCASTB ymm, xmm", (VPBROADCASTB(ymm3, xmm7),)))
instruction_list.append(("VPBROADCASTB ymm, m8", (MOV(esi, esi), VPBROADCASTB(ymm3, byte[r15+rsi*1+8]))))

instruction_list.append(("VPBROADCASTW xmm, xmm", (VPBROADCASTW(xmm7, xmm7),)))
instruction_list.append(("VPBROADCASTW xmm, m16", (MOV(esi, esi), VPBROADCASTW(xmm7, word[r15+rsi*1+16]))))
instruction_list.append(("VPBROADCASTW ymm, xmm", (VPBROADCASTW(ymm3, xmm7),)))
instruction_list.append(("VPBROADCASTW ymm, m16", (MOV(esi, esi), VPBROADCASTW(ymm3, word[r15+rsi*1+16]))))

instruction_list.append(("VPBROADCASTD xmm, xmm", (VPBROADCASTD(xmm7, xmm7),)))
instruction_list.append(("VPBROADCASTD xmm, m32", (MOV(esi, esi), VPBROADCASTD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VPBROADCASTD ymm, xmm", (VPBROADCASTD(ymm3, xmm7),)))
instruction_list.append(("VPBROADCASTD ymm, m32", (MOV(esi, esi), VPBROADCASTD(ymm3, dword[r15+rsi*1+32]))))

instruction_list.append(("VPBROADCASTQ xmm, xmm", (VPBROADCASTQ(xmm7, xmm7),)))
instruction_list.append(("VPBROADCASTQ xmm, m64", (MOV(esi, esi), VPBROADCASTQ(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VPBROADCASTQ ymm, xmm", (VPBROADCASTQ(ymm3, xmm7),)))
instruction_list.append(("VPBROADCASTQ ymm, m64", (MOV(esi, esi), VPBROADCASTQ(ymm3, qword[r15+rsi*1+64]))))

instruction_list.append(("VPCMPESTRI xmm, xmm, imm8", (VPCMPESTRI(xmm7, xmm7, 2),)))
instruction_list.append(("VPCMPESTRI xmm, m128, imm8", (MOV(esi, esi), VPCMPESTRI(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCMPESTRM xmm, xmm, imm8", (VPCMPESTRM(xmm7, xmm7, 2),)))
instruction_list.append(("VPCMPESTRM xmm, m128, imm8", (MOV(esi, esi), VPCMPESTRM(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCMPISTRI xmm, xmm, imm8", (VPCMPISTRI(xmm7, xmm7, 2),)))
instruction_list.append(("VPCMPISTRI xmm, m128, imm8", (MOV(esi, esi), VPCMPISTRI(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCMPISTRM xmm, xmm, imm8", (VPCMPISTRM(xmm7, xmm7, 2),)))
instruction_list.append(("VPCMPISTRM xmm, m128, imm8", (MOV(esi, esi), VPCMPISTRM(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VCVTSS2SI r32, xmm", (VCVTSS2SI(ebx, xmm7),)))
instruction_list.append(("VCVTSS2SI r32, m32", (MOV(esi, esi), VCVTSS2SI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("VCVTSS2SI r64, xmm", (VCVTSS2SI(rdi, xmm7),)))
instruction_list.append(("VCVTSS2SI r64, m32", (MOV(esi, esi), VCVTSS2SI(rdi, dword[r15+rsi*1+32]))))

instruction_list.append(("VCVTTSS2SI r32, xmm", (VCVTTSS2SI(ebx, xmm7),)))
instruction_list.append(("VCVTTSS2SI r32, m32", (MOV(esi, esi), VCVTTSS2SI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("VCVTTSS2SI r64, xmm", (VCVTTSS2SI(rdi, xmm7),)))
instruction_list.append(("VCVTTSS2SI r64, m32", (MOV(esi, esi), VCVTTSS2SI(rdi, dword[r15+rsi*1+32]))))

instruction_list.append(("VCVTSI2SS xmm, xmm, r32", (VCVTSI2SS(xmm7, xmm7, ebx),)))
instruction_list.append(("VCVTSI2SS xmm, xmm, r64", (VCVTSI2SS(xmm7, xmm7, rdi),)))
instruction_list.append(("VCVTSI2SS xmm, xmm, m32", (MOV(esi, esi), VCVTSI2SS(xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VCVTSI2SS xmm, xmm, m64", (MOV(esi, esi), VCVTSI2SS(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VCVTSD2SI r32, xmm", (VCVTSD2SI(ebx, xmm7),)))
instruction_list.append(("VCVTSD2SI r32, m64", (MOV(esi, esi), VCVTSD2SI(ebx, qword[r15+rsi*1+64]))))
instruction_list.append(("VCVTSD2SI r64, xmm", (VCVTSD2SI(rdi, xmm7),)))
instruction_list.append(("VCVTSD2SI r64, m64", (MOV(esi, esi), VCVTSD2SI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("VCVTTSD2SI r32, xmm", (VCVTTSD2SI(ebx, xmm7),)))
instruction_list.append(("VCVTTSD2SI r32, m64", (MOV(esi, esi), VCVTTSD2SI(ebx, qword[r15+rsi*1+64]))))
instruction_list.append(("VCVTTSD2SI r64, xmm", (VCVTTSD2SI(rdi, xmm7),)))
instruction_list.append(("VCVTTSD2SI r64, m64", (MOV(esi, esi), VCVTTSD2SI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("VCVTSI2SD xmm, xmm, r32", (VCVTSI2SD(xmm7, xmm7, ebx),)))
instruction_list.append(("VCVTSI2SD xmm, xmm, r64", (VCVTSI2SD(xmm7, xmm7, rdi),)))
instruction_list.append(("VCVTSI2SD xmm, xmm, m32", (MOV(esi, esi), VCVTSI2SD(xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VCVTSI2SD xmm, xmm, m64", (MOV(esi, esi), VCVTSI2SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VCVTPS2DQ xmm, xmm", (VCVTPS2DQ(xmm7, xmm7),)))
instruction_list.append(("VCVTPS2DQ xmm, m128", (MOV(esi, esi), VCVTPS2DQ(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTPS2DQ ymm, ymm", (VCVTPS2DQ(ymm3, ymm3),)))
instruction_list.append(("VCVTPS2DQ ymm, m256", (MOV(esi, esi), VCVTPS2DQ(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTTPS2DQ xmm, xmm", (VCVTTPS2DQ(xmm7, xmm7),)))
instruction_list.append(("VCVTTPS2DQ xmm, m128", (MOV(esi, esi), VCVTTPS2DQ(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTTPS2DQ ymm, ymm", (VCVTTPS2DQ(ymm3, ymm3),)))
instruction_list.append(("VCVTTPS2DQ ymm, m256", (MOV(esi, esi), VCVTTPS2DQ(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTDQ2PS xmm, xmm", (VCVTDQ2PS(xmm7, xmm7),)))
instruction_list.append(("VCVTDQ2PS xmm, m128", (MOV(esi, esi), VCVTDQ2PS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTDQ2PS ymm, ymm", (VCVTDQ2PS(ymm3, ymm3),)))
instruction_list.append(("VCVTDQ2PS ymm, m256", (MOV(esi, esi), VCVTDQ2PS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTPD2DQ xmm, xmm", (VCVTPD2DQ(xmm7, xmm7),)))
instruction_list.append(("VCVTPD2DQ xmm, ymm", (VCVTPD2DQ(xmm7, ymm3),)))
instruction_list.append(("VCVTPD2DQ xmm, m128", (MOV(esi, esi), VCVTPD2DQ(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTPD2DQ xmm, m256", (MOV(esi, esi), VCVTPD2DQ(xmm7, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTTPD2DQ xmm, xmm", (VCVTTPD2DQ(xmm7, xmm7),)))
instruction_list.append(("VCVTTPD2DQ xmm, ymm", (VCVTTPD2DQ(xmm7, ymm3),)))
instruction_list.append(("VCVTTPD2DQ xmm, m128", (MOV(esi, esi), VCVTTPD2DQ(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTTPD2DQ xmm, m256", (MOV(esi, esi), VCVTTPD2DQ(xmm7, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTDQ2PD xmm, xmm", (VCVTDQ2PD(xmm7, xmm7),)))
instruction_list.append(("VCVTDQ2PD xmm, m64", (MOV(esi, esi), VCVTDQ2PD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VCVTDQ2PD ymm, xmm", (VCVTDQ2PD(ymm3, xmm7),)))
instruction_list.append(("VCVTDQ2PD ymm, m128", (MOV(esi, esi), VCVTDQ2PD(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VCVTSD2SS xmm, xmm, xmm", (VCVTSD2SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VCVTSD2SS xmm, xmm, m64", (MOV(esi, esi), VCVTSD2SS(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VCVTSS2SD xmm, xmm, xmm", (VCVTSS2SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VCVTSS2SD xmm, xmm, m32", (MOV(esi, esi), VCVTSS2SD(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VCVTPD2PS xmm, xmm", (VCVTPD2PS(xmm7, xmm7),)))
instruction_list.append(("VCVTPD2PS xmm, ymm", (VCVTPD2PS(xmm7, ymm3),)))
instruction_list.append(("VCVTPD2PS xmm, m128", (MOV(esi, esi), VCVTPD2PS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VCVTPD2PS xmm, m256", (MOV(esi, esi), VCVTPD2PS(xmm7, hword[r15+rsi*1+256]))))

instruction_list.append(("VCVTPS2PD xmm, xmm", (VCVTPS2PD(xmm7, xmm7),)))
instruction_list.append(("VCVTPS2PD xmm, m64", (MOV(esi, esi), VCVTPS2PD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VCVTPS2PD ymm, xmm", (VCVTPS2PD(ymm3, xmm7),)))
instruction_list.append(("VCVTPS2PD ymm, m128", (MOV(esi, esi), VCVTPS2PD(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VCVTPS2PH xmm, xmm, imm8", (VCVTPS2PH(xmm7, xmm7, 2),)))
instruction_list.append(("VCVTPS2PH xmm, ymm, imm8", (VCVTPS2PH(xmm7, ymm3, 2),)))
instruction_list.append(("VCVTPS2PH m64, xmm, imm8", (MOV(esi, esi), VCVTPS2PH(qword[r15+rsi*1+64], xmm7, 2))))
instruction_list.append(("VCVTPS2PH m128, ymm, imm8", (MOV(esi, esi), VCVTPS2PH(oword[r15+rsi*1+128], ymm3, 2))))

instruction_list.append(("VCVTPH2PS xmm, xmm", (VCVTPH2PS(xmm7, xmm7),)))
instruction_list.append(("VCVTPH2PS xmm, m64", (MOV(esi, esi), VCVTPH2PS(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VCVTPH2PS ymm, xmm", (VCVTPH2PS(ymm3, xmm7),)))
instruction_list.append(("VCVTPH2PS ymm, m128", (MOV(esi, esi), VCVTPH2PS(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VBROADCASTF128 ymm, m128", (MOV(esi, esi), VBROADCASTF128(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VBROADCASTI128 ymm, m128", (MOV(esi, esi), VBROADCASTI128(ymm3, oword[r15+rsi*1+128]))))

instruction_list.append(("VEXTRACTF128 xmm, ymm, imm8", (VEXTRACTF128(xmm7, ymm3, 2),)))
instruction_list.append(("VEXTRACTF128 m128, ymm, imm8", (MOV(esi, esi), VEXTRACTF128(oword[r15+rsi*1+128], ymm3, 2))))

instruction_list.append(("VEXTRACTI128 xmm, ymm, imm8", (VEXTRACTI128(xmm7, ymm3, 2),)))
instruction_list.append(("VEXTRACTI128 m128, ymm, imm8", (MOV(esi, esi), VEXTRACTI128(oword[r15+rsi*1+128], ymm3, 2))))

instruction_list.append(("VINSERTF128 ymm, ymm, xmm, imm8", (VINSERTF128(ymm3, ymm3, xmm7, 2),)))
instruction_list.append(("VINSERTF128 ymm, ymm, m128, imm8", (MOV(esi, esi), VINSERTF128(ymm3, ymm3, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VINSERTI128 ymm, ymm, xmm, imm8", (VINSERTI128(ymm3, ymm3, xmm7, 2),)))
instruction_list.append(("VINSERTI128 ymm, ymm, m128, imm8", (MOV(esi, esi), VINSERTI128(ymm3, ymm3, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPERM2F128 ymm, ymm, ymm, imm8", (VPERM2F128(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VPERM2F128 ymm, ymm, m256, imm8", (MOV(esi, esi), VPERM2F128(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VPERM2I128 ymm, ymm, ymm, imm8", (VPERM2I128(ymm3, ymm3, ymm3, 2),)))
instruction_list.append(("VPERM2I128 ymm, ymm, m256, imm8", (MOV(esi, esi), VPERM2I128(ymm3, ymm3, hword[r15+rsi*1+256], 2))))

instruction_list.append(("VLDMXCSR m32", (MOV(esi, esi), VLDMXCSR(dword[r15+rsi*1+32]))))

instruction_list.append(("VSTMXCSR m32", (MOV(esi, esi), VSTMXCSR(dword[r15+rsi*1+32]))))

instruction_list.append(("VZEROUPPER", (VZEROUPPER(),)))

instruction_list.append(("VZEROALL", (VZEROALL(),)))
# generic

instruction_list.append(("ADD al, imm8", (ADD(al, 2),)))
instruction_list.append(("ADD r8, imm8", (ADD(dl, 2),)))
instruction_list.append(("ADD r8, r8", (ADD(dl, dl),)))
instruction_list.append(("ADD r8, m8", (MOV(esi, esi), ADD(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("ADD ax, imm16", (ADD(ax, 32000),)))
instruction_list.append(("ADD r16, imm8", (ADD(cx, 2),)))
instruction_list.append(("ADD r16, imm16", (ADD(cx, 32000),)))
instruction_list.append(("ADD r16, r16", (ADD(cx, cx),)))
instruction_list.append(("ADD r16, m16", (MOV(esi, esi), ADD(cx, word[r15+rsi*1+16]))))
instruction_list.append(("ADD eax, imm32", (ADD(eax, 0x10000000),)))
instruction_list.append(("ADD r32, imm8", (ADD(ebx, 2),)))
instruction_list.append(("ADD r32, imm32", (ADD(ebx, 0x10000000),)))
instruction_list.append(("ADD r32, r32", (ADD(ebx, ebx),)))
instruction_list.append(("ADD r32, m32", (MOV(esi, esi), ADD(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("ADD rax, imm32", (ADD(rax, 0x10000000),)))
instruction_list.append(("ADD r64, imm8", (ADD(rdi, 2),)))
instruction_list.append(("ADD r64, imm32", (ADD(rdi, 0x10000000),)))
instruction_list.append(("ADD r64, r64", (ADD(rdi, rdi),)))
instruction_list.append(("ADD r64, m64", (MOV(esi, esi), ADD(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("ADD m8, imm8", (MOV(esi, esi), ADD(byte[r15+rsi*1+8], 2))))
instruction_list.append(("ADD m8, r8", (MOV(esi, esi), ADD(byte[r15+rsi*1+8], dl))))
instruction_list.append(("ADD m16, imm8", (MOV(esi, esi), ADD(word[r15+rsi*1+16], 2))))
instruction_list.append(("ADD m16, imm16", (MOV(esi, esi), ADD(word[r15+rsi*1+16], 32000))))
instruction_list.append(("ADD m16, r16", (MOV(esi, esi), ADD(word[r15+rsi*1+16], cx))))
instruction_list.append(("ADD m32, imm8", (MOV(esi, esi), ADD(dword[r15+rsi*1+32], 2))))
instruction_list.append(("ADD m32, imm32", (MOV(esi, esi), ADD(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("ADD m32, r32", (MOV(esi, esi), ADD(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("ADD m64, imm8", (MOV(esi, esi), ADD(qword[r15+rsi*1+64], 2))))
instruction_list.append(("ADD m64, imm32", (MOV(esi, esi), ADD(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("ADD m64, r64", (MOV(esi, esi), ADD(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("SUB al, imm8", (SUB(al, 2),)))
instruction_list.append(("SUB r8, imm8", (SUB(dl, 2),)))
instruction_list.append(("SUB r8, r8", (SUB(dl, dl),)))
instruction_list.append(("SUB r8, m8", (MOV(esi, esi), SUB(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("SUB ax, imm16", (SUB(ax, 32000),)))
instruction_list.append(("SUB r16, imm8", (SUB(cx, 2),)))
instruction_list.append(("SUB r16, imm16", (SUB(cx, 32000),)))
instruction_list.append(("SUB r16, r16", (SUB(cx, cx),)))
instruction_list.append(("SUB r16, m16", (MOV(esi, esi), SUB(cx, word[r15+rsi*1+16]))))
instruction_list.append(("SUB eax, imm32", (SUB(eax, 0x10000000),)))
instruction_list.append(("SUB r32, imm8", (SUB(ebx, 2),)))
instruction_list.append(("SUB r32, imm32", (SUB(ebx, 0x10000000),)))
instruction_list.append(("SUB r32, r32", (SUB(ebx, ebx),)))
instruction_list.append(("SUB r32, m32", (MOV(esi, esi), SUB(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("SUB rax, imm32", (SUB(rax, 0x10000000),)))
instruction_list.append(("SUB r64, imm8", (SUB(rdi, 2),)))
instruction_list.append(("SUB r64, imm32", (SUB(rdi, 0x10000000),)))
instruction_list.append(("SUB r64, r64", (SUB(rdi, rdi),)))
instruction_list.append(("SUB r64, m64", (MOV(esi, esi), SUB(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("SUB m8, imm8", (MOV(esi, esi), SUB(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SUB m8, r8", (MOV(esi, esi), SUB(byte[r15+rsi*1+8], dl))))
instruction_list.append(("SUB m16, imm8", (MOV(esi, esi), SUB(word[r15+rsi*1+16], 2))))
instruction_list.append(("SUB m16, imm16", (MOV(esi, esi), SUB(word[r15+rsi*1+16], 32000))))
instruction_list.append(("SUB m16, r16", (MOV(esi, esi), SUB(word[r15+rsi*1+16], cx))))
instruction_list.append(("SUB m32, imm8", (MOV(esi, esi), SUB(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SUB m32, imm32", (MOV(esi, esi), SUB(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("SUB m32, r32", (MOV(esi, esi), SUB(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("SUB m64, imm8", (MOV(esi, esi), SUB(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SUB m64, imm32", (MOV(esi, esi), SUB(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("SUB m64, r64", (MOV(esi, esi), SUB(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("ADC al, imm8", (ADC(al, 2),)))
instruction_list.append(("ADC r8, imm8", (ADC(dl, 2),)))
instruction_list.append(("ADC r8, r8", (ADC(dl, dl),)))
instruction_list.append(("ADC r8, m8", (MOV(esi, esi), ADC(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("ADC ax, imm16", (ADC(ax, 32000),)))
instruction_list.append(("ADC r16, imm8", (ADC(cx, 2),)))
instruction_list.append(("ADC r16, imm16", (ADC(cx, 32000),)))
instruction_list.append(("ADC r16, r16", (ADC(cx, cx),)))
instruction_list.append(("ADC r16, m16", (MOV(esi, esi), ADC(cx, word[r15+rsi*1+16]))))
instruction_list.append(("ADC eax, imm32", (ADC(eax, 0x10000000),)))
instruction_list.append(("ADC r32, imm8", (ADC(ebx, 2),)))
instruction_list.append(("ADC r32, imm32", (ADC(ebx, 0x10000000),)))
instruction_list.append(("ADC r32, r32", (ADC(ebx, ebx),)))
instruction_list.append(("ADC r32, m32", (MOV(esi, esi), ADC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("ADC rax, imm32", (ADC(rax, 0x10000000),)))
instruction_list.append(("ADC r64, imm8", (ADC(rdi, 2),)))
instruction_list.append(("ADC r64, imm32", (ADC(rdi, 0x10000000),)))
instruction_list.append(("ADC r64, r64", (ADC(rdi, rdi),)))
instruction_list.append(("ADC r64, m64", (MOV(esi, esi), ADC(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("ADC m8, imm8", (MOV(esi, esi), ADC(byte[r15+rsi*1+8], 2))))
instruction_list.append(("ADC m8, r8", (MOV(esi, esi), ADC(byte[r15+rsi*1+8], dl))))
instruction_list.append(("ADC m16, imm8", (MOV(esi, esi), ADC(word[r15+rsi*1+16], 2))))
instruction_list.append(("ADC m16, imm16", (MOV(esi, esi), ADC(word[r15+rsi*1+16], 32000))))
instruction_list.append(("ADC m16, r16", (MOV(esi, esi), ADC(word[r15+rsi*1+16], cx))))
instruction_list.append(("ADC m32, imm8", (MOV(esi, esi), ADC(dword[r15+rsi*1+32], 2))))
instruction_list.append(("ADC m32, imm32", (MOV(esi, esi), ADC(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("ADC m32, r32", (MOV(esi, esi), ADC(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("ADC m64, imm8", (MOV(esi, esi), ADC(qword[r15+rsi*1+64], 2))))
instruction_list.append(("ADC m64, imm32", (MOV(esi, esi), ADC(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("ADC m64, r64", (MOV(esi, esi), ADC(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("SBB al, imm8", (SBB(al, 2),)))
instruction_list.append(("SBB r8, imm8", (SBB(dl, 2),)))
instruction_list.append(("SBB r8, r8", (SBB(dl, dl),)))
instruction_list.append(("SBB r8, m8", (MOV(esi, esi), SBB(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("SBB ax, imm16", (SBB(ax, 32000),)))
instruction_list.append(("SBB r16, imm8", (SBB(cx, 2),)))
instruction_list.append(("SBB r16, imm16", (SBB(cx, 32000),)))
instruction_list.append(("SBB r16, r16", (SBB(cx, cx),)))
instruction_list.append(("SBB r16, m16", (MOV(esi, esi), SBB(cx, word[r15+rsi*1+16]))))
instruction_list.append(("SBB eax, imm32", (SBB(eax, 0x10000000),)))
instruction_list.append(("SBB r32, imm8", (SBB(ebx, 2),)))
instruction_list.append(("SBB r32, imm32", (SBB(ebx, 0x10000000),)))
instruction_list.append(("SBB r32, r32", (SBB(ebx, ebx),)))
instruction_list.append(("SBB r32, m32", (MOV(esi, esi), SBB(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("SBB rax, imm32", (SBB(rax, 0x10000000),)))
instruction_list.append(("SBB r64, imm8", (SBB(rdi, 2),)))
instruction_list.append(("SBB r64, imm32", (SBB(rdi, 0x10000000),)))
instruction_list.append(("SBB r64, r64", (SBB(rdi, rdi),)))
instruction_list.append(("SBB r64, m64", (MOV(esi, esi), SBB(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("SBB m8, imm8", (MOV(esi, esi), SBB(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SBB m8, r8", (MOV(esi, esi), SBB(byte[r15+rsi*1+8], dl))))
instruction_list.append(("SBB m16, imm8", (MOV(esi, esi), SBB(word[r15+rsi*1+16], 2))))
instruction_list.append(("SBB m16, imm16", (MOV(esi, esi), SBB(word[r15+rsi*1+16], 32000))))
instruction_list.append(("SBB m16, r16", (MOV(esi, esi), SBB(word[r15+rsi*1+16], cx))))
instruction_list.append(("SBB m32, imm8", (MOV(esi, esi), SBB(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SBB m32, imm32", (MOV(esi, esi), SBB(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("SBB m32, r32", (MOV(esi, esi), SBB(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("SBB m64, imm8", (MOV(esi, esi), SBB(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SBB m64, imm32", (MOV(esi, esi), SBB(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("SBB m64, r64", (MOV(esi, esi), SBB(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("ADCX r32, r32", (ADCX(ebx, ebx),)))
instruction_list.append(("ADCX r32, m32", (MOV(esi, esi), ADCX(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("ADCX r64, r64", (ADCX(rdi, rdi),)))
instruction_list.append(("ADCX r64, m64", (MOV(esi, esi), ADCX(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("ADOX r32, r32", (ADOX(ebx, ebx),)))
instruction_list.append(("ADOX r32, m32", (MOV(esi, esi), ADOX(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("ADOX r64, r64", (ADOX(rdi, rdi),)))
instruction_list.append(("ADOX r64, m64", (MOV(esi, esi), ADOX(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("AND al, imm8", (AND(al, 2),)))
instruction_list.append(("AND r8, imm8", (AND(dl, 2),)))
instruction_list.append(("AND r8, r8", (AND(dl, dl),)))
instruction_list.append(("AND r8, m8", (MOV(esi, esi), AND(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("AND ax, imm16", (AND(ax, 32000),)))
instruction_list.append(("AND r16, imm8", (AND(cx, 2),)))
instruction_list.append(("AND r16, imm16", (AND(cx, 32000),)))
instruction_list.append(("AND r16, r16", (AND(cx, cx),)))
instruction_list.append(("AND r16, m16", (MOV(esi, esi), AND(cx, word[r15+rsi*1+16]))))
instruction_list.append(("AND eax, imm32", (AND(eax, 0x10000000),)))
instruction_list.append(("AND r32, imm8", (AND(ebx, 2),)))
instruction_list.append(("AND r32, imm32", (AND(ebx, 0x10000000),)))
instruction_list.append(("AND r32, r32", (AND(ebx, ebx),)))
instruction_list.append(("AND r32, m32", (MOV(esi, esi), AND(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("AND rax, imm32", (AND(rax, 0x10000000),)))
instruction_list.append(("AND r64, imm8", (AND(rdi, 2),)))
instruction_list.append(("AND r64, imm32", (AND(rdi, 0x10000000),)))
instruction_list.append(("AND r64, r64", (AND(rdi, rdi),)))
instruction_list.append(("AND r64, m64", (MOV(esi, esi), AND(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("AND m8, imm8", (MOV(esi, esi), AND(byte[r15+rsi*1+8], 2))))
instruction_list.append(("AND m8, r8", (MOV(esi, esi), AND(byte[r15+rsi*1+8], dl))))
instruction_list.append(("AND m16, imm8", (MOV(esi, esi), AND(word[r15+rsi*1+16], 2))))
instruction_list.append(("AND m16, imm16", (MOV(esi, esi), AND(word[r15+rsi*1+16], 32000))))
instruction_list.append(("AND m16, r16", (MOV(esi, esi), AND(word[r15+rsi*1+16], cx))))
instruction_list.append(("AND m32, imm8", (MOV(esi, esi), AND(dword[r15+rsi*1+32], 2))))
instruction_list.append(("AND m32, imm32", (MOV(esi, esi), AND(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("AND m32, r32", (MOV(esi, esi), AND(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("AND m64, imm8", (MOV(esi, esi), AND(qword[r15+rsi*1+64], 2))))
instruction_list.append(("AND m64, imm32", (MOV(esi, esi), AND(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("AND m64, r64", (MOV(esi, esi), AND(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("OR al, imm8", (OR(al, 2),)))
instruction_list.append(("OR r8, imm8", (OR(dl, 2),)))
instruction_list.append(("OR r8, r8", (OR(dl, dl),)))
instruction_list.append(("OR r8, m8", (MOV(esi, esi), OR(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("OR ax, imm16", (OR(ax, 32000),)))
instruction_list.append(("OR r16, imm8", (OR(cx, 2),)))
instruction_list.append(("OR r16, imm16", (OR(cx, 32000),)))
instruction_list.append(("OR r16, r16", (OR(cx, cx),)))
instruction_list.append(("OR r16, m16", (MOV(esi, esi), OR(cx, word[r15+rsi*1+16]))))
instruction_list.append(("OR eax, imm32", (OR(eax, 0x10000000),)))
instruction_list.append(("OR r32, imm8", (OR(ebx, 2),)))
instruction_list.append(("OR r32, imm32", (OR(ebx, 0x10000000),)))
instruction_list.append(("OR r32, r32", (OR(ebx, ebx),)))
instruction_list.append(("OR r32, m32", (MOV(esi, esi), OR(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("OR rax, imm32", (OR(rax, 0x10000000),)))
instruction_list.append(("OR r64, imm8", (OR(rdi, 2),)))
instruction_list.append(("OR r64, imm32", (OR(rdi, 0x10000000),)))
instruction_list.append(("OR r64, r64", (OR(rdi, rdi),)))
instruction_list.append(("OR r64, m64", (MOV(esi, esi), OR(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("OR m8, imm8", (MOV(esi, esi), OR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("OR m8, r8", (MOV(esi, esi), OR(byte[r15+rsi*1+8], dl))))
instruction_list.append(("OR m16, imm8", (MOV(esi, esi), OR(word[r15+rsi*1+16], 2))))
instruction_list.append(("OR m16, imm16", (MOV(esi, esi), OR(word[r15+rsi*1+16], 32000))))
instruction_list.append(("OR m16, r16", (MOV(esi, esi), OR(word[r15+rsi*1+16], cx))))
instruction_list.append(("OR m32, imm8", (MOV(esi, esi), OR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("OR m32, imm32", (MOV(esi, esi), OR(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("OR m32, r32", (MOV(esi, esi), OR(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("OR m64, imm8", (MOV(esi, esi), OR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("OR m64, imm32", (MOV(esi, esi), OR(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("OR m64, r64", (MOV(esi, esi), OR(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("XOR al, imm8", (XOR(al, 2),)))
instruction_list.append(("XOR r8, imm8", (XOR(dl, 2),)))
instruction_list.append(("XOR r8, r8", (XOR(dl, dl),)))
instruction_list.append(("XOR r8, m8", (MOV(esi, esi), XOR(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("XOR ax, imm16", (XOR(ax, 32000),)))
instruction_list.append(("XOR r16, imm8", (XOR(cx, 2),)))
instruction_list.append(("XOR r16, imm16", (XOR(cx, 32000),)))
instruction_list.append(("XOR r16, r16", (XOR(cx, cx),)))
instruction_list.append(("XOR r16, m16", (MOV(esi, esi), XOR(cx, word[r15+rsi*1+16]))))
instruction_list.append(("XOR eax, imm32", (XOR(eax, 0x10000000),)))
instruction_list.append(("XOR r32, imm8", (XOR(ebx, 2),)))
instruction_list.append(("XOR r32, imm32", (XOR(ebx, 0x10000000),)))
instruction_list.append(("XOR r32, r32", (XOR(ebx, ebx),)))
instruction_list.append(("XOR r32, m32", (MOV(esi, esi), XOR(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("XOR rax, imm32", (XOR(rax, 0x10000000),)))
instruction_list.append(("XOR r64, imm8", (XOR(rdi, 2),)))
instruction_list.append(("XOR r64, imm32", (XOR(rdi, 0x10000000),)))
instruction_list.append(("XOR r64, r64", (XOR(rdi, rdi),)))
instruction_list.append(("XOR r64, m64", (MOV(esi, esi), XOR(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("XOR m8, imm8", (MOV(esi, esi), XOR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("XOR m8, r8", (MOV(esi, esi), XOR(byte[r15+rsi*1+8], dl))))
instruction_list.append(("XOR m16, imm8", (MOV(esi, esi), XOR(word[r15+rsi*1+16], 2))))
instruction_list.append(("XOR m16, imm16", (MOV(esi, esi), XOR(word[r15+rsi*1+16], 32000))))
instruction_list.append(("XOR m16, r16", (MOV(esi, esi), XOR(word[r15+rsi*1+16], cx))))
instruction_list.append(("XOR m32, imm8", (MOV(esi, esi), XOR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("XOR m32, imm32", (MOV(esi, esi), XOR(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("XOR m32, r32", (MOV(esi, esi), XOR(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("XOR m64, imm8", (MOV(esi, esi), XOR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("XOR m64, imm32", (MOV(esi, esi), XOR(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("XOR m64, r64", (MOV(esi, esi), XOR(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("ANDN r32, r32, r32", (ANDN(ebx, ebx, ebx),)))
instruction_list.append(("ANDN r32, r32, m32", (MOV(esi, esi), ANDN(ebx, ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("ANDN r64, r64, r64", (ANDN(rdi, rdi, rdi),)))
instruction_list.append(("ANDN r64, r64, m64", (MOV(esi, esi), ANDN(rdi, rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("NOT r8", (NOT(dl),)))
instruction_list.append(("NOT r16", (NOT(cx),)))
instruction_list.append(("NOT r32", (NOT(ebx),)))
instruction_list.append(("NOT r64", (NOT(rdi),)))
instruction_list.append(("NOT m8", (MOV(esi, esi), NOT(byte[r15+rsi*1+8]))))
instruction_list.append(("NOT m16", (MOV(esi, esi), NOT(word[r15+rsi*1+16]))))
instruction_list.append(("NOT m32", (MOV(esi, esi), NOT(dword[r15+rsi*1+32]))))
instruction_list.append(("NOT m64", (MOV(esi, esi), NOT(qword[r15+rsi*1+64]))))

instruction_list.append(("NEG r8", (NEG(dl),)))
instruction_list.append(("NEG r16", (NEG(cx),)))
instruction_list.append(("NEG r32", (NEG(ebx),)))
instruction_list.append(("NEG r64", (NEG(rdi),)))
instruction_list.append(("NEG m8", (MOV(esi, esi), NEG(byte[r15+rsi*1+8]))))
instruction_list.append(("NEG m16", (MOV(esi, esi), NEG(word[r15+rsi*1+16]))))
instruction_list.append(("NEG m32", (MOV(esi, esi), NEG(dword[r15+rsi*1+32]))))
instruction_list.append(("NEG m64", (MOV(esi, esi), NEG(qword[r15+rsi*1+64]))))

instruction_list.append(("INC r8", (INC(dl),)))
instruction_list.append(("INC r16", (INC(cx),)))
instruction_list.append(("INC r32", (INC(ebx),)))
instruction_list.append(("INC r64", (INC(rdi),)))
instruction_list.append(("INC m8", (MOV(esi, esi), INC(byte[r15+rsi*1+8]))))
instruction_list.append(("INC m16", (MOV(esi, esi), INC(word[r15+rsi*1+16]))))
instruction_list.append(("INC m32", (MOV(esi, esi), INC(dword[r15+rsi*1+32]))))
instruction_list.append(("INC m64", (MOV(esi, esi), INC(qword[r15+rsi*1+64]))))

instruction_list.append(("DEC r8", (DEC(dl),)))
instruction_list.append(("DEC r16", (DEC(cx),)))
instruction_list.append(("DEC r32", (DEC(ebx),)))
instruction_list.append(("DEC r64", (DEC(rdi),)))
instruction_list.append(("DEC m8", (MOV(esi, esi), DEC(byte[r15+rsi*1+8]))))
instruction_list.append(("DEC m16", (MOV(esi, esi), DEC(word[r15+rsi*1+16]))))
instruction_list.append(("DEC m32", (MOV(esi, esi), DEC(dword[r15+rsi*1+32]))))
instruction_list.append(("DEC m64", (MOV(esi, esi), DEC(qword[r15+rsi*1+64]))))

instruction_list.append(("TEST al, imm8", (TEST(al, 2),)))
instruction_list.append(("TEST r8, imm8", (TEST(dl, 2),)))
instruction_list.append(("TEST r8, r8", (TEST(dl, dl),)))
instruction_list.append(("TEST ax, imm16", (TEST(ax, 32000),)))
instruction_list.append(("TEST r16, imm16", (TEST(cx, 32000),)))
instruction_list.append(("TEST r16, r16", (TEST(cx, cx),)))
instruction_list.append(("TEST eax, imm32", (TEST(eax, 0x10000000),)))
instruction_list.append(("TEST r32, imm32", (TEST(ebx, 0x10000000),)))
instruction_list.append(("TEST r32, r32", (TEST(ebx, ebx),)))
instruction_list.append(("TEST rax, imm32", (TEST(rax, 0x10000000),)))
instruction_list.append(("TEST r64, imm32", (TEST(rdi, 0x10000000),)))
instruction_list.append(("TEST r64, r64", (TEST(rdi, rdi),)))
instruction_list.append(("TEST m8, imm8", (MOV(esi, esi), TEST(byte[r15+rsi*1+8], 2))))
instruction_list.append(("TEST m8, r8", (MOV(esi, esi), TEST(byte[r15+rsi*1+8], dl))))
instruction_list.append(("TEST m16, imm16", (MOV(esi, esi), TEST(word[r15+rsi*1+16], 32000))))
instruction_list.append(("TEST m16, r16", (MOV(esi, esi), TEST(word[r15+rsi*1+16], cx))))
instruction_list.append(("TEST m32, imm32", (MOV(esi, esi), TEST(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("TEST m32, r32", (MOV(esi, esi), TEST(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("TEST m64, imm32", (MOV(esi, esi), TEST(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("TEST m64, r64", (MOV(esi, esi), TEST(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("CMP al, imm8", (CMP(al, 2),)))
instruction_list.append(("CMP r8, imm8", (CMP(dl, 2),)))
instruction_list.append(("CMP r8, r8", (CMP(dl, dl),)))
instruction_list.append(("CMP r8, m8", (MOV(esi, esi), CMP(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("CMP ax, imm16", (CMP(ax, 32000),)))
instruction_list.append(("CMP r16, imm8", (CMP(cx, 2),)))
instruction_list.append(("CMP r16, imm16", (CMP(cx, 32000),)))
instruction_list.append(("CMP r16, r16", (CMP(cx, cx),)))
instruction_list.append(("CMP r16, m16", (MOV(esi, esi), CMP(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMP eax, imm32", (CMP(eax, 0x10000000),)))
instruction_list.append(("CMP r32, imm8", (CMP(ebx, 2),)))
instruction_list.append(("CMP r32, imm32", (CMP(ebx, 0x10000000),)))
instruction_list.append(("CMP r32, r32", (CMP(ebx, ebx),)))
instruction_list.append(("CMP r32, m32", (MOV(esi, esi), CMP(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMP rax, imm32", (CMP(rax, 0x10000000),)))
instruction_list.append(("CMP r64, imm8", (CMP(rdi, 2),)))
instruction_list.append(("CMP r64, imm32", (CMP(rdi, 0x10000000),)))
instruction_list.append(("CMP r64, r64", (CMP(rdi, rdi),)))
instruction_list.append(("CMP r64, m64", (MOV(esi, esi), CMP(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("CMP m8, imm8", (MOV(esi, esi), CMP(byte[r15+rsi*1+8], 2))))
instruction_list.append(("CMP m8, r8", (MOV(esi, esi), CMP(byte[r15+rsi*1+8], dl))))
instruction_list.append(("CMP m16, imm8", (MOV(esi, esi), CMP(word[r15+rsi*1+16], 2))))
instruction_list.append(("CMP m16, imm16", (MOV(esi, esi), CMP(word[r15+rsi*1+16], 32000))))
instruction_list.append(("CMP m16, r16", (MOV(esi, esi), CMP(word[r15+rsi*1+16], cx))))
instruction_list.append(("CMP m32, imm8", (MOV(esi, esi), CMP(dword[r15+rsi*1+32], 2))))
instruction_list.append(("CMP m32, imm32", (MOV(esi, esi), CMP(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("CMP m32, r32", (MOV(esi, esi), CMP(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("CMP m64, imm8", (MOV(esi, esi), CMP(qword[r15+rsi*1+64], 2))))
instruction_list.append(("CMP m64, imm32", (MOV(esi, esi), CMP(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("CMP m64, r64", (MOV(esi, esi), CMP(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("MOV r8, imm8", (MOV(dl, 2),)))
instruction_list.append(("MOV r8, r8", (MOV(dl, dl),)))
instruction_list.append(("MOV r8, m8", (MOV(esi, esi), MOV(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("MOV r16, imm16", (MOV(cx, 32000),)))
instruction_list.append(("MOV r16, r16", (MOV(cx, cx),)))
instruction_list.append(("MOV r16, m16", (MOV(esi, esi), MOV(cx, word[r15+rsi*1+16]))))
instruction_list.append(("MOV r32, imm32", (MOV(ebx, 0x10000000),)))
instruction_list.append(("MOV r32, r32", (MOV(ebx, ebx),)))
instruction_list.append(("MOV r32, m32", (MOV(esi, esi), MOV(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("MOV r64, imm32", (MOV(rdi, 0x10000000),)))
instruction_list.append(("MOV r64, imm64", (MOV(rdi, 0x100000000),)))
instruction_list.append(("MOV r64, r64", (MOV(rdi, rdi),)))
instruction_list.append(("MOV r64, m64", (MOV(esi, esi), MOV(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("MOV m8, imm8", (MOV(esi, esi), MOV(byte[r15+rsi*1+8], 2))))
instruction_list.append(("MOV m8, r8", (MOV(esi, esi), MOV(byte[r15+rsi*1+8], dl))))
instruction_list.append(("MOV m16, imm16", (MOV(esi, esi), MOV(word[r15+rsi*1+16], 32000))))
instruction_list.append(("MOV m16, r16", (MOV(esi, esi), MOV(word[r15+rsi*1+16], cx))))
instruction_list.append(("MOV m32, imm32", (MOV(esi, esi), MOV(dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("MOV m32, r32", (MOV(esi, esi), MOV(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("MOV m64, imm32", (MOV(esi, esi), MOV(qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("MOV m64, r64", (MOV(esi, esi), MOV(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("MOVZX r16, r8", (MOVZX(cx, dl),)))
instruction_list.append(("MOVZX r16, m8", (MOV(esi, esi), MOVZX(cx, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVZX r32, r8", (MOVZX(ebx, dl),)))
instruction_list.append(("MOVZX r32, r16", (MOVZX(ebx, cx),)))
instruction_list.append(("MOVZX r32, m8", (MOV(esi, esi), MOVZX(ebx, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVZX r32, m16", (MOV(esi, esi), MOVZX(ebx, word[r15+rsi*1+16]))))
instruction_list.append(("MOVZX r64, r8", (MOVZX(rdi, dl),)))
instruction_list.append(("MOVZX r64, r16", (MOVZX(rdi, cx),)))
instruction_list.append(("MOVZX r64, m8", (MOV(esi, esi), MOVZX(rdi, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVZX r64, m16", (MOV(esi, esi), MOVZX(rdi, word[r15+rsi*1+16]))))

instruction_list.append(("MOVSX r16, r8", (MOVSX(cx, dl),)))
instruction_list.append(("MOVSX r16, m8", (MOV(esi, esi), MOVSX(cx, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVSX r32, r8", (MOVSX(ebx, dl),)))
instruction_list.append(("MOVSX r32, r16", (MOVSX(ebx, cx),)))
instruction_list.append(("MOVSX r32, m8", (MOV(esi, esi), MOVSX(ebx, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVSX r32, m16", (MOV(esi, esi), MOVSX(ebx, word[r15+rsi*1+16]))))
instruction_list.append(("MOVSX r64, r8", (MOVSX(rdi, dl),)))
instruction_list.append(("MOVSX r64, r16", (MOVSX(rdi, cx),)))
instruction_list.append(("MOVSX r64, m8", (MOV(esi, esi), MOVSX(rdi, byte[r15+rsi*1+8]))))
instruction_list.append(("MOVSX r64, m16", (MOV(esi, esi), MOVSX(rdi, word[r15+rsi*1+16]))))

instruction_list.append(("MOVSXD r64, r32", (MOVSXD(rdi, ebx),)))
instruction_list.append(("MOVSXD r64, m32", (MOV(esi, esi), MOVSXD(rdi, dword[r15+rsi*1+32]))))

instruction_list.append(("MOVBE r16, m16", (MOV(esi, esi), MOVBE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("MOVBE r32, m32", (MOV(esi, esi), MOVBE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("MOVBE r64, m64", (MOV(esi, esi), MOVBE(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVBE m16, r16", (MOV(esi, esi), MOVBE(word[r15+rsi*1+16], cx))))
instruction_list.append(("MOVBE m32, r32", (MOV(esi, esi), MOVBE(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("MOVBE m64, r64", (MOV(esi, esi), MOVBE(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("MOVNTI m32, r32", (MOV(esi, esi), MOVNTI(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("MOVNTI m64, r64", (MOV(esi, esi), MOVNTI(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("BT r16, imm8", (BT(cx, 2),)))
instruction_list.append(("BT r16, r16", (BT(cx, cx),)))
instruction_list.append(("BT r32, imm8", (BT(ebx, 2),)))
instruction_list.append(("BT r32, r32", (BT(ebx, ebx),)))
instruction_list.append(("BT r64, imm8", (BT(rdi, 2),)))
instruction_list.append(("BT r64, r64", (BT(rdi, rdi),)))
instruction_list.append(("BT m16, imm8", (MOV(esi, esi), BT(word[r15+rsi*1+16], 2))))
instruction_list.append(("BT m16, r16", (MOV(esi, esi), BT(word[r15+rsi*1+16], cx))))
instruction_list.append(("BT m32, imm8", (MOV(esi, esi), BT(dword[r15+rsi*1+32], 2))))
instruction_list.append(("BT m32, r32", (MOV(esi, esi), BT(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BT m64, imm8", (MOV(esi, esi), BT(qword[r15+rsi*1+64], 2))))
instruction_list.append(("BT m64, r64", (MOV(esi, esi), BT(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("BTS r16, imm8", (BTS(cx, 2),)))
instruction_list.append(("BTS r16, r16", (BTS(cx, cx),)))
instruction_list.append(("BTS r32, imm8", (BTS(ebx, 2),)))
instruction_list.append(("BTS r32, r32", (BTS(ebx, ebx),)))
instruction_list.append(("BTS r64, imm8", (BTS(rdi, 2),)))
instruction_list.append(("BTS r64, r64", (BTS(rdi, rdi),)))
instruction_list.append(("BTS m16, imm8", (MOV(esi, esi), BTS(word[r15+rsi*1+16], 2))))
instruction_list.append(("BTS m16, r16", (MOV(esi, esi), BTS(word[r15+rsi*1+16], cx))))
instruction_list.append(("BTS m32, imm8", (MOV(esi, esi), BTS(dword[r15+rsi*1+32], 2))))
instruction_list.append(("BTS m32, r32", (MOV(esi, esi), BTS(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BTS m64, imm8", (MOV(esi, esi), BTS(qword[r15+rsi*1+64], 2))))
instruction_list.append(("BTS m64, r64", (MOV(esi, esi), BTS(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("BTR r16, imm8", (BTR(cx, 2),)))
instruction_list.append(("BTR r16, r16", (BTR(cx, cx),)))
instruction_list.append(("BTR r32, imm8", (BTR(ebx, 2),)))
instruction_list.append(("BTR r32, r32", (BTR(ebx, ebx),)))
instruction_list.append(("BTR r64, imm8", (BTR(rdi, 2),)))
instruction_list.append(("BTR r64, r64", (BTR(rdi, rdi),)))
instruction_list.append(("BTR m16, imm8", (MOV(esi, esi), BTR(word[r15+rsi*1+16], 2))))
instruction_list.append(("BTR m16, r16", (MOV(esi, esi), BTR(word[r15+rsi*1+16], cx))))
instruction_list.append(("BTR m32, imm8", (MOV(esi, esi), BTR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("BTR m32, r32", (MOV(esi, esi), BTR(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BTR m64, imm8", (MOV(esi, esi), BTR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("BTR m64, r64", (MOV(esi, esi), BTR(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("BTC r16, imm8", (BTC(cx, 2),)))
instruction_list.append(("BTC r16, r16", (BTC(cx, cx),)))
instruction_list.append(("BTC r32, imm8", (BTC(ebx, 2),)))
instruction_list.append(("BTC r32, r32", (BTC(ebx, ebx),)))
instruction_list.append(("BTC r64, imm8", (BTC(rdi, 2),)))
instruction_list.append(("BTC r64, r64", (BTC(rdi, rdi),)))
instruction_list.append(("BTC m16, imm8", (MOV(esi, esi), BTC(word[r15+rsi*1+16], 2))))
instruction_list.append(("BTC m16, r16", (MOV(esi, esi), BTC(word[r15+rsi*1+16], cx))))
instruction_list.append(("BTC m32, imm8", (MOV(esi, esi), BTC(dword[r15+rsi*1+32], 2))))
instruction_list.append(("BTC m32, r32", (MOV(esi, esi), BTC(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BTC m64, imm8", (MOV(esi, esi), BTC(qword[r15+rsi*1+64], 2))))
instruction_list.append(("BTC m64, r64", (MOV(esi, esi), BTC(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("POPCNT r16, r16", (POPCNT(cx, cx),)))
instruction_list.append(("POPCNT r16, m16", (MOV(esi, esi), POPCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("POPCNT r32, r32", (POPCNT(ebx, ebx),)))
instruction_list.append(("POPCNT r32, m32", (MOV(esi, esi), POPCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("POPCNT r64, r64", (POPCNT(rdi, rdi),)))
instruction_list.append(("POPCNT r64, m64", (MOV(esi, esi), POPCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BSWAP r32", (BSWAP(ebx),)))
instruction_list.append(("BSWAP r64", (BSWAP(rdi),)))

instruction_list.append(("BSF r16, r16", (BSF(cx, cx),)))
instruction_list.append(("BSF r16, m16", (MOV(esi, esi), BSF(cx, word[r15+rsi*1+16]))))
instruction_list.append(("BSF r32, r32", (BSF(ebx, ebx),)))
instruction_list.append(("BSF r32, m32", (MOV(esi, esi), BSF(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BSF r64, r64", (BSF(rdi, rdi),)))
instruction_list.append(("BSF r64, m64", (MOV(esi, esi), BSF(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BSR r16, r16", (BSR(cx, cx),)))
instruction_list.append(("BSR r16, m16", (MOV(esi, esi), BSR(cx, word[r15+rsi*1+16]))))
instruction_list.append(("BSR r32, r32", (BSR(ebx, ebx),)))
instruction_list.append(("BSR r32, m32", (MOV(esi, esi), BSR(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BSR r64, r64", (BSR(rdi, rdi),)))
instruction_list.append(("BSR r64, m64", (MOV(esi, esi), BSR(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("LZCNT r16, r16", (LZCNT(cx, cx),)))
instruction_list.append(("LZCNT r16, m16", (MOV(esi, esi), LZCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("LZCNT r32, r32", (LZCNT(ebx, ebx),)))
instruction_list.append(("LZCNT r32, m32", (MOV(esi, esi), LZCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("LZCNT r64, r64", (LZCNT(rdi, rdi),)))
instruction_list.append(("LZCNT r64, m64", (MOV(esi, esi), LZCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("TZCNT r16, r16", (TZCNT(cx, cx),)))
instruction_list.append(("TZCNT r16, m16", (MOV(esi, esi), TZCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("TZCNT r32, r32", (TZCNT(ebx, ebx),)))
instruction_list.append(("TZCNT r32, m32", (MOV(esi, esi), TZCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("TZCNT r64, r64", (TZCNT(rdi, rdi),)))
instruction_list.append(("TZCNT r64, m64", (MOV(esi, esi), TZCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("SHR r8, 1", (SHR(dl, 1),)))
instruction_list.append(("SHR r8, imm8", (SHR(dl, 2),)))
instruction_list.append(("SHR r8, cl", (SHR(dl, cl),)))
instruction_list.append(("SHR r16, 1", (SHR(cx, 1),)))
instruction_list.append(("SHR r16, imm8", (SHR(cx, 2),)))
instruction_list.append(("SHR r16, cl", (SHR(cx, cl),)))
instruction_list.append(("SHR r32, 1", (SHR(ebx, 1),)))
instruction_list.append(("SHR r32, imm8", (SHR(ebx, 2),)))
instruction_list.append(("SHR r32, cl", (SHR(ebx, cl),)))
instruction_list.append(("SHR r64, 1", (SHR(rdi, 1),)))
instruction_list.append(("SHR r64, imm8", (SHR(rdi, 2),)))
instruction_list.append(("SHR r64, cl", (SHR(rdi, cl),)))
instruction_list.append(("SHR m8, 1", (MOV(esi, esi), SHR(byte[r15+rsi*1+8], 1))))
instruction_list.append(("SHR m8, imm8", (MOV(esi, esi), SHR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SHR m8, cl", (MOV(esi, esi), SHR(byte[r15+rsi*1+8], cl))))
instruction_list.append(("SHR m16, 1", (MOV(esi, esi), SHR(word[r15+rsi*1+16], 1))))
instruction_list.append(("SHR m16, imm8", (MOV(esi, esi), SHR(word[r15+rsi*1+16], 2))))
instruction_list.append(("SHR m16, cl", (MOV(esi, esi), SHR(word[r15+rsi*1+16], cl))))
instruction_list.append(("SHR m32, 1", (MOV(esi, esi), SHR(dword[r15+rsi*1+32], 1))))
instruction_list.append(("SHR m32, imm8", (MOV(esi, esi), SHR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SHR m32, cl", (MOV(esi, esi), SHR(dword[r15+rsi*1+32], cl))))
instruction_list.append(("SHR m64, 1", (MOV(esi, esi), SHR(qword[r15+rsi*1+64], 1))))
instruction_list.append(("SHR m64, imm8", (MOV(esi, esi), SHR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SHR m64, cl", (MOV(esi, esi), SHR(qword[r15+rsi*1+64], cl))))

instruction_list.append(("SAR r8, 1", (SAR(dl, 1),)))
instruction_list.append(("SAR r8, imm8", (SAR(dl, 2),)))
instruction_list.append(("SAR r8, cl", (SAR(dl, cl),)))
instruction_list.append(("SAR r16, 1", (SAR(cx, 1),)))
instruction_list.append(("SAR r16, imm8", (SAR(cx, 2),)))
instruction_list.append(("SAR r16, cl", (SAR(cx, cl),)))
instruction_list.append(("SAR r32, 1", (SAR(ebx, 1),)))
instruction_list.append(("SAR r32, imm8", (SAR(ebx, 2),)))
instruction_list.append(("SAR r32, cl", (SAR(ebx, cl),)))
instruction_list.append(("SAR r64, 1", (SAR(rdi, 1),)))
instruction_list.append(("SAR r64, imm8", (SAR(rdi, 2),)))
instruction_list.append(("SAR r64, cl", (SAR(rdi, cl),)))
instruction_list.append(("SAR m8, 1", (MOV(esi, esi), SAR(byte[r15+rsi*1+8], 1))))
instruction_list.append(("SAR m8, imm8", (MOV(esi, esi), SAR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SAR m8, cl", (MOV(esi, esi), SAR(byte[r15+rsi*1+8], cl))))
instruction_list.append(("SAR m16, 1", (MOV(esi, esi), SAR(word[r15+rsi*1+16], 1))))
instruction_list.append(("SAR m16, imm8", (MOV(esi, esi), SAR(word[r15+rsi*1+16], 2))))
instruction_list.append(("SAR m16, cl", (MOV(esi, esi), SAR(word[r15+rsi*1+16], cl))))
instruction_list.append(("SAR m32, 1", (MOV(esi, esi), SAR(dword[r15+rsi*1+32], 1))))
instruction_list.append(("SAR m32, imm8", (MOV(esi, esi), SAR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SAR m32, cl", (MOV(esi, esi), SAR(dword[r15+rsi*1+32], cl))))
instruction_list.append(("SAR m64, 1", (MOV(esi, esi), SAR(qword[r15+rsi*1+64], 1))))
instruction_list.append(("SAR m64, imm8", (MOV(esi, esi), SAR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SAR m64, cl", (MOV(esi, esi), SAR(qword[r15+rsi*1+64], cl))))

instruction_list.append(("SHL r8, 1", (SHL(dl, 1),)))
instruction_list.append(("SHL r8, imm8", (SHL(dl, 2),)))
instruction_list.append(("SHL r8, cl", (SHL(dl, cl),)))
instruction_list.append(("SHL r16, 1", (SHL(cx, 1),)))
instruction_list.append(("SHL r16, imm8", (SHL(cx, 2),)))
instruction_list.append(("SHL r16, cl", (SHL(cx, cl),)))
instruction_list.append(("SHL r32, 1", (SHL(ebx, 1),)))
instruction_list.append(("SHL r32, imm8", (SHL(ebx, 2),)))
instruction_list.append(("SHL r32, cl", (SHL(ebx, cl),)))
instruction_list.append(("SHL r64, 1", (SHL(rdi, 1),)))
instruction_list.append(("SHL r64, imm8", (SHL(rdi, 2),)))
instruction_list.append(("SHL r64, cl", (SHL(rdi, cl),)))
instruction_list.append(("SHL m8, 1", (MOV(esi, esi), SHL(byte[r15+rsi*1+8], 1))))
instruction_list.append(("SHL m8, imm8", (MOV(esi, esi), SHL(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SHL m8, cl", (MOV(esi, esi), SHL(byte[r15+rsi*1+8], cl))))
instruction_list.append(("SHL m16, 1", (MOV(esi, esi), SHL(word[r15+rsi*1+16], 1))))
instruction_list.append(("SHL m16, imm8", (MOV(esi, esi), SHL(word[r15+rsi*1+16], 2))))
instruction_list.append(("SHL m16, cl", (MOV(esi, esi), SHL(word[r15+rsi*1+16], cl))))
instruction_list.append(("SHL m32, 1", (MOV(esi, esi), SHL(dword[r15+rsi*1+32], 1))))
instruction_list.append(("SHL m32, imm8", (MOV(esi, esi), SHL(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SHL m32, cl", (MOV(esi, esi), SHL(dword[r15+rsi*1+32], cl))))
instruction_list.append(("SHL m64, 1", (MOV(esi, esi), SHL(qword[r15+rsi*1+64], 1))))
instruction_list.append(("SHL m64, imm8", (MOV(esi, esi), SHL(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SHL m64, cl", (MOV(esi, esi), SHL(qword[r15+rsi*1+64], cl))))

instruction_list.append(("SAL r8, 1", (SAL(dl, 1),)))
instruction_list.append(("SAL r8, imm8", (SAL(dl, 2),)))
instruction_list.append(("SAL r8, cl", (SAL(dl, cl),)))
instruction_list.append(("SAL r16, 1", (SAL(cx, 1),)))
instruction_list.append(("SAL r16, imm8", (SAL(cx, 2),)))
instruction_list.append(("SAL r16, cl", (SAL(cx, cl),)))
instruction_list.append(("SAL r32, 1", (SAL(ebx, 1),)))
instruction_list.append(("SAL r32, imm8", (SAL(ebx, 2),)))
instruction_list.append(("SAL r32, cl", (SAL(ebx, cl),)))
instruction_list.append(("SAL r64, 1", (SAL(rdi, 1),)))
instruction_list.append(("SAL r64, imm8", (SAL(rdi, 2),)))
instruction_list.append(("SAL r64, cl", (SAL(rdi, cl),)))
instruction_list.append(("SAL m8, 1", (MOV(esi, esi), SAL(byte[r15+rsi*1+8], 1))))
instruction_list.append(("SAL m8, imm8", (MOV(esi, esi), SAL(byte[r15+rsi*1+8], 2))))
instruction_list.append(("SAL m8, cl", (MOV(esi, esi), SAL(byte[r15+rsi*1+8], cl))))
instruction_list.append(("SAL m16, 1", (MOV(esi, esi), SAL(word[r15+rsi*1+16], 1))))
instruction_list.append(("SAL m16, imm8", (MOV(esi, esi), SAL(word[r15+rsi*1+16], 2))))
instruction_list.append(("SAL m16, cl", (MOV(esi, esi), SAL(word[r15+rsi*1+16], cl))))
instruction_list.append(("SAL m32, 1", (MOV(esi, esi), SAL(dword[r15+rsi*1+32], 1))))
instruction_list.append(("SAL m32, imm8", (MOV(esi, esi), SAL(dword[r15+rsi*1+32], 2))))
instruction_list.append(("SAL m32, cl", (MOV(esi, esi), SAL(dword[r15+rsi*1+32], cl))))
instruction_list.append(("SAL m64, 1", (MOV(esi, esi), SAL(qword[r15+rsi*1+64], 1))))
instruction_list.append(("SAL m64, imm8", (MOV(esi, esi), SAL(qword[r15+rsi*1+64], 2))))
instruction_list.append(("SAL m64, cl", (MOV(esi, esi), SAL(qword[r15+rsi*1+64], cl))))

instruction_list.append(("SHRX r32, r32, r32", (SHRX(ebx, ebx, ebx),)))
instruction_list.append(("SHRX r32, m32, r32", (MOV(esi, esi), SHRX(ebx, dword[r15+rsi*1+32], ebx))))
instruction_list.append(("SHRX r64, r64, r64", (SHRX(rdi, rdi, rdi),)))
instruction_list.append(("SHRX r64, m64, r64", (MOV(esi, esi), SHRX(rdi, qword[r15+rsi*1+64], rdi))))

instruction_list.append(("SARX r32, r32, r32", (SARX(ebx, ebx, ebx),)))
instruction_list.append(("SARX r32, m32, r32", (MOV(esi, esi), SARX(ebx, dword[r15+rsi*1+32], ebx))))
instruction_list.append(("SARX r64, r64, r64", (SARX(rdi, rdi, rdi),)))
instruction_list.append(("SARX r64, m64, r64", (MOV(esi, esi), SARX(rdi, qword[r15+rsi*1+64], rdi))))

instruction_list.append(("SHLX r32, r32, r32", (SHLX(ebx, ebx, ebx),)))
instruction_list.append(("SHLX r32, m32, r32", (MOV(esi, esi), SHLX(ebx, dword[r15+rsi*1+32], ebx))))
instruction_list.append(("SHLX r64, r64, r64", (SHLX(rdi, rdi, rdi),)))
instruction_list.append(("SHLX r64, m64, r64", (MOV(esi, esi), SHLX(rdi, qword[r15+rsi*1+64], rdi))))

instruction_list.append(("SHRD r16, r16, imm8", (SHRD(cx, cx, 2),)))
instruction_list.append(("SHRD r16, r16, cl", (SHRD(cx, cx, cl),)))
instruction_list.append(("SHRD r32, r32, imm8", (SHRD(ebx, ebx, 2),)))
instruction_list.append(("SHRD r32, r32, cl", (SHRD(ebx, ebx, cl),)))
instruction_list.append(("SHRD r64, r64, imm8", (SHRD(rdi, rdi, 2),)))
instruction_list.append(("SHRD r64, r64, cl", (SHRD(rdi, rdi, cl),)))
instruction_list.append(("SHRD m16, r16, imm8", (MOV(esi, esi), SHRD(word[r15+rsi*1+16], cx, 2))))
instruction_list.append(("SHRD m16, r16, cl", (MOV(esi, esi), SHRD(word[r15+rsi*1+16], cx, cl))))
instruction_list.append(("SHRD m32, r32, imm8", (MOV(esi, esi), SHRD(dword[r15+rsi*1+32], ebx, 2))))
instruction_list.append(("SHRD m32, r32, cl", (MOV(esi, esi), SHRD(dword[r15+rsi*1+32], ebx, cl))))
instruction_list.append(("SHRD m64, r64, imm8", (MOV(esi, esi), SHRD(qword[r15+rsi*1+64], rdi, 2))))
instruction_list.append(("SHRD m64, r64, cl", (MOV(esi, esi), SHRD(qword[r15+rsi*1+64], rdi, cl))))

instruction_list.append(("SHLD r16, r16, imm8", (SHLD(cx, cx, 2),)))
instruction_list.append(("SHLD r16, r16, cl", (SHLD(cx, cx, cl),)))
instruction_list.append(("SHLD r32, r32, imm8", (SHLD(ebx, ebx, 2),)))
instruction_list.append(("SHLD r32, r32, cl", (SHLD(ebx, ebx, cl),)))
instruction_list.append(("SHLD r64, r64, imm8", (SHLD(rdi, rdi, 2),)))
instruction_list.append(("SHLD r64, r64, cl", (SHLD(rdi, rdi, cl),)))
instruction_list.append(("SHLD m16, r16, imm8", (MOV(esi, esi), SHLD(word[r15+rsi*1+16], cx, 2))))
instruction_list.append(("SHLD m16, r16, cl", (MOV(esi, esi), SHLD(word[r15+rsi*1+16], cx, cl))))
instruction_list.append(("SHLD m32, r32, imm8", (MOV(esi, esi), SHLD(dword[r15+rsi*1+32], ebx, 2))))
instruction_list.append(("SHLD m32, r32, cl", (MOV(esi, esi), SHLD(dword[r15+rsi*1+32], ebx, cl))))
instruction_list.append(("SHLD m64, r64, imm8", (MOV(esi, esi), SHLD(qword[r15+rsi*1+64], rdi, 2))))
instruction_list.append(("SHLD m64, r64, cl", (MOV(esi, esi), SHLD(qword[r15+rsi*1+64], rdi, cl))))

instruction_list.append(("ROR r8, 1", (ROR(dl, 1),)))
instruction_list.append(("ROR r8, imm8", (ROR(dl, 2),)))
instruction_list.append(("ROR r8, cl", (ROR(dl, cl),)))
instruction_list.append(("ROR r16, 1", (ROR(cx, 1),)))
instruction_list.append(("ROR r16, imm8", (ROR(cx, 2),)))
instruction_list.append(("ROR r16, cl", (ROR(cx, cl),)))
instruction_list.append(("ROR r32, 1", (ROR(ebx, 1),)))
instruction_list.append(("ROR r32, imm8", (ROR(ebx, 2),)))
instruction_list.append(("ROR r32, cl", (ROR(ebx, cl),)))
instruction_list.append(("ROR r64, 1", (ROR(rdi, 1),)))
instruction_list.append(("ROR r64, imm8", (ROR(rdi, 2),)))
instruction_list.append(("ROR r64, cl", (ROR(rdi, cl),)))
instruction_list.append(("ROR m8, 1", (MOV(esi, esi), ROR(byte[r15+rsi*1+8], 1))))
instruction_list.append(("ROR m8, imm8", (MOV(esi, esi), ROR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("ROR m8, cl", (MOV(esi, esi), ROR(byte[r15+rsi*1+8], cl))))
instruction_list.append(("ROR m16, 1", (MOV(esi, esi), ROR(word[r15+rsi*1+16], 1))))
instruction_list.append(("ROR m16, imm8", (MOV(esi, esi), ROR(word[r15+rsi*1+16], 2))))
instruction_list.append(("ROR m16, cl", (MOV(esi, esi), ROR(word[r15+rsi*1+16], cl))))
instruction_list.append(("ROR m32, 1", (MOV(esi, esi), ROR(dword[r15+rsi*1+32], 1))))
instruction_list.append(("ROR m32, imm8", (MOV(esi, esi), ROR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("ROR m32, cl", (MOV(esi, esi), ROR(dword[r15+rsi*1+32], cl))))
instruction_list.append(("ROR m64, 1", (MOV(esi, esi), ROR(qword[r15+rsi*1+64], 1))))
instruction_list.append(("ROR m64, imm8", (MOV(esi, esi), ROR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("ROR m64, cl", (MOV(esi, esi), ROR(qword[r15+rsi*1+64], cl))))

instruction_list.append(("ROL r8, 1", (ROL(dl, 1),)))
instruction_list.append(("ROL r8, imm8", (ROL(dl, 2),)))
instruction_list.append(("ROL r8, cl", (ROL(dl, cl),)))
instruction_list.append(("ROL r16, 1", (ROL(cx, 1),)))
instruction_list.append(("ROL r16, imm8", (ROL(cx, 2),)))
instruction_list.append(("ROL r16, cl", (ROL(cx, cl),)))
instruction_list.append(("ROL r32, 1", (ROL(ebx, 1),)))
instruction_list.append(("ROL r32, imm8", (ROL(ebx, 2),)))
instruction_list.append(("ROL r32, cl", (ROL(ebx, cl),)))
instruction_list.append(("ROL r64, 1", (ROL(rdi, 1),)))
instruction_list.append(("ROL r64, imm8", (ROL(rdi, 2),)))
instruction_list.append(("ROL r64, cl", (ROL(rdi, cl),)))
instruction_list.append(("ROL m8, 1", (MOV(esi, esi), ROL(byte[r15+rsi*1+8], 1))))
instruction_list.append(("ROL m8, imm8", (MOV(esi, esi), ROL(byte[r15+rsi*1+8], 2))))
instruction_list.append(("ROL m8, cl", (MOV(esi, esi), ROL(byte[r15+rsi*1+8], cl))))
instruction_list.append(("ROL m16, 1", (MOV(esi, esi), ROL(word[r15+rsi*1+16], 1))))
instruction_list.append(("ROL m16, imm8", (MOV(esi, esi), ROL(word[r15+rsi*1+16], 2))))
instruction_list.append(("ROL m16, cl", (MOV(esi, esi), ROL(word[r15+rsi*1+16], cl))))
instruction_list.append(("ROL m32, 1", (MOV(esi, esi), ROL(dword[r15+rsi*1+32], 1))))
instruction_list.append(("ROL m32, imm8", (MOV(esi, esi), ROL(dword[r15+rsi*1+32], 2))))
instruction_list.append(("ROL m32, cl", (MOV(esi, esi), ROL(dword[r15+rsi*1+32], cl))))
instruction_list.append(("ROL m64, 1", (MOV(esi, esi), ROL(qword[r15+rsi*1+64], 1))))
instruction_list.append(("ROL m64, imm8", (MOV(esi, esi), ROL(qword[r15+rsi*1+64], 2))))
instruction_list.append(("ROL m64, cl", (MOV(esi, esi), ROL(qword[r15+rsi*1+64], cl))))

instruction_list.append(("RORX r32, r32, imm8", (RORX(ebx, ebx, 2),)))
instruction_list.append(("RORX r32, m32, imm8", (MOV(esi, esi), RORX(ebx, dword[r15+rsi*1+32], 2))))
instruction_list.append(("RORX r64, r64, imm8", (RORX(rdi, rdi, 2),)))
instruction_list.append(("RORX r64, m64, imm8", (MOV(esi, esi), RORX(rdi, qword[r15+rsi*1+64], 2))))

instruction_list.append(("RCR r8, 1", (RCR(dl, 1),)))
instruction_list.append(("RCR r8, imm8", (RCR(dl, 2),)))
instruction_list.append(("RCR r8, cl", (RCR(dl, cl),)))
instruction_list.append(("RCR r16, 1", (RCR(cx, 1),)))
instruction_list.append(("RCR r16, imm8", (RCR(cx, 2),)))
instruction_list.append(("RCR r16, cl", (RCR(cx, cl),)))
instruction_list.append(("RCR r32, 1", (RCR(ebx, 1),)))
instruction_list.append(("RCR r32, imm8", (RCR(ebx, 2),)))
instruction_list.append(("RCR r32, cl", (RCR(ebx, cl),)))
instruction_list.append(("RCR r64, 1", (RCR(rdi, 1),)))
instruction_list.append(("RCR r64, imm8", (RCR(rdi, 2),)))
instruction_list.append(("RCR r64, cl", (RCR(rdi, cl),)))
instruction_list.append(("RCR m8, 1", (MOV(esi, esi), RCR(byte[r15+rsi*1+8], 1))))
instruction_list.append(("RCR m8, imm8", (MOV(esi, esi), RCR(byte[r15+rsi*1+8], 2))))
instruction_list.append(("RCR m8, cl", (MOV(esi, esi), RCR(byte[r15+rsi*1+8], cl))))
instruction_list.append(("RCR m16, 1", (MOV(esi, esi), RCR(word[r15+rsi*1+16], 1))))
instruction_list.append(("RCR m16, imm8", (MOV(esi, esi), RCR(word[r15+rsi*1+16], 2))))
instruction_list.append(("RCR m16, cl", (MOV(esi, esi), RCR(word[r15+rsi*1+16], cl))))
instruction_list.append(("RCR m32, 1", (MOV(esi, esi), RCR(dword[r15+rsi*1+32], 1))))
instruction_list.append(("RCR m32, imm8", (MOV(esi, esi), RCR(dword[r15+rsi*1+32], 2))))
instruction_list.append(("RCR m32, cl", (MOV(esi, esi), RCR(dword[r15+rsi*1+32], cl))))
instruction_list.append(("RCR m64, 1", (MOV(esi, esi), RCR(qword[r15+rsi*1+64], 1))))
instruction_list.append(("RCR m64, imm8", (MOV(esi, esi), RCR(qword[r15+rsi*1+64], 2))))
instruction_list.append(("RCR m64, cl", (MOV(esi, esi), RCR(qword[r15+rsi*1+64], cl))))

instruction_list.append(("RCL r8, 1", (RCL(dl, 1),)))
instruction_list.append(("RCL r8, imm8", (RCL(dl, 2),)))
instruction_list.append(("RCL r8, cl", (RCL(dl, cl),)))
instruction_list.append(("RCL r16, 1", (RCL(cx, 1),)))
instruction_list.append(("RCL r16, imm8", (RCL(cx, 2),)))
instruction_list.append(("RCL r16, cl", (RCL(cx, cl),)))
instruction_list.append(("RCL r32, 1", (RCL(ebx, 1),)))
instruction_list.append(("RCL r32, imm8", (RCL(ebx, 2),)))
instruction_list.append(("RCL r32, cl", (RCL(ebx, cl),)))
instruction_list.append(("RCL r64, 1", (RCL(rdi, 1),)))
instruction_list.append(("RCL r64, imm8", (RCL(rdi, 2),)))
instruction_list.append(("RCL r64, cl", (RCL(rdi, cl),)))
instruction_list.append(("RCL m8, 1", (MOV(esi, esi), RCL(byte[r15+rsi*1+8], 1))))
instruction_list.append(("RCL m8, imm8", (MOV(esi, esi), RCL(byte[r15+rsi*1+8], 2))))
instruction_list.append(("RCL m8, cl", (MOV(esi, esi), RCL(byte[r15+rsi*1+8], cl))))
instruction_list.append(("RCL m16, 1", (MOV(esi, esi), RCL(word[r15+rsi*1+16], 1))))
instruction_list.append(("RCL m16, imm8", (MOV(esi, esi), RCL(word[r15+rsi*1+16], 2))))
instruction_list.append(("RCL m16, cl", (MOV(esi, esi), RCL(word[r15+rsi*1+16], cl))))
instruction_list.append(("RCL m32, 1", (MOV(esi, esi), RCL(dword[r15+rsi*1+32], 1))))
instruction_list.append(("RCL m32, imm8", (MOV(esi, esi), RCL(dword[r15+rsi*1+32], 2))))
instruction_list.append(("RCL m32, cl", (MOV(esi, esi), RCL(dword[r15+rsi*1+32], cl))))
instruction_list.append(("RCL m64, 1", (MOV(esi, esi), RCL(qword[r15+rsi*1+64], 1))))
instruction_list.append(("RCL m64, imm8", (MOV(esi, esi), RCL(qword[r15+rsi*1+64], 2))))
instruction_list.append(("RCL m64, cl", (MOV(esi, esi), RCL(qword[r15+rsi*1+64], cl))))

instruction_list.append(("IMUL r8", (IMUL(dl),)))
instruction_list.append(("IMUL r16", (IMUL(cx),)))
instruction_list.append(("IMUL r32", (IMUL(ebx),)))
instruction_list.append(("IMUL r64", (IMUL(rdi),)))
instruction_list.append(("IMUL m8", (MOV(esi, esi), IMUL(byte[r15+rsi*1+8]))))
instruction_list.append(("IMUL m16", (MOV(esi, esi), IMUL(word[r15+rsi*1+16]))))
instruction_list.append(("IMUL m32", (MOV(esi, esi), IMUL(dword[r15+rsi*1+32]))))
instruction_list.append(("IMUL m64", (MOV(esi, esi), IMUL(qword[r15+rsi*1+64]))))
instruction_list.append(("IMUL r16, r16", (IMUL(cx, cx),)))
instruction_list.append(("IMUL r16, m16", (MOV(esi, esi), IMUL(cx, word[r15+rsi*1+16]))))
instruction_list.append(("IMUL r32, r32", (IMUL(ebx, ebx),)))
instruction_list.append(("IMUL r32, m32", (MOV(esi, esi), IMUL(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("IMUL r64, r64", (IMUL(rdi, rdi),)))
instruction_list.append(("IMUL r64, m64", (MOV(esi, esi), IMUL(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("IMUL r16, r16, imm8", (IMUL(cx, cx, 2),)))
instruction_list.append(("IMUL r16, r16, imm16", (IMUL(cx, cx, 32000),)))
instruction_list.append(("IMUL r16, m16, imm8", (MOV(esi, esi), IMUL(cx, word[r15+rsi*1+16], 2))))
instruction_list.append(("IMUL r16, m16, imm16", (MOV(esi, esi), IMUL(cx, word[r15+rsi*1+16], 32000))))
instruction_list.append(("IMUL r32, r32, imm8", (IMUL(ebx, ebx, 2),)))
instruction_list.append(("IMUL r32, r32, imm32", (IMUL(ebx, ebx, 0x10000000),)))
instruction_list.append(("IMUL r32, m32, imm8", (MOV(esi, esi), IMUL(ebx, dword[r15+rsi*1+32], 2))))
instruction_list.append(("IMUL r32, m32, imm32", (MOV(esi, esi), IMUL(ebx, dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("IMUL r64, r64, imm8", (IMUL(rdi, rdi, 2),)))
instruction_list.append(("IMUL r64, r64, imm32", (IMUL(rdi, rdi, 0x10000000),)))
instruction_list.append(("IMUL r64, m64, imm8", (MOV(esi, esi), IMUL(rdi, qword[r15+rsi*1+64], 2))))
instruction_list.append(("IMUL r64, m64, imm32", (MOV(esi, esi), IMUL(rdi, qword[r15+rsi*1+64], 0x10000000))))

instruction_list.append(("MUL r8", (MUL(dl),)))
instruction_list.append(("MUL r16", (MUL(cx),)))
instruction_list.append(("MUL r32", (MUL(ebx),)))
instruction_list.append(("MUL r64", (MUL(rdi),)))
instruction_list.append(("MUL m8", (MOV(esi, esi), MUL(byte[r15+rsi*1+8]))))
instruction_list.append(("MUL m16", (MOV(esi, esi), MUL(word[r15+rsi*1+16]))))
instruction_list.append(("MUL m32", (MOV(esi, esi), MUL(dword[r15+rsi*1+32]))))
instruction_list.append(("MUL m64", (MOV(esi, esi), MUL(qword[r15+rsi*1+64]))))

instruction_list.append(("MULX r32, r32, r32", (MULX(ebx, ebx, ebx),)))
instruction_list.append(("MULX r32, r32, m32", (MOV(esi, esi), MULX(ebx, ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("MULX r64, r64, r64", (MULX(rdi, rdi, rdi),)))
instruction_list.append(("MULX r64, r64, m64", (MOV(esi, esi), MULX(rdi, rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("IDIV r8", (IDIV(dl),)))
instruction_list.append(("IDIV r16", (IDIV(cx),)))
instruction_list.append(("IDIV r32", (IDIV(ebx),)))
instruction_list.append(("IDIV r64", (IDIV(rdi),)))
instruction_list.append(("IDIV m8", (MOV(esi, esi), IDIV(byte[r15+rsi*1+8]))))
instruction_list.append(("IDIV m16", (MOV(esi, esi), IDIV(word[r15+rsi*1+16]))))
instruction_list.append(("IDIV m32", (MOV(esi, esi), IDIV(dword[r15+rsi*1+32]))))
instruction_list.append(("IDIV m64", (MOV(esi, esi), IDIV(qword[r15+rsi*1+64]))))

instruction_list.append(("DIV r8", (DIV(dl),)))
instruction_list.append(("DIV r16", (DIV(cx),)))
instruction_list.append(("DIV r32", (DIV(ebx),)))
instruction_list.append(("DIV r64", (DIV(rdi),)))
instruction_list.append(("DIV m8", (MOV(esi, esi), DIV(byte[r15+rsi*1+8]))))
instruction_list.append(("DIV m16", (MOV(esi, esi), DIV(word[r15+rsi*1+16]))))
instruction_list.append(("DIV m32", (MOV(esi, esi), DIV(dword[r15+rsi*1+32]))))
instruction_list.append(("DIV m64", (MOV(esi, esi), DIV(qword[r15+rsi*1+64]))))

instruction_list.append(("LEA r16, m", (MOV(esi, esi), LEA(cx, [r15+rsi*1-128]))))
instruction_list.append(("LEA r32, m", (MOV(esi, esi), LEA(ebx, [r15+rsi*1-128]))))
instruction_list.append(("LEA r64, m", (MOV(esi, esi), LEA(rdi, [r15+rsi*1-128]))))

instruction_list.append(("PUSH imm8", (PUSH(2),)))
instruction_list.append(("PUSH imm32", (PUSH(0x10000000),)))
instruction_list.append(("PUSH r16", (PUSH(cx),)))
instruction_list.append(("PUSH r64", (PUSH(rdi),)))
instruction_list.append(("PUSH m16", (MOV(esi, esi), PUSH(word[r15+rsi*1+16]))))
instruction_list.append(("PUSH m64", (MOV(esi, esi), PUSH(qword[r15+rsi*1+64]))))

instruction_list.append(("POP r16", (POP(cx),)))
instruction_list.append(("POP r64", (POP(rdi),)))
instruction_list.append(("POP m16", (MOV(esi, esi), POP(word[r15+rsi*1+16]))))
instruction_list.append(("POP m64", (MOV(esi, esi), POP(qword[r15+rsi*1+64]))))

instruction_list.append(("POPCNT r16, r16", (POPCNT(cx, cx),)))
instruction_list.append(("POPCNT r16, m16", (MOV(esi, esi), POPCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("POPCNT r32, r32", (POPCNT(ebx, ebx),)))
instruction_list.append(("POPCNT r32, m32", (MOV(esi, esi), POPCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("POPCNT r64, r64", (POPCNT(rdi, rdi),)))
instruction_list.append(("POPCNT r64, m64", (MOV(esi, esi), POPCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("LZCNT r16, r16", (LZCNT(cx, cx),)))
instruction_list.append(("LZCNT r16, m16", (MOV(esi, esi), LZCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("LZCNT r32, r32", (LZCNT(ebx, ebx),)))
instruction_list.append(("LZCNT r32, m32", (MOV(esi, esi), LZCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("LZCNT r64, r64", (LZCNT(rdi, rdi),)))
instruction_list.append(("LZCNT r64, m64", (MOV(esi, esi), LZCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("TZCNT r16, r16", (TZCNT(cx, cx),)))
instruction_list.append(("TZCNT r16, m16", (MOV(esi, esi), TZCNT(cx, word[r15+rsi*1+16]))))
instruction_list.append(("TZCNT r32, r32", (TZCNT(ebx, ebx),)))
instruction_list.append(("TZCNT r32, m32", (MOV(esi, esi), TZCNT(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("TZCNT r64, r64", (TZCNT(rdi, rdi),)))
instruction_list.append(("TZCNT r64, m64", (MOV(esi, esi), TZCNT(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BEXTR r32, r32, imm32", (BEXTR(ebx, ebx, 0x10000000),)))
instruction_list.append(("BEXTR r32, r32, r32", (BEXTR(ebx, ebx, ebx),)))
instruction_list.append(("BEXTR r32, m32, imm32", (MOV(esi, esi), BEXTR(ebx, dword[r15+rsi*1+32], 0x10000000))))
instruction_list.append(("BEXTR r32, m32, r32", (MOV(esi, esi), BEXTR(ebx, dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BEXTR r64, r64, imm32", (BEXTR(rdi, rdi, 0x10000000),)))
instruction_list.append(("BEXTR r64, r64, r64", (BEXTR(rdi, rdi, rdi),)))
instruction_list.append(("BEXTR r64, m64, imm32", (MOV(esi, esi), BEXTR(rdi, qword[r15+rsi*1+64], 0x10000000))))
instruction_list.append(("BEXTR r64, m64, r64", (MOV(esi, esi), BEXTR(rdi, qword[r15+rsi*1+64], rdi))))

instruction_list.append(("PDEP r32, r32, r32", (PDEP(ebx, ebx, ebx),)))
instruction_list.append(("PDEP r32, r32, m32", (MOV(esi, esi), PDEP(ebx, ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("PDEP r64, r64, r64", (PDEP(rdi, rdi, rdi),)))
instruction_list.append(("PDEP r64, r64, m64", (MOV(esi, esi), PDEP(rdi, rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("PEXT r32, r32, r32", (PEXT(ebx, ebx, ebx),)))
instruction_list.append(("PEXT r32, r32, m32", (MOV(esi, esi), PEXT(ebx, ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("PEXT r64, r64, r64", (PEXT(rdi, rdi, rdi),)))
instruction_list.append(("PEXT r64, r64, m64", (MOV(esi, esi), PEXT(rdi, rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BZHI r32, r32, r32", (BZHI(ebx, ebx, ebx),)))
instruction_list.append(("BZHI r32, m32, r32", (MOV(esi, esi), BZHI(ebx, dword[r15+rsi*1+32], ebx))))
instruction_list.append(("BZHI r64, r64, r64", (BZHI(rdi, rdi, rdi),)))
instruction_list.append(("BZHI r64, m64, r64", (MOV(esi, esi), BZHI(rdi, qword[r15+rsi*1+64], rdi))))

instruction_list.append(("BLCFILL r32, r32", (BLCFILL(ebx, ebx),)))
instruction_list.append(("BLCFILL r32, m32", (MOV(esi, esi), BLCFILL(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLCFILL r64, r64", (BLCFILL(rdi, rdi),)))
instruction_list.append(("BLCFILL r64, m64", (MOV(esi, esi), BLCFILL(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLCI r32, r32", (BLCI(ebx, ebx),)))
instruction_list.append(("BLCI r32, m32", (MOV(esi, esi), BLCI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLCI r64, r64", (BLCI(rdi, rdi),)))
instruction_list.append(("BLCI r64, m64", (MOV(esi, esi), BLCI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLCIC r32, r32", (BLCIC(ebx, ebx),)))
instruction_list.append(("BLCIC r32, m32", (MOV(esi, esi), BLCIC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLCIC r64, r64", (BLCIC(rdi, rdi),)))
instruction_list.append(("BLCIC r64, m64", (MOV(esi, esi), BLCIC(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLCMSK r32, r32", (BLCMSK(ebx, ebx),)))
instruction_list.append(("BLCMSK r32, m32", (MOV(esi, esi), BLCMSK(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLCMSK r64, r64", (BLCMSK(rdi, rdi),)))
instruction_list.append(("BLCMSK r64, m64", (MOV(esi, esi), BLCMSK(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLCS r32, r32", (BLCS(ebx, ebx),)))
instruction_list.append(("BLCS r32, m32", (MOV(esi, esi), BLCS(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLCS r64, r64", (BLCS(rdi, rdi),)))
instruction_list.append(("BLCS r64, m64", (MOV(esi, esi), BLCS(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLSFILL r32, r32", (BLSFILL(ebx, ebx),)))
instruction_list.append(("BLSFILL r32, m32", (MOV(esi, esi), BLSFILL(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLSFILL r64, r64", (BLSFILL(rdi, rdi),)))
instruction_list.append(("BLSFILL r64, m64", (MOV(esi, esi), BLSFILL(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLSI r32, r32", (BLSI(ebx, ebx),)))
instruction_list.append(("BLSI r32, m32", (MOV(esi, esi), BLSI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLSI r64, r64", (BLSI(rdi, rdi),)))
instruction_list.append(("BLSI r64, m64", (MOV(esi, esi), BLSI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLSIC r32, r32", (BLSIC(ebx, ebx),)))
instruction_list.append(("BLSIC r32, m32", (MOV(esi, esi), BLSIC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLSIC r64, r64", (BLSIC(rdi, rdi),)))
instruction_list.append(("BLSIC r64, m64", (MOV(esi, esi), BLSIC(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLSMSK r32, r32", (BLSMSK(ebx, ebx),)))
instruction_list.append(("BLSMSK r32, m32", (MOV(esi, esi), BLSMSK(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLSMSK r64, r64", (BLSMSK(rdi, rdi),)))
instruction_list.append(("BLSMSK r64, m64", (MOV(esi, esi), BLSMSK(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("BLSR r32, r32", (BLSR(ebx, ebx),)))
instruction_list.append(("BLSR r32, m32", (MOV(esi, esi), BLSR(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("BLSR r64, r64", (BLSR(rdi, rdi),)))
instruction_list.append(("BLSR r64, m64", (MOV(esi, esi), BLSR(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("T1MSKC r32, r32", (T1MSKC(ebx, ebx),)))
instruction_list.append(("T1MSKC r32, m32", (MOV(esi, esi), T1MSKC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("T1MSKC r64, r64", (T1MSKC(rdi, rdi),)))
instruction_list.append(("T1MSKC r64, m64", (MOV(esi, esi), T1MSKC(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("TZMSK r32, r32", (TZMSK(ebx, ebx),)))
instruction_list.append(("TZMSK r32, m32", (MOV(esi, esi), TZMSK(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("TZMSK r64, r64", (TZMSK(rdi, rdi),)))
instruction_list.append(("TZMSK r64, m64", (MOV(esi, esi), TZMSK(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CRC32 r32, r8", (CRC32(ebx, dl),)))
instruction_list.append(("CRC32 r32, r16", (CRC32(ebx, cx),)))
instruction_list.append(("CRC32 r32, r32", (CRC32(ebx, ebx),)))
instruction_list.append(("CRC32 r32, m8", (MOV(esi, esi), CRC32(ebx, byte[r15+rsi*1+8]))))
instruction_list.append(("CRC32 r32, m16", (MOV(esi, esi), CRC32(ebx, word[r15+rsi*1+16]))))
instruction_list.append(("CRC32 r32, m32", (MOV(esi, esi), CRC32(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CRC32 r64, r8", (CRC32(rdi, dl),)))
instruction_list.append(("CRC32 r64, r64", (CRC32(rdi, rdi),)))
instruction_list.append(("CRC32 r64, m8", (MOV(esi, esi), CRC32(rdi, byte[r15+rsi*1+8]))))
instruction_list.append(("CRC32 r64, m64", (MOV(esi, esi), CRC32(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CBW", (CBW(),)))

instruction_list.append(("CDQ", (CDQ(),)))

instruction_list.append(("CQO", (CQO(),)))

instruction_list.append(("CWD", (CWD(),)))

instruction_list.append(("CWDE", (CWDE(),)))

instruction_list.append(("CDQE", (CDQE(),)))

instruction_list.append(("CMOVA r16, r16", (CMOVA(cx, cx),)))
instruction_list.append(("CMOVA r16, m16", (MOV(esi, esi), CMOVA(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVA r32, r32", (CMOVA(ebx, ebx),)))
instruction_list.append(("CMOVA r32, m32", (MOV(esi, esi), CMOVA(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVA r64, r64", (CMOVA(rdi, rdi),)))
instruction_list.append(("CMOVA r64, m64", (MOV(esi, esi), CMOVA(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNA r16, r16", (CMOVNA(cx, cx),)))
instruction_list.append(("CMOVNA r16, m16", (MOV(esi, esi), CMOVNA(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNA r32, r32", (CMOVNA(ebx, ebx),)))
instruction_list.append(("CMOVNA r32, m32", (MOV(esi, esi), CMOVNA(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNA r64, r64", (CMOVNA(rdi, rdi),)))
instruction_list.append(("CMOVNA r64, m64", (MOV(esi, esi), CMOVNA(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVAE r16, r16", (CMOVAE(cx, cx),)))
instruction_list.append(("CMOVAE r16, m16", (MOV(esi, esi), CMOVAE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVAE r32, r32", (CMOVAE(ebx, ebx),)))
instruction_list.append(("CMOVAE r32, m32", (MOV(esi, esi), CMOVAE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVAE r64, r64", (CMOVAE(rdi, rdi),)))
instruction_list.append(("CMOVAE r64, m64", (MOV(esi, esi), CMOVAE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNAE r16, r16", (CMOVNAE(cx, cx),)))
instruction_list.append(("CMOVNAE r16, m16", (MOV(esi, esi), CMOVNAE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNAE r32, r32", (CMOVNAE(ebx, ebx),)))
instruction_list.append(("CMOVNAE r32, m32", (MOV(esi, esi), CMOVNAE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNAE r64, r64", (CMOVNAE(rdi, rdi),)))
instruction_list.append(("CMOVNAE r64, m64", (MOV(esi, esi), CMOVNAE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVB r16, r16", (CMOVB(cx, cx),)))
instruction_list.append(("CMOVB r16, m16", (MOV(esi, esi), CMOVB(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVB r32, r32", (CMOVB(ebx, ebx),)))
instruction_list.append(("CMOVB r32, m32", (MOV(esi, esi), CMOVB(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVB r64, r64", (CMOVB(rdi, rdi),)))
instruction_list.append(("CMOVB r64, m64", (MOV(esi, esi), CMOVB(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNB r16, r16", (CMOVNB(cx, cx),)))
instruction_list.append(("CMOVNB r16, m16", (MOV(esi, esi), CMOVNB(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNB r32, r32", (CMOVNB(ebx, ebx),)))
instruction_list.append(("CMOVNB r32, m32", (MOV(esi, esi), CMOVNB(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNB r64, r64", (CMOVNB(rdi, rdi),)))
instruction_list.append(("CMOVNB r64, m64", (MOV(esi, esi), CMOVNB(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVBE r16, r16", (CMOVBE(cx, cx),)))
instruction_list.append(("CMOVBE r16, m16", (MOV(esi, esi), CMOVBE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVBE r32, r32", (CMOVBE(ebx, ebx),)))
instruction_list.append(("CMOVBE r32, m32", (MOV(esi, esi), CMOVBE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVBE r64, r64", (CMOVBE(rdi, rdi),)))
instruction_list.append(("CMOVBE r64, m64", (MOV(esi, esi), CMOVBE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNBE r16, r16", (CMOVNBE(cx, cx),)))
instruction_list.append(("CMOVNBE r16, m16", (MOV(esi, esi), CMOVNBE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNBE r32, r32", (CMOVNBE(ebx, ebx),)))
instruction_list.append(("CMOVNBE r32, m32", (MOV(esi, esi), CMOVNBE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNBE r64, r64", (CMOVNBE(rdi, rdi),)))
instruction_list.append(("CMOVNBE r64, m64", (MOV(esi, esi), CMOVNBE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVC r16, r16", (CMOVC(cx, cx),)))
instruction_list.append(("CMOVC r16, m16", (MOV(esi, esi), CMOVC(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVC r32, r32", (CMOVC(ebx, ebx),)))
instruction_list.append(("CMOVC r32, m32", (MOV(esi, esi), CMOVC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVC r64, r64", (CMOVC(rdi, rdi),)))
instruction_list.append(("CMOVC r64, m64", (MOV(esi, esi), CMOVC(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNC r16, r16", (CMOVNC(cx, cx),)))
instruction_list.append(("CMOVNC r16, m16", (MOV(esi, esi), CMOVNC(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNC r32, r32", (CMOVNC(ebx, ebx),)))
instruction_list.append(("CMOVNC r32, m32", (MOV(esi, esi), CMOVNC(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNC r64, r64", (CMOVNC(rdi, rdi),)))
instruction_list.append(("CMOVNC r64, m64", (MOV(esi, esi), CMOVNC(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVE r16, r16", (CMOVE(cx, cx),)))
instruction_list.append(("CMOVE r16, m16", (MOV(esi, esi), CMOVE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVE r32, r32", (CMOVE(ebx, ebx),)))
instruction_list.append(("CMOVE r32, m32", (MOV(esi, esi), CMOVE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVE r64, r64", (CMOVE(rdi, rdi),)))
instruction_list.append(("CMOVE r64, m64", (MOV(esi, esi), CMOVE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNE r16, r16", (CMOVNE(cx, cx),)))
instruction_list.append(("CMOVNE r16, m16", (MOV(esi, esi), CMOVNE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNE r32, r32", (CMOVNE(ebx, ebx),)))
instruction_list.append(("CMOVNE r32, m32", (MOV(esi, esi), CMOVNE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNE r64, r64", (CMOVNE(rdi, rdi),)))
instruction_list.append(("CMOVNE r64, m64", (MOV(esi, esi), CMOVNE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVG r16, r16", (CMOVG(cx, cx),)))
instruction_list.append(("CMOVG r16, m16", (MOV(esi, esi), CMOVG(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVG r32, r32", (CMOVG(ebx, ebx),)))
instruction_list.append(("CMOVG r32, m32", (MOV(esi, esi), CMOVG(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVG r64, r64", (CMOVG(rdi, rdi),)))
instruction_list.append(("CMOVG r64, m64", (MOV(esi, esi), CMOVG(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNG r16, r16", (CMOVNG(cx, cx),)))
instruction_list.append(("CMOVNG r16, m16", (MOV(esi, esi), CMOVNG(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNG r32, r32", (CMOVNG(ebx, ebx),)))
instruction_list.append(("CMOVNG r32, m32", (MOV(esi, esi), CMOVNG(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNG r64, r64", (CMOVNG(rdi, rdi),)))
instruction_list.append(("CMOVNG r64, m64", (MOV(esi, esi), CMOVNG(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVGE r16, r16", (CMOVGE(cx, cx),)))
instruction_list.append(("CMOVGE r16, m16", (MOV(esi, esi), CMOVGE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVGE r32, r32", (CMOVGE(ebx, ebx),)))
instruction_list.append(("CMOVGE r32, m32", (MOV(esi, esi), CMOVGE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVGE r64, r64", (CMOVGE(rdi, rdi),)))
instruction_list.append(("CMOVGE r64, m64", (MOV(esi, esi), CMOVGE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNGE r16, r16", (CMOVNGE(cx, cx),)))
instruction_list.append(("CMOVNGE r16, m16", (MOV(esi, esi), CMOVNGE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNGE r32, r32", (CMOVNGE(ebx, ebx),)))
instruction_list.append(("CMOVNGE r32, m32", (MOV(esi, esi), CMOVNGE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNGE r64, r64", (CMOVNGE(rdi, rdi),)))
instruction_list.append(("CMOVNGE r64, m64", (MOV(esi, esi), CMOVNGE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVL r16, r16", (CMOVL(cx, cx),)))
instruction_list.append(("CMOVL r16, m16", (MOV(esi, esi), CMOVL(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVL r32, r32", (CMOVL(ebx, ebx),)))
instruction_list.append(("CMOVL r32, m32", (MOV(esi, esi), CMOVL(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVL r64, r64", (CMOVL(rdi, rdi),)))
instruction_list.append(("CMOVL r64, m64", (MOV(esi, esi), CMOVL(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNL r16, r16", (CMOVNL(cx, cx),)))
instruction_list.append(("CMOVNL r16, m16", (MOV(esi, esi), CMOVNL(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNL r32, r32", (CMOVNL(ebx, ebx),)))
instruction_list.append(("CMOVNL r32, m32", (MOV(esi, esi), CMOVNL(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNL r64, r64", (CMOVNL(rdi, rdi),)))
instruction_list.append(("CMOVNL r64, m64", (MOV(esi, esi), CMOVNL(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVLE r16, r16", (CMOVLE(cx, cx),)))
instruction_list.append(("CMOVLE r16, m16", (MOV(esi, esi), CMOVLE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVLE r32, r32", (CMOVLE(ebx, ebx),)))
instruction_list.append(("CMOVLE r32, m32", (MOV(esi, esi), CMOVLE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVLE r64, r64", (CMOVLE(rdi, rdi),)))
instruction_list.append(("CMOVLE r64, m64", (MOV(esi, esi), CMOVLE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNLE r16, r16", (CMOVNLE(cx, cx),)))
instruction_list.append(("CMOVNLE r16, m16", (MOV(esi, esi), CMOVNLE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNLE r32, r32", (CMOVNLE(ebx, ebx),)))
instruction_list.append(("CMOVNLE r32, m32", (MOV(esi, esi), CMOVNLE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNLE r64, r64", (CMOVNLE(rdi, rdi),)))
instruction_list.append(("CMOVNLE r64, m64", (MOV(esi, esi), CMOVNLE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVO r16, r16", (CMOVO(cx, cx),)))
instruction_list.append(("CMOVO r16, m16", (MOV(esi, esi), CMOVO(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVO r32, r32", (CMOVO(ebx, ebx),)))
instruction_list.append(("CMOVO r32, m32", (MOV(esi, esi), CMOVO(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVO r64, r64", (CMOVO(rdi, rdi),)))
instruction_list.append(("CMOVO r64, m64", (MOV(esi, esi), CMOVO(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNO r16, r16", (CMOVNO(cx, cx),)))
instruction_list.append(("CMOVNO r16, m16", (MOV(esi, esi), CMOVNO(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNO r32, r32", (CMOVNO(ebx, ebx),)))
instruction_list.append(("CMOVNO r32, m32", (MOV(esi, esi), CMOVNO(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNO r64, r64", (CMOVNO(rdi, rdi),)))
instruction_list.append(("CMOVNO r64, m64", (MOV(esi, esi), CMOVNO(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVP r16, r16", (CMOVP(cx, cx),)))
instruction_list.append(("CMOVP r16, m16", (MOV(esi, esi), CMOVP(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVP r32, r32", (CMOVP(ebx, ebx),)))
instruction_list.append(("CMOVP r32, m32", (MOV(esi, esi), CMOVP(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVP r64, r64", (CMOVP(rdi, rdi),)))
instruction_list.append(("CMOVP r64, m64", (MOV(esi, esi), CMOVP(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNP r16, r16", (CMOVNP(cx, cx),)))
instruction_list.append(("CMOVNP r16, m16", (MOV(esi, esi), CMOVNP(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNP r32, r32", (CMOVNP(ebx, ebx),)))
instruction_list.append(("CMOVNP r32, m32", (MOV(esi, esi), CMOVNP(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNP r64, r64", (CMOVNP(rdi, rdi),)))
instruction_list.append(("CMOVNP r64, m64", (MOV(esi, esi), CMOVNP(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVS r16, r16", (CMOVS(cx, cx),)))
instruction_list.append(("CMOVS r16, m16", (MOV(esi, esi), CMOVS(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVS r32, r32", (CMOVS(ebx, ebx),)))
instruction_list.append(("CMOVS r32, m32", (MOV(esi, esi), CMOVS(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVS r64, r64", (CMOVS(rdi, rdi),)))
instruction_list.append(("CMOVS r64, m64", (MOV(esi, esi), CMOVS(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNS r16, r16", (CMOVNS(cx, cx),)))
instruction_list.append(("CMOVNS r16, m16", (MOV(esi, esi), CMOVNS(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNS r32, r32", (CMOVNS(ebx, ebx),)))
instruction_list.append(("CMOVNS r32, m32", (MOV(esi, esi), CMOVNS(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNS r64, r64", (CMOVNS(rdi, rdi),)))
instruction_list.append(("CMOVNS r64, m64", (MOV(esi, esi), CMOVNS(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVZ r16, r16", (CMOVZ(cx, cx),)))
instruction_list.append(("CMOVZ r16, m16", (MOV(esi, esi), CMOVZ(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVZ r32, r32", (CMOVZ(ebx, ebx),)))
instruction_list.append(("CMOVZ r32, m32", (MOV(esi, esi), CMOVZ(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVZ r64, r64", (CMOVZ(rdi, rdi),)))
instruction_list.append(("CMOVZ r64, m64", (MOV(esi, esi), CMOVZ(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVNZ r16, r16", (CMOVNZ(cx, cx),)))
instruction_list.append(("CMOVNZ r16, m16", (MOV(esi, esi), CMOVNZ(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVNZ r32, r32", (CMOVNZ(ebx, ebx),)))
instruction_list.append(("CMOVNZ r32, m32", (MOV(esi, esi), CMOVNZ(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVNZ r64, r64", (CMOVNZ(rdi, rdi),)))
instruction_list.append(("CMOVNZ r64, m64", (MOV(esi, esi), CMOVNZ(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVPE r16, r16", (CMOVPE(cx, cx),)))
instruction_list.append(("CMOVPE r16, m16", (MOV(esi, esi), CMOVPE(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVPE r32, r32", (CMOVPE(ebx, ebx),)))
instruction_list.append(("CMOVPE r32, m32", (MOV(esi, esi), CMOVPE(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVPE r64, r64", (CMOVPE(rdi, rdi),)))
instruction_list.append(("CMOVPE r64, m64", (MOV(esi, esi), CMOVPE(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CMOVPO r16, r16", (CMOVPO(cx, cx),)))
instruction_list.append(("CMOVPO r16, m16", (MOV(esi, esi), CMOVPO(cx, word[r15+rsi*1+16]))))
instruction_list.append(("CMOVPO r32, r32", (CMOVPO(ebx, ebx),)))
instruction_list.append(("CMOVPO r32, m32", (MOV(esi, esi), CMOVPO(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CMOVPO r64, r64", (CMOVPO(rdi, rdi),)))
instruction_list.append(("CMOVPO r64, m64", (MOV(esi, esi), CMOVPO(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("SETA r8", (SETA(dl),)))
instruction_list.append(("SETA m8", (MOV(esi, esi), SETA(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNA r8", (SETNA(dl),)))
instruction_list.append(("SETNA m8", (MOV(esi, esi), SETNA(byte[r15+rsi*1+8]))))

instruction_list.append(("SETAE r8", (SETAE(dl),)))
instruction_list.append(("SETAE m8", (MOV(esi, esi), SETAE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNAE r8", (SETNAE(dl),)))
instruction_list.append(("SETNAE m8", (MOV(esi, esi), SETNAE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETB r8", (SETB(dl),)))
instruction_list.append(("SETB m8", (MOV(esi, esi), SETB(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNB r8", (SETNB(dl),)))
instruction_list.append(("SETNB m8", (MOV(esi, esi), SETNB(byte[r15+rsi*1+8]))))

instruction_list.append(("SETBE r8", (SETBE(dl),)))
instruction_list.append(("SETBE m8", (MOV(esi, esi), SETBE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNBE r8", (SETNBE(dl),)))
instruction_list.append(("SETNBE m8", (MOV(esi, esi), SETNBE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETC r8", (SETC(dl),)))
instruction_list.append(("SETC m8", (MOV(esi, esi), SETC(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNC r8", (SETNC(dl),)))
instruction_list.append(("SETNC m8", (MOV(esi, esi), SETNC(byte[r15+rsi*1+8]))))

instruction_list.append(("SETE r8", (SETE(dl),)))
instruction_list.append(("SETE m8", (MOV(esi, esi), SETE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNE r8", (SETNE(dl),)))
instruction_list.append(("SETNE m8", (MOV(esi, esi), SETNE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETG r8", (SETG(dl),)))
instruction_list.append(("SETG m8", (MOV(esi, esi), SETG(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNG r8", (SETNG(dl),)))
instruction_list.append(("SETNG m8", (MOV(esi, esi), SETNG(byte[r15+rsi*1+8]))))

instruction_list.append(("SETGE r8", (SETGE(dl),)))
instruction_list.append(("SETGE m8", (MOV(esi, esi), SETGE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNGE r8", (SETNGE(dl),)))
instruction_list.append(("SETNGE m8", (MOV(esi, esi), SETNGE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETL r8", (SETL(dl),)))
instruction_list.append(("SETL m8", (MOV(esi, esi), SETL(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNL r8", (SETNL(dl),)))
instruction_list.append(("SETNL m8", (MOV(esi, esi), SETNL(byte[r15+rsi*1+8]))))

instruction_list.append(("SETLE r8", (SETLE(dl),)))
instruction_list.append(("SETLE m8", (MOV(esi, esi), SETLE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNLE r8", (SETNLE(dl),)))
instruction_list.append(("SETNLE m8", (MOV(esi, esi), SETNLE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETO r8", (SETO(dl),)))
instruction_list.append(("SETO m8", (MOV(esi, esi), SETO(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNO r8", (SETNO(dl),)))
instruction_list.append(("SETNO m8", (MOV(esi, esi), SETNO(byte[r15+rsi*1+8]))))

instruction_list.append(("SETP r8", (SETP(dl),)))
instruction_list.append(("SETP m8", (MOV(esi, esi), SETP(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNP r8", (SETNP(dl),)))
instruction_list.append(("SETNP m8", (MOV(esi, esi), SETNP(byte[r15+rsi*1+8]))))

instruction_list.append(("SETS r8", (SETS(dl),)))
instruction_list.append(("SETS m8", (MOV(esi, esi), SETS(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNS r8", (SETNS(dl),)))
instruction_list.append(("SETNS m8", (MOV(esi, esi), SETNS(byte[r15+rsi*1+8]))))

instruction_list.append(("SETZ r8", (SETZ(dl),)))
instruction_list.append(("SETZ m8", (MOV(esi, esi), SETZ(byte[r15+rsi*1+8]))))

instruction_list.append(("SETNZ r8", (SETNZ(dl),)))
instruction_list.append(("SETNZ m8", (MOV(esi, esi), SETNZ(byte[r15+rsi*1+8]))))

instruction_list.append(("SETPE r8", (SETPE(dl),)))
instruction_list.append(("SETPE m8", (MOV(esi, esi), SETPE(byte[r15+rsi*1+8]))))

instruction_list.append(("SETPO r8", (SETPO(dl),)))
instruction_list.append(("SETPO m8", (MOV(esi, esi), SETPO(byte[r15+rsi*1+8]))))

instruction_list.append(("JA rel8", (JA(rip+0),)))
instruction_list.append(("JA rel32", (JA(rip+0),)))

instruction_list.append(("JNA rel8", (JNA(rip+0),)))
instruction_list.append(("JNA rel32", (JNA(rip+0),)))

instruction_list.append(("JAE rel8", (JAE(rip+0),)))
instruction_list.append(("JAE rel32", (JAE(rip+0),)))

instruction_list.append(("JNAE rel8", (JNAE(rip+0),)))
instruction_list.append(("JNAE rel32", (JNAE(rip+0),)))

instruction_list.append(("JB rel8", (JB(rip+0),)))
instruction_list.append(("JB rel32", (JB(rip+0),)))

instruction_list.append(("JNB rel8", (JNB(rip+0),)))
instruction_list.append(("JNB rel32", (JNB(rip+0),)))

instruction_list.append(("JBE rel8", (JBE(rip+0),)))
instruction_list.append(("JBE rel32", (JBE(rip+0),)))

instruction_list.append(("JNBE rel8", (JNBE(rip+0),)))
instruction_list.append(("JNBE rel32", (JNBE(rip+0),)))

instruction_list.append(("JC rel8", (JC(rip+0),)))
instruction_list.append(("JC rel32", (JC(rip+0),)))

instruction_list.append(("JNC rel8", (JNC(rip+0),)))
instruction_list.append(("JNC rel32", (JNC(rip+0),)))

instruction_list.append(("JE rel8", (JE(rip+0),)))
instruction_list.append(("JE rel32", (JE(rip+0),)))

instruction_list.append(("JNE rel8", (JNE(rip+0),)))
instruction_list.append(("JNE rel32", (JNE(rip+0),)))

instruction_list.append(("JG rel8", (JG(rip+0),)))
instruction_list.append(("JG rel32", (JG(rip+0),)))

instruction_list.append(("JNG rel8", (JNG(rip+0),)))
instruction_list.append(("JNG rel32", (JNG(rip+0),)))

instruction_list.append(("JGE rel8", (JGE(rip+0),)))
instruction_list.append(("JGE rel32", (JGE(rip+0),)))

instruction_list.append(("JNGE rel8", (JNGE(rip+0),)))
instruction_list.append(("JNGE rel32", (JNGE(rip+0),)))

instruction_list.append(("JL rel8", (JL(rip+0),)))
instruction_list.append(("JL rel32", (JL(rip+0),)))

instruction_list.append(("JNL rel8", (JNL(rip+0),)))
instruction_list.append(("JNL rel32", (JNL(rip+0),)))

instruction_list.append(("JLE rel8", (JLE(rip+0),)))
instruction_list.append(("JLE rel32", (JLE(rip+0),)))

instruction_list.append(("JNLE rel8", (JNLE(rip+0),)))
instruction_list.append(("JNLE rel32", (JNLE(rip+0),)))

instruction_list.append(("JO rel8", (JO(rip+0),)))
instruction_list.append(("JO rel32", (JO(rip+0),)))

instruction_list.append(("JNO rel8", (JNO(rip+0),)))
instruction_list.append(("JNO rel32", (JNO(rip+0),)))

instruction_list.append(("JP rel8", (JP(rip+0),)))
instruction_list.append(("JP rel32", (JP(rip+0),)))

instruction_list.append(("JNP rel8", (JNP(rip+0),)))
instruction_list.append(("JNP rel32", (JNP(rip+0),)))

instruction_list.append(("JS rel8", (JS(rip+0),)))
instruction_list.append(("JS rel32", (JS(rip+0),)))

instruction_list.append(("JNS rel8", (JNS(rip+0),)))
instruction_list.append(("JNS rel32", (JNS(rip+0),)))

instruction_list.append(("JZ rel8", (JZ(rip+0),)))
instruction_list.append(("JZ rel32", (JZ(rip+0),)))

instruction_list.append(("JNZ rel8", (JNZ(rip+0),)))
instruction_list.append(("JNZ rel32", (JNZ(rip+0),)))

instruction_list.append(("JPE rel8", (JPE(rip+0),)))
instruction_list.append(("JPE rel32", (JPE(rip+0),)))

instruction_list.append(("JPO rel8", (JPO(rip+0),)))
instruction_list.append(("JPO rel32", (JPO(rip+0),)))

instruction_list.append(("JMP rel8", (JMP(rip+0),)))
instruction_list.append(("JMP rel32", (JMP(rip+0),)))
instruction_list.append(("JMP r64", (JMP(rdi),)))
instruction_list.append(("JMP m64", (MOV(esi, esi), JMP(qword[r15+rsi*1+64]))))

instruction_list.append(("JRCXZ rel8", (JRCXZ(rip+0),)))

instruction_list.append(("JECXZ rel8", (JECXZ(rip+0),)))

instruction_list.append(("RET", (RET(),)))
instruction_list.append(("RET imm16", (RET(32000),)))

instruction_list.append(("CALL rel32", (CALL(rip+0),)))
instruction_list.append(("CALL r64", (CALL(rdi),)))
instruction_list.append(("CALL m64", (MOV(esi, esi), CALL(qword[r15+rsi*1+64]))))

instruction_list.append(("PAUSE", (PAUSE(),)))

instruction_list.append(("NOP", (NOP(),)))

instruction_list.append(("INT 3", (INT(3),)))
instruction_list.append(("INT imm8", (INT(2),)))

instruction_list.append(("UD2", (UD2(),)))

instruction_list.append(("CPUID", (CPUID(),)))

instruction_list.append(("RDTSC", (RDTSC(),)))

instruction_list.append(("RDTSCP", (RDTSCP(),)))

instruction_list.append(("XGETBV", (XGETBV(),)))

instruction_list.append(("STC", (STC(),)))

instruction_list.append(("CLC", (CLC(),)))

instruction_list.append(("CMC", (CMC(),)))

instruction_list.append(("STD", (STD(),)))

instruction_list.append(("CLD", (CLD(),)))

instruction_list.append(("XADD r8, r8", (XADD(dl, dl),)))
instruction_list.append(("XADD r16, r16", (XADD(cx, cx),)))
instruction_list.append(("XADD r32, r32", (XADD(ebx, ebx),)))
instruction_list.append(("XADD r64, r64", (XADD(rdi, rdi),)))
instruction_list.append(("XADD m8, r8", (MOV(esi, esi), XADD(byte[r15+rsi*1+8], dl))))
instruction_list.append(("XADD m16, r16", (MOV(esi, esi), XADD(word[r15+rsi*1+16], cx))))
instruction_list.append(("XADD m32, r32", (MOV(esi, esi), XADD(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("XADD m64, r64", (MOV(esi, esi), XADD(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("XCHG r8, r8", (XCHG(dl, dl),)))
instruction_list.append(("XCHG r8, m8", (MOV(esi, esi), XCHG(dl, byte[r15+rsi*1+8]))))
instruction_list.append(("XCHG ax, r16", (XCHG(ax, cx),)))
instruction_list.append(("XCHG r16, ax", (XCHG(cx, ax),)))
instruction_list.append(("XCHG r16, r16", (XCHG(cx, cx),)))
instruction_list.append(("XCHG r16, m16", (MOV(esi, esi), XCHG(cx, word[r15+rsi*1+16]))))
instruction_list.append(("XCHG eax, r32", (XCHG(eax, ebx),)))
instruction_list.append(("XCHG r32, eax", (XCHG(ebx, eax),)))
instruction_list.append(("XCHG r32, r32", (XCHG(ebx, ebx),)))
instruction_list.append(("XCHG r32, m32", (MOV(esi, esi), XCHG(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("XCHG rax, r64", (XCHG(rax, rdi),)))
instruction_list.append(("XCHG r64, rax", (XCHG(rdi, rax),)))
instruction_list.append(("XCHG r64, r64", (XCHG(rdi, rdi),)))
instruction_list.append(("XCHG r64, m64", (MOV(esi, esi), XCHG(rdi, qword[r15+rsi*1+64]))))
instruction_list.append(("XCHG m8, r8", (MOV(esi, esi), XCHG(byte[r15+rsi*1+8], dl))))
instruction_list.append(("XCHG m16, r16", (MOV(esi, esi), XCHG(word[r15+rsi*1+16], cx))))
instruction_list.append(("XCHG m32, r32", (MOV(esi, esi), XCHG(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("XCHG m64, r64", (MOV(esi, esi), XCHG(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("CMPXCHG r8, r8", (CMPXCHG(dl, dl),)))
instruction_list.append(("CMPXCHG r16, r16", (CMPXCHG(cx, cx),)))
instruction_list.append(("CMPXCHG r32, r32", (CMPXCHG(ebx, ebx),)))
instruction_list.append(("CMPXCHG r64, r64", (CMPXCHG(rdi, rdi),)))
instruction_list.append(("CMPXCHG m8, r8", (MOV(esi, esi), CMPXCHG(byte[r15+rsi*1+8], dl))))
instruction_list.append(("CMPXCHG m16, r16", (MOV(esi, esi), CMPXCHG(word[r15+rsi*1+16], cx))))
instruction_list.append(("CMPXCHG m32, r32", (MOV(esi, esi), CMPXCHG(dword[r15+rsi*1+32], ebx))))
instruction_list.append(("CMPXCHG m64, r64", (MOV(esi, esi), CMPXCHG(qword[r15+rsi*1+64], rdi))))

instruction_list.append(("CMPXCHG8B m64", (MOV(esi, esi), CMPXCHG8B(qword[r15+rsi*1+64]))))

instruction_list.append(("CMPXCHG16B m128", (MOV(esi, esi), CMPXCHG16B(oword[r15+rsi*1+128]))))

instruction_list.append(("SFENCE", (SFENCE(),)))

instruction_list.append(("MFENCE", (MFENCE(),)))

instruction_list.append(("LFENCE", (LFENCE(),)))

instruction_list.append(("PREFETCHNTA m8", (MOV(esi, esi), PREFETCHNTA(byte[r15+rsi*1+8]))))

instruction_list.append(("PREFETCHT0 m8", (MOV(esi, esi), PREFETCHT0(byte[r15+rsi*1+8]))))

instruction_list.append(("PREFETCHT1 m8", (MOV(esi, esi), PREFETCHT1(byte[r15+rsi*1+8]))))

instruction_list.append(("PREFETCHT2 m8", (MOV(esi, esi), PREFETCHT2(byte[r15+rsi*1+8]))))

instruction_list.append(("PREFETCHW m8", (MOV(esi, esi), PREFETCHW(byte[r15+rsi*1+8]))))

instruction_list.append(("PREFETCHWT1 m8", (MOV(esi, esi), PREFETCHWT1(byte[r15+rsi*1+8]))))
# mask



















































# crypto

instruction_list.append(("AESDEC xmm, xmm", (AESDEC(xmm7, xmm7),)))
instruction_list.append(("AESDEC xmm, m128", (MOV(esi, esi), AESDEC(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("AESDECLAST xmm, xmm", (AESDECLAST(xmm7, xmm7),)))
instruction_list.append(("AESDECLAST xmm, m128", (MOV(esi, esi), AESDECLAST(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("AESENC xmm, xmm", (AESENC(xmm7, xmm7),)))
instruction_list.append(("AESENC xmm, m128", (MOV(esi, esi), AESENC(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("AESENCLAST xmm, xmm", (AESENCLAST(xmm7, xmm7),)))
instruction_list.append(("AESENCLAST xmm, m128", (MOV(esi, esi), AESENCLAST(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("AESIMC xmm, xmm", (AESIMC(xmm7, xmm7),)))
instruction_list.append(("AESIMC xmm, m128", (MOV(esi, esi), AESIMC(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("AESKEYGENASSIST xmm, xmm, imm8", (AESKEYGENASSIST(xmm7, xmm7, 2),)))
instruction_list.append(("AESKEYGENASSIST xmm, m128, imm8", (MOV(esi, esi), AESKEYGENASSIST(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VAESDEC xmm, xmm, xmm", (VAESDEC(xmm7, xmm7, xmm7),)))
instruction_list.append(("VAESDEC xmm, xmm, m128", (MOV(esi, esi), VAESDEC(xmm7, xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VAESDECLAST xmm, xmm, xmm", (VAESDECLAST(xmm7, xmm7, xmm7),)))
instruction_list.append(("VAESDECLAST xmm, xmm, m128", (MOV(esi, esi), VAESDECLAST(xmm7, xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VAESENC xmm, xmm, xmm", (VAESENC(xmm7, xmm7, xmm7),)))
instruction_list.append(("VAESENC xmm, xmm, m128", (MOV(esi, esi), VAESENC(xmm7, xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VAESENCLAST xmm, xmm, xmm", (VAESENCLAST(xmm7, xmm7, xmm7),)))
instruction_list.append(("VAESENCLAST xmm, xmm, m128", (MOV(esi, esi), VAESENCLAST(xmm7, xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VAESIMC xmm, xmm", (VAESIMC(xmm7, xmm7),)))
instruction_list.append(("VAESIMC xmm, m128", (MOV(esi, esi), VAESIMC(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VAESKEYGENASSIST xmm, xmm, imm8", (VAESKEYGENASSIST(xmm7, xmm7, 2),)))
instruction_list.append(("VAESKEYGENASSIST xmm, m128, imm8", (MOV(esi, esi), VAESKEYGENASSIST(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("SHA1MSG1 xmm, xmm", (SHA1MSG1(xmm7, xmm7),)))
instruction_list.append(("SHA1MSG1 xmm, m128", (MOV(esi, esi), SHA1MSG1(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHA1MSG2 xmm, xmm", (SHA1MSG2(xmm7, xmm7),)))
instruction_list.append(("SHA1MSG2 xmm, m128", (MOV(esi, esi), SHA1MSG2(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHA1NEXTE xmm, xmm", (SHA1NEXTE(xmm7, xmm7),)))
instruction_list.append(("SHA1NEXTE xmm, m128", (MOV(esi, esi), SHA1NEXTE(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHA1RNDS4 xmm, xmm, imm8", (SHA1RNDS4(xmm7, xmm7, 2),)))
instruction_list.append(("SHA1RNDS4 xmm, m128, imm8", (MOV(esi, esi), SHA1RNDS4(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("SHA256MSG1 xmm, xmm", (SHA256MSG1(xmm7, xmm7),)))
instruction_list.append(("SHA256MSG1 xmm, m128", (MOV(esi, esi), SHA256MSG1(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHA256MSG2 xmm, xmm", (SHA256MSG2(xmm7, xmm7),)))
instruction_list.append(("SHA256MSG2 xmm, m128", (MOV(esi, esi), SHA256MSG2(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHA256RNDS2 xmm, xmm, xmm0", (SHA256RNDS2(xmm7, xmm7, xmm0),)))
instruction_list.append(("SHA256RNDS2 xmm, m128, xmm0", (MOV(esi, esi), SHA256RNDS2(xmm7, oword[r15+rsi*1+128], xmm0))))

instruction_list.append(("PCLMULQDQ xmm, xmm, imm8", (PCLMULQDQ(xmm7, xmm7, 2),)))
instruction_list.append(("PCLMULQDQ xmm, m128, imm8", (MOV(esi, esi), PCLMULQDQ(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCLMULQDQ xmm, xmm, xmm, imm8", (VPCLMULQDQ(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCLMULQDQ xmm, xmm, m128, imm8", (MOV(esi, esi), VPCLMULQDQ(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("RDRAND r16", (RDRAND(cx),)))
instruction_list.append(("RDRAND r32", (RDRAND(ebx),)))
instruction_list.append(("RDRAND r64", (RDRAND(rdi),)))

instruction_list.append(("RDSEED r16", (RDSEED(cx),)))
instruction_list.append(("RDSEED r32", (RDSEED(ebx),)))
instruction_list.append(("RDSEED r64", (RDSEED(rdi),)))
# amd

instruction_list.append(("PAVGUSB mm, mm", (PAVGUSB(mm4, mm4),)))
instruction_list.append(("PAVGUSB mm, m64", (MOV(esi, esi), PAVGUSB(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PMULHRW mm, mm", (PMULHRW(mm4, mm4),)))
instruction_list.append(("PMULHRW mm, m64", (MOV(esi, esi), PMULHRW(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PF2ID mm, mm", (PF2ID(mm4, mm4),)))
instruction_list.append(("PF2ID mm, m64", (MOV(esi, esi), PF2ID(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PF2IW mm, mm", (PF2IW(mm4, mm4),)))
instruction_list.append(("PF2IW mm, m64", (MOV(esi, esi), PF2IW(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PI2FW mm, mm", (PI2FW(mm4, mm4),)))
instruction_list.append(("PI2FW mm, m64", (MOV(esi, esi), PI2FW(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PI2FD mm, mm", (PI2FD(mm4, mm4),)))
instruction_list.append(("PI2FD mm, m64", (MOV(esi, esi), PI2FD(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFADD mm, mm", (PFADD(mm4, mm4),)))
instruction_list.append(("PFADD mm, m64", (MOV(esi, esi), PFADD(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFSUB mm, mm", (PFSUB(mm4, mm4),)))
instruction_list.append(("PFSUB mm, m64", (MOV(esi, esi), PFSUB(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFSUBR mm, mm", (PFSUBR(mm4, mm4),)))
instruction_list.append(("PFSUBR mm, m64", (MOV(esi, esi), PFSUBR(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFMUL mm, mm", (PFMUL(mm4, mm4),)))
instruction_list.append(("PFMUL mm, m64", (MOV(esi, esi), PFMUL(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFMAX mm, mm", (PFMAX(mm4, mm4),)))
instruction_list.append(("PFMAX mm, m64", (MOV(esi, esi), PFMAX(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFMIN mm, mm", (PFMIN(mm4, mm4),)))
instruction_list.append(("PFMIN mm, m64", (MOV(esi, esi), PFMIN(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFACC mm, mm", (PFACC(mm4, mm4),)))
instruction_list.append(("PFACC mm, m64", (MOV(esi, esi), PFACC(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFNACC mm, mm", (PFNACC(mm4, mm4),)))
instruction_list.append(("PFNACC mm, m64", (MOV(esi, esi), PFNACC(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFPNACC mm, mm", (PFPNACC(mm4, mm4),)))
instruction_list.append(("PFPNACC mm, m64", (MOV(esi, esi), PFPNACC(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PSWAPD mm, mm", (PSWAPD(mm4, mm4),)))
instruction_list.append(("PSWAPD mm, m64", (MOV(esi, esi), PSWAPD(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFCMPEQ mm, mm", (PFCMPEQ(mm4, mm4),)))
instruction_list.append(("PFCMPEQ mm, m64", (MOV(esi, esi), PFCMPEQ(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFCMPGT mm, mm", (PFCMPGT(mm4, mm4),)))
instruction_list.append(("PFCMPGT mm, m64", (MOV(esi, esi), PFCMPGT(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFCMPGE mm, mm", (PFCMPGE(mm4, mm4),)))
instruction_list.append(("PFCMPGE mm, m64", (MOV(esi, esi), PFCMPGE(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFRCP mm, mm", (PFRCP(mm4, mm4),)))
instruction_list.append(("PFRCP mm, m64", (MOV(esi, esi), PFRCP(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFRCPIT1 mm, mm", (PFRCPIT1(mm4, mm4),)))
instruction_list.append(("PFRCPIT1 mm, m64", (MOV(esi, esi), PFRCPIT1(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFRCPIT2 mm, mm", (PFRCPIT2(mm4, mm4),)))
instruction_list.append(("PFRCPIT2 mm, m64", (MOV(esi, esi), PFRCPIT2(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFRSQRT mm, mm", (PFRSQRT(mm4, mm4),)))
instruction_list.append(("PFRSQRT mm, m64", (MOV(esi, esi), PFRSQRT(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("PFRSQIT1 mm, mm", (PFRSQIT1(mm4, mm4),)))
instruction_list.append(("PFRSQIT1 mm, m64", (MOV(esi, esi), PFRSQIT1(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("FEMMS", (FEMMS(),)))

instruction_list.append(("MOVNTSS m32, xmm", (MOV(esi, esi), MOVNTSS(dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("MOVNTSD m64, xmm", (MOV(esi, esi), MOVNTSD(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("INSERTQ xmm, xmm", (INSERTQ(xmm7, xmm7),)))
instruction_list.append(("INSERTQ xmm, xmm, imm8, imm8", (INSERTQ(xmm7, xmm7, 2, 2),)))

instruction_list.append(("EXTRQ xmm, xmm", (EXTRQ(xmm7, xmm7),)))
instruction_list.append(("EXTRQ xmm, imm8, imm8", (EXTRQ(xmm7, 2, 2),)))

instruction_list.append(("VPPERM xmm, xmm, xmm, xmm", (VPPERM(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPPERM xmm, xmm, xmm, m128", (MOV(esi, esi), VPPERM(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPPERM xmm, xmm, m128, xmm", (MOV(esi, esi), VPPERM(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPCMOV xmm, xmm, xmm, xmm", (VPCMOV(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPCMOV xmm, xmm, xmm, m128", (MOV(esi, esi), VPCMOV(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPCMOV xmm, xmm, m128, xmm", (MOV(esi, esi), VPCMOV(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VPCMOV ymm, ymm, ymm, ymm", (VPCMOV(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VPCMOV ymm, ymm, ymm, m256", (MOV(esi, esi), VPCMOV(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VPCMOV ymm, ymm, m256, ymm", (MOV(esi, esi), VPCMOV(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VPROTB xmm, xmm, imm8", (VPROTB(xmm7, xmm7, 2),)))
instruction_list.append(("VPROTB xmm, xmm, xmm", (VPROTB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPROTB xmm, xmm, m128", (MOV(esi, esi), VPROTB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPROTB xmm, m128, imm8", (MOV(esi, esi), VPROTB(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPROTB xmm, m128, xmm", (MOV(esi, esi), VPROTB(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPROTW xmm, xmm, imm8", (VPROTW(xmm7, xmm7, 2),)))
instruction_list.append(("VPROTW xmm, xmm, xmm", (VPROTW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPROTW xmm, xmm, m128", (MOV(esi, esi), VPROTW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPROTW xmm, m128, imm8", (MOV(esi, esi), VPROTW(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPROTW xmm, m128, xmm", (MOV(esi, esi), VPROTW(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPROTD xmm, xmm, imm8", (VPROTD(xmm7, xmm7, 2),)))
instruction_list.append(("VPROTD xmm, xmm, xmm", (VPROTD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPROTD xmm, xmm, m128", (MOV(esi, esi), VPROTD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPROTD xmm, m128, imm8", (MOV(esi, esi), VPROTD(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPROTD xmm, m128, xmm", (MOV(esi, esi), VPROTD(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPROTQ xmm, xmm, imm8", (VPROTQ(xmm7, xmm7, 2),)))
instruction_list.append(("VPROTQ xmm, xmm, xmm", (VPROTQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPROTQ xmm, xmm, m128", (MOV(esi, esi), VPROTQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPROTQ xmm, m128, imm8", (MOV(esi, esi), VPROTQ(xmm7, oword[r15+rsi*1+128], 2))))
instruction_list.append(("VPROTQ xmm, m128, xmm", (MOV(esi, esi), VPROTQ(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHAB xmm, xmm, xmm", (VPSHAB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHAB xmm, xmm, m128", (MOV(esi, esi), VPSHAB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHAB xmm, m128, xmm", (MOV(esi, esi), VPSHAB(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHAW xmm, xmm, xmm", (VPSHAW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHAW xmm, xmm, m128", (MOV(esi, esi), VPSHAW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHAW xmm, m128, xmm", (MOV(esi, esi), VPSHAW(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHAD xmm, xmm, xmm", (VPSHAD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHAD xmm, xmm, m128", (MOV(esi, esi), VPSHAD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHAD xmm, m128, xmm", (MOV(esi, esi), VPSHAD(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHAQ xmm, xmm, xmm", (VPSHAQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHAQ xmm, xmm, m128", (MOV(esi, esi), VPSHAQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHAQ xmm, m128, xmm", (MOV(esi, esi), VPSHAQ(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHLB xmm, xmm, xmm", (VPSHLB(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHLB xmm, xmm, m128", (MOV(esi, esi), VPSHLB(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHLB xmm, m128, xmm", (MOV(esi, esi), VPSHLB(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHLW xmm, xmm, xmm", (VPSHLW(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHLW xmm, xmm, m128", (MOV(esi, esi), VPSHLW(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHLW xmm, m128, xmm", (MOV(esi, esi), VPSHLW(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHLD xmm, xmm, xmm", (VPSHLD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHLD xmm, xmm, m128", (MOV(esi, esi), VPSHLD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHLD xmm, m128, xmm", (MOV(esi, esi), VPSHLD(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPSHLQ xmm, xmm, xmm", (VPSHLQ(xmm7, xmm7, xmm7),)))
instruction_list.append(("VPSHLQ xmm, xmm, m128", (MOV(esi, esi), VPSHLQ(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VPSHLQ xmm, m128, xmm", (MOV(esi, esi), VPSHLQ(xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPCOMB xmm, xmm, xmm, imm8", (VPCOMB(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMB xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMB(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMW xmm, xmm, xmm, imm8", (VPCOMW(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMW xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMW(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMD xmm, xmm, xmm, imm8", (VPCOMD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMD xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMQ xmm, xmm, xmm, imm8", (VPCOMQ(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMQ xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMQ(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMUB xmm, xmm, xmm, imm8", (VPCOMUB(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMUB xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMUB(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMUW xmm, xmm, xmm, imm8", (VPCOMUW(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMUW xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMUW(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMUD xmm, xmm, xmm, imm8", (VPCOMUD(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMUD xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMUD(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPCOMUQ xmm, xmm, xmm, imm8", (VPCOMUQ(xmm7, xmm7, xmm7, 2),)))
instruction_list.append(("VPCOMUQ xmm, xmm, m128, imm8", (MOV(esi, esi), VPCOMUQ(xmm7, xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("VPHADDBW xmm, xmm", (VPHADDBW(xmm7, xmm7),)))
instruction_list.append(("VPHADDBW xmm, m128", (MOV(esi, esi), VPHADDBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDBD xmm, xmm", (VPHADDBD(xmm7, xmm7),)))
instruction_list.append(("VPHADDBD xmm, m128", (MOV(esi, esi), VPHADDBD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDBQ xmm, xmm", (VPHADDBQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDBQ xmm, m128", (MOV(esi, esi), VPHADDBQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDWD xmm, xmm", (VPHADDWD(xmm7, xmm7),)))
instruction_list.append(("VPHADDWD xmm, m128", (MOV(esi, esi), VPHADDWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDWQ xmm, xmm", (VPHADDWQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDWQ xmm, m128", (MOV(esi, esi), VPHADDWQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDDQ xmm, xmm", (VPHADDDQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDDQ xmm, m128", (MOV(esi, esi), VPHADDDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUBW xmm, xmm", (VPHADDUBW(xmm7, xmm7),)))
instruction_list.append(("VPHADDUBW xmm, m128", (MOV(esi, esi), VPHADDUBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUBD xmm, xmm", (VPHADDUBD(xmm7, xmm7),)))
instruction_list.append(("VPHADDUBD xmm, m128", (MOV(esi, esi), VPHADDUBD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUBQ xmm, xmm", (VPHADDUBQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDUBQ xmm, m128", (MOV(esi, esi), VPHADDUBQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUWD xmm, xmm", (VPHADDUWD(xmm7, xmm7),)))
instruction_list.append(("VPHADDUWD xmm, m128", (MOV(esi, esi), VPHADDUWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUWQ xmm, xmm", (VPHADDUWQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDUWQ xmm, m128", (MOV(esi, esi), VPHADDUWQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHADDUDQ xmm, xmm", (VPHADDUDQ(xmm7, xmm7),)))
instruction_list.append(("VPHADDUDQ xmm, m128", (MOV(esi, esi), VPHADDUDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHSUBBW xmm, xmm", (VPHSUBBW(xmm7, xmm7),)))
instruction_list.append(("VPHSUBBW xmm, m128", (MOV(esi, esi), VPHSUBBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHSUBWD xmm, xmm", (VPHSUBWD(xmm7, xmm7),)))
instruction_list.append(("VPHSUBWD xmm, m128", (MOV(esi, esi), VPHSUBWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPHSUBDQ xmm, xmm", (VPHSUBDQ(xmm7, xmm7),)))
instruction_list.append(("VPHSUBDQ xmm, m128", (MOV(esi, esi), VPHSUBDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("VPMACSDQH xmm, xmm, xmm, xmm", (VPMACSDQH(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSDQH xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSDQH(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSDQL xmm, xmm, xmm, xmm", (VPMACSDQL(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSDQL xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSDQL(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSDD xmm, xmm, xmm, xmm", (VPMACSDD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSDD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSDD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSWD xmm, xmm, xmm, xmm", (VPMACSWD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSWD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSWD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSWW xmm, xmm, xmm, xmm", (VPMACSWW(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSWW xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSWW(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMADCSWD xmm, xmm, xmm, xmm", (VPMADCSWD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMADCSWD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMADCSWD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSSDD xmm, xmm, xmm, xmm", (VPMACSSDD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSSDD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSSDD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSSDQH xmm, xmm, xmm, xmm", (VPMACSSDQH(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSSDQH xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSSDQH(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSSDQL xmm, xmm, xmm, xmm", (VPMACSSDQL(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSSDQL xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSSDQL(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSSWD xmm, xmm, xmm, xmm", (VPMACSSWD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSSWD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSSWD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMACSSWW xmm, xmm, xmm, xmm", (VPMACSSWW(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMACSSWW xmm, xmm, m128, xmm", (MOV(esi, esi), VPMACSSWW(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VPMADCSSWD xmm, xmm, xmm, xmm", (VPMADCSSWD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VPMADCSSWD xmm, xmm, m128, xmm", (MOV(esi, esi), VPMADCSSWD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("VFRCZSS xmm, xmm", (VFRCZSS(xmm7, xmm7),)))
instruction_list.append(("VFRCZSS xmm, m32", (MOV(esi, esi), VFRCZSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFRCZSD xmm, xmm", (VFRCZSD(xmm7, xmm7),)))
instruction_list.append(("VFRCZSD xmm, m64", (MOV(esi, esi), VFRCZSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFRCZPS xmm, xmm", (VFRCZPS(xmm7, xmm7),)))
instruction_list.append(("VFRCZPS xmm, m128", (MOV(esi, esi), VFRCZPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFRCZPS ymm, ymm", (VFRCZPS(ymm3, ymm3),)))
instruction_list.append(("VFRCZPS ymm, m256", (MOV(esi, esi), VFRCZPS(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFRCZPD xmm, xmm", (VFRCZPD(xmm7, xmm7),)))
instruction_list.append(("VFRCZPD xmm, m128", (MOV(esi, esi), VFRCZPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFRCZPD ymm, ymm", (VFRCZPD(ymm3, ymm3),)))
instruction_list.append(("VFRCZPD ymm, m256", (MOV(esi, esi), VFRCZPD(ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VPERMIL2PD xmm, xmm, xmm, xmm, imm4", (VPERMIL2PD(xmm7, xmm7, xmm7, xmm7, 0b11),)))
instruction_list.append(("VPERMIL2PD xmm, xmm, xmm, m128, imm4", (MOV(esi, esi), VPERMIL2PD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128], 0b11))))
instruction_list.append(("VPERMIL2PD xmm, xmm, m128, xmm, imm4", (MOV(esi, esi), VPERMIL2PD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7, 0b11))))
instruction_list.append(("VPERMIL2PD ymm, ymm, ymm, ymm, imm4", (VPERMIL2PD(ymm3, ymm3, ymm3, ymm3, 0b11),)))
instruction_list.append(("VPERMIL2PD ymm, ymm, ymm, m256, imm4", (MOV(esi, esi), VPERMIL2PD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256], 0b11))))
instruction_list.append(("VPERMIL2PD ymm, ymm, m256, ymm, imm4", (MOV(esi, esi), VPERMIL2PD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3, 0b11))))

instruction_list.append(("VPERMIL2PS xmm, xmm, xmm, xmm, imm4", (VPERMIL2PS(xmm7, xmm7, xmm7, xmm7, 0b11),)))
instruction_list.append(("VPERMIL2PS xmm, xmm, xmm, m128, imm4", (MOV(esi, esi), VPERMIL2PS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128], 0b11))))
instruction_list.append(("VPERMIL2PS xmm, xmm, m128, xmm, imm4", (MOV(esi, esi), VPERMIL2PS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7, 0b11))))
instruction_list.append(("VPERMIL2PS ymm, ymm, ymm, ymm, imm4", (VPERMIL2PS(ymm3, ymm3, ymm3, ymm3, 0b11),)))
instruction_list.append(("VPERMIL2PS ymm, ymm, ymm, m256, imm4", (MOV(esi, esi), VPERMIL2PS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256], 0b11))))
instruction_list.append(("VPERMIL2PS ymm, ymm, m256, ymm, imm4", (MOV(esi, esi), VPERMIL2PS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3, 0b11))))
# mmxsse

instruction_list.append(("MOVSS xmm, xmm", (MOVSS(xmm7, xmm7),)))
instruction_list.append(("MOVSS xmm, m32", (MOV(esi, esi), MOVSS(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("MOVSS m32, xmm", (MOV(esi, esi), MOVSS(dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("EXTRACTPS r32, xmm, imm8", (EXTRACTPS(ebx, xmm7, 2),)))
instruction_list.append(("EXTRACTPS m32, xmm, imm8", (MOV(esi, esi), EXTRACTPS(dword[r15+rsi*1+32], xmm7, 2))))

instruction_list.append(("INSERTPS xmm, xmm, imm8", (INSERTPS(xmm7, xmm7, 2),)))
instruction_list.append(("INSERTPS xmm, m32, imm8", (MOV(esi, esi), INSERTPS(xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("ADDSS xmm, xmm", (ADDSS(xmm7, xmm7),)))
instruction_list.append(("ADDSS xmm, m32", (MOV(esi, esi), ADDSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("SUBSS xmm, xmm", (SUBSS(xmm7, xmm7),)))
instruction_list.append(("SUBSS xmm, m32", (MOV(esi, esi), SUBSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("MULSS xmm, xmm", (MULSS(xmm7, xmm7),)))
instruction_list.append(("MULSS xmm, m32", (MOV(esi, esi), MULSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("DIVSS xmm, xmm", (DIVSS(xmm7, xmm7),)))
instruction_list.append(("DIVSS xmm, m32", (MOV(esi, esi), DIVSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("SQRTSS xmm, xmm", (SQRTSS(xmm7, xmm7),)))
instruction_list.append(("SQRTSS xmm, m32", (MOV(esi, esi), SQRTSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("ROUNDSS xmm, xmm, imm8", (ROUNDSS(xmm7, xmm7, 2),)))
instruction_list.append(("ROUNDSS xmm, m32, imm8", (MOV(esi, esi), ROUNDSS(xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("MINSS xmm, xmm", (MINSS(xmm7, xmm7),)))
instruction_list.append(("MINSS xmm, m32", (MOV(esi, esi), MINSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("MAXSS xmm, xmm", (MAXSS(xmm7, xmm7),)))
instruction_list.append(("MAXSS xmm, m32", (MOV(esi, esi), MAXSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("RCPSS xmm, xmm", (RCPSS(xmm7, xmm7),)))
instruction_list.append(("RCPSS xmm, m32", (MOV(esi, esi), RCPSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("RSQRTSS xmm, xmm", (RSQRTSS(xmm7, xmm7),)))
instruction_list.append(("RSQRTSS xmm, m32", (MOV(esi, esi), RSQRTSS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("CMPSS xmm, xmm, imm8", (CMPSS(xmm7, xmm7, 2),)))
instruction_list.append(("CMPSS xmm, m32, imm8", (MOV(esi, esi), CMPSS(xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("COMISS xmm, xmm", (COMISS(xmm7, xmm7),)))
instruction_list.append(("COMISS xmm, m32", (MOV(esi, esi), COMISS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("UCOMISS xmm, xmm", (UCOMISS(xmm7, xmm7),)))
instruction_list.append(("UCOMISS xmm, m32", (MOV(esi, esi), UCOMISS(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("MOVSD xmm, xmm", (MOVSD(xmm7, xmm7),)))
instruction_list.append(("MOVSD xmm, m64", (MOV(esi, esi), MOVSD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVSD m64, xmm", (MOV(esi, esi), MOVSD(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("ADDSD xmm, xmm", (ADDSD(xmm7, xmm7),)))
instruction_list.append(("ADDSD xmm, m64", (MOV(esi, esi), ADDSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("SUBSD xmm, xmm", (SUBSD(xmm7, xmm7),)))
instruction_list.append(("SUBSD xmm, m64", (MOV(esi, esi), SUBSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("MULSD xmm, xmm", (MULSD(xmm7, xmm7),)))
instruction_list.append(("MULSD xmm, m64", (MOV(esi, esi), MULSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("DIVSD xmm, xmm", (DIVSD(xmm7, xmm7),)))
instruction_list.append(("DIVSD xmm, m64", (MOV(esi, esi), DIVSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("SQRTSD xmm, xmm", (SQRTSD(xmm7, xmm7),)))
instruction_list.append(("SQRTSD xmm, m64", (MOV(esi, esi), SQRTSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("ROUNDSD xmm, xmm, imm8", (ROUNDSD(xmm7, xmm7, 2),)))
instruction_list.append(("ROUNDSD xmm, m64, imm8", (MOV(esi, esi), ROUNDSD(xmm7, qword[r15+rsi*1+64], 2))))

instruction_list.append(("MINSD xmm, xmm", (MINSD(xmm7, xmm7),)))
instruction_list.append(("MINSD xmm, m64", (MOV(esi, esi), MINSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("MAXSD xmm, xmm", (MAXSD(xmm7, xmm7),)))
instruction_list.append(("MAXSD xmm, m64", (MOV(esi, esi), MAXSD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CMPSD xmm, xmm, imm8", (CMPSD(xmm7, xmm7, 2),)))
instruction_list.append(("CMPSD xmm, m64, imm8", (MOV(esi, esi), CMPSD(xmm7, qword[r15+rsi*1+64], 2))))

instruction_list.append(("COMISD xmm, xmm", (COMISD(xmm7, xmm7),)))
instruction_list.append(("COMISD xmm, m64", (MOV(esi, esi), COMISD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("UCOMISD xmm, xmm", (UCOMISD(xmm7, xmm7),)))
instruction_list.append(("UCOMISD xmm, m64", (MOV(esi, esi), UCOMISD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("MOVAPS xmm, xmm", (MOVAPS(xmm7, xmm7),)))
instruction_list.append(("MOVAPS xmm, m128", (MOV(esi, esi), MOVAPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVAPS m128, xmm", (MOV(esi, esi), MOVAPS(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVUPS xmm, xmm", (MOVUPS(xmm7, xmm7),)))
instruction_list.append(("MOVUPS xmm, m128", (MOV(esi, esi), MOVUPS(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVUPS m128, xmm", (MOV(esi, esi), MOVUPS(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVLPS xmm, m64", (MOV(esi, esi), MOVLPS(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVLPS m64, xmm", (MOV(esi, esi), MOVLPS(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("MOVNTPS m128, xmm", (MOV(esi, esi), MOVNTPS(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVHPS xmm, m64", (MOV(esi, esi), MOVHPS(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVHPS m64, xmm", (MOV(esi, esi), MOVHPS(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("MOVSLDUP xmm, xmm", (MOVSLDUP(xmm7, xmm7),)))
instruction_list.append(("MOVSLDUP xmm, m128", (MOV(esi, esi), MOVSLDUP(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MOVSHDUP xmm, xmm", (MOVSHDUP(xmm7, xmm7),)))
instruction_list.append(("MOVSHDUP xmm, m128", (MOV(esi, esi), MOVSHDUP(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MOVAPD xmm, xmm", (MOVAPD(xmm7, xmm7),)))
instruction_list.append(("MOVAPD xmm, m128", (MOV(esi, esi), MOVAPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVAPD m128, xmm", (MOV(esi, esi), MOVAPD(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVUPD xmm, xmm", (MOVUPD(xmm7, xmm7),)))
instruction_list.append(("MOVUPD xmm, m128", (MOV(esi, esi), MOVUPD(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVUPD m128, xmm", (MOV(esi, esi), MOVUPD(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVLPD xmm, m64", (MOV(esi, esi), MOVLPD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVLPD m64, xmm", (MOV(esi, esi), MOVLPD(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("MOVNTPD m128, xmm", (MOV(esi, esi), MOVNTPD(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVHPD xmm, m64", (MOV(esi, esi), MOVHPD(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVHPD m64, xmm", (MOV(esi, esi), MOVHPD(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("MOVDDUP xmm, xmm", (MOVDDUP(xmm7, xmm7),)))
instruction_list.append(("MOVDDUP xmm, m64", (MOV(esi, esi), MOVDDUP(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("ADDPS xmm, xmm", (ADDPS(xmm7, xmm7),)))
instruction_list.append(("ADDPS xmm, m128", (MOV(esi, esi), ADDPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("HADDPS xmm, xmm", (HADDPS(xmm7, xmm7),)))
instruction_list.append(("HADDPS xmm, m128", (MOV(esi, esi), HADDPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SUBPS xmm, xmm", (SUBPS(xmm7, xmm7),)))
instruction_list.append(("SUBPS xmm, m128", (MOV(esi, esi), SUBPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("HSUBPS xmm, xmm", (HSUBPS(xmm7, xmm7),)))
instruction_list.append(("HSUBPS xmm, m128", (MOV(esi, esi), HSUBPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ADDSUBPS xmm, xmm", (ADDSUBPS(xmm7, xmm7),)))
instruction_list.append(("ADDSUBPS xmm, m128", (MOV(esi, esi), ADDSUBPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MULPS xmm, xmm", (MULPS(xmm7, xmm7),)))
instruction_list.append(("MULPS xmm, m128", (MOV(esi, esi), MULPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("DIVPS xmm, xmm", (DIVPS(xmm7, xmm7),)))
instruction_list.append(("DIVPS xmm, m128", (MOV(esi, esi), DIVPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SQRTPS xmm, xmm", (SQRTPS(xmm7, xmm7),)))
instruction_list.append(("SQRTPS xmm, m128", (MOV(esi, esi), SQRTPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ADDPD xmm, xmm", (ADDPD(xmm7, xmm7),)))
instruction_list.append(("ADDPD xmm, m128", (MOV(esi, esi), ADDPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("HADDPD xmm, xmm", (HADDPD(xmm7, xmm7),)))
instruction_list.append(("HADDPD xmm, m128", (MOV(esi, esi), HADDPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SUBPD xmm, xmm", (SUBPD(xmm7, xmm7),)))
instruction_list.append(("SUBPD xmm, m128", (MOV(esi, esi), SUBPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("HSUBPD xmm, xmm", (HSUBPD(xmm7, xmm7),)))
instruction_list.append(("HSUBPD xmm, m128", (MOV(esi, esi), HSUBPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ADDSUBPD xmm, xmm", (ADDSUBPD(xmm7, xmm7),)))
instruction_list.append(("ADDSUBPD xmm, m128", (MOV(esi, esi), ADDSUBPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MULPD xmm, xmm", (MULPD(xmm7, xmm7),)))
instruction_list.append(("MULPD xmm, m128", (MOV(esi, esi), MULPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("DIVPD xmm, xmm", (DIVPD(xmm7, xmm7),)))
instruction_list.append(("DIVPD xmm, m128", (MOV(esi, esi), DIVPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SQRTPD xmm, xmm", (SQRTPD(xmm7, xmm7),)))
instruction_list.append(("SQRTPD xmm, m128", (MOV(esi, esi), SQRTPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ROUNDPS xmm, xmm, imm8", (ROUNDPS(xmm7, xmm7, 2),)))
instruction_list.append(("ROUNDPS xmm, m128, imm8", (MOV(esi, esi), ROUNDPS(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("MINPS xmm, xmm", (MINPS(xmm7, xmm7),)))
instruction_list.append(("MINPS xmm, m128", (MOV(esi, esi), MINPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MAXPS xmm, xmm", (MAXPS(xmm7, xmm7),)))
instruction_list.append(("MAXPS xmm, m128", (MOV(esi, esi), MAXPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("RCPPS xmm, xmm", (RCPPS(xmm7, xmm7),)))
instruction_list.append(("RCPPS xmm, m128", (MOV(esi, esi), RCPPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("RSQRTPS xmm, xmm", (RSQRTPS(xmm7, xmm7),)))
instruction_list.append(("RSQRTPS xmm, m128", (MOV(esi, esi), RSQRTPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("DPPS xmm, xmm, imm8", (DPPS(xmm7, xmm7, 2),)))
instruction_list.append(("DPPS xmm, m128, imm8", (MOV(esi, esi), DPPS(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("CMPPS xmm, xmm, imm8", (CMPPS(xmm7, xmm7, 2),)))
instruction_list.append(("CMPPS xmm, m128, imm8", (MOV(esi, esi), CMPPS(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("MOVMSKPS r32, xmm", (MOVMSKPS(ebx, xmm7),)))

instruction_list.append(("ROUNDPD xmm, xmm, imm8", (ROUNDPD(xmm7, xmm7, 2),)))
instruction_list.append(("ROUNDPD xmm, m128, imm8", (MOV(esi, esi), ROUNDPD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("MINPD xmm, xmm", (MINPD(xmm7, xmm7),)))
instruction_list.append(("MINPD xmm, m128", (MOV(esi, esi), MINPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MAXPD xmm, xmm", (MAXPD(xmm7, xmm7),)))
instruction_list.append(("MAXPD xmm, m128", (MOV(esi, esi), MAXPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("DPPD xmm, xmm, imm8", (DPPD(xmm7, xmm7, 2),)))
instruction_list.append(("DPPD xmm, m128, imm8", (MOV(esi, esi), DPPD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("CMPPD xmm, xmm, imm8", (CMPPD(xmm7, xmm7, 2),)))
instruction_list.append(("CMPPD xmm, m128, imm8", (MOV(esi, esi), CMPPD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("MOVMSKPD r32, xmm", (MOVMSKPD(ebx, xmm7),)))

instruction_list.append(("ANDPS xmm, xmm", (ANDPS(xmm7, xmm7),)))
instruction_list.append(("ANDPS xmm, m128", (MOV(esi, esi), ANDPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ANDNPS xmm, xmm", (ANDNPS(xmm7, xmm7),)))
instruction_list.append(("ANDNPS xmm, m128", (MOV(esi, esi), ANDNPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ORPS xmm, xmm", (ORPS(xmm7, xmm7),)))
instruction_list.append(("ORPS xmm, m128", (MOV(esi, esi), ORPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("XORPS xmm, xmm", (XORPS(xmm7, xmm7),)))
instruction_list.append(("XORPS xmm, m128", (MOV(esi, esi), XORPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("BLENDPS xmm, xmm, imm8", (BLENDPS(xmm7, xmm7, 2),)))
instruction_list.append(("BLENDPS xmm, m128, imm8", (MOV(esi, esi), BLENDPS(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("BLENDVPS xmm, xmm, xmm0", (BLENDVPS(xmm7, xmm7, xmm0),)))
instruction_list.append(("BLENDVPS xmm, m128, xmm0", (MOV(esi, esi), BLENDVPS(xmm7, oword[r15+rsi*1+128], xmm0))))

instruction_list.append(("ANDPD xmm, xmm", (ANDPD(xmm7, xmm7),)))
instruction_list.append(("ANDPD xmm, m128", (MOV(esi, esi), ANDPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ANDNPD xmm, xmm", (ANDNPD(xmm7, xmm7),)))
instruction_list.append(("ANDNPD xmm, m128", (MOV(esi, esi), ANDNPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("ORPD xmm, xmm", (ORPD(xmm7, xmm7),)))
instruction_list.append(("ORPD xmm, m128", (MOV(esi, esi), ORPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("XORPD xmm, xmm", (XORPD(xmm7, xmm7),)))
instruction_list.append(("XORPD xmm, m128", (MOV(esi, esi), XORPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("BLENDPD xmm, xmm, imm8", (BLENDPD(xmm7, xmm7, 2),)))
instruction_list.append(("BLENDPD xmm, m128, imm8", (MOV(esi, esi), BLENDPD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("BLENDVPD xmm, xmm, xmm0", (BLENDVPD(xmm7, xmm7, xmm0),)))
instruction_list.append(("BLENDVPD xmm, m128, xmm0", (MOV(esi, esi), BLENDVPD(xmm7, oword[r15+rsi*1+128], xmm0))))

instruction_list.append(("UNPCKLPS xmm, xmm", (UNPCKLPS(xmm7, xmm7),)))
instruction_list.append(("UNPCKLPS xmm, m128", (MOV(esi, esi), UNPCKLPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("UNPCKHPS xmm, xmm", (UNPCKHPS(xmm7, xmm7),)))
instruction_list.append(("UNPCKHPS xmm, m128", (MOV(esi, esi), UNPCKHPS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MOVLHPS xmm, xmm", (MOVLHPS(xmm7, xmm7),)))

instruction_list.append(("MOVHLPS xmm, xmm", (MOVHLPS(xmm7, xmm7),)))

instruction_list.append(("SHUFPS xmm, xmm, imm8", (SHUFPS(xmm7, xmm7, 2),)))
instruction_list.append(("SHUFPS xmm, m128, imm8", (MOV(esi, esi), SHUFPS(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("UNPCKLPD xmm, xmm", (UNPCKLPD(xmm7, xmm7),)))
instruction_list.append(("UNPCKLPD xmm, m128", (MOV(esi, esi), UNPCKLPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("UNPCKHPD xmm, xmm", (UNPCKHPD(xmm7, xmm7),)))
instruction_list.append(("UNPCKHPD xmm, m128", (MOV(esi, esi), UNPCKHPD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("SHUFPD xmm, xmm, imm8", (SHUFPD(xmm7, xmm7, 2),)))
instruction_list.append(("SHUFPD xmm, m128, imm8", (MOV(esi, esi), SHUFPD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("MOVD r32, mm", (MOVD(ebx, mm4),)))
instruction_list.append(("MOVD r32, xmm", (MOVD(ebx, xmm7),)))
instruction_list.append(("MOVD mm, r32", (MOVD(mm4, ebx),)))
instruction_list.append(("MOVD mm, m32", (MOV(esi, esi), MOVD(mm4, dword[r15+rsi*1+32]))))
instruction_list.append(("MOVD xmm, r32", (MOVD(xmm7, ebx),)))
instruction_list.append(("MOVD xmm, m32", (MOV(esi, esi), MOVD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("MOVD m32, mm", (MOV(esi, esi), MOVD(dword[r15+rsi*1+32], mm4))))
instruction_list.append(("MOVD m32, xmm", (MOV(esi, esi), MOVD(dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("MOVQ r64, mm", (MOVQ(rdi, mm4),)))
instruction_list.append(("MOVQ r64, xmm", (MOVQ(rdi, xmm7),)))
instruction_list.append(("MOVQ mm, r64", (MOVQ(mm4, rdi),)))
instruction_list.append(("MOVQ mm, mm", (MOVQ(mm4, mm4),)))
instruction_list.append(("MOVQ mm, m64", (MOV(esi, esi), MOVQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVQ xmm, r64", (MOVQ(xmm7, rdi),)))
instruction_list.append(("MOVQ xmm, xmm", (MOVQ(xmm7, xmm7),)))
instruction_list.append(("MOVQ xmm, m64", (MOV(esi, esi), MOVQ(xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("MOVQ m64, mm", (MOV(esi, esi), MOVQ(qword[r15+rsi*1+64], mm4))))
instruction_list.append(("MOVQ m64, xmm", (MOV(esi, esi), MOVQ(qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("MOVDQ2Q mm, xmm", (MOVDQ2Q(mm4, xmm7),)))

instruction_list.append(("MOVQ2DQ xmm, mm", (MOVQ2DQ(xmm7, mm4),)))

instruction_list.append(("MOVDQA xmm, xmm", (MOVDQA(xmm7, xmm7),)))
instruction_list.append(("MOVDQA xmm, m128", (MOV(esi, esi), MOVDQA(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVDQA m128, xmm", (MOV(esi, esi), MOVDQA(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVDQU xmm, xmm", (MOVDQU(xmm7, xmm7),)))
instruction_list.append(("MOVDQU xmm, m128", (MOV(esi, esi), MOVDQU(xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("MOVDQU m128, xmm", (MOV(esi, esi), MOVDQU(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("LDDQU xmm, m128", (MOV(esi, esi), LDDQU(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MASKMOVQ mm, mm", (MASKMOVQ(mm4, mm4),)))

instruction_list.append(("MASKMOVDQU xmm, xmm", (MASKMOVDQU(xmm7, xmm7),)))

instruction_list.append(("MOVNTQ m64, mm", (MOV(esi, esi), MOVNTQ(qword[r15+rsi*1+64], mm4))))

instruction_list.append(("MOVNTDQ m128, xmm", (MOV(esi, esi), MOVNTDQ(oword[r15+rsi*1+128], xmm7))))

instruction_list.append(("MOVNTDQA xmm, m128", (MOV(esi, esi), MOVNTDQA(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMOVSXBW xmm, xmm", (PMOVSXBW(xmm7, xmm7),)))
instruction_list.append(("PMOVSXBW xmm, m64", (MOV(esi, esi), PMOVSXBW(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PMOVSXBD xmm, xmm", (PMOVSXBD(xmm7, xmm7),)))
instruction_list.append(("PMOVSXBD xmm, m32", (MOV(esi, esi), PMOVSXBD(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("PMOVSXBQ xmm, xmm", (PMOVSXBQ(xmm7, xmm7),)))
instruction_list.append(("PMOVSXBQ xmm, m16", (MOV(esi, esi), PMOVSXBQ(xmm7, word[r15+rsi*1+16]))))

instruction_list.append(("PMOVSXWD xmm, xmm", (PMOVSXWD(xmm7, xmm7),)))
instruction_list.append(("PMOVSXWD xmm, m64", (MOV(esi, esi), PMOVSXWD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PMOVSXWQ xmm, xmm", (PMOVSXWQ(xmm7, xmm7),)))
instruction_list.append(("PMOVSXWQ xmm, m32", (MOV(esi, esi), PMOVSXWQ(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("PMOVSXDQ xmm, xmm", (PMOVSXDQ(xmm7, xmm7),)))
instruction_list.append(("PMOVSXDQ xmm, m64", (MOV(esi, esi), PMOVSXDQ(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PMOVZXBW xmm, xmm", (PMOVZXBW(xmm7, xmm7),)))
instruction_list.append(("PMOVZXBW xmm, m64", (MOV(esi, esi), PMOVZXBW(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PMOVZXBD xmm, xmm", (PMOVZXBD(xmm7, xmm7),)))
instruction_list.append(("PMOVZXBD xmm, m32", (MOV(esi, esi), PMOVZXBD(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("PMOVZXBQ xmm, xmm", (PMOVZXBQ(xmm7, xmm7),)))
instruction_list.append(("PMOVZXBQ xmm, m16", (MOV(esi, esi), PMOVZXBQ(xmm7, word[r15+rsi*1+16]))))

instruction_list.append(("PMOVZXWD xmm, xmm", (PMOVZXWD(xmm7, xmm7),)))
instruction_list.append(("PMOVZXWD xmm, m64", (MOV(esi, esi), PMOVZXWD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PMOVZXWQ xmm, xmm", (PMOVZXWQ(xmm7, xmm7),)))
instruction_list.append(("PMOVZXWQ xmm, m32", (MOV(esi, esi), PMOVZXWQ(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("PMOVZXDQ xmm, xmm", (PMOVZXDQ(xmm7, xmm7),)))
instruction_list.append(("PMOVZXDQ xmm, m64", (MOV(esi, esi), PMOVZXDQ(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("PEXTRB r32, xmm, imm8", (PEXTRB(ebx, xmm7, 2),)))
instruction_list.append(("PEXTRB m8, xmm, imm8", (MOV(esi, esi), PEXTRB(byte[r15+rsi*1+8], xmm7, 2))))

instruction_list.append(("PEXTRW r32, mm, imm8", (PEXTRW(ebx, mm4, 2),)))
instruction_list.append(("PEXTRW r32, xmm, imm8", (PEXTRW(ebx, xmm7, 2),)))
instruction_list.append(("PEXTRW m16, xmm, imm8", (MOV(esi, esi), PEXTRW(word[r15+rsi*1+16], xmm7, 2))))

instruction_list.append(("PEXTRD r32, xmm, imm8", (PEXTRD(ebx, xmm7, 2),)))
instruction_list.append(("PEXTRD m32, xmm, imm8", (MOV(esi, esi), PEXTRD(dword[r15+rsi*1+32], xmm7, 2))))

instruction_list.append(("PEXTRQ r64, xmm, imm8", (PEXTRQ(rdi, xmm7, 2),)))
instruction_list.append(("PEXTRQ m64, xmm, imm8", (MOV(esi, esi), PEXTRQ(qword[r15+rsi*1+64], xmm7, 2))))

instruction_list.append(("PINSRB xmm, r32, imm8", (PINSRB(xmm7, ebx, 2),)))
instruction_list.append(("PINSRB xmm, m8, imm8", (MOV(esi, esi), PINSRB(xmm7, byte[r15+rsi*1+8], 2))))

instruction_list.append(("PINSRW mm, r32, imm8", (PINSRW(mm4, ebx, 2),)))
instruction_list.append(("PINSRW mm, m16, imm8", (MOV(esi, esi), PINSRW(mm4, word[r15+rsi*1+16], 2))))
instruction_list.append(("PINSRW xmm, r32, imm8", (PINSRW(xmm7, ebx, 2),)))
instruction_list.append(("PINSRW xmm, m16, imm8", (MOV(esi, esi), PINSRW(xmm7, word[r15+rsi*1+16], 2))))

instruction_list.append(("PINSRD xmm, r32, imm8", (PINSRD(xmm7, ebx, 2),)))
instruction_list.append(("PINSRD xmm, m32, imm8", (MOV(esi, esi), PINSRD(xmm7, dword[r15+rsi*1+32], 2))))

instruction_list.append(("PINSRQ xmm, r64, imm8", (PINSRQ(xmm7, rdi, 2),)))
instruction_list.append(("PINSRQ xmm, m64, imm8", (MOV(esi, esi), PINSRQ(xmm7, qword[r15+rsi*1+64], 2))))

instruction_list.append(("PMOVMSKB r32, mm", (PMOVMSKB(ebx, mm4),)))
instruction_list.append(("PMOVMSKB r32, xmm", (PMOVMSKB(ebx, xmm7),)))

instruction_list.append(("PTEST xmm, xmm", (PTEST(xmm7, xmm7),)))
instruction_list.append(("PTEST xmm, m128", (MOV(esi, esi), PTEST(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDB mm, mm", (PADDB(mm4, mm4),)))
instruction_list.append(("PADDB mm, m64", (MOV(esi, esi), PADDB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDB xmm, xmm", (PADDB(xmm7, xmm7),)))
instruction_list.append(("PADDB xmm, m128", (MOV(esi, esi), PADDB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDW mm, mm", (PADDW(mm4, mm4),)))
instruction_list.append(("PADDW mm, m64", (MOV(esi, esi), PADDW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDW xmm, xmm", (PADDW(xmm7, xmm7),)))
instruction_list.append(("PADDW xmm, m128", (MOV(esi, esi), PADDW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDD mm, mm", (PADDD(mm4, mm4),)))
instruction_list.append(("PADDD mm, m64", (MOV(esi, esi), PADDD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDD xmm, xmm", (PADDD(xmm7, xmm7),)))
instruction_list.append(("PADDD xmm, m128", (MOV(esi, esi), PADDD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDQ mm, mm", (PADDQ(mm4, mm4),)))
instruction_list.append(("PADDQ mm, m64", (MOV(esi, esi), PADDQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDQ xmm, xmm", (PADDQ(xmm7, xmm7),)))
instruction_list.append(("PADDQ xmm, m128", (MOV(esi, esi), PADDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDSB mm, mm", (PADDSB(mm4, mm4),)))
instruction_list.append(("PADDSB mm, m64", (MOV(esi, esi), PADDSB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDSB xmm, xmm", (PADDSB(xmm7, xmm7),)))
instruction_list.append(("PADDSB xmm, m128", (MOV(esi, esi), PADDSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDSW mm, mm", (PADDSW(mm4, mm4),)))
instruction_list.append(("PADDSW mm, m64", (MOV(esi, esi), PADDSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDSW xmm, xmm", (PADDSW(xmm7, xmm7),)))
instruction_list.append(("PADDSW xmm, m128", (MOV(esi, esi), PADDSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDUSB mm, mm", (PADDUSB(mm4, mm4),)))
instruction_list.append(("PADDUSB mm, m64", (MOV(esi, esi), PADDUSB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDUSB xmm, xmm", (PADDUSB(xmm7, xmm7),)))
instruction_list.append(("PADDUSB xmm, m128", (MOV(esi, esi), PADDUSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PADDUSW mm, mm", (PADDUSW(mm4, mm4),)))
instruction_list.append(("PADDUSW mm, m64", (MOV(esi, esi), PADDUSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PADDUSW xmm, xmm", (PADDUSW(xmm7, xmm7),)))
instruction_list.append(("PADDUSW xmm, m128", (MOV(esi, esi), PADDUSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHADDW mm, mm", (PHADDW(mm4, mm4),)))
instruction_list.append(("PHADDW mm, m64", (MOV(esi, esi), PHADDW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHADDW xmm, xmm", (PHADDW(xmm7, xmm7),)))
instruction_list.append(("PHADDW xmm, m128", (MOV(esi, esi), PHADDW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHADDD mm, mm", (PHADDD(mm4, mm4),)))
instruction_list.append(("PHADDD mm, m64", (MOV(esi, esi), PHADDD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHADDD xmm, xmm", (PHADDD(xmm7, xmm7),)))
instruction_list.append(("PHADDD xmm, m128", (MOV(esi, esi), PHADDD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHADDSW mm, mm", (PHADDSW(mm4, mm4),)))
instruction_list.append(("PHADDSW mm, m64", (MOV(esi, esi), PHADDSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHADDSW xmm, xmm", (PHADDSW(xmm7, xmm7),)))
instruction_list.append(("PHADDSW xmm, m128", (MOV(esi, esi), PHADDSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBB mm, mm", (PSUBB(mm4, mm4),)))
instruction_list.append(("PSUBB mm, m64", (MOV(esi, esi), PSUBB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBB xmm, xmm", (PSUBB(xmm7, xmm7),)))
instruction_list.append(("PSUBB xmm, m128", (MOV(esi, esi), PSUBB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBW mm, mm", (PSUBW(mm4, mm4),)))
instruction_list.append(("PSUBW mm, m64", (MOV(esi, esi), PSUBW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBW xmm, xmm", (PSUBW(xmm7, xmm7),)))
instruction_list.append(("PSUBW xmm, m128", (MOV(esi, esi), PSUBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBD mm, mm", (PSUBD(mm4, mm4),)))
instruction_list.append(("PSUBD mm, m64", (MOV(esi, esi), PSUBD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBD xmm, xmm", (PSUBD(xmm7, xmm7),)))
instruction_list.append(("PSUBD xmm, m128", (MOV(esi, esi), PSUBD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBQ mm, mm", (PSUBQ(mm4, mm4),)))
instruction_list.append(("PSUBQ mm, m64", (MOV(esi, esi), PSUBQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBQ xmm, xmm", (PSUBQ(xmm7, xmm7),)))
instruction_list.append(("PSUBQ xmm, m128", (MOV(esi, esi), PSUBQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBSB mm, mm", (PSUBSB(mm4, mm4),)))
instruction_list.append(("PSUBSB mm, m64", (MOV(esi, esi), PSUBSB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBSB xmm, xmm", (PSUBSB(xmm7, xmm7),)))
instruction_list.append(("PSUBSB xmm, m128", (MOV(esi, esi), PSUBSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBSW mm, mm", (PSUBSW(mm4, mm4),)))
instruction_list.append(("PSUBSW mm, m64", (MOV(esi, esi), PSUBSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBSW xmm, xmm", (PSUBSW(xmm7, xmm7),)))
instruction_list.append(("PSUBSW xmm, m128", (MOV(esi, esi), PSUBSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBUSB mm, mm", (PSUBUSB(mm4, mm4),)))
instruction_list.append(("PSUBUSB mm, m64", (MOV(esi, esi), PSUBUSB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBUSB xmm, xmm", (PSUBUSB(xmm7, xmm7),)))
instruction_list.append(("PSUBUSB xmm, m128", (MOV(esi, esi), PSUBUSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSUBUSW mm, mm", (PSUBUSW(mm4, mm4),)))
instruction_list.append(("PSUBUSW mm, m64", (MOV(esi, esi), PSUBUSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSUBUSW xmm, xmm", (PSUBUSW(xmm7, xmm7),)))
instruction_list.append(("PSUBUSW xmm, m128", (MOV(esi, esi), PSUBUSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHSUBW mm, mm", (PHSUBW(mm4, mm4),)))
instruction_list.append(("PHSUBW mm, m64", (MOV(esi, esi), PHSUBW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHSUBW xmm, xmm", (PHSUBW(xmm7, xmm7),)))
instruction_list.append(("PHSUBW xmm, m128", (MOV(esi, esi), PHSUBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHSUBD mm, mm", (PHSUBD(mm4, mm4),)))
instruction_list.append(("PHSUBD mm, m64", (MOV(esi, esi), PHSUBD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHSUBD xmm, xmm", (PHSUBD(xmm7, xmm7),)))
instruction_list.append(("PHSUBD xmm, m128", (MOV(esi, esi), PHSUBD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PHSUBSW mm, mm", (PHSUBSW(mm4, mm4),)))
instruction_list.append(("PHSUBSW mm, m64", (MOV(esi, esi), PHSUBSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PHSUBSW xmm, xmm", (PHSUBSW(xmm7, xmm7),)))
instruction_list.append(("PHSUBSW xmm, m128", (MOV(esi, esi), PHSUBSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXSB xmm, xmm", (PMAXSB(xmm7, xmm7),)))
instruction_list.append(("PMAXSB xmm, m128", (MOV(esi, esi), PMAXSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXSW mm, mm", (PMAXSW(mm4, mm4),)))
instruction_list.append(("PMAXSW mm, m64", (MOV(esi, esi), PMAXSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMAXSW xmm, xmm", (PMAXSW(xmm7, xmm7),)))
instruction_list.append(("PMAXSW xmm, m128", (MOV(esi, esi), PMAXSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXSD xmm, xmm", (PMAXSD(xmm7, xmm7),)))
instruction_list.append(("PMAXSD xmm, m128", (MOV(esi, esi), PMAXSD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXUB mm, mm", (PMAXUB(mm4, mm4),)))
instruction_list.append(("PMAXUB mm, m64", (MOV(esi, esi), PMAXUB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMAXUB xmm, xmm", (PMAXUB(xmm7, xmm7),)))
instruction_list.append(("PMAXUB xmm, m128", (MOV(esi, esi), PMAXUB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXUW xmm, xmm", (PMAXUW(xmm7, xmm7),)))
instruction_list.append(("PMAXUW xmm, m128", (MOV(esi, esi), PMAXUW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMAXUD xmm, xmm", (PMAXUD(xmm7, xmm7),)))
instruction_list.append(("PMAXUD xmm, m128", (MOV(esi, esi), PMAXUD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINSB xmm, xmm", (PMINSB(xmm7, xmm7),)))
instruction_list.append(("PMINSB xmm, m128", (MOV(esi, esi), PMINSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINSW mm, mm", (PMINSW(mm4, mm4),)))
instruction_list.append(("PMINSW mm, m64", (MOV(esi, esi), PMINSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMINSW xmm, xmm", (PMINSW(xmm7, xmm7),)))
instruction_list.append(("PMINSW xmm, m128", (MOV(esi, esi), PMINSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINSD xmm, xmm", (PMINSD(xmm7, xmm7),)))
instruction_list.append(("PMINSD xmm, m128", (MOV(esi, esi), PMINSD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINUB mm, mm", (PMINUB(mm4, mm4),)))
instruction_list.append(("PMINUB mm, m64", (MOV(esi, esi), PMINUB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMINUB xmm, xmm", (PMINUB(xmm7, xmm7),)))
instruction_list.append(("PMINUB xmm, m128", (MOV(esi, esi), PMINUB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINUW xmm, xmm", (PMINUW(xmm7, xmm7),)))
instruction_list.append(("PMINUW xmm, m128", (MOV(esi, esi), PMINUW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMINUD xmm, xmm", (PMINUD(xmm7, xmm7),)))
instruction_list.append(("PMINUD xmm, m128", (MOV(esi, esi), PMINUD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSLLW mm, imm8", (PSLLW(mm4, 2),)))
instruction_list.append(("PSLLW mm, mm", (PSLLW(mm4, mm4),)))
instruction_list.append(("PSLLW mm, m64", (MOV(esi, esi), PSLLW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSLLW xmm, imm8", (PSLLW(xmm7, 2),)))
instruction_list.append(("PSLLW xmm, xmm", (PSLLW(xmm7, xmm7),)))
instruction_list.append(("PSLLW xmm, m128", (MOV(esi, esi), PSLLW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSLLD mm, imm8", (PSLLD(mm4, 2),)))
instruction_list.append(("PSLLD mm, mm", (PSLLD(mm4, mm4),)))
instruction_list.append(("PSLLD mm, m64", (MOV(esi, esi), PSLLD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSLLD xmm, imm8", (PSLLD(xmm7, 2),)))
instruction_list.append(("PSLLD xmm, xmm", (PSLLD(xmm7, xmm7),)))
instruction_list.append(("PSLLD xmm, m128", (MOV(esi, esi), PSLLD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSLLQ mm, imm8", (PSLLQ(mm4, 2),)))
instruction_list.append(("PSLLQ mm, mm", (PSLLQ(mm4, mm4),)))
instruction_list.append(("PSLLQ mm, m64", (MOV(esi, esi), PSLLQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSLLQ xmm, imm8", (PSLLQ(xmm7, 2),)))
instruction_list.append(("PSLLQ xmm, xmm", (PSLLQ(xmm7, xmm7),)))
instruction_list.append(("PSLLQ xmm, m128", (MOV(esi, esi), PSLLQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSRLW mm, imm8", (PSRLW(mm4, 2),)))
instruction_list.append(("PSRLW mm, mm", (PSRLW(mm4, mm4),)))
instruction_list.append(("PSRLW mm, m64", (MOV(esi, esi), PSRLW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSRLW xmm, imm8", (PSRLW(xmm7, 2),)))
instruction_list.append(("PSRLW xmm, xmm", (PSRLW(xmm7, xmm7),)))
instruction_list.append(("PSRLW xmm, m128", (MOV(esi, esi), PSRLW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSRLD mm, imm8", (PSRLD(mm4, 2),)))
instruction_list.append(("PSRLD mm, mm", (PSRLD(mm4, mm4),)))
instruction_list.append(("PSRLD mm, m64", (MOV(esi, esi), PSRLD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSRLD xmm, imm8", (PSRLD(xmm7, 2),)))
instruction_list.append(("PSRLD xmm, xmm", (PSRLD(xmm7, xmm7),)))
instruction_list.append(("PSRLD xmm, m128", (MOV(esi, esi), PSRLD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSRLQ mm, imm8", (PSRLQ(mm4, 2),)))
instruction_list.append(("PSRLQ mm, mm", (PSRLQ(mm4, mm4),)))
instruction_list.append(("PSRLQ mm, m64", (MOV(esi, esi), PSRLQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSRLQ xmm, imm8", (PSRLQ(xmm7, 2),)))
instruction_list.append(("PSRLQ xmm, xmm", (PSRLQ(xmm7, xmm7),)))
instruction_list.append(("PSRLQ xmm, m128", (MOV(esi, esi), PSRLQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSRAW mm, imm8", (PSRAW(mm4, 2),)))
instruction_list.append(("PSRAW mm, mm", (PSRAW(mm4, mm4),)))
instruction_list.append(("PSRAW mm, m64", (MOV(esi, esi), PSRAW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSRAW xmm, imm8", (PSRAW(xmm7, 2),)))
instruction_list.append(("PSRAW xmm, xmm", (PSRAW(xmm7, xmm7),)))
instruction_list.append(("PSRAW xmm, m128", (MOV(esi, esi), PSRAW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSRAD mm, imm8", (PSRAD(mm4, 2),)))
instruction_list.append(("PSRAD mm, mm", (PSRAD(mm4, mm4),)))
instruction_list.append(("PSRAD mm, m64", (MOV(esi, esi), PSRAD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSRAD xmm, imm8", (PSRAD(xmm7, 2),)))
instruction_list.append(("PSRAD xmm, xmm", (PSRAD(xmm7, xmm7),)))
instruction_list.append(("PSRAD xmm, m128", (MOV(esi, esi), PSRAD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULLW mm, mm", (PMULLW(mm4, mm4),)))
instruction_list.append(("PMULLW mm, m64", (MOV(esi, esi), PMULLW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMULLW xmm, xmm", (PMULLW(xmm7, xmm7),)))
instruction_list.append(("PMULLW xmm, m128", (MOV(esi, esi), PMULLW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULHW mm, mm", (PMULHW(mm4, mm4),)))
instruction_list.append(("PMULHW mm, m64", (MOV(esi, esi), PMULHW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMULHW xmm, xmm", (PMULHW(xmm7, xmm7),)))
instruction_list.append(("PMULHW xmm, m128", (MOV(esi, esi), PMULHW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULHUW mm, mm", (PMULHUW(mm4, mm4),)))
instruction_list.append(("PMULHUW mm, m64", (MOV(esi, esi), PMULHUW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMULHUW xmm, xmm", (PMULHUW(xmm7, xmm7),)))
instruction_list.append(("PMULHUW xmm, m128", (MOV(esi, esi), PMULHUW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULLD xmm, xmm", (PMULLD(xmm7, xmm7),)))
instruction_list.append(("PMULLD xmm, m128", (MOV(esi, esi), PMULLD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULDQ xmm, xmm", (PMULDQ(xmm7, xmm7),)))
instruction_list.append(("PMULDQ xmm, m128", (MOV(esi, esi), PMULDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULUDQ mm, mm", (PMULUDQ(mm4, mm4),)))
instruction_list.append(("PMULUDQ mm, m64", (MOV(esi, esi), PMULUDQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMULUDQ xmm, xmm", (PMULUDQ(xmm7, xmm7),)))
instruction_list.append(("PMULUDQ xmm, m128", (MOV(esi, esi), PMULUDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMULHRSW mm, mm", (PMULHRSW(mm4, mm4),)))
instruction_list.append(("PMULHRSW mm, m64", (MOV(esi, esi), PMULHRSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMULHRSW xmm, xmm", (PMULHRSW(xmm7, xmm7),)))
instruction_list.append(("PMULHRSW xmm, m128", (MOV(esi, esi), PMULHRSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMADDWD mm, mm", (PMADDWD(mm4, mm4),)))
instruction_list.append(("PMADDWD mm, m64", (MOV(esi, esi), PMADDWD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMADDWD xmm, xmm", (PMADDWD(xmm7, xmm7),)))
instruction_list.append(("PMADDWD xmm, m128", (MOV(esi, esi), PMADDWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PMADDUBSW mm, mm", (PMADDUBSW(mm4, mm4),)))
instruction_list.append(("PMADDUBSW mm, m64", (MOV(esi, esi), PMADDUBSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PMADDUBSW xmm, xmm", (PMADDUBSW(xmm7, xmm7),)))
instruction_list.append(("PMADDUBSW xmm, m128", (MOV(esi, esi), PMADDUBSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PAVGB mm, mm", (PAVGB(mm4, mm4),)))
instruction_list.append(("PAVGB mm, m64", (MOV(esi, esi), PAVGB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PAVGB xmm, xmm", (PAVGB(xmm7, xmm7),)))
instruction_list.append(("PAVGB xmm, m128", (MOV(esi, esi), PAVGB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PAVGW mm, mm", (PAVGW(mm4, mm4),)))
instruction_list.append(("PAVGW mm, m64", (MOV(esi, esi), PAVGW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PAVGW xmm, xmm", (PAVGW(xmm7, xmm7),)))
instruction_list.append(("PAVGW xmm, m128", (MOV(esi, esi), PAVGW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSADBW mm, mm", (PSADBW(mm4, mm4),)))
instruction_list.append(("PSADBW mm, m64", (MOV(esi, esi), PSADBW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSADBW xmm, xmm", (PSADBW(xmm7, xmm7),)))
instruction_list.append(("PSADBW xmm, m128", (MOV(esi, esi), PSADBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("MPSADBW xmm, xmm, imm8", (MPSADBW(xmm7, xmm7, 2),)))
instruction_list.append(("MPSADBW xmm, m128, imm8", (MOV(esi, esi), MPSADBW(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PHMINPOSUW xmm, xmm", (PHMINPOSUW(xmm7, xmm7),)))
instruction_list.append(("PHMINPOSUW xmm, m128", (MOV(esi, esi), PHMINPOSUW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPEQB mm, mm", (PCMPEQB(mm4, mm4),)))
instruction_list.append(("PCMPEQB mm, m64", (MOV(esi, esi), PCMPEQB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPEQB xmm, xmm", (PCMPEQB(xmm7, xmm7),)))
instruction_list.append(("PCMPEQB xmm, m128", (MOV(esi, esi), PCMPEQB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPEQW mm, mm", (PCMPEQW(mm4, mm4),)))
instruction_list.append(("PCMPEQW mm, m64", (MOV(esi, esi), PCMPEQW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPEQW xmm, xmm", (PCMPEQW(xmm7, xmm7),)))
instruction_list.append(("PCMPEQW xmm, m128", (MOV(esi, esi), PCMPEQW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPEQD mm, mm", (PCMPEQD(mm4, mm4),)))
instruction_list.append(("PCMPEQD mm, m64", (MOV(esi, esi), PCMPEQD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPEQD xmm, xmm", (PCMPEQD(xmm7, xmm7),)))
instruction_list.append(("PCMPEQD xmm, m128", (MOV(esi, esi), PCMPEQD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPEQQ xmm, xmm", (PCMPEQQ(xmm7, xmm7),)))
instruction_list.append(("PCMPEQQ xmm, m128", (MOV(esi, esi), PCMPEQQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPGTB mm, mm", (PCMPGTB(mm4, mm4),)))
instruction_list.append(("PCMPGTB mm, m64", (MOV(esi, esi), PCMPGTB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPGTB xmm, xmm", (PCMPGTB(xmm7, xmm7),)))
instruction_list.append(("PCMPGTB xmm, m128", (MOV(esi, esi), PCMPGTB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPGTW mm, mm", (PCMPGTW(mm4, mm4),)))
instruction_list.append(("PCMPGTW mm, m64", (MOV(esi, esi), PCMPGTW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPGTW xmm, xmm", (PCMPGTW(xmm7, xmm7),)))
instruction_list.append(("PCMPGTW xmm, m128", (MOV(esi, esi), PCMPGTW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPGTD mm, mm", (PCMPGTD(mm4, mm4),)))
instruction_list.append(("PCMPGTD mm, m64", (MOV(esi, esi), PCMPGTD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PCMPGTD xmm, xmm", (PCMPGTD(xmm7, xmm7),)))
instruction_list.append(("PCMPGTD xmm, m128", (MOV(esi, esi), PCMPGTD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PCMPGTQ xmm, xmm", (PCMPGTQ(xmm7, xmm7),)))
instruction_list.append(("PCMPGTQ xmm, m128", (MOV(esi, esi), PCMPGTQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PABSB mm, mm", (PABSB(mm4, mm4),)))
instruction_list.append(("PABSB mm, m64", (MOV(esi, esi), PABSB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PABSB xmm, xmm", (PABSB(xmm7, xmm7),)))
instruction_list.append(("PABSB xmm, m128", (MOV(esi, esi), PABSB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PABSW mm, mm", (PABSW(mm4, mm4),)))
instruction_list.append(("PABSW mm, m64", (MOV(esi, esi), PABSW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PABSW xmm, xmm", (PABSW(xmm7, xmm7),)))
instruction_list.append(("PABSW xmm, m128", (MOV(esi, esi), PABSW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PABSD mm, mm", (PABSD(mm4, mm4),)))
instruction_list.append(("PABSD mm, m64", (MOV(esi, esi), PABSD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PABSD xmm, xmm", (PABSD(xmm7, xmm7),)))
instruction_list.append(("PABSD xmm, m128", (MOV(esi, esi), PABSD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSIGNB mm, mm", (PSIGNB(mm4, mm4),)))
instruction_list.append(("PSIGNB mm, m64", (MOV(esi, esi), PSIGNB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSIGNB xmm, xmm", (PSIGNB(xmm7, xmm7),)))
instruction_list.append(("PSIGNB xmm, m128", (MOV(esi, esi), PSIGNB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSIGNW mm, mm", (PSIGNW(mm4, mm4),)))
instruction_list.append(("PSIGNW mm, m64", (MOV(esi, esi), PSIGNW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSIGNW xmm, xmm", (PSIGNW(xmm7, xmm7),)))
instruction_list.append(("PSIGNW xmm, m128", (MOV(esi, esi), PSIGNW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSIGND mm, mm", (PSIGND(mm4, mm4),)))
instruction_list.append(("PSIGND mm, m64", (MOV(esi, esi), PSIGND(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSIGND xmm, xmm", (PSIGND(xmm7, xmm7),)))
instruction_list.append(("PSIGND xmm, m128", (MOV(esi, esi), PSIGND(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PAND mm, mm", (PAND(mm4, mm4),)))
instruction_list.append(("PAND mm, m64", (MOV(esi, esi), PAND(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PAND xmm, xmm", (PAND(xmm7, xmm7),)))
instruction_list.append(("PAND xmm, m128", (MOV(esi, esi), PAND(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PANDN mm, mm", (PANDN(mm4, mm4),)))
instruction_list.append(("PANDN mm, m64", (MOV(esi, esi), PANDN(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PANDN xmm, xmm", (PANDN(xmm7, xmm7),)))
instruction_list.append(("PANDN xmm, m128", (MOV(esi, esi), PANDN(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("POR mm, mm", (POR(mm4, mm4),)))
instruction_list.append(("POR mm, m64", (MOV(esi, esi), POR(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("POR xmm, xmm", (POR(xmm7, xmm7),)))
instruction_list.append(("POR xmm, m128", (MOV(esi, esi), POR(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PXOR mm, mm", (PXOR(mm4, mm4),)))
instruction_list.append(("PXOR mm, m64", (MOV(esi, esi), PXOR(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PXOR xmm, xmm", (PXOR(xmm7, xmm7),)))
instruction_list.append(("PXOR xmm, m128", (MOV(esi, esi), PXOR(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PBLENDW xmm, xmm, imm8", (PBLENDW(xmm7, xmm7, 2),)))
instruction_list.append(("PBLENDW xmm, m128, imm8", (MOV(esi, esi), PBLENDW(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PBLENDVB xmm, xmm, xmm0", (PBLENDVB(xmm7, xmm7, xmm0),)))
instruction_list.append(("PBLENDVB xmm, m128, xmm0", (MOV(esi, esi), PBLENDVB(xmm7, oword[r15+rsi*1+128], xmm0))))

instruction_list.append(("PUNPCKLBW mm, mm", (PUNPCKLBW(mm4, mm4),)))
instruction_list.append(("PUNPCKLBW mm, m32", (MOV(esi, esi), PUNPCKLBW(mm4, dword[r15+rsi*1+32]))))
instruction_list.append(("PUNPCKLBW xmm, xmm", (PUNPCKLBW(xmm7, xmm7),)))
instruction_list.append(("PUNPCKLBW xmm, m128", (MOV(esi, esi), PUNPCKLBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKLWD mm, mm", (PUNPCKLWD(mm4, mm4),)))
instruction_list.append(("PUNPCKLWD mm, m32", (MOV(esi, esi), PUNPCKLWD(mm4, dword[r15+rsi*1+32]))))
instruction_list.append(("PUNPCKLWD xmm, xmm", (PUNPCKLWD(xmm7, xmm7),)))
instruction_list.append(("PUNPCKLWD xmm, m128", (MOV(esi, esi), PUNPCKLWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKLDQ mm, mm", (PUNPCKLDQ(mm4, mm4),)))
instruction_list.append(("PUNPCKLDQ mm, m32", (MOV(esi, esi), PUNPCKLDQ(mm4, dword[r15+rsi*1+32]))))
instruction_list.append(("PUNPCKLDQ xmm, xmm", (PUNPCKLDQ(xmm7, xmm7),)))
instruction_list.append(("PUNPCKLDQ xmm, m128", (MOV(esi, esi), PUNPCKLDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKLQDQ xmm, xmm", (PUNPCKLQDQ(xmm7, xmm7),)))
instruction_list.append(("PUNPCKLQDQ xmm, m128", (MOV(esi, esi), PUNPCKLQDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKHBW mm, mm", (PUNPCKHBW(mm4, mm4),)))
instruction_list.append(("PUNPCKHBW mm, m64", (MOV(esi, esi), PUNPCKHBW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PUNPCKHBW xmm, xmm", (PUNPCKHBW(xmm7, xmm7),)))
instruction_list.append(("PUNPCKHBW xmm, m128", (MOV(esi, esi), PUNPCKHBW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKHWD mm, mm", (PUNPCKHWD(mm4, mm4),)))
instruction_list.append(("PUNPCKHWD mm, m64", (MOV(esi, esi), PUNPCKHWD(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PUNPCKHWD xmm, xmm", (PUNPCKHWD(xmm7, xmm7),)))
instruction_list.append(("PUNPCKHWD xmm, m128", (MOV(esi, esi), PUNPCKHWD(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKHDQ mm, mm", (PUNPCKHDQ(mm4, mm4),)))
instruction_list.append(("PUNPCKHDQ mm, m64", (MOV(esi, esi), PUNPCKHDQ(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PUNPCKHDQ xmm, xmm", (PUNPCKHDQ(xmm7, xmm7),)))
instruction_list.append(("PUNPCKHDQ xmm, m128", (MOV(esi, esi), PUNPCKHDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PUNPCKHQDQ xmm, xmm", (PUNPCKHQDQ(xmm7, xmm7),)))
instruction_list.append(("PUNPCKHQDQ xmm, m128", (MOV(esi, esi), PUNPCKHQDQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PACKSSWB mm, mm", (PACKSSWB(mm4, mm4),)))
instruction_list.append(("PACKSSWB mm, m64", (MOV(esi, esi), PACKSSWB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PACKSSWB xmm, xmm", (PACKSSWB(xmm7, xmm7),)))
instruction_list.append(("PACKSSWB xmm, m128", (MOV(esi, esi), PACKSSWB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PACKSSDW mm, mm", (PACKSSDW(mm4, mm4),)))
instruction_list.append(("PACKSSDW mm, m64", (MOV(esi, esi), PACKSSDW(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PACKSSDW xmm, xmm", (PACKSSDW(xmm7, xmm7),)))
instruction_list.append(("PACKSSDW xmm, m128", (MOV(esi, esi), PACKSSDW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PACKUSWB mm, mm", (PACKUSWB(mm4, mm4),)))
instruction_list.append(("PACKUSWB mm, m64", (MOV(esi, esi), PACKUSWB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PACKUSWB xmm, xmm", (PACKUSWB(xmm7, xmm7),)))
instruction_list.append(("PACKUSWB xmm, m128", (MOV(esi, esi), PACKUSWB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PACKUSDW xmm, xmm", (PACKUSDW(xmm7, xmm7),)))
instruction_list.append(("PACKUSDW xmm, m128", (MOV(esi, esi), PACKUSDW(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSHUFB mm, mm", (PSHUFB(mm4, mm4),)))
instruction_list.append(("PSHUFB mm, m64", (MOV(esi, esi), PSHUFB(mm4, qword[r15+rsi*1+64]))))
instruction_list.append(("PSHUFB xmm, xmm", (PSHUFB(xmm7, xmm7),)))
instruction_list.append(("PSHUFB xmm, m128", (MOV(esi, esi), PSHUFB(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("PSHUFW mm, mm, imm8", (PSHUFW(mm4, mm4, 2),)))
instruction_list.append(("PSHUFW mm, m64, imm8", (MOV(esi, esi), PSHUFW(mm4, qword[r15+rsi*1+64], 2))))

instruction_list.append(("PSHUFLW xmm, xmm, imm8", (PSHUFLW(xmm7, xmm7, 2),)))
instruction_list.append(("PSHUFLW xmm, m128, imm8", (MOV(esi, esi), PSHUFLW(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PSHUFHW xmm, xmm, imm8", (PSHUFHW(xmm7, xmm7, 2),)))
instruction_list.append(("PSHUFHW xmm, m128, imm8", (MOV(esi, esi), PSHUFHW(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PSHUFD xmm, xmm, imm8", (PSHUFD(xmm7, xmm7, 2),)))
instruction_list.append(("PSHUFD xmm, m128, imm8", (MOV(esi, esi), PSHUFD(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PSLLDQ xmm, imm8", (PSLLDQ(xmm7, 2),)))

instruction_list.append(("PSRLDQ xmm, imm8", (PSRLDQ(xmm7, 2),)))

instruction_list.append(("PALIGNR mm, mm, imm8", (PALIGNR(mm4, mm4, 2),)))
instruction_list.append(("PALIGNR mm, m64, imm8", (MOV(esi, esi), PALIGNR(mm4, qword[r15+rsi*1+64], 2))))
instruction_list.append(("PALIGNR xmm, xmm, imm8", (PALIGNR(xmm7, xmm7, 2),)))
instruction_list.append(("PALIGNR xmm, m128, imm8", (MOV(esi, esi), PALIGNR(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PCMPESTRI xmm, xmm, imm8", (PCMPESTRI(xmm7, xmm7, 2),)))
instruction_list.append(("PCMPESTRI xmm, m128, imm8", (MOV(esi, esi), PCMPESTRI(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PCMPESTRM xmm, xmm, imm8", (PCMPESTRM(xmm7, xmm7, 2),)))
instruction_list.append(("PCMPESTRM xmm, m128, imm8", (MOV(esi, esi), PCMPESTRM(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PCMPISTRI xmm, xmm, imm8", (PCMPISTRI(xmm7, xmm7, 2),)))
instruction_list.append(("PCMPISTRI xmm, m128, imm8", (MOV(esi, esi), PCMPISTRI(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("PCMPISTRM xmm, xmm, imm8", (PCMPISTRM(xmm7, xmm7, 2),)))
instruction_list.append(("PCMPISTRM xmm, m128, imm8", (MOV(esi, esi), PCMPISTRM(xmm7, oword[r15+rsi*1+128], 2))))

instruction_list.append(("CVTSS2SI r32, xmm", (CVTSS2SI(ebx, xmm7),)))
instruction_list.append(("CVTSS2SI r32, m32", (MOV(esi, esi), CVTSS2SI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CVTSS2SI r64, xmm", (CVTSS2SI(rdi, xmm7),)))
instruction_list.append(("CVTSS2SI r64, m32", (MOV(esi, esi), CVTSS2SI(rdi, dword[r15+rsi*1+32]))))

instruction_list.append(("CVTTSS2SI r32, xmm", (CVTTSS2SI(ebx, xmm7),)))
instruction_list.append(("CVTTSS2SI r32, m32", (MOV(esi, esi), CVTTSS2SI(ebx, dword[r15+rsi*1+32]))))
instruction_list.append(("CVTTSS2SI r64, xmm", (CVTTSS2SI(rdi, xmm7),)))
instruction_list.append(("CVTTSS2SI r64, m32", (MOV(esi, esi), CVTTSS2SI(rdi, dword[r15+rsi*1+32]))))

instruction_list.append(("CVTSI2SS xmm, r32", (CVTSI2SS(xmm7, ebx),)))
instruction_list.append(("CVTSI2SS xmm, r64", (CVTSI2SS(xmm7, rdi),)))
instruction_list.append(("CVTSI2SS xmm, m32", (MOV(esi, esi), CVTSI2SS(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("CVTSI2SS xmm, m64", (MOV(esi, esi), CVTSI2SS(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTSD2SI r32, xmm", (CVTSD2SI(ebx, xmm7),)))
instruction_list.append(("CVTSD2SI r32, m64", (MOV(esi, esi), CVTSD2SI(ebx, qword[r15+rsi*1+64]))))
instruction_list.append(("CVTSD2SI r64, xmm", (CVTSD2SI(rdi, xmm7),)))
instruction_list.append(("CVTSD2SI r64, m64", (MOV(esi, esi), CVTSD2SI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTTSD2SI r32, xmm", (CVTTSD2SI(ebx, xmm7),)))
instruction_list.append(("CVTTSD2SI r32, m64", (MOV(esi, esi), CVTTSD2SI(ebx, qword[r15+rsi*1+64]))))
instruction_list.append(("CVTTSD2SI r64, xmm", (CVTTSD2SI(rdi, xmm7),)))
instruction_list.append(("CVTTSD2SI r64, m64", (MOV(esi, esi), CVTTSD2SI(rdi, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTSI2SD xmm, r32", (CVTSI2SD(xmm7, ebx),)))
instruction_list.append(("CVTSI2SD xmm, r64", (CVTSI2SD(xmm7, rdi),)))
instruction_list.append(("CVTSI2SD xmm, m32", (MOV(esi, esi), CVTSI2SD(xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("CVTSI2SD xmm, m64", (MOV(esi, esi), CVTSI2SD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTPS2DQ xmm, xmm", (CVTPS2DQ(xmm7, xmm7),)))
instruction_list.append(("CVTPS2DQ xmm, m128", (MOV(esi, esi), CVTPS2DQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTTPS2DQ xmm, xmm", (CVTTPS2DQ(xmm7, xmm7),)))
instruction_list.append(("CVTTPS2DQ xmm, m128", (MOV(esi, esi), CVTTPS2DQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTDQ2PS xmm, xmm", (CVTDQ2PS(xmm7, xmm7),)))
instruction_list.append(("CVTDQ2PS xmm, m128", (MOV(esi, esi), CVTDQ2PS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTPD2DQ xmm, xmm", (CVTPD2DQ(xmm7, xmm7),)))
instruction_list.append(("CVTPD2DQ xmm, m128", (MOV(esi, esi), CVTPD2DQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTTPD2DQ xmm, xmm", (CVTTPD2DQ(xmm7, xmm7),)))
instruction_list.append(("CVTTPD2DQ xmm, m128", (MOV(esi, esi), CVTTPD2DQ(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTDQ2PD xmm, xmm", (CVTDQ2PD(xmm7, xmm7),)))
instruction_list.append(("CVTDQ2PD xmm, m64", (MOV(esi, esi), CVTDQ2PD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTPS2PI mm, xmm", (CVTPS2PI(mm4, xmm7),)))
instruction_list.append(("CVTPS2PI mm, m64", (MOV(esi, esi), CVTPS2PI(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTTPS2PI mm, xmm", (CVTTPS2PI(mm4, xmm7),)))
instruction_list.append(("CVTTPS2PI mm, m64", (MOV(esi, esi), CVTTPS2PI(mm4, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTPI2PS xmm, mm", (CVTPI2PS(xmm7, mm4),)))
instruction_list.append(("CVTPI2PS xmm, m64", (MOV(esi, esi), CVTPI2PS(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTPD2PI mm, xmm", (CVTPD2PI(mm4, xmm7),)))
instruction_list.append(("CVTPD2PI mm, m128", (MOV(esi, esi), CVTPD2PI(mm4, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTTPD2PI mm, xmm", (CVTTPD2PI(mm4, xmm7),)))
instruction_list.append(("CVTTPD2PI mm, m128", (MOV(esi, esi), CVTTPD2PI(mm4, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTPI2PD xmm, mm", (CVTPI2PD(xmm7, mm4),)))
instruction_list.append(("CVTPI2PD xmm, m64", (MOV(esi, esi), CVTPI2PD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTSD2SS xmm, xmm", (CVTSD2SS(xmm7, xmm7),)))
instruction_list.append(("CVTSD2SS xmm, m64", (MOV(esi, esi), CVTSD2SS(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("CVTSS2SD xmm, xmm", (CVTSS2SD(xmm7, xmm7),)))
instruction_list.append(("CVTSS2SD xmm, m32", (MOV(esi, esi), CVTSS2SD(xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("CVTPD2PS xmm, xmm", (CVTPD2PS(xmm7, xmm7),)))
instruction_list.append(("CVTPD2PS xmm, m128", (MOV(esi, esi), CVTPD2PS(xmm7, oword[r15+rsi*1+128]))))

instruction_list.append(("CVTPS2PD xmm, xmm", (CVTPS2PD(xmm7, xmm7),)))
instruction_list.append(("CVTPS2PD xmm, m64", (MOV(esi, esi), CVTPS2PD(xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("LDMXCSR m32", (MOV(esi, esi), LDMXCSR(dword[r15+rsi*1+32]))))

instruction_list.append(("STMXCSR m32", (MOV(esi, esi), STMXCSR(dword[r15+rsi*1+32]))))

instruction_list.append(("EMMS", (EMMS(),)))
# fma

instruction_list.append(("VFMADD132SS xmm, xmm, xmm", (VFMADD132SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD132SS xmm, xmm, m32", (MOV(esi, esi), VFMADD132SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMADD213SS xmm, xmm, xmm", (VFMADD213SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD213SS xmm, xmm, m32", (MOV(esi, esi), VFMADD213SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMADD231SS xmm, xmm, xmm", (VFMADD231SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD231SS xmm, xmm, m32", (MOV(esi, esi), VFMADD231SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMADDSS xmm, xmm, xmm, xmm", (VFMADDSS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSS xmm, xmm, xmm, m32", (MOV(esi, esi), VFMADDSS(xmm7, xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VFMADDSS xmm, xmm, m32, xmm", (MOV(esi, esi), VFMADDSS(xmm7, xmm7, dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("VFMSUB132SS xmm, xmm, xmm", (VFMSUB132SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB132SS xmm, xmm, m32", (MOV(esi, esi), VFMSUB132SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMSUB213SS xmm, xmm, xmm", (VFMSUB213SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB213SS xmm, xmm, m32", (MOV(esi, esi), VFMSUB213SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMSUB231SS xmm, xmm, xmm", (VFMSUB231SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB231SS xmm, xmm, m32", (MOV(esi, esi), VFMSUB231SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFMSUBSS xmm, xmm, xmm, xmm", (VFMSUBSS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBSS xmm, xmm, xmm, m32", (MOV(esi, esi), VFMSUBSS(xmm7, xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VFMSUBSS xmm, xmm, m32, xmm", (MOV(esi, esi), VFMSUBSS(xmm7, xmm7, dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("VFNMADD132SS xmm, xmm, xmm", (VFNMADD132SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD132SS xmm, xmm, m32", (MOV(esi, esi), VFNMADD132SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMADD213SS xmm, xmm, xmm", (VFNMADD213SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD213SS xmm, xmm, m32", (MOV(esi, esi), VFNMADD213SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMADD231SS xmm, xmm, xmm", (VFNMADD231SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD231SS xmm, xmm, m32", (MOV(esi, esi), VFNMADD231SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMADDSS xmm, xmm, xmm, xmm", (VFNMADDSS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADDSS xmm, xmm, xmm, m32", (MOV(esi, esi), VFNMADDSS(xmm7, xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VFNMADDSS xmm, xmm, m32, xmm", (MOV(esi, esi), VFNMADDSS(xmm7, xmm7, dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("VFNMSUB132SS xmm, xmm, xmm", (VFNMSUB132SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB132SS xmm, xmm, m32", (MOV(esi, esi), VFNMSUB132SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMSUB213SS xmm, xmm, xmm", (VFNMSUB213SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB213SS xmm, xmm, m32", (MOV(esi, esi), VFNMSUB213SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMSUB231SS xmm, xmm, xmm", (VFNMSUB231SS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB231SS xmm, xmm, m32", (MOV(esi, esi), VFNMSUB231SS(xmm7, xmm7, dword[r15+rsi*1+32]))))

instruction_list.append(("VFNMSUBSS xmm, xmm, xmm, xmm", (VFNMSUBSS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUBSS xmm, xmm, xmm, m32", (MOV(esi, esi), VFNMSUBSS(xmm7, xmm7, xmm7, dword[r15+rsi*1+32]))))
instruction_list.append(("VFNMSUBSS xmm, xmm, m32, xmm", (MOV(esi, esi), VFNMSUBSS(xmm7, xmm7, dword[r15+rsi*1+32], xmm7))))

instruction_list.append(("VFMADD132SD xmm, xmm, xmm", (VFMADD132SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD132SD xmm, xmm, m64", (MOV(esi, esi), VFMADD132SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMADD213SD xmm, xmm, xmm", (VFMADD213SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD213SD xmm, xmm, m64", (MOV(esi, esi), VFMADD213SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMADD231SD xmm, xmm, xmm", (VFMADD231SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD231SD xmm, xmm, m64", (MOV(esi, esi), VFMADD231SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMADDSD xmm, xmm, xmm, xmm", (VFMADDSD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSD xmm, xmm, xmm, m64", (MOV(esi, esi), VFMADDSD(xmm7, xmm7, xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VFMADDSD xmm, xmm, m64, xmm", (MOV(esi, esi), VFMADDSD(xmm7, xmm7, qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("VFMSUB132SD xmm, xmm, xmm", (VFMSUB132SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB132SD xmm, xmm, m64", (MOV(esi, esi), VFMSUB132SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMSUB213SD xmm, xmm, xmm", (VFMSUB213SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB213SD xmm, xmm, m64", (MOV(esi, esi), VFMSUB213SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMSUB231SD xmm, xmm, xmm", (VFMSUB231SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB231SD xmm, xmm, m64", (MOV(esi, esi), VFMSUB231SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFMSUBSD xmm, xmm, xmm, xmm", (VFMSUBSD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBSD xmm, xmm, xmm, m64", (MOV(esi, esi), VFMSUBSD(xmm7, xmm7, xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VFMSUBSD xmm, xmm, m64, xmm", (MOV(esi, esi), VFMSUBSD(xmm7, xmm7, qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("VFNMADD132SD xmm, xmm, xmm", (VFNMADD132SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD132SD xmm, xmm, m64", (MOV(esi, esi), VFNMADD132SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMADD213SD xmm, xmm, xmm", (VFNMADD213SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD213SD xmm, xmm, m64", (MOV(esi, esi), VFNMADD213SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMADD231SD xmm, xmm, xmm", (VFNMADD231SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD231SD xmm, xmm, m64", (MOV(esi, esi), VFNMADD231SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMADDSD xmm, xmm, xmm, xmm", (VFNMADDSD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADDSD xmm, xmm, xmm, m64", (MOV(esi, esi), VFNMADDSD(xmm7, xmm7, xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VFNMADDSD xmm, xmm, m64, xmm", (MOV(esi, esi), VFNMADDSD(xmm7, xmm7, qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("VFNMSUB132SD xmm, xmm, xmm", (VFNMSUB132SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB132SD xmm, xmm, m64", (MOV(esi, esi), VFNMSUB132SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMSUB213SD xmm, xmm, xmm", (VFNMSUB213SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB213SD xmm, xmm, m64", (MOV(esi, esi), VFNMSUB213SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMSUB231SD xmm, xmm, xmm", (VFNMSUB231SD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB231SD xmm, xmm, m64", (MOV(esi, esi), VFNMSUB231SD(xmm7, xmm7, qword[r15+rsi*1+64]))))

instruction_list.append(("VFNMSUBSD xmm, xmm, xmm, xmm", (VFNMSUBSD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUBSD xmm, xmm, xmm, m64", (MOV(esi, esi), VFNMSUBSD(xmm7, xmm7, xmm7, qword[r15+rsi*1+64]))))
instruction_list.append(("VFNMSUBSD xmm, xmm, m64, xmm", (MOV(esi, esi), VFNMSUBSD(xmm7, xmm7, qword[r15+rsi*1+64], xmm7))))

instruction_list.append(("VFMADD132PS xmm, xmm, xmm", (VFMADD132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD132PS xmm, xmm, m128", (MOV(esi, esi), VFMADD132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD132PS ymm, ymm, ymm", (VFMADD132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD132PS ymm, ymm, m256", (MOV(esi, esi), VFMADD132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADD213PS xmm, xmm, xmm", (VFMADD213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD213PS xmm, xmm, m128", (MOV(esi, esi), VFMADD213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD213PS ymm, ymm, ymm", (VFMADD213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD213PS ymm, ymm, m256", (MOV(esi, esi), VFMADD213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADD231PS xmm, xmm, xmm", (VFMADD231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD231PS xmm, xmm, m128", (MOV(esi, esi), VFMADD231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD231PS ymm, ymm, ymm", (VFMADD231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD231PS ymm, ymm, m256", (MOV(esi, esi), VFMADD231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDPS xmm, xmm, xmm, xmm", (VFMADDPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFMADDPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFMADDPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMADDPS ymm, ymm, ymm, ymm", (VFMADDPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFMADDPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMADDPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFMADDPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMSUB132PS xmm, xmm, xmm", (VFMSUB132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB132PS xmm, xmm, m128", (MOV(esi, esi), VFMSUB132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB132PS ymm, ymm, ymm", (VFMSUB132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB132PS ymm, ymm, m256", (MOV(esi, esi), VFMSUB132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUB213PS xmm, xmm, xmm", (VFMSUB213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB213PS xmm, xmm, m128", (MOV(esi, esi), VFMSUB213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB213PS ymm, ymm, ymm", (VFMSUB213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB213PS ymm, ymm, m256", (MOV(esi, esi), VFMSUB213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUB231PS xmm, xmm, xmm", (VFMSUB231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB231PS xmm, xmm, m128", (MOV(esi, esi), VFMSUB231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB231PS ymm, ymm, ymm", (VFMSUB231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB231PS ymm, ymm, m256", (MOV(esi, esi), VFMSUB231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBPS xmm, xmm, xmm, xmm", (VFMSUBPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFMSUBPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFMSUBPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMSUBPS ymm, ymm, ymm, ymm", (VFMSUBPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFMSUBPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMSUBPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFMSUBPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFNMADD132PS xmm, xmm, xmm", (VFNMADD132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD132PS xmm, xmm, m128", (MOV(esi, esi), VFNMADD132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD132PS ymm, ymm, ymm", (VFNMADD132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD132PS ymm, ymm, m256", (MOV(esi, esi), VFNMADD132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADD213PS xmm, xmm, xmm", (VFNMADD213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD213PS xmm, xmm, m128", (MOV(esi, esi), VFNMADD213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD213PS ymm, ymm, ymm", (VFNMADD213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD213PS ymm, ymm, m256", (MOV(esi, esi), VFNMADD213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADD231PS xmm, xmm, xmm", (VFNMADD231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD231PS xmm, xmm, m128", (MOV(esi, esi), VFNMADD231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD231PS ymm, ymm, ymm", (VFNMADD231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD231PS ymm, ymm, m256", (MOV(esi, esi), VFNMADD231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADDPS xmm, xmm, xmm, xmm", (VFNMADDPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADDPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFNMADDPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADDPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFNMADDPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFNMADDPS ymm, ymm, ymm, ymm", (VFNMADDPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADDPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFNMADDPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFNMADDPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFNMADDPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFNMSUB132PS xmm, xmm, xmm", (VFNMSUB132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB132PS xmm, xmm, m128", (MOV(esi, esi), VFNMSUB132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB132PS ymm, ymm, ymm", (VFNMSUB132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB132PS ymm, ymm, m256", (MOV(esi, esi), VFNMSUB132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUB213PS xmm, xmm, xmm", (VFNMSUB213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB213PS xmm, xmm, m128", (MOV(esi, esi), VFNMSUB213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB213PS ymm, ymm, ymm", (VFNMSUB213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB213PS ymm, ymm, m256", (MOV(esi, esi), VFNMSUB213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUB231PS xmm, xmm, xmm", (VFNMSUB231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB231PS xmm, xmm, m128", (MOV(esi, esi), VFNMSUB231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB231PS ymm, ymm, ymm", (VFNMSUB231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB231PS ymm, ymm, m256", (MOV(esi, esi), VFNMSUB231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUBPS xmm, xmm, xmm, xmm", (VFNMSUBPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUBPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFNMSUBPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUBPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFNMSUBPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFNMSUBPS ymm, ymm, ymm, ymm", (VFNMSUBPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUBPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFNMSUBPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFNMSUBPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFNMSUBPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMADD132PD xmm, xmm, xmm", (VFMADD132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD132PD xmm, xmm, m128", (MOV(esi, esi), VFMADD132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD132PD ymm, ymm, ymm", (VFMADD132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD132PD ymm, ymm, m256", (MOV(esi, esi), VFMADD132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADD213PD xmm, xmm, xmm", (VFMADD213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD213PD xmm, xmm, m128", (MOV(esi, esi), VFMADD213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD213PD ymm, ymm, ymm", (VFMADD213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD213PD ymm, ymm, m256", (MOV(esi, esi), VFMADD213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADD231PD xmm, xmm, xmm", (VFMADD231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADD231PD xmm, xmm, m128", (MOV(esi, esi), VFMADD231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADD231PD ymm, ymm, ymm", (VFMADD231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADD231PD ymm, ymm, m256", (MOV(esi, esi), VFMADD231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDPD xmm, xmm, xmm, xmm", (VFMADDPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFMADDPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFMADDPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMADDPD ymm, ymm, ymm, ymm", (VFMADDPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFMADDPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMADDPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFMADDPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMSUB132PD xmm, xmm, xmm", (VFMSUB132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB132PD xmm, xmm, m128", (MOV(esi, esi), VFMSUB132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB132PD ymm, ymm, ymm", (VFMSUB132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB132PD ymm, ymm, m256", (MOV(esi, esi), VFMSUB132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUB213PD xmm, xmm, xmm", (VFMSUB213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB213PD xmm, xmm, m128", (MOV(esi, esi), VFMSUB213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB213PD ymm, ymm, ymm", (VFMSUB213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB213PD ymm, ymm, m256", (MOV(esi, esi), VFMSUB213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUB231PD xmm, xmm, xmm", (VFMSUB231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUB231PD xmm, xmm, m128", (MOV(esi, esi), VFMSUB231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUB231PD ymm, ymm, ymm", (VFMSUB231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUB231PD ymm, ymm, m256", (MOV(esi, esi), VFMSUB231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBPD xmm, xmm, xmm, xmm", (VFMSUBPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFMSUBPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFMSUBPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMSUBPD ymm, ymm, ymm, ymm", (VFMSUBPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFMSUBPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMSUBPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFMSUBPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFNMADD132PD xmm, xmm, xmm", (VFNMADD132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD132PD xmm, xmm, m128", (MOV(esi, esi), VFNMADD132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD132PD ymm, ymm, ymm", (VFNMADD132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD132PD ymm, ymm, m256", (MOV(esi, esi), VFNMADD132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADD213PD xmm, xmm, xmm", (VFNMADD213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD213PD xmm, xmm, m128", (MOV(esi, esi), VFNMADD213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD213PD ymm, ymm, ymm", (VFNMADD213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD213PD ymm, ymm, m256", (MOV(esi, esi), VFNMADD213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADD231PD xmm, xmm, xmm", (VFNMADD231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADD231PD xmm, xmm, m128", (MOV(esi, esi), VFNMADD231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADD231PD ymm, ymm, ymm", (VFNMADD231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADD231PD ymm, ymm, m256", (MOV(esi, esi), VFNMADD231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMADDPD xmm, xmm, xmm, xmm", (VFNMADDPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMADDPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFNMADDPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMADDPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFNMADDPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFNMADDPD ymm, ymm, ymm, ymm", (VFNMADDPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMADDPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFNMADDPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFNMADDPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFNMADDPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFNMSUB132PD xmm, xmm, xmm", (VFNMSUB132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB132PD xmm, xmm, m128", (MOV(esi, esi), VFNMSUB132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB132PD ymm, ymm, ymm", (VFNMSUB132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB132PD ymm, ymm, m256", (MOV(esi, esi), VFNMSUB132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUB213PD xmm, xmm, xmm", (VFNMSUB213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB213PD xmm, xmm, m128", (MOV(esi, esi), VFNMSUB213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB213PD ymm, ymm, ymm", (VFNMSUB213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB213PD ymm, ymm, m256", (MOV(esi, esi), VFNMSUB213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUB231PD xmm, xmm, xmm", (VFNMSUB231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUB231PD xmm, xmm, m128", (MOV(esi, esi), VFNMSUB231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUB231PD ymm, ymm, ymm", (VFNMSUB231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUB231PD ymm, ymm, m256", (MOV(esi, esi), VFNMSUB231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFNMSUBPD xmm, xmm, xmm, xmm", (VFNMSUBPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFNMSUBPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFNMSUBPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFNMSUBPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFNMSUBPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFNMSUBPD ymm, ymm, ymm, ymm", (VFNMSUBPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFNMSUBPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFNMSUBPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFNMSUBPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFNMSUBPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMADDSUB132PS xmm, xmm, xmm", (VFMADDSUB132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB132PS xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB132PS ymm, ymm, ymm", (VFMADDSUB132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB132PS ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUB213PS xmm, xmm, xmm", (VFMADDSUB213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB213PS xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB213PS ymm, ymm, ymm", (VFMADDSUB213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB213PS ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUB231PS xmm, xmm, xmm", (VFMADDSUB231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB231PS xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB231PS ymm, ymm, ymm", (VFMADDSUB231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB231PS ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUBPS xmm, xmm, xmm, xmm", (VFMADDSUBPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUBPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFMADDSUBPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUBPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFMADDSUBPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMADDSUBPS ymm, ymm, ymm, ymm", (VFMADDSUBPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUBPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFMADDSUBPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMADDSUBPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFMADDSUBPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMSUBADD132PS xmm, xmm, xmm", (VFMSUBADD132PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD132PS xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD132PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD132PS ymm, ymm, ymm", (VFMSUBADD132PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD132PS ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD132PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADD213PS xmm, xmm, xmm", (VFMSUBADD213PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD213PS xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD213PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD213PS ymm, ymm, ymm", (VFMSUBADD213PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD213PS ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD213PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADD231PS xmm, xmm, xmm", (VFMSUBADD231PS(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD231PS xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD231PS(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD231PS ymm, ymm, ymm", (VFMSUBADD231PS(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD231PS ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD231PS(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADDPS xmm, xmm, xmm, xmm", (VFMSUBADDPS(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADDPS xmm, xmm, xmm, m128", (MOV(esi, esi), VFMSUBADDPS(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADDPS xmm, xmm, m128, xmm", (MOV(esi, esi), VFMSUBADDPS(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMSUBADDPS ymm, ymm, ymm, ymm", (VFMSUBADDPS(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADDPS ymm, ymm, ymm, m256", (MOV(esi, esi), VFMSUBADDPS(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMSUBADDPS ymm, ymm, m256, ymm", (MOV(esi, esi), VFMSUBADDPS(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMADDSUB132PD xmm, xmm, xmm", (VFMADDSUB132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB132PD xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB132PD ymm, ymm, ymm", (VFMADDSUB132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB132PD ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUB213PD xmm, xmm, xmm", (VFMADDSUB213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB213PD xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB213PD ymm, ymm, ymm", (VFMADDSUB213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB213PD ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUB231PD xmm, xmm, xmm", (VFMADDSUB231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUB231PD xmm, xmm, m128", (MOV(esi, esi), VFMADDSUB231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUB231PD ymm, ymm, ymm", (VFMADDSUB231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUB231PD ymm, ymm, m256", (MOV(esi, esi), VFMADDSUB231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMADDSUBPD xmm, xmm, xmm, xmm", (VFMADDSUBPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMADDSUBPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFMADDSUBPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMADDSUBPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFMADDSUBPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMADDSUBPD ymm, ymm, ymm, ymm", (VFMADDSUBPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMADDSUBPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFMADDSUBPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMADDSUBPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFMADDSUBPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

instruction_list.append(("VFMSUBADD132PD xmm, xmm, xmm", (VFMSUBADD132PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD132PD xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD132PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD132PD ymm, ymm, ymm", (VFMSUBADD132PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD132PD ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD132PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADD213PD xmm, xmm, xmm", (VFMSUBADD213PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD213PD xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD213PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD213PD ymm, ymm, ymm", (VFMSUBADD213PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD213PD ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD213PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADD231PD xmm, xmm, xmm", (VFMSUBADD231PD(xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADD231PD xmm, xmm, m128", (MOV(esi, esi), VFMSUBADD231PD(xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADD231PD ymm, ymm, ymm", (VFMSUBADD231PD(ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADD231PD ymm, ymm, m256", (MOV(esi, esi), VFMSUBADD231PD(ymm3, ymm3, hword[r15+rsi*1+256]))))

instruction_list.append(("VFMSUBADDPD xmm, xmm, xmm, xmm", (VFMSUBADDPD(xmm7, xmm7, xmm7, xmm7),)))
instruction_list.append(("VFMSUBADDPD xmm, xmm, xmm, m128", (MOV(esi, esi), VFMSUBADDPD(xmm7, xmm7, xmm7, oword[r15+rsi*1+128]))))
instruction_list.append(("VFMSUBADDPD xmm, xmm, m128, xmm", (MOV(esi, esi), VFMSUBADDPD(xmm7, xmm7, oword[r15+rsi*1+128], xmm7))))
instruction_list.append(("VFMSUBADDPD ymm, ymm, ymm, ymm", (VFMSUBADDPD(ymm3, ymm3, ymm3, ymm3),)))
instruction_list.append(("VFMSUBADDPD ymm, ymm, ymm, m256", (MOV(esi, esi), VFMSUBADDPD(ymm3, ymm3, ymm3, hword[r15+rsi*1+256]))))
instruction_list.append(("VFMSUBADDPD ymm, ymm, m256, ymm", (MOV(esi, esi), VFMSUBADDPD(ymm3, ymm3, hword[r15+rsi*1+256], ymm3))))

import operator

bundles = open("codegen/x86_64_bundles.h", "w")
names = open("codegen/x86_64_names.h", "w")

print("static const uint8_t bundles[][32] = {", file=bundles)
print("static const char* names[] = {", file=names)

for (text, instructions) in instruction_list:
    bundle = bytearray([0xF4] * 32)
    encoding = sum(map(operator.methodcaller("encode"), instructions), bytearray())
    bundle[0:len(encoding)] = encoding
    print("\t{" + ", ".join(map(lambda b: "0x%02X" % b, bundle)) + "},", file=bundles)
    print("\t\"%s\"," % text, file=names)

print("};\n", file=names)
print("};\n", file=bundles)
