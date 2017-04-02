# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.x86_64 import isa


class Microarchitecture:
    def __init__(self, name, extensions, alu_width, fpu_width, load_with, store_width):
        self.name = name
        self.extensions = isa.Extensions(*[prerequisite for extension in extensions
                                           for prerequisite in extension.prerequisites])
        self.alu_width = alu_width
        self.fpu_width = fpu_width
        self.load_width = load_with
        self.store_width = store_width

    def is_supported(self, extension):
        return extension in self.extensions

    @property
    def id(self):
        return self.name.replace(" ", "")

    @property
    def has_sse3(self):
        return isa.sse3 in self.extensions

    @property
    def has_ssse3(self):
        return isa.ssse3 in self.extensions

    @property
    def has_sse4_1(self):
        return isa.sse4_1 in self.extensions

    @property
    def has_sse4_2(self):
        return isa.sse4_2 in self.extensions

    @property
    def has_avx(self):
        return isa.avx in self.extensions

    @property
    def has_avx2(self):
        return isa.avx2 in self.extensions

    @property
    def has_fma3(self):
        return isa.fma3 in self.extensions

    @property
    def has_fma4(self):
        return isa.fma4 in self.extensions

    @property
    def has_fma(self):
        return self.has_fma3 or self.has_fma4

    @property
    def has_avx512f(self):
        return isa.avx512f in self.extensions

    def __add__(self, extension):
        return Microarchitecture(self.name, self.extensions + extension,
                                 self.alu_width, self.fpu_width, self.load_width, self.store_width)

    def __sub__(self, extension):
        return Microarchitecture(self.name, self.extensions - extension,
                                 self.alu_width, self.fpu_width, self.load_width, self.store_width)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Microarchitecture) and self.name == other.name

    def __ne__(self, other):
        return not isinstance(other, Microarchitecture) or self.name != other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

default = Microarchitecture('Default', isa.default,
                            alu_width=128, fpu_width=128, load_with=128, store_width=128)
prescott = Microarchitecture('Prescott', (isa.cmov, isa.sse3, isa.clflush),
                             alu_width=64, fpu_width=64, load_with=64, store_width=64)
conroe = Microarchitecture('Conroe', (isa.cmov, isa.mmx_plus, isa.ssse3, isa.clflush),
                           alu_width=128, fpu_width=128, load_with=128, store_width=128)
penryn = Microarchitecture('Penryn', (isa.cmov, isa.mmx_plus, isa.sse4_1, isa.clflush),
                           alu_width=128, fpu_width=128, load_with=128, store_width=128)
nehalem = Microarchitecture('Nehalem', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.clflush),
                            alu_width=128, fpu_width=128, load_with=128, store_width=128)
sandy_bridge = Microarchitecture('Sandy Bridge', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.avx),
                                 alu_width=128, fpu_width=256, load_with=256, store_width=128)
ivy_bridge = Microarchitecture('Ivy Bridge', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.avx, isa.f16c),
                               alu_width=128, fpu_width=256, load_with=256, store_width=128)
haswell = Microarchitecture('Haswell', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.avx, isa.f16c, isa.fma3,
                                        isa.avx2, isa.lzcnt, isa.prefetchw, isa.movbe, isa.bmi2),
                            alu_width=256, fpu_width=256, load_with=256, store_width=256)
broadwell = Microarchitecture('Broadwell', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.f16c, isa.fma3, isa.avx2,
                                            isa.lzcnt, isa.prefetchw, isa.movbe, isa.bmi2, isa.adx),
                              alu_width=256, fpu_width=256, load_with=256, store_width=256)
skylake = Microarchitecture('Skylake', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.f16c, isa.fma3, isa.avx2,
                                        isa.lzcnt, isa.prefetchw, isa.clflushopt, isa.movbe, isa.bmi2, isa.adx),
                            alu_width=256, fpu_width=256, load_with=256, store_width=256)
skylake_xeon = Microarchitecture('Skylake Xeon', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.f16c, isa.fma3,
                                                  isa.lzcnt, isa.prefetchw, isa.clflushopt, isa.movbe, isa.bmi2, isa.adx,
                                                  isa.avx512bw, isa.avx512dq, isa.avx512vl, isa.avx512cd),
                                 alu_width=512, fpu_width=512, load_with=512, store_width=512)
cannonlake = Microarchitecture('Cannonlake', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.f16c, isa.fma3,
                                              isa.lzcnt, isa.prefetchw, isa.clflushopt, isa.movbe, isa.bmi2, isa.adx,
                                              isa.avx512bw, isa.avx512dq, isa.avx512vl, isa.avx512cd,
                                              isa.avx512ifma, isa.avx512vbmi),
                               # TODO: update EU width when CNL is out
                               alu_width=512, fpu_width=512, load_with=512, store_width=512)
knights_landing = Microarchitecture('Knights Landing',
                                    (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.popcnt, isa.f16c, isa.fma3,
                                     isa.lzcnt, isa.prefetchw, isa.movbe, isa.bmi2, isa.adx,
                                     isa.avx512cd, isa.avx512cd, isa.avx512er),
                                    alu_width=512, fpu_width=512, load_with=512, store_width=512)
k8 = Microarchitecture('K8', (isa.cmov, isa.mmx_plus, isa.three_d_now_plus, isa.sse2,
                              isa.prefetch, isa.prefetchw, isa.clflush),
                       alu_width=64, fpu_width=64, load_with=64, store_width=64)
k10 = Microarchitecture('K10', (isa.cmov, isa.mmx_plus, isa.three_d_now_plus, isa.sse4a,
                                isa.prefetch, isa.prefetchw, isa.clflush, isa.popcnt, isa.lzcnt),
                        alu_width=128, fpu_width=128, load_with=128, store_width=64)
bulldozer = Microarchitecture('Bulldozer', (isa.cmov, isa.mmx_plus, isa.sse4a, isa.avx, isa.xop, isa.fma4,
                                            isa.prefetch, isa.prefetchw, isa.clflush,
                                            isa.aes, isa.pclmulqdq, isa.lzcnt, isa.popcnt),
                              alu_width=128, fpu_width=128, load_with=128, store_width=128)
piledriver = Microarchitecture('Piledriver', (isa.cmov, isa.mmx_plus, isa.sse4a, isa.sse4_2,
                                              isa.avx, isa.xop, isa.fma4, isa.fma3, isa.f16c, isa.aes, isa.pclmulqdq,
                                              isa.prefetch, isa.prefetchw, isa.clflush,
                                              isa.lzcnt, isa.popcnt, isa.bmi, isa.tbm),
                               alu_width=128, fpu_width=128, load_with=128, store_width=128)
steamroller = Microarchitecture('Steamroller', (isa.cmov, isa.mmx_plus, isa.sse4a, isa.sse4_2,
                                                isa.avx, isa.xop, isa.fma4, isa.fma3, isa.f16c, isa.aes, isa.pclmulqdq,
                                                isa.prefetch, isa.prefetchw, isa.clflush,
                                                isa.lzcnt, isa.popcnt, isa.bmi, isa.tbm),
                                alu_width=128, fpu_width=256, load_with=256, store_width=128)
excavator = Microarchitecture('Excavator', (isa.cmov, isa.mmx_plus, isa.sse4a, isa.xop, isa.fma4, isa.fma3, isa.f16c,
                                            isa.avx2, isa.aes, isa.pclmulqdq, isa.rdrand,
                                            isa.prefetch, isa.prefetchw, isa.clflush,
                                            isa.lzcnt, isa.popcnt, isa.bmi2, isa.tbm),
                              alu_width=256, fpu_width=256, load_with=256, store_width=128)
zen = Microarchitecture('Zen', (isa.cmov, isa.mmx_plus, isa.fma4, isa.fma3, isa.f16c, isa.avx2,
                                isa.aes, isa.pclmulqdq, isa.rdseed, isa.sha,
                                isa.prefetch, isa.prefetchw, isa.clflushopt, isa.clzero,
                                isa.lzcnt, isa.popcnt, isa.bmi2, isa.adx),
                        alu_width=256, fpu_width=256, load_with=256, store_width=256)
bonnell = Microarchitecture('Bonnell', (isa.cmov, isa.movbe, isa.mmx_plus, isa.ssse3, isa.clflush),
                            alu_width=128, fpu_width=64, load_with=128, store_width=128)
saltwell = Microarchitecture('Saltwell', (isa.cmov, isa.movbe, isa.mmx_plus, isa.ssse3, isa.clflush),
                             alu_width=128, fpu_width=64, load_with=128, store_width=128)
silvermont = Microarchitecture('Silvermont', (isa.cmov, isa.movbe, isa.popcnt, isa.clflush,
                                              isa.mmx_plus, isa.sse4_2, isa.aes, isa.pclmulqdq),
                               alu_width=128, fpu_width=64, load_with=128, store_width=128)
airmont = Microarchitecture('Airmont', (isa.cmov, isa.movbe, isa.popcnt,
                                        isa.mmx_plus, isa.sse4_2,
                                        isa.aes, isa.pclmulqdq, isa.rdrand,
                                        isa.prefetchw, isa.clflush, isa.rdtscp),
                            alu_width=128, fpu_width=64, load_with=128, store_width=128)
goldmont = Microarchitecture('Goldmont', (isa.cmov, isa.movbe, isa.popcnt, isa.adx,
                                          isa.mmx_plus, isa.sse4_2, isa.prefetchw, isa.clflushopt,
                                          isa.aes, isa.pclmulqdq, isa.rdseed, isa.sha,
                                          isa.rdtscp),
                             alu_width=128, fpu_width=64, load_with=128, store_width=128)
bobcat = Microarchitecture('Bobcat', (isa.cmov, isa.mmx_plus, isa.ssse3, isa.sse4a,
                                      isa.prefetch, isa.prefetchw, isa.clflush, isa.lzcnt, isa.popcnt),
                           alu_width=64, fpu_width=64, load_with=64, store_width=64)
jaguar = Microarchitecture('Jaguar', (isa.cmov, isa.mmx_plus, isa.sse4_2, isa.sse4a, isa.avx, isa.f16c,
                                      isa.prefetch, isa.prefetchw, isa.clflush, isa.lzcnt, isa.popcnt, isa.movbe,
                                      isa.aes, isa.pclmulqdq),
                           alu_width=128, fpu_width=128, load_with=128, store_width=128)
