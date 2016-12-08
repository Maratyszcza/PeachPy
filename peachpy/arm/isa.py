# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Extension:
    def __init__(self, name):
        if name in {'V4', 'V5', 'V5E', 'V6', 'V6K', 'V7', 'V7MP', 'Div', 'Thumb', 'Thumb2',
                    'VFP', 'VFP2', 'VFP3', 'VFPd32', 'VFPHP', 'VFP4', 'VFPVectorMode',
                    'XScale', 'WMMX', 'WMMX2', 'NEON', 'NEONHP', 'NEON2'}:
            self.name = name
        else:
            raise ValueError('Invalid ISA extension: {0} is not supported on this architecture'.format(name))

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __gt__(self, other):
        return other in self.prerequisites

    def __lt__(self, other):
        return self in other.prerequisites

    @property
    def prerequisites(self):
        return {
            'V4': [Extension.V4],
            'V5': [Extension.V4, Extension.V5],
            'V5E': [Extension.V4, Extension.V5, Extension.V5E],
            'V6': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6],
            'V6K': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K],
            'V7': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7],
            'V7MP': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7,
                     Extension.V7MP],
            'Div': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7,
                    Extension.V7MP, Extension.Div],
            'Thumb': [Extension.Thumb],
            'Thumb2': [Extension.Thumb, Extension.Thumb2],
            'VFP': [Extension.VFP],
            'VFP2': [Extension.VFP, Extension.VFP2],
            'VFP3': [Extension.VFP, Extension.VFP2, Extension.VFP3],
            'VFPd32': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPd32],
            'VFPHP': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPHP],
            'VFP4': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPHP, Extension.VFP4],
            'VFPVectorMode': [Extension.VFP, Extension.VFP2, Extension.VFPVectorMode],
            'XScale': [Extension.XScale],
            'WMMX': [Extension.WMMX],
            'WMMX2': [Extension.WMMX, Extension.WMMX2],
            'NEON': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPd32, Extension.NEON],
            'NEONHP': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPd32, Extension.NEON,
                       Extension.NEONHP],
            'NEON2': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPd32, Extension.NEON,
                      Extension.NEONHP, Extension.NEON2],
        }[self.name]

    @property
    def ancestors(self):
        return {
            'V4': [Extension.V4],
            'V5': [Extension.V4, Extension.V5],
            'V5E': [Extension.V4, Extension.V5. Extension.V5E],
            'V6': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6],
            'V6K': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K],
            'V7': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7],
            'V7MP': [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7,
                     Extension.V7MP],
            'Div': [Extension.Div],
            'Thumb': [Extension.Thumb],
            'Thumb2': [Extension.Thumb, Extension.Thumb2],
            'VFP': [Extension.VFP],
            'VFP2': [Extension.VFP, Extension.VFP2],
            'VFP3': [Extension.VFP, Extension.VFP2, Extension.VFP3],
            'VFPd32': [Extension.VFPd32],
            'VFPHP': [Extension.VFPHP],
            'VFP4': [Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFPHP, Extension.VFP4],
            'VFPVectorMode': [Extension.VFPVectorMode],
            'XScale': [Extension.XScale],
            'WMMX': [Extension.WMMX],
            'WMMX2': [Extension.WMMX, Extension.WMMX2],
            'NEON': [Extension.NEON],
            'NEONHP': [Extension.NEON, Extension.NEONHP],
            'NEON2': [Extension.NEON, Extension.NEONHP, Extension.NEON2],
        }[self.name]

    def __add__(self, extension):
        return Extensions(self, extension)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    V4, V5, V5E, V6, V6K, V7, V7MP = None, None, None, None, None, None, None
    Div = None
    Thumb, Thumb2 = None, None
    VFP, VFP2, VFP3, VFP4 = None, None, None, None
    VFPVectorMode, VFPd32, VFPHP = None, None, None
    XScale, WMMX, WMMX2 = None, None, None
    NEON, NEONHP, NEON2 = None, None, None
    All = None

Extension.V4 = Extension('V4')
Extension.V5 = Extension('V5')
Extension.V5E = Extension('V5E')
Extension.V6 = Extension('V6')
Extension.V6K = Extension('V6K')
Extension.V7 = Extension('V7')
Extension.V7MP = Extension('V7MP')
Extension.Div = Extension('Div')
Extension.Thumb = Extension('Thumb')
Extension.Thumb2 = Extension('Thumb2')
Extension.VFP = Extension('VFP')
Extension.VFP2 = Extension('VFP2')
Extension.VFP3 = Extension('VFP3')
Extension.VFP4 = Extension('VFP4')
Extension.VFPd32 = Extension('VFPd32')
Extension.VFPHP = Extension('VFPHP')
Extension.VFPVectorMode = Extension('VFPVectorMode')
Extension.XScale = Extension('XScale')
Extension.WMMX = Extension('WMMX')
Extension.WMMX2 = Extension('WMMX2')
Extension.NEON = Extension('NEON')
Extension.NEONHP = Extension('NEONHP')
Extension.NEON2 = Extension('NEON2')
Extension.All = [Extension.V4, Extension.V5, Extension.V5E, Extension.V6, Extension.V6K, Extension.V7, Extension.V7MP,
                 Extension.Div, Extension.Thumb, Extension.Thumb2,
                 Extension.VFP, Extension.VFP2, Extension.VFP3, Extension.VFP4, Extension.VFPd32, Extension.VFPHP,
                 Extension.VFPVectorMode, Extension.XScale, Extension.WMMX, Extension.WMMX2,
                 Extension.NEON, Extension.NEONHP, Extension.NEON2]


class Extensions:
    def __init__(self, *args):
        self.extensions = set()
        for extension in args:
            if extension is None:
                pass
            elif isinstance(extension, Extensions):
                self.extensions.add(extension.extensions)
            elif isinstance(extension, Extension):
                self.extensions.add(extension)
            else:
                self.extensions.add(Extension(extension))

    def __add__(self, extension):
        extensions = set(self.extensions)
        if isinstance(extension, Extension):
            extensions.add(extension)
        else:
            extensions.add(Extension(extension))
        return Extensions(*extensions)

    def __sub__(self, extension):
        extensions = set(self.extensions)
        if extension in extensions:
            del extensions[extension]
        else:
            raise KeyError('Extension set does not contain {0}'.format(extension))
        return Extensions(*extensions)

    def __str__(self):
        extensions = list(reversed(sorted(self.extensions)))
        for extension in extensions:
            for ancestor in extension.ancestors:
                if ancestor != extension and ancestor in extensions:
                    extensions.remove(ancestor)
        return ", ".join(sorted(map(str, extensions)))

    def __contains__(self, item):
        return item in self.extensions

    def __len__(self):
        return len(self.extensions)

    def __not__(self):
        return not self.extensions

    def __iter__(self):
        return iter(self.extensions)

