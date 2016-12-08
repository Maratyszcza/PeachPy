# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import Enum


class SectionType(Enum):
    code = 0
    const_data = 1


class Section(object):
    max_alignment = 4096

    def __init__(self, type, alignment_byte=None):
        from peachpy.util import is_uint8
        if not isinstance(type, SectionType):
            raise TypeError("Type %s is not in SectionType enumeration" % str(type))
        if alignment_byte is None:
            alignment_byte = 0
        elif not is_uint8(alignment_byte):
            raise TypeError("Alignment byte %s is not an 8-bit unsigned integer" % str(alignment_byte))

        self.type = type
        self.alignment_byte = alignment_byte
        self.content = bytearray()
        self.symbols = list()
        self.relocations = list()
        self._alignment = 1

    def __len__(self):
        return len(self.content)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, alignment):
        from peachpy.util import is_int
        if not is_int(alignment):
            raise TypeError("Alignment %s is not an integer" % str(alignment))
        if alignment < 0:
            raise ValueError("Alignment %d is not a positive integer" % alignment)
        if alignment & (alignment - 1) != 0:
            raise ValueError("Alignment %d is not a power of 2" % alignment)
        if alignment > Section.max_alignment:
            raise ValueError("Alignment %d exceeds maximum alignment (%d)" % (alignment, Section.max_alignment))
        if alignment == 0:
            alignment = 1
        self._alignment = alignment

    def add_symbol(self, symbol):
        if not isinstance(symbol, Symbol):
            raise TypeError("Symbol %s is not an instance of Symbol type" % str(symbol))
        self.symbols.append(symbol)

    def add_relocation(self, relocation):
        if not isinstance(relocation, Relocation):
            raise TypeError("Relocation %s is not an instance of Relocation type" % str(relocation))
        self.relocations.append(relocation)


class RelocationType(Enum):
    """Relocation for RIP-relative disp32 offset"""
    rip_disp32 = 0


class Relocation:
    def __init__(self, offset, type, symbol=None, program_counter=None):
        from peachpy.util import is_int
        if not is_int(offset):
            raise TypeError("Offset %s is not an integer" % str(offset))
        if offset < 0:
            raise ValueError("Offset %d is negative" % offset)
        if not isinstance(type, RelocationType):
            raise TypeError("Relocation type %s is not in RelocationType enumeration" % str(type))
        if symbol is not None and not isinstance(symbol, Symbol):
            raise TypeError("Symbol %s is not an instance of Symbol type" % str(symbol))
        if program_counter is not None:
            if not is_int(program_counter):
                raise TypeError("Program counter %s is not an integer" % str(program_counter))
            if program_counter < 0:
                raise TypeError("Program counter %d is negative" % program_counter)

        self.offset = offset
        self.type = type
        self.symbol = symbol
        self.program_counter = program_counter


class SymbolType(Enum):
    """Literal constant"""
    literal_constant = 0
    """Label"""
    label = 1


class Symbol:
    def __init__(self, offset, type, name=None, size=None):
        from peachpy.util import is_int
        if not is_int(offset):
            raise TypeError("Offset %s is not an integer" % str(offset))
        if offset < 0:
            raise ValueError("Offset %d is negative" % offset)
        if not isinstance(type, SymbolType):
            raise TypeError("Symbol type %s is not in SymbolType enumeration" % str(type))
        from peachpy.name import Name
        if name is not None and not (isinstance(name, tuple) and all(isinstance(part, Name) for part in name)):
            raise TypeError("Name %s must be a tuple of Name objects" % str(name))
        if size is not None:
            if not is_int(size):
                raise TypeError("Size %s is not an integer" % str(size))
            if size < 0:
                raise ValueError("Size %d is negative" % size)

        self.offset = offset
        self.type = type
        self.name = ".".join(map(str, name))
        self.size = size
