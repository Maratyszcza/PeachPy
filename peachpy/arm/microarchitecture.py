# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.arm.isa import Extension, Extensions


class Microarchitecture:
    def __init__(self, name, extensions):
        self.name = name
        self.extensions = Extensions(*[prerequisite for extension in extensions
                                       for prerequisite in extension.prerequisites])

    def is_supported(self, extension):
        return extension in self.extensions

    @property
    def id(self):
        return self.name.replace(" ", "")

    def __add__(self, extension):
        return Microarchitecture(self.name, self.extensions + extension)

    def __sub__(self, extension):
        return Microarchitecture(self.name, self.extensions - extension)

    def __str__(self):
        return self.name

    Default = None
    XScale = None
    ARM9, ARM11 = None, None
    CortexA5, CortexA7, CortexA8, CortexA9, CortexA12, CortexA15 = None, None, None, None, None, None
    Scorpion, Krait = None, None
    PJ4 = None

Microarchitecture.Default = Microarchitecture('Default', Extension.All)
Microarchitecture.XScale = Microarchitecture('XScale', [Extension.V5E, Extension.Thumb,
                                                        Extension.XScale, Extension.WMMX2])
Microarchitecture.ARM9 = Microarchitecture('ARM9', [Extension.V5E, Extension.Thumb])
Microarchitecture.ARM11 = Microarchitecture('ARM11', [Extension.V6K, Extension.Thumb,
                                                      Extension.VFP2, Extension.VFPVectorMode])
Microarchitecture.CortexA5 = Microarchitecture('Cortex A5', [Extension.V7MP, Extension.Thumb2,
                                                             Extension.VFP4, Extension.VFPd32, Extension.NEON2])
Microarchitecture.CortexA7 = Microarchitecture('Cortex A7', [Extension.V7MP, Extension.Thumb2, Extension.Div,
                                                             Extension.VFP4, Extension.VFPd32, Extension.NEON2])
Microarchitecture.CortexA8 = Microarchitecture('Cortex A8', [Extension.V7, Extension.Thumb2,
                                                             Extension.VFP3, Extension.VFPd32, Extension.NEON])
Microarchitecture.CortexA9 = Microarchitecture('Cortex A9', [Extension.V7MP, Extension.Thumb2,
                                                             Extension.VFP3, Extension.VFPHP])
Microarchitecture.CortexA12 = Microarchitecture('Cortex A12', [Extension.V7MP, Extension.Thumb2, Extension.Div,
                                                               Extension.VFP4, Extension.VFPd32, Extension.NEON2])
Microarchitecture.CortexA15 = Microarchitecture('Cortex A15', [Extension.V7MP, Extension.Thumb2, Extension.Div,
                                                               Extension.VFP4, Extension.VFPd32, Extension.NEON2])
Microarchitecture.Scorpion = Microarchitecture('Scorpion', [Extension.V7MP, Extension.Thumb2,
                                                            Extension.VFP3, Extension.VFPd32, Extension.VFPHP,
                                                            Extension.NEON, Extension.NEONHP])
Microarchitecture.Krait = Microarchitecture('Krait', [Extension.V7MP, Extension.Thumb2, Extension.Div,
                                                      Extension.VFP4, Extension.VFPd32, Extension.NEON2])
Microarchitecture.PJ4 = Microarchitecture('PJ4', [Extension.V7, Extension.Thumb2,
                                                  Extension.VFP3, Extension.WMMX2])
